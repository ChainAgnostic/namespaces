---
namespace-identifier: algorand-caip19
title: Algorand Namespace - Asset Specification
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

Algorand has exactly two kinds of on-ledger value.
The first is the native unit, ALGO, which is not an asset object at all: it lives in the `microalgos` field of an account and has no identifier.
The second is the [Algorand Standard Asset][] (ASA), a first-class ledger primitive configured by an `acfg` transaction and identified by a uint64 **asset ID** assigned by the protocol.

Everything else an Algorand user would call a "token" — a stablecoin, a governance token, an NFT, a fractional NFT, a receipt — is an ASA.
There is no separate NFT contract, no collection contract, and no token registry: [ARC-3][] and [ARC-69][] are conventions about an ASA's *parameters* and *metadata*, not different ledger objects.
This profile therefore defines a single asset namespace for ASAs, plus `slip44` for ALGO, and nothing else.

The asset ID is a plain decimal integer.
It contains no characters outside `[0-9]`, so it needs no encoding of any kind to fit the [CAIP-19][] `asset_reference` charset — Algorand is one of the few ecosystems where a CAIP-19 reference is byte-identical to the identifier the chain itself uses.
That is worth stating plainly, because it means an implementer can round-trip an Algorand CAIP-19 string through `parseInt`/`toString` with no escaping layer and no risk of a canonicalization bug.

This profile was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a way to name 38 assets on this chain.
The authors do not represent the Algorand ecosystem and offer this for its community to correct, adopt or replace.

## Syntax

After the [CAIP-2][] chain ID, a slash defines an `asset_namespace` and an `asset_reference`.

### Asset Namespaces

