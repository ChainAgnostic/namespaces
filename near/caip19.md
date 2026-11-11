---
namespace-identifier: near-caip19
title: NEAR Protocol Namespace - Asset Type and Asset ID Specification
author: ["Iker Alustiza (@IkerAlus)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/issues/106
status: Draft
type: Standard
created: 2026-11-11
requires: ["CAIP-2", "CAIP-10", "CAIP-19", "CAIP-20"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Introduction

NEAR has one native asset, the NEAR token, and fungible tokens issued by contracts that implement the [NEP-141][] standard.
A NEP-141 token is identified by the account ID of its contract, such as `usdt.tether-token.near` for Tether USD, and each contract implements exactly one token.
This profile defines two asset namespaces: `slip44` for native NEAR, as [CAIP-20][] does for every chain's native asset, and `nep141` for fungible tokens.
Contract account IDs are written as in the [NEAR CAIP-10 profile][CAIP-10 Profile], with `_` percent-encoded as `%5F`.
Non-fungible tokens and multi-tokens are left to a later revision; see [Additional Considerations](#additional-considerations).

## Specification

### Semantics

| Asset | `asset_namespace` | `asset_reference` | Example |
| --- | --- | --- | --- |
| Native NEAR | `slip44` | `397`, NEAR's [SLIP-0044][] coin type | `near:mainnet/slip44:397` |
| NEP-141 fungible token | `nep141` | The token contract's account ID, encoded as in the CAIP-10 profile | `near:mainnet/nep141:usdt.tether-token.near` |

Native NEAR is held in an account's balance, counted in yoctoNEAR (24 decimals), and has no contract.
Wrapped NEAR is a separate NEP-141 token, `near:mainnet/nep141:wrap.near`, and the two identifiers do not name the same asset.
A NEP-141 token's name, symbol and decimals come from its contract's `ft_metadata` method ([NEP-148][]), not from the identifier.
Bridged assets are NEP-141 tokens like any other: `near:mainnet/nep141:btc.omft.near` is a bridged representation of bitcoin on NEAR, and a different asset from bitcoin on the Bitcoin network.

None of these assets uses a `token_id`, so a NEAR asset ID is always a bare asset type.

### Syntax

```text
asset_type:      chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:        a NEAR CAIP-2 chain ID, e.g. near:mainnet
asset_namespace: "slip44" or "nep141"
asset_reference: "397" for slip44;
                 for nep141, the contract's account ID with every "_" replaced by "%5F"
```

A `nep141` reference follows the [CAIP-10 profile][CAIP-10 Profile]'s rules exactly: it matches the regular expression below and, after `%5F` is replaced by `_`, is between 2 and 64 characters long.

```regex
^(([a-z0-9]+(-|%5F))*[a-z0-9]+\.)*([a-z0-9]+(-|%5F))*[a-z0-9]+$
```

A whole NEAR asset type can be checked with the following regular expression, plus the decoded-length check for `nep141`:

```regex
^near:[-_a-zA-Z0-9]{1,32}/(slip44:397|nep141:(([a-z0-9]+(-|%5F))*[a-z0-9]+\.)*([a-z0-9]+(-|%5F))*[a-z0-9]+)$
```

Each asset has exactly one identifier per network, so two NEAR asset types name the same asset exactly when they are equal strings.

### Resolution Mechanics

To confirm that a `nep141` identifier names a fungible token and to read its metadata, decode the account ID and call its `ft_metadata` view method through the [`call_function`][] query, with empty arguments (`e30=` is `{}` in base64):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "query",
  "params": {
    "request_type": "call_function",
    "finality": "final",
    "account_id": "usdt.tether-token.near",
    "method_name": "ft_metadata",
    "args_base64": "e30="
  }
}
```

`result.result` holds the method's return value as an array of bytes.
Decoded as UTF-8 JSON, the mainnet response for `usdt.tether-token.near`, retrieved 2026-11-11, includes:

```json
{
  "spec": "ft-1.0.0",
  "name": "Tether USD",
  "symbol": "USDt",
  "decimals": 6
}
```

A missing account returns an `UNKNOWN_ACCOUNT` error, and a contract without `ft_metadata` returns an execution error such as `MethodNotFound`.
Native NEAR needs no contract call: an account's balance is the `amount` field of `view_account`, as shown in the CAIP-10 profile.
Confirm the endpoint's network first, by resolving its chain ID as described in the [CAIP-2 profile][CAIP-2 Profile].

## Rationale

### Why `nep141`

NEAR standards are named by their NEP number, and fungible tokens are NEP-141, NEAR's counterpart of ERC-20.
Naming the namespace after the standard follows the `eip155` profile's `erc20` and the Stacks profile's `sip010`.
It is also the prefix NEAR tooling already uses: NEAR Intents and its 1Click API name NEP-141 assets `nep141:<account_id>`, so those names map to this profile by prefixing the chain ID and encoding any `_`.
`nep141` fits CAIP-19's `asset_namespace` grammar, `[-a-z0-9]{3,8}`.

### Why the contract account ID

A NEP-141 contract implements exactly one token, and its account ID is how wallets, explorers and other contracts already refer to it, with no registry or lookup.
Using the CAIP-10 profile's encoding means a token contract has the same `asset_reference` here as its account has `account_address` there.

### Why `slip44:397`

[CAIP-20][] reserves the `slip44` namespace for native assets, identified by their [SLIP-0044][] coin type, and coin type 397 is registered to NEAR Protocol.

### Backwards Compatibility

There is no earlier NEAR CAIP-19 profile.
`near:mainnet/nep141:<account_id>` identifiers, with `_` encoded as `%5F`, are already used in production by NEAR payment tooling for x402 and MPP, as noted on [the CAIP-2 profile's pull request][namespaces PR #203].
Identifiers written with a raw `_` follow the CAIP-10 profile's backwards-compatibility rules: consumers MAY accept them, and MUST convert `_` to `%5F` before comparing or re-emitting them.

## Test Cases

### Valid asset types

| Identifier | Asset | Notes |
| --- | --- | --- |
| `near:mainnet/slip44:397` | NEAR | Native asset |
| `near:testnet/slip44:397` | NEAR on testnet | Native asset |
| `near:mainnet/nep141:wrap.near` | wNEAR, 24 decimals | Wrapped NEAR, a different asset from `slip44:397` |
| `near:testnet/nep141:wrap.testnet` | wNEAR on testnet, 24 decimals | |
| `near:mainnet/nep141:usdt.tether-token.near` | USDt, 6 decimals | |
| `near:mainnet/nep141:17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1` | USDC, 6 decimals | Contract at an account with the NEAR-implicit shape |
| `near:mainnet/nep141:token.sweat` | SWEAT, 18 decimals | Not under the `near` top-level account |
| `near:mainnet/nep141:btc.omft.near` | BTC, 8 decimals | Bridged bitcoin, a different asset from bitcoin on the Bitcoin network |
| `near:mainnet/nep141:v3.oin%5Ffinance.near` | nUSDO, 8 decimals | `_` encoded as `%5F` |

### Invalid asset types

| Identifier | Reason |
| --- | --- |
| `near:mainnet/nep141:` | Empty asset reference |
| `near:mainnet/nep141:v3.oin_finance.near` | Raw `_` is outside CAIP-19's grammar |
| `near:mainnet/nep141:v3.oin%5ffinance.near` | Lowercase escape; the canonical form is `%5F` |
| `near:mainnet/nep141:Wrap.near` | Uppercase letters are never valid in NEAR account IDs |
| `near:mainnet/nep141:a` | Not a valid account ID: shorter than 2 characters |
| `near:mainnet/NEP141:wrap.near` | Asset namespaces are lowercase |
| `near:mainnet/erc20:wrap.near` | `erc20` is not a NEAR asset namespace |
| `near:mainnet/slip44:60` | Coin type 60 is ether; NEAR's native asset is 397 |
| `near:mainnet/nep141:wrap.near/1` | NEP-141 tokens have no `token_id` |
| `near:mainnet/slip44:397/1` | Native NEAR has no `token_id` |

## Security Considerations

Any account can deploy a NEP-141 contract with any name, symbol and decimals, and none of them is unique or verified.
Applications should identify tokens by their full identifier, which includes the contract account ID, and show it alongside the symbol: a token whose symbol is `USDC` is not necessarily the USDC contract.

A bridged token's value depends on its bridge: `btc.omft.near` represents bitcoin held by the bridge that issues it.

A token contract's code can change: an account with a full-access key can deploy new code, so a token's behaviour, and even whether it still implements NEP-141, can change under the same identifier.
A contract account can also be deleted and created again, as described in the CAIP-10 profile.

Native NEAR and wrapped NEAR are different assets.
Payment and accounting systems must not treat a `slip44:397` balance as a `nep141:wrap.near` balance, or the reverse.

## Additional Considerations

Non-fungible tokens ([NEP-171][]) and multi-tokens ([NEP-245][]) are not covered.
Both identify an asset by a contract and a token ID, and NEAR token IDs are arbitrary strings that CAIP-19's `token_id`, `[-.%a-zA-Z0-9]{1,78}`, cannot always hold.
For example, multi-token IDs on NEAR Intents (`intents.near`) embed another asset's ID: `nep245:v2_1.omni.hot.tg:1117_3tsdfyziyc7EJbP2aULWSKU4toBaAcN4FdTgfm5W1mC4ouR` is 76 characters before its `:` and `_` are escaped, and 84 after.
A later revision can add `nep171` and `nep245` once a mapping for such token IDs is agreed.

Holding a NEP-141 token usually requires registering storage with its contract ([NEP-145][]); this affects transfers, not identifiers.

## References

- [CAIP-2 Profile][] - NEAR chain IDs
- [CAIP-10 Profile][] - NEAR account IDs and the `%5F` encoding reused here
- [CAIP-19][] - Asset type and asset ID specification
- [CAIP-20][] - The `slip44` asset namespace for native assets
- [SLIP-0044][] - Registered coin types; 397 is NEAR Protocol
- [NEP-141][] - Fungible token standard
- [NEP-148][] - Fungible token metadata, including `ft_metadata`
- [NEP-145][] - Storage management
- [NEP-171][] - Non-fungible token standard
- [NEP-245][] - Multi-token standard
- [`call_function`][] - RPC query for calling a contract's view methods
- [namespaces PR #203][] - The NEAR CAIP-2 profile and its review discussion

[CAIP-2 Profile]: ./caip2.md
[CAIP-10 Profile]: ./caip10.md
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[CAIP-20]: https://chainagnostic.org/CAIPs/caip-20
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[NEP-141]: https://github.com/near/NEPs/blob/master/neps/nep-0141.md
[NEP-145]: https://github.com/near/NEPs/blob/master/neps/nep-0145.md
[NEP-148]: https://github.com/near/NEPs/blob/master/neps/nep-0148.md
[NEP-171]: https://github.com/near/NEPs/blob/master/neps/nep-0171.md
[NEP-245]: https://github.com/near/NEPs/blob/master/neps/nep-0245.md
[`call_function`]: https://docs.near.org/api/rpc/contracts#call-a-contract-function
[namespaces PR #203]: https://github.com/ChainAgnostic/namespaces/pull/203

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
