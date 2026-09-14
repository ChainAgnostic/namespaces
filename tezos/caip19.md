---
namespace-identifier: tezos-caip19
title: Tezos Namespace - Asset Specification
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

Tezos has one native unit, tez (XTZ), and two ratified token interfaces, and the difference between those two interfaces is the whole reason this profile needs more than one asset namespace.

[TZIP-7][] ("FA1.2 - Approvable Ledger") describes a contract that is a single ledger: one `KT1` address, one token, balances keyed by address alone.
An FA1.2 contract's `transfer` and `getBalance` entrypoints take no token identifier because there is nothing to identify — the contract *is* the token.

[TZIP-12][] ("FA2 - Multi-Asset Interface") describes the opposite.
It states that a "Token type is uniquely identified on the chain by a pair composed of the token contract address and token ID, a natural number (`nat`)", and that a single-token FA2 contract MUST use token ID `0n` while a multi-token contract "is fully responsible for assigning and managing token IDs".
An FA2 contract can hold thousands of unrelated assets: Youves' synthetic-asset contract `KT1XRPEPXbZK25r3Htzp2o1x7xdMMmfocKNW` carries uUSD at token ID 0, uDEFI at 1, uBTC at 2, uXTZ at 3 and uXAU at 4, and they are different assets in every sense that matters to an accountant.

So FA2 genuinely requires the [CAIP-19][] `token_id` component and FA1.2 genuinely must not have one.
Giving both standards one namespace with an optional suffix would let the same asset be written two ways; giving FA1.2 a `token_id` of `0` would encode an indexer's convenience as a chain fact.
This profile keeps them apart.

Contract addresses are `KT1`-prefixed base58check strings of 36 characters and token IDs are decimal naturals, so like Algorand — and unlike Move or Cosmos chains — Tezos needs no percent-encoding anywhere.
Every character of every identifier defined here is already inside the CAIP-19 `asset_reference` and `token_id` charsets.

This profile was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a way to name 13 assets on this chain.
The authors do not represent the Tezos ecosystem and offer this for its community to correct, adopt or replace.

## Syntax

After the [CAIP-2][] chain ID, a slash defines an `asset_namespace` and an `asset_reference`.
For FA2 a further slash and a `token_id` complete the identifier.

### Asset Namespaces