| Namespace | Description | Reference Format |
| :--- | :--- | :--- |
| `slip44` | Native ALGO via [SLIP-0044][] | `283` (Algorand's registered coin type) |
| `asa` | Any Algorand Standard Asset | the asset ID, in decimal |

### Asset ID Requirements

An `asa` reference:

- **MUST** be the ASA's asset ID written in base 10 with no `0x` prefix, no grouping separators and no sign.
- **MUST NOT** carry leading zeros; `asa:31566704` and `asa:031566704` are not two spellings of one asset, the second is invalid.
- **MUST** be in the range 1 to 18446744073709551615 (2^64 - 1) inclusive.
- **MUST NOT** be `0`.
  Asset ID 0 is the sentinel that an `acfg` transaction uses to request a *new* asset, and many dApps and indexer APIs reuse it as shorthand for ALGO.
  It is not an asset ID, and ALGO is named by `slip44:283`.

## RegEx

```sh
asset_id:           asset_type
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           "algorand:" + blockchain_id (as defined in [CAIP-2])

asset_namespace:    "slip44" | "asa"

asset_reference:    slip44_ref | asa_ref
slip44_ref:         "283"
asa_ref:            [1-9][0-9]{0,19}
```

The `asa_ref` pattern admits values above 2^64 - 1, which a validator **MUST** reject numerically; the ceiling is not expressible as a regular expression of useful length.

## Semantics

### Native Asset (ALGO)

ALGO is identified with the `slip44` namespace and coin type `283`, registered in [SLIP-0044][] as `| 283 | ALGO | Algorand |`.
It pays fees, funds the minimum-balance reserve that every ASA opt-in consumes, and is the only unit that is not an ASA.
It has no asset ID, and no `asa` reference denotes it.

Example: `algorand:wGHE2Pwdvd7S12BL5FaOP20EGYesN73k/slip44:283`

### Fungible ASAs

A fungible ASA is one whose creator chose a total supply and decimal count that make units interchangeable.
Its `total` and `decimals` are immutable after creation; its `manager`, `reserve`, `freeze` and `clawback` addresses are not, and the asset may be frozen, clawed back or destroyed by whoever holds those roles.
None of that affects identity: the asset ID does.

### Non-Fungible ASAs (ARC-3, ARC-69)

An NFT on Algorand **is an ASA** and uses the same `asa` namespace.
[ARC-3][] defines a *pure* non-fungible token as an ASA whose total number of units is 1 and whose decimal count is 0, and a *fractional* non-fungible token as one whose total is a power of ten greater than 1 with decimals equal to log10 of that total.
[ARC-69][] describes the same ledger object with its metadata carried in the asset-configuration transaction's note field rather than at the asset URL.

This profile deliberately does **not** mint a second `nft` namespace, for three reasons.

1. There is nothing to distinguish. An ARC-3 NFT and a USDC-style stablecoin are the same kind of ledger record, created by the same transaction type, differing only in two integer parameters. A namespace split would encode a reader's judgement, not a protocol fact.
2. ARC-3's fractional NFT makes that judgement undecidable in the general case. An ASA with `total = 100, decimals = 2` is a hundredth-divisible single item under ARC-3 and an ordinary small-supply fungible token under any other reading. Two implementers would emit two different identifiers for it.
3. The split would be a collision by construction. Both namespaces would carry the same asset ID, so `asa:326189642` and a hypothetical `nft:326189642` would name one asset with two strings, defeating the point of a canonical identifier.

The consequence is that for Algorand `asset_type` and `asset_id` coincide: there is no container contract holding a series, so there is no `token_id` component and a CAIP-19 string in this namespace never has a third slash-separated part.
An NFT *collection* on Algorand is a set of independent ASAs related only by metadata, and is not addressable as a CAIP-19 asset type.

### ARC-200 and other application-level tokens

[ARC-200][] specifies fungible tokens implemented as Algorand smart contracts rather than ASAs, identified by a uint64 **application ID** instead of an asset ID.
They are a genuinely distinct ledger object and would need their own namespace — the obvious candidate being `arc200` with the application ID in decimal, mirroring `asa` exactly.
This profile does not define it: the FAR corpus contains no ARC-200 assets, ARC-200 usage on Algorand MainNet is currently thin, and the authors would rather leave the name unclaimed than claim it wrongly.
Reviewers who want it defined should say so.

## Examples

```sh
# Native ALGO on MainNet
algorand:wGHE2Pwdvd7S12BL5FaOP20EGYesN73k/slip44:283

# USDC (asset ID 31566704, 6 decimals, issued by Circle) on MainNet
algorand:wGHE2Pwdvd7S12BL5FaOP20EGYesN73k/asa:31566704

# Tether USDt (asset ID 312769, 6 decimals) on MainNet
algorand:wGHE2Pwdvd7S12BL5FaOP20EGYesN73k/asa:312769

# "Al Goanna 001", a pure NFT (total 1, decimals 0) on MainNet
algorand:wGHE2Pwdvd7S12BL5FaOP20EGYesN73k/asa:326189642

# Native ALGO on TestNet
algorand:SGO1GKSzyE7IEPItTxCByw9x8FmnrCDe/slip44:283
```

## Security Considerations

### An asset ID is the only identity an ASA has

`name` and `unit-name` are free-text fields with no uniqueness constraint.
At the time of writing, Algorand MainNet carries at least twelve live ASAs whose unit name is `USDC` in some capitalization, including asset 25077 ("USD Coin"), 377479508 ("USDC") and 384235993 ("USDC"), none of which is Circle's asset 31566704.
Case variants (`USDc`, `Usdc`, `usdc`) are also in use.
A consumer that resolves an Algorand asset by ticker will pick the wrong one; only the asset ID may be treated as identity, and this profile offers no way to write a ticker into a reference.

### Asset IDs are not reused

The Algorand ledger specification states that an asset-configuration transaction with an asset ID of zero creates "a new asset with an ID corresponding to one plus this transaction's unique counter value", where the counter is the block header's transaction counter plus the transaction's index in the block.
The counter is strictly increasing over the life of the chain, so an asset ID is allocated once and never re-allocated, even after the asset is destroyed.
A CAIP-19 `asa` reference is therefore stable for the life of the network: it may come to denote a destroyed asset, but never a different one.

### Asset IDs are not portable between networks

The counter is per-network, so the same asset ID denotes unrelated assets on MainNet, TestNet and BetaNet.
The [CAIP-2][] chain ID is load-bearing and **MUST NOT** be dropped, including in storage where an implementation "knows" it is on MainNet.

### Mutable parameters under an immutable identifier

An ASA's manager may reconfigure the `manager`, `reserve`, `freeze` and `clawback` addresses, and may destroy the asset outright when it holds the entire supply.
An ARC-69 asset's metadata may be rewritten by a later `acfg` transaction.
Identity is unaffected, which is correct but worth stating: a CAIP-19 reference pins *which* asset, never what it currently claims to be.

## Backwards Compatibility

ASAs have existed since the ASA feature launched in 2019 and their identifier scheme has not changed.
This profile introduces no new encoding and can be produced from, and parsed back into, the `index` field of the algod `/v2/assets/{asset-id}` response without loss.

## References

- [Algorand Standard Asset][] - ASA overview in the Algorand developer documentation
- [Algorand Ledger Specification][] - normative asset-transaction semantics, including asset ID allocation
- [Algorand REST API][] - `algod` `/v2/assets/{asset-id}` and the indexer asset endpoints
- [ARC-3][] - Conventions Fungible/Non-Fungible Tokens, including the pure and fractional NFT definitions
- [ARC-69][] - ASA Parameters Conventions, Digital Media
- [ARC-200][] - Algorand Smart Contract Token Specification
- [SLIP-0044][] - registered coin types, `283` for ALGO
- [CAIP-2][] - the Algorand chain ID profile in this namespace
- [CAIP-19][] - Asset Type and Asset ID Specification

[CAIP-2]: ./caip2.md
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[Algorand Standard Asset]: https://dev.algorand.co/concepts/assets/overview/
[Algorand Ledger Specification]: https://github.com/algorandfoundation/specs/blob/master/_archive/dev/ledger.md
[Algorand REST API]: https://developer.algorand.org/docs/rest-apis/algod/
[ARC-3]: https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md
[ARC-69]: https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0069.md
[ARC-200]: https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0200.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
