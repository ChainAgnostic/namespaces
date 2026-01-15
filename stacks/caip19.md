---
namespace-identifier: stacks-caip19
title: Stacks Namespace - Assets
author: Friedger Müffke (@friedger), Jason Schrader (@whoabuddy)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/68
status: Draft
type: Standard
created: 2023-05-21
updated: 2025-01-14
requires: ["CAIP-2", "CAIP-10", "CAIP-19"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Rationale

In the Stacks ecosystem, token assets are defined within smart contracts written in [Clarity][], a decidable language with native asset primitives.
A single contract can define multiple fungible tokens (FTs) and non-fungible tokens (NFTs), each identified by a unique name within the contract.

Token assets are uniquely identified by combining the deployer address, contract name, and the token name declared within that contract using `define-fungible-token` or `define-non-fungible-token`.

The Stacks community has established standard interfaces for tokens:

- [SIP-010][]: Fungible Token Standard (analogous to ERC-20)
- [SIP-009][]: Non-Fungible Token Standard (analogous to ERC-721)

## Syntax

After the [CAIP-2][] namespace+chainID, a slash defines an `asset_namespace` and an `asset_reference`.

### Asset Namespaces

| Namespace | Description | Reference Format |
| :--- | :--- | :--- |
| `sip010` | Fungible token ([SIP-010][]) | `{contract-principal}.{token-name}` |
| `sip009` | Non-fungible token ([SIP-009][]) | `{contract-principal}.{token-name}` |

### Asset Reference Components

The asset reference combines the contract principal with the token identifier:

```
{address}.{contract}.{token-name}
```

- **address**: A valid Stacks address in [c32check][] encoding (starts with `SP` for mainnet, `ST` for testnet)
- **contract**: The deployed contract name (1-40 characters, alphanumeric with hyphens and underscores, must start with a letter)
- **token-name**: The identifier used in the contract's `define-fungible-token` or `define-non-fungible-token` declaration

All three components are separated by periods (`.`).
The first period separates the address from the contract name (forming the contract principal), and the second period separates the contract principal from the token name.

Note: In Clarity source code, the fully-qualified asset identifier uses `::` as a separator (e.g., `SP...contract::token`).
For CAIP-19 compatibility, this specification uses `.` as the separator since colons are not permitted in asset references per the [CAIP-19][] specification.

### Token ID (NFTs)

For non-fungible tokens (SIP-009), an optional token ID can be appended after a forward slash (`/`) to identify a specific token instance.
Token IDs are typically unsigned integers starting from 1, as returned by the contract's `get-last-token-id` function.

## RegEx

The RegEx validation strings are as follows:

```
asset_id:           asset_type + "/" + token_id (optional for sip009)
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           namespace + ":" + blockchain_id (as defined in CAIP-2)

asset_namespace:    "sip010" | "sip009"

asset_reference:    address + "." + contract_name + "." + token_name
address:            S[PMNT][A-Z0-9]{38,39}
contract_name:      [a-zA-Z][a-zA-Z0-9_-]{0,39}
token_name:         [a-zA-Z][a-zA-Z0-9_-]{0,127}

token_id:           [1-9][0-9]{0,38}
```

Note: Stacks mainnet addresses start with `SP` or `SM`, while testnet addresses start with `ST` or `SN`.

### Case Sensitivity

Stacks addresses use [c32check][] encoding, which is case-insensitive but canonically represented in uppercase (as specified in [CAIP-10][]).
However, contract names and token names in Clarity are case-sensitive.

Implementations SHOULD:
- Accept addresses in any case but normalize to uppercase for comparison
- Preserve exact case for contract names and token names as deployed on-chain

Note: The total `asset_reference` (address + contract + token name) must not exceed 128 characters per the [CAIP-19][] specification.

## Semantics

### Fungible Tokens (SIP-010)

Fungible tokens following the [SIP-010][] standard implement a common interface for token transfers, balance queries, and metadata.
The standard requires implementation of:

- `transfer`: Move tokens between principals
- `get-balance`: Query token balance for an address
- `get-total-supply`: Query total token supply
- `get-name`, `get-symbol`, `get-decimals`: Token metadata

Each fungible token is uniquely identified by its contract principal and the token name declared via `(define-fungible-token <token-name>)`.

### Non-Fungible Tokens (SIP-009)

Non-fungible tokens following the [SIP-009][] standard represent unique digital assets.
The standard requires implementation of:

- `transfer`: Move NFT ownership
- `get-owner`: Query current owner of a token ID
- `get-last-token-id`: Query the highest minted token ID
- `get-token-uri`: Query metadata URI for a token

Each NFT collection is identified by its contract principal and token name declared via `(define-non-fungible-token <token-name> <token-type>)`.
Individual tokens within a collection are distinguished by their token ID.

## Examples

```
# SIP-010 Fungible Token: sBTC on Mainnet
stacks:1/sip010:SM3VDXK3WZZSA84XXFKAFAF15NNZX32CTSG82JFQ4.sbtc-token.sbtc-token

# SIP-009 NFT Collection: Megapont Ape Club on Mainnet
stacks:1/sip009:SP3D6PV2ACBPEKYJTCMH7HEN02KP87QSP8KTEH335.megapont-ape-club-nft.Megapont-Ape-Club

# SIP-009 NFT: Specific Megapont Ape (#4) on Mainnet
stacks:1/sip009:SP3D6PV2ACBPEKYJTCMH7HEN02KP87QSP8KTEH335.megapont-ape-club-nft.Megapont-Ape-Club/4

# SIP-010 Fungible Token on Testnet
stacks:2147483648/sip010:ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM.my-token.my-ft

# SIP-009 NFT on Testnet
stacks:2147483648/sip009:ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM.my-nft.my-nft-token/1
```

## Backwards Compatibility

This specification supersedes the approach proposed in [PR #68][], which used `sip9` and `sip10` namespaces without the token name component.
The updated format provides more precise asset identification by including the token name as declared in the smart contract, which is necessary because a single Stacks contract can define multiple distinct tokens.

## References

- [Clarity Language Reference][Clarity] - Smart contract language documentation
- [SIP-009][] - Non-Fungible Token Standard
- [SIP-010][] - Fungible Token Standard
- [c32check][] - Stacks address encoding

[CAIP-2]: ./caip2.md
[CAIP-10]: ./caip10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[Clarity]: https://docs.stacks.co/clarity/overview
[SIP-009]: https://github.com/stacksgov/sips/blob/main/sips/sip-009/sip-009-nft-standard.md
[SIP-010]: https://github.com/stacksgov/sips/blob/main/sips/sip-010/sip-010-fungible-token-standard.md
[c32check]: https://github.com/stacks-network/c32check
[PR #68]: https://github.com/ChainAgnostic/namespaces/pull/68

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