| Namespace | Description | Reference Format | `token_id` |
| :--- | :--- | :--- | :--- |
| `slip44` | Native tez (XTZ) via [SLIP-0044][] | `1729` (Tezos' coin type) | never |
| `fa12` | A [TZIP-7][] FA1.2 single-asset contract | the contract's `KT1` address | never |
| `fa2` | One asset inside a [TZIP-12][] FA2 contract | the contract's `KT1` address | **required** |

`fa12` is spelled without the dot because `asset_namespace` admits only `[-a-z0-9]`; `fa2` is three characters, which is the minimum the grammar allows.

### Contract Address

The reference for `fa12` and `fa2` **MUST** be an originated (smart-contract) address: the literal `KT1`, followed by 33 characters of the Bitcoin base58 alphabet, 36 characters in total.
It is case-sensitive and carries its own base58check checksum, which implementations **SHOULD** verify rather than pattern-match.
Implicit accounts (`tz1`, `tz2`, `tz3`, `tz4`) hold no code and **MUST NOT** appear as an asset reference.

### Token ID

A `fa2` `token_id` **MUST** be the Michelson `nat` written in base 10, with no sign, no `0x` prefix and no leading zeros; `0` itself is written `0`.
A single-asset FA2 contract uses `0`, as TZIP-12 requires.

## RegEx

```sh
asset_id:           asset_type | asset_type + "/" + token_id
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           "tezos:" + blockchain_id (as defined in [CAIP-2])

asset_namespace:    "slip44" | "fa12" | "fa2"

asset_reference:    slip44_ref | kt1_address
slip44_ref:         "1729"
kt1_address:        KT1[1-9A-HJ-NP-Za-km-z]{33}

token_id:           0|[1-9][0-9]{0,76}
```

`slip44` and `fa12` asset types take no `token_id`; `fa2` asset types are incomplete without one.

## Semantics

### Native Asset (XTZ)

Tez is identified with the `slip44` namespace and coin type `1729`, registered in [SLIP-0044][] as `| 1729 | XTZ | Tezos |`.
It pays fees and storage burn, is the unit of staking and delegation, and is not held in any contract ledger.

Example: `tezos:NetXdQprcVkpaWU/slip44:1729`

### FA1.2 Assets

An FA1.2 contract implements a single approvable ledger, so its `KT1` address identifies the asset outright and the asset type is complete without a `token_id`.

Block explorers and indexers commonly normalise FA1.2 into their FA2 data model by synthesising a token ID of `0`.
That `0` is an artefact of the indexer, not of the chain: no FA1.2 entrypoint accepts or returns it.
It **MUST NOT** be appended to a `fa12` reference, and an FA1.2 contract **MUST NOT** be written as `fa2:<address>/0`.

### FA2 Assets

An FA2 asset type is the `(contract address, token ID)` pair that TZIP-12 makes normative, written as a CAIP-19 `asset_id`.

[CAIP-19][] introduces the `token_id` suffix "in the case of non-fungible tokens or other collections", and FA2 is squarely the second case: an FA2 contract is a collection of token types that may be fungible, non-fungible, or a mix in one contract, exactly as ERC-1155 is on EVM chains.
An FA2 asset therefore always renders as an `asset_id`, whether or not the asset it names is fungible.
Consumers **MUST NOT** infer fungibility from the presence of the suffix.

Fungible example — Tether USD on Tezos, an FA2 contract with one token type at ID 0, 6 decimals:

```
tezos:NetXdQprcVkpaWU/fa2:KT1XnTn74bUtxHfDtBmm2bGZAQfhPbvKWR8o/0
```

Multi-asset example — Youves uDEFI, token ID 1 inside a contract that also issues uUSD, uBTC, uXTZ and uXAU:

```
tezos:NetXdQprcVkpaWU/fa2:KT1XRPEPXbZK25r3Htzp2o1x7xdMMmfocKNW/1
```

### Non-Fungible Assets

Tezos has no NFT standard separate from FA2; an NFT is an FA2 token type whose supply is 1, usually with `decimals` 0 and TZIP-21 metadata.
It uses the `fa2` namespace and the same `contract/token_id` shape as any other FA2 asset, which is the intended reading of CAIP-19's asset-type/asset-ID split.

```
tezos:NetXdQprcVkpaWU/fa2:KT1RJ6PbjHpwc3M5rw5s2Nbmefwbuwbdxton/884710
```

The FA2 asset *type* — `fa2:KT1RJ6PbjHpwc3M5rw5s2Nbmefwbuwbdxton` without a suffix — is not a valid identifier under this profile.
It would name a contract, not an asset, and on a contract like hic et nunc's that is a marketplace-wide container of unrelated works rather than a collection in the ERC-721 sense.

### Tickets

Michelson tickets are a protocol-level asset primitive, typed by `(issuer address, content)` rather than by a contract address, and are not addressable through any token-standard entrypoint.
No namespace is defined for them here.
They are named for completeness so that a reviewer can see the omission is deliberate.

## Examples

```sh
# Native tez on Mainnet
tezos:NetXdQprcVkpaWU/slip44:1729

# Tether USD (USDt), FA2, single token type, 6 decimals
tezos:NetXdQprcVkpaWU/fa2:KT1XnTn74bUtxHfDtBmm2bGZAQfhPbvKWR8o/0

# youves uDEFI, FA2 token ID 1 of a multi-asset contract
tezos:NetXdQprcVkpaWU/fa2:KT1XRPEPXbZK25r3Htzp2o1x7xdMMmfocKNW/1

# Kolibri USD (kUSD), FA1.2, 18 decimals -- no token_id
tezos:NetXdQprcVkpaWU/fa12:KT1K9gCRgaLRFKTErYt1wVxA3Frb9FjasjTV

# tzBTC, FA1.2, 8 decimals
tezos:NetXdQprcVkpaWU/fa12:KT1PWx2mnDueood7fEmfbBDKx1D9BAnnXitn

# hic et nunc OBJKT #884710, an FA2 non-fungible
tezos:NetXdQprcVkpaWU/fa2:KT1RJ6PbjHpwc3M5rw5s2Nbmefwbuwbdxton/884710

# Native tez on Ghostnet
tezos:NetXnHfVqm9iesp/slip44:1729
```

## Security Considerations

### Symbols are metadata and collide freely

Token symbols live in TZIP-16/TZIP-21 metadata and are neither unique nor validated.
Tezos Mainnet currently carries at least two FA2 contracts whose token metadata claims the symbol `USDt` at token ID 0: `KT1XnTn74bUtxHfDtBmm2bGZAQfhPbvKWR8o`, the Tether issuance with roughly 141 million units and thousands of holders, and `KT19f2aMEKeG3zVY7vRiSGsW2pnVQ3svRff9`, a 2022 contract whose entire supply was minted and burned and which has had no transfers since.
No part of this profile lets a symbol into an identifier, and consumers **MUST NOT** resolve Tezos assets by symbol.

### Same address, two namespaces

A contract address is unique on-chain, but nothing stops a producer from writing an FA1.2 contract as `fa2:<address>/0` or an FA2 contract as `fa12:<address>`.
Both are wrong and both parse.
Producers **MUST** choose the namespace from the contract's declared interface — TZIP-016 metadata, or the presence of a `nat %token_id` field in the `transfer` parameter type — not from an indexer's normalised view.
Consumers that see the same `KT1` address under both namespaces **SHOULD** treat it as a data-quality error rather than as two assets.

### `nat` is unbounded, `token_id` is not

Michelson's `nat` has no upper bound, while [CAIP-19][] caps `token_id` at 78 characters.
Tezos contracts already use large token IDs — Youves' contract has a live entry at token ID `30000000000000` — and a contract is free to assign an ID above 10^78, which this profile cannot express.
Such an asset is unrepresentable in CAIP-19 and implementations **MUST** fail loudly rather than truncate or hash.
No such asset is known to the authors today; the limit is recorded so that whoever meets one first knows it is a specification gap and not their bug.

### The address is the identity, not the code

A Tezos contract's behaviour can change without its address changing, through lambdas stored in its own storage or through a proxy pattern.
A CAIP-19 reference pins the address; it makes no claim about the code currently running there or about the asset's continued redeemability.

## Backwards Compatibility

FA1.2 (2019) and FA2 (2020) are both Final TZIPs and neither has been superseded, so both namespaces are needed indefinitely; `fa12` is not a legacy alias for `fa2`.
The `NetX…` chain IDs used above are those already defined by this namespace's [CAIP-2][] profile and are unchanged here.

## References

- [TZIP-7][] - FA1.2, the Approvable Ledger interface
- [TZIP-12][] - FA2, the Multi-Asset Interface, including the contract-address-plus-token-ID identity rule
- [TZIP-16][] - Contract metadata
- [TZIP-21][] - Rich token metadata, used by Tezos NFTs
- [TzKT API][] - the indexer queried to verify every contract and token ID in this document
- [SLIP-0044][] - registered coin types, `1729` for XTZ
- [CAIP-2][] - the Tezos chain ID profile in this namespace
- [CAIP-19][] - Asset Type and Asset ID Specification

[CAIP-2]: ./caip2.md
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[TZIP-7]: https://gitlab.com/tezos/tzip/-/blob/master/proposals/tzip-7/tzip-7.md
[TZIP-12]: https://gitlab.com/tezos/tzip/-/blob/master/proposals/tzip-12/tzip-12.md
[TZIP-16]: https://gitlab.com/tezos/tzip/-/blob/master/proposals/tzip-16/tzip-16.md
[TZIP-21]: https://gitlab.com/tezos/tzip/-/blob/master/proposals/tzip-21/tzip-21.md
[TzKT API]: https://api.tzkt.io/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
