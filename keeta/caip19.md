---
namespace-identifier: keeta-caip19
title: Keeta - Asset Type and Asset ID Specification
author: ["@sc4l3r"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/XXXX
status: Draft
type: Standard
created: 2026-04-27
requires: ["CAIP-2", "CAIP-19"]
---

# CAIP-19

_For context, see the [CAIP-19][] specification._

## Introduction

Keeta has a single, native, first-class token model: every transferable asset on a Keeta network -- including the network's own base token -- is a [token account][accounts] with its own `keeta_...` address.
There is no separate token-contract registry, no ERC-20-style metadata contract, and no parallel address space for NFTs: an NFT on Keeta is simply a token account whose total supply is `1` and whose decimal count is `0`.

Because of this, every Keeta asset is fully identified by:

1. The CAIP-2 reference for its network (defined by the [Keeta CAIP-2 Profile][CAIP-2 Profile]).
2. The token account's address (defined in the same form as the [Keeta CAIP-10 Profile][CAIP-10 Profile]).

## Specification

### Semantics

The inputs are:

- A Keeta `networkId` identifying the network the asset lives on.
- An asset-namespace tag drawn from the fixed set (`token`, `nft`).
- A Keeta token-account address (see [Keeta CAIP-10 Profile][CAIP-10 Profile]).

The asset-namespace tag carries **no on-chain meaning** -- Keeta itself does not distinguish "fungible" from "non-fungible" at the protocol level -- and is purely an interoperability hint to consumers.
A CAIP-19 string with `nft:` referring to a token whose supply is greater than `1` SHOULD be treated as malformed by validators that have access to the chain.

| `asset_namespace` | Use                                                                                               | Equivalent in other namespaces                 |
| :---------------- | :------------------------------------------------------------------------------------------------ | :--------------------------------------------- |
| `token`           | Any fungible token on a Keeta network, including the network's base token.                        | `eip155:1/erc20:0x...`, `solana:.../token:...` |
| `nft`             | A non-fungible token. Implementations SHOULD only use `nft` when the token's supply is exactly 1. | `eip155:1/erc721:0x...`, `solana:.../nft:...`  |

The base token of a Keeta network is just another token account: it is referenced via the `token` asset namespace using the address returned by `Account.generateBaseAddresses(networkId).baseToken`.
Mainnet KTA is also registered in [SLIP-0044][] as coin type `8887` for use in HD-wallet derivation paths and similar SLIP-0044-indexed contexts; this profile does not surface SLIP-0044 in [CAIP-19][] form, since on Keeta the base token has a first-class on-chain address that already serves as a canonical [CAIP-19][] reference, and only mainnet has a SLIP-0044 entry.

### Syntax

A Keeta [CAIP-19][] **asset type** identifier MUST take the form:

```
keeta:<networkId>/<asset_namespace>:<address>
```

A Keeta [CAIP-19][] **asset ID** identifier (a specific NFT) MUST take the form:

```
keeta:<networkId>/<asset_namespace>:<address>/<token_id>
```

Where:

- `keeta` is the namespace.
- `<networkId>` is a CAIP-2 reference for a Keeta network as defined by the [Keeta CAIP-2 Profile][CAIP-2 Profile].
- `<asset_namespace>` is `token` or `nft` (see the table above).
- `<address>` is the canonical Keeta token-account address, **including** its `keeta_` prefix (see [Keeta CAIP-10 Profile][CAIP-10 Profile] for validation).
- `<token_id>`, when present, is the decimal index of an individual unit within a multi-unit token account; see [NFT collections](#nft-collections) below. It MUST match the [CAIP-19][] `token_id` character set, `^[-.%a-zA-Z0-9]{1,78}$`.

#### NFT collections

Multi-unit NFT collection identity is not yet standardized in the Keeta protocol.
The `<token_id>` form is documented here because [CAIP-19][] permits it, but this profile does not define its semantics.
Producers SHOULD omit the `<token_id>` segment; a future revision of this profile will specify its use once the protocol standardizes collection identity (e.g. for fractional NFTs that adopt sub-unit identity at the application layer).

### Resolution Mechanics

To validate a Keeta CAIP-19 identifier:

1. Split on `/` and `:` and verify the namespace is `keeta` and the asset-namespace is `token` or `nft`.
2. Validate `<networkId>` against the [Keeta CAIP-2 Profile][CAIP-2 Profile].
3. Validate `<address>` against the same codec used by the [Keeta CAIP-10 Profile][CAIP-10 Profile] (type must be `TOKEN`; checksum must verify).
4. For `nft`, consumers SHOULD query a node on the indicated network to confirm the token's `supply == 1` and `decimalPlaces == 0` before treating the identifier as a non-fungible asset, and SHOULD treat any identifier that fails this check as malformed.

## Rationale

Keeta uses a single, unified address space for every transferable asset, including the base token: there is no separate native-coin concept at the protocol level.
This profile reflects that by using `token` for every fungible asset and `nft` only as an interoperability hint for token accounts whose supply is `1` and decimals are `0`, mirroring the approach taken by the Solana namespace, which has a similarly unified address space for fungible and non-fungible assets.

### Backwards Compatibility

This is the first [CAIP-19][] specification for the `keeta` namespace, so there are no legacy identifiers to support.

## Test Cases

Base token (KTA) of the Keeta main network, referenced by its on-chain token-account address:

```
keeta:21378/token:keeta_anqdilpazdekdu4acw65fj7smltcp26wbrildkqtszqvverljpwpezmd44ssg
```

Any other fungible token on mainnet uses the same form, with the address of the relevant token account.

NFT on mainnet (total supply == 1, decimals == 0):

```
keeta:21378/nft:keeta_amob7pxzhexqych4g56bmmtovdgwr6kljloyzkyb34k37jntj24doaqfbx4xk
```

Invalid:

```
# Non-token address used with a token asset namespace (storage prefix `aq`)
keeta:21378/token:keeta_aqltdal4rshtky5iehd765y3mdjkcmku5d4ulo5fgonzqrxulwepnogq33mle

# Missing keeta_ prefix
keeta:21378/token:anqdilpazdekdu4acw65fj7smltcp26wbrildkqtszqvverljpwpezmd44ssg

# Hex networkId (see Keeta CAIP-2 Profile)
keeta:0x5382/token:keeta_anqdilpazdekdu4acw65fj7smltcp26wbrildkqtszqvverljpwpezmd44ssg
```

## References

- Keeta [accounts] - defines token accounts and the unified address space for fungible/non-fungible assets.
- Keeta [SDK source][sdk] - `Account.AccountKeyAlgorithm.TOKEN` and `generateBaseAddresses(networkId)` define how a token account's address is constructed.
- [Keeta CAIP-2 Profile][CAIP-2 Profile] - the network portion of the identifier.
- [Keeta CAIP-10 Profile][CAIP-10 Profile] - the address syntax reused for the `<address>` segment.

[CAIP-2 Profile]: ./caip2.md
[CAIP-10 Profile]: ./caip10.md
[accounts]: https://docs.keeta.com/components/accounts
[sdk]: https://github.com/KeetaNetwork/keetanet-client
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
