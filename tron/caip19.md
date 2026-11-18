---
namespace-identifier: tron-caip19
title: Tron Namespace - Asset Specification
author: ["Billy Rennekamp (@okwme)"]
discussions-to: https://github.com/0xcounting/FAR/issues/1
status: Draft
type: Standard
created: 2026-09-14
requires: ["CAIP-19", "CAIP-2"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Rationale

Tron carries four kinds of asset, and they are not variations on one another.
TRX is the native coin.
[TRC-10][TIP-10] tokens are issued by the protocol itself and are identified by a numeric id the chain assigns at issuance — there is no contract behind them.
[TRC-20][TIP-20], [TRC-721][TIP-721] and [TRC-1155][TIP-1155] tokens are smart contracts on the TVM, addressed like any other Tron account.
The TRC-10 case is the unusual one: it is a genuinely contract-less fungible asset class, and folding it into the contract-addressed namespaces would misrepresent both.

Tron's character set is kind to [CAIP-19][].
Base58Check addresses and decimal token ids are alphanumeric, so **no percent-encoding is required anywhere in this profile**.
The only real decision is which of the several circulating spellings of a Tron address is canonical, and this profile answers it the same way the ratified [CAIP-10][] profile for this namespace already did: Base58Check.

This profile was drafted by the maintainers of FAR, an open cross-reference between [CAIP-19][], CoinGecko and ISO 24165 identifiers, which needs a way to name 92 assets on this chain.
The authors do not represent the Tron ecosystem and offer this for its community to correct, adopt or replace.

## Syntax

After the [CAIP-2][] namespace and chain ID, a slash introduces an `asset_namespace` and an `asset_reference`.

### Asset Namespaces

| Namespace | Asset kind | Reference format |
| :--- | :--- | :--- |
| `slip44` | Native coin (TRX) | `195`, Tron's [SLIP-0044][] coin type |
| `trc10` | [TRC-10][TIP-10] protocol-issued token | the numeric token id in decimal |
| `trc20` | [TRC-20][TIP-20] fungible token | contract address, Base58Check |
| `trc721` | [TRC-721][TIP-721] non-fungible token | contract address, Base58Check |
| `trc1155` | [TRC-1155][TIP-1155] multi-token | contract address, Base58Check |

`trc721` and `trc1155` take a `token_id`; `slip44`, `trc10` and `trc20` are bare `asset_type`s.

### Contract address format

The canonical reference for `trc20`, `trc721` and `trc1155` is the contract's **Base58Check** address: exactly 34 characters, always beginning with `T`, drawn from the Bitcoin Base58 alphabet, case-sensitive.
This is the form specified for accounts by the [CAIP-10][] profile in this namespace, and using anything else for assets would leave one namespace describing the same 20 bytes two different ways.

Three further reasons make Base58Check the right choice over the hexadecimal forms:

- It carries a four-byte double-SHA-256 checksum, so a mistyped or truncated reference fails locally rather than resolving to nothing or, worse, to another account.
- It has exactly one spelling per address.
  Hexadecimal is case-insensitive in practice, so a 20-byte address has 2^40 hexadecimal spellings and no canonicalisation scheme comparable to [EIP-55][] is in use on Tron.
- It is what users, wallets and [Tronscan][] display, so a reference can be compared against what a signer sees.

### Converting from the hexadecimal forms

Two hexadecimal spellings circulate and neither is canonical here.

The **21-byte form** is what Tron's own HTTP API returns when `visible` is false: the byte `0x41` followed by the 20-byte account identifier, rendered as 42 hexadecimal digits, e.g. `41a614f803b6fd780986a42c78ec9c7f77e6ded13c`.

The **20-byte form** is what Tron's EVM-compatible JSON-RPC uses: the same 20 bytes with a `0x` prefix and no `0x41`, e.g. `0xa614f803b6fd780986a42c78ec9c7f77e6ded13c`.

To convert either to the canonical form:

1. Strip a `0x` prefix if present.
2. If the result is 40 hexadecimal digits, prepend `41`; it must now be 42 digits beginning with `41`.
3. Decode those 21 bytes; append the first four bytes of `SHA-256(SHA-256(payload))` as a checksum.
4. Base58-encode the 25 bytes.

The inverse — Base58-decode, verify the checksum, drop it, hex-encode — recovers the 21-byte form, and dropping the leading `41` recovers the 20-byte form.
Implementations MUST verify the checksum when accepting a Base58Check reference.

### TRC-10 token ids

A TRC-10 token id is an unsigned integer assigned by the chain when the asset is issued, rendered in decimal without leading zeroes.
Ids currently in use begin at `1000001`.
The id, and only the id, identifies a TRC-10 asset, for the reasons set out in the Collisions section below.

## RegEx

The RegEx validation strings are as follows:

```sh
asset_id:           asset_type | asset_type + "/" + token_id
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           namespace + ":" + blockchain_id (as defined in [CAIP-2])

asset_namespace:    "slip44" | "trc10" | "trc20" | "trc721" | "trc1155"

asset_reference:    slip44_ref | trc10_ref | address_ref
slip44_ref:         "195"
trc10_ref:          [1-9][0-9]{0,18}
address_ref:        T[1-9A-HJ-NP-Za-km-z]{33}

token_id:           0|[1-9][0-9]{0,77}
```

`address_ref` is the canonical reference for `trc20`, `trc721` and `trc1155`, and is the same production the [CAIP-10][] profile uses for accounts.
`token_id` applies to `trc721` and `trc1155` only.

## Semantics

### Native coin (`slip44`)

TRX is identified with the `slip44` asset namespace and Tron's registered coin type, as [CAIP-20][] describes.
The [SLIP-0044][] registry line is:

```
| 195        | TRX     | Tron                              |
```

TRX has six decimals; its smallest unit is the SUN, and 1 TRX = 1,000,000 SUN.
The same identifier shape applies on the testnets, qualified by their chain IDs, so TRX on Shasta is `tron:2494104990/slip44:195`.

### TRC-10 (`trc10`)

[TRC-10][TIP-10] is Tron's protocol-level token standard.
An asset is created by an `AssetIssueContract` transaction rather than by deploying code, and the chain assigns it a numeric id.
There is no contract address to name, and no ABI to call: an asset's parameters are read with `wallet/getassetissuebyid`.

A TRC-10 asset carries a `name`, an `abbr` and a `precision`, all chosen by the issuer and none of them unique.
Only the numeric id is an identifier.

### TRC-20 (`trc20`)

[TRC-20][TIP-20] is the TVM fungible token interface, functionally [ERC-20][].
The reference is the token contract's address in canonical Base58Check form.
`name()`, `symbol()` and `decimals()` are metadata: they may be absent, may be duplicated across contracts, and in an upgradeable contract may change.

### TRC-721 (`trc721`)

[TRC-721][TIP-721] is the TVM non-fungible token interface, functionally [ERC-721][].
The `asset_type` is `trc721:` + the contract address and the `token_id` is the item's `uint256` id in decimal, without leading zeroes.
A `uint256` is at most 78 decimal digits, exactly the `token_id` limit, so every well-formed id fits.

A TRC-721 contract can be recognised on-chain: `supportsInterface(0x80ac58cd)` returns true, and `supportsInterface(0x5b5e139f)` indicates the metadata extension.

### TRC-1155 (`trc1155`)

[TRC-1155][TIP-1155] is the TVM multi-token interface, functionally [ERC-1155][].
A single contract holds many token types, each of which may be fungible, non-fungible or semi-fungible, so the contract address alone does **not** name an asset.
A `trc1155` identifier MUST therefore carry a `token_id`; the bare `asset_type` names the contract, not a balance-bearing asset, and implementations SHOULD NOT emit it as an asset identifier.

A TRC-1155 contract is recognised by `supportsInterface(0xd9b67a26)`.

## Examples

```sh
# TRX, the native coin of Tron mainnet
tron:728126428/slip44:195

# TRX on the Shasta testnet
tron:2494104990/slip44:195

# Tether USD (USDT), the flagship TRC-20 token
# hex forms: 41a614f803b6fd780986a42c78ec9c7f77e6ded13c / 0xa614f803b6fd780986a42c78ec9c7f77e6ded13c
tron:728126428/trc20:TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t

# BitTorrent (BTT) as a TRC-20 contract, 18 decimals
tron:728126428/trc20:TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4

# BitTorrent (BTT) as TRC-10 token id 1002000, 6 decimals -- a different asset
tron:728126428/trc10:1002000

# SEED, TRC-10 token id 1000001
tron:728126428/trc10:1000001

# Devikins NFT (DVKNFT) item 1, a TRC-721 non-fungible
tron:728126428/trc721:THjYwnDDN6aYxrzKb88CSMTEYjBuHpoYxS/1

# PHONFT1155 token type 1, a TRC-1155 asset
tron:728126428/trc1155:TXWLT4N9vDcmNHDnSuKv2odhBtizYuEMKJ/1
```

### Address round trip

The three spellings of the USDT contract, and the single identifier they all reduce to:

```sh
TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t            # Base58Check -- canonical
41a614f803b6fd780986a42c78ec9c7f77e6ded13c    # 21-byte hex, Tron HTTP API with visible=false
0xa614f803b6fd780986a42c78ec9c7f77e6ded13c    # 20-byte hex, Tron JSON-RPC (eth_call and friends)

tron:728126428/trc20:TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t
```

## Collisions and Security Considerations

### TRC-10 names and tickers are massively duplicated

TRC-10 assets were originally addressed by name, and the numeric id was introduced precisely because names are not unique.
Querying `wallet/getassetissuelistbyname` on mainnet returns **thirteen** distinct TRC-10 assets named `BitTorrent` with the abbreviation `BTT`, ids `1000491`, `1001948`, `1001952`, `1001964`, `1002000`, `1002001`, `1002009`, `1002038`, `1002065`, `1002101`, `1002443`, `1002928` and `1004648`, each with a different issuer.
Seven distinct assets are named `SEED`, and one of those uses the abbreviation `Trx`.

An implementation that keys TRC-10 assets on name or ticker will merge thirteen unrelated tokens into one, twelve of them worthless impostors of the thirteenth.
Only `trc10:<id>` is safe.

### The same ticker spans standards

`BTT` names both TRC-10 id `1002000` (6 decimals) and the TRC-20 contract `TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4` (18 decimals), the latter being the migration target of the former.
They are separate assets with separate balances and different scaling, and the namespace separation between `trc10` and `trc20` is what keeps them apart.
This is the principal reason TRC-10 is given its own `asset_namespace` rather than being squeezed into `trc20`.

### The 20-byte hexadecimal form is indistinguishable from an Ethereum address

Tron derives account identifiers with Keccak-256 over a secp256k1 public key, exactly as Ethereum does, and its JSON-RPC exposes them as bare `0x`-prefixed 20-byte values.
A reference built naively from an `eth_call` result is therefore byte-identical in shape to an `eip155` [ERC-20][] reference, and the two are told apart only by the `chain_id` in front.
Base58Check removes the hazard at the reference level: a Tron asset reference is visibly a Tron asset reference.

### Hexadecimal has no canonical capitalisation on Tron

`41A614F8…` and `41a614f8…` are the same contract.
[EIP-55][]-style checksummed capitalisation is not used on Tron, so any hexadecimal reference form would admit 2^40 spellings of one asset with no rule to pick among them.
Base58Check admits exactly one.

### A bare TRC-1155 contract reference is not an asset

Because one TRC-1155 contract can hold arbitrarily many token types, `trc1155:<address>` with no `token_id` is a category error rather than a fungible class.
Consumers MUST NOT treat a bare `trc1155` `asset_type` as naming a balance.

### Contract addresses are not self-describing

Nothing in an address says which standard its contract implements, and the same address can never be two standards at once but can easily be mislabelled.
A resolver SHOULD confirm the standard before emitting an identifier: `supportsInterface(0x80ac58cd)` for `trc721`, `supportsInterface(0xd9b67a26)` for `trc1155`, and, since [TRC-20][TIP-20] defines no interface detection, a successful `decimals()`/`symbol()` call plus the absence of the two interface flags for `trc20`.

### Metadata is not an identifier

`name()`, `symbol()` and `decimals()` on a TRC-20 contract, and the `name`/`abbr`/`precision` fields of a TRC-10 asset, are issuer-chosen strings.
No identifier in this profile is derived from them.

## Backwards Compatibility

This is the first asset specification for the `tron` namespace, so there is no prior [CAIP-19][] profile to be compatible with.

It is consistent with the ratified [CAIP-2][] profile, which fixes the decimal chain ID (`tron:728126428` for mainnet), and with the ratified [CAIP-10][] profile, whose account regular expression `^T[1-9A-HJ-NP-Za-km-z]{33}$` this document reuses unchanged for contract-addressed assets.
Implementations that previously emitted hexadecimal asset references should treat them as deprecated aliases: accept them on input, convert as described above, and emit only Base58Check.
The underlying contract is unchanged, so no on-chain migration is required.

All four token standards are Final TIPs with deployed contracts long predating this document.

## References

- [CAIP-2][]: Blockchain ID Specification
- [CAIP-10][]: Account ID Specification
- [CAIP-19][]: Asset Type and Asset ID Specification
- [CAIP-20][]: Asset Reference for the SLIP44 Asset Namespace
- [SLIP-0044][]: Registered coin types for BIP-0044
- [TIP-10][]: TRC-10 Token Standard
- [TIP-20][]: TRC-20 Token Standard
- [TIP-721][]: TRC-721 Non-Fungible Token Standard
- [TIP-1155][]: TRC-1155 Multi Token Standard
- [Tron Address Format][]: Base58Check address derivation
- [TronGrid][]: Tron HTTP API and JSON-RPC service
- [TronGrid Docs][]: Documentation for the TronGrid hosted node service
- [getassetissuebyid][]: The HTTP API used to resolve a TRC-10 token id
- [Tronscan][]: Tron block explorer
- [EIP-55][]: Mixed-case checksum address encoding, referenced for contrast
- [ERC-20][], [ERC-721][], [ERC-1155][]: the Ethereum standards the TVM ones mirror

[CAIP-2]: ./caip2.md
[CAIP-10]: ./caip10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-20]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-20.md
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[TIP-10]: https://github.com/tronprotocol/tips/blob/master/tip-10.md
[TIP-20]: https://github.com/tronprotocol/tips/blob/master/tip-20.md
[TIP-721]: https://github.com/tronprotocol/tips/blob/master/tip-721.md
[TIP-1155]: https://github.com/tronprotocol/tips/blob/master/tip-1155.md
[Tron Address Format]: https://tronprotocol.github.io/documentation-en/mechanism-algorithm/account/
[TronGrid]: https://www.trongrid.io/
[TronGrid Docs]: https://developers.tron.network/docs/trongrid
[getassetissuebyid]: https://developers.tron.network/reference/getassetissuebyid
[Tronscan]: https://tronscan.org/
[EIP-55]: https://eips.ethereum.org/EIPS/eip-55
[ERC-20]: https://eips.ethereum.org/EIPS/eip-20
[ERC-721]: https://eips.ethereum.org/EIPS/eip-721
[ERC-1155]: https://eips.ethereum.org/EIPS/eip-1155

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
