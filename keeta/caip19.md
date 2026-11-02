---
namespace-identifier: keeta-caip19
title: Keeta - Asset Type and Asset ID Specification
author: ["@sc4l3r", "@xescure"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/183
status: Draft
type: Standard
created: 2026-04-27
requires: ["CAIP-2", "CAIP-19"]
---

# CAIP-19

_For context, see the [CAIP-19][] specification._

## Introduction

Keeta has a single, native, first-class token model: every transferable asset on a Keeta network -- including the network's own base token -- is a [token account][accounts] with its own `keeta_...` address.
There is no separate token-contract registry, no ERC-20-style metadata contract, and no parallel address space for NFTs: an NFT on Keeta is simply a token account whose raw on-chain supply (before display decimals) is `1`.

Because of this, every Keeta asset is fully identified by:

1. The network identifier (defined by the [Keeta CAIP-2 Profile][CAIP-2 Profile]).
2. The token account's address (in the form defined by the [Keeta CAIP-10 Profile][CAIP-10 Profile]).

## Specification

### Semantics

The inputs are:

- A Keeta network identifier, as defined in the [Keeta CAIP-2 Profile][CAIP-2 Profile], identifying the network the asset lives on.
- An asset-namespace tag drawn from the fixed set (`token`, `nft`).
- The address of a token account, in the form defined by the [Keeta CAIP-10 Profile][CAIP-10 Profile].

The asset-namespace tag is not enforced by the protocol -- Keeta itself does not distinguish "fungible" from "non-fungible" -- and is purely an interoperability hint to consumers.
A validator with access to the chain MAY confirm the supply; a mismatch means the tag is stale, not that the identifier is invalid.

| `asset_namespace` | Use                                                                                               | Equivalent in other namespaces                 |
| :---------------- | :------------------------------------------------------------------------------------------------ | :--------------------------------------------- |
| `token`           | Any fungible token on a Keeta network, including the network's base token.                        | `eip155:1/erc20:0x...`, `solana:.../token:...` |
| `nft`             | A non-fungible token. Implementations SHOULD only use `nft` when the token's raw supply is exactly 1. | `eip155:1/erc721:0x...`, `solana:.../nft:...`  |

The base token of a Keeta network is just another token account: it is referenced via the `token` asset namespace using the address returned by `Account.generateBaseAddresses(networkId).baseToken`.

### Syntax

A Keeta [CAIP-19][] **asset type** identifier MUST take the form:

```
keeta:<network>/<asset_namespace>:<address>
```

Where:

- `keeta` is the namespace.
- `<network>` is a Keeta network identifier as defined by the [Keeta CAIP-2 Profile][CAIP-2 Profile].
- `<asset_namespace>` is `token` or `nft` (see the table above).
- `<address>` is the body of the token account's address, without the `keeta_` display prefix, as defined by the [Keeta CAIP-10 Profile][CAIP-10 Profile].

### Resolution Mechanics

To validate a Keeta CAIP-19 identifier:

1. Split on `/` and `:` and verify the namespace is `keeta` and the asset-namespace is `token` or `nft`.
2. Validate `<network>` against the [Keeta CAIP-2 Profile][CAIP-2 Profile].
3. Validate `<address>` as described in the [Keeta CAIP-10 Profile][CAIP-10 Profile]; the type byte MUST be that of a token account and the checksum MUST verify.
4. For `nft`, consumers SHOULD query a node on the indicated network to confirm the token's raw on-chain supply is `1` (not its display amount after metadata decimals) before treating the identifier as a non-fungible asset; because supply may be mutable, a mismatch means the hint is stale, not that the identifier is invalid.

## Rationale

Keeta uses a single, unified address space for every transferable asset, including the base token: there is no separate native-coin concept at the protocol level.
This profile reflects that by using `token` for every fungible asset and `nft` only as an interoperability hint for token accounts whose raw supply is `1`, mirroring the approach taken by the [Solana namespace][solana-caip19], which has a similarly unified address space for fungible and non-fungible assets.

### Backwards Compatibility

This is the first [CAIP-19][] specification for the `keeta` namespace, so there are no legacy identifiers to support.

## Test Cases

Base token (KTA) of the Keeta main network, referenced by its on-chain token-account address:

```
keeta:21378/token:anqdilpazdekdu4acw65fj7smltcp26wbrildkqtszqvverljpwpezmd44ssg
```

Base token of the Keeta test network:

```
keeta:1413829460/token:anyiff4v34alvumupagmdyosydeq24lc4def5mrpmmyhx3j6vj2uucckeqn52
```

Any other fungible token uses the same form, with the address of the relevant token account; for example USDC on the main network:

```
keeta:21378/token:amnkge74xitii5dsobstldatv3irmyimujfjotftx7plaaaseam4bntb7wnna
```

NFT on the main network (raw supply `1`):

```
keeta:21378/nft:amob7pxzhexqych4g56bmmtovdgwr6kljloyzkyb34k37jntj24doaqfbx4xk
```

Invalid:

```
# Non-token address used with a token asset namespace (storage account)
keeta:21378/token:aqltdal4rshtky5iehd765y3mdjkcmku5d4ulo5fgonzqrxulwepnogq33mle

# Display prefix included in the address
keeta:21378/token:keeta_anqdilpazdekdu4acw65fj7smltcp26wbrildkqtszqvverljpwpezmd44ssg

# Hex network identifier (see Keeta CAIP-2 Profile)
keeta:0x5382/token:anqdilpazdekdu4acw65fj7smltcp26wbrildkqtszqvverljpwpezmd44ssg
```

## Additional Considerations

This profile defines asset types only.
The [CAIP-19][] `token_id` segment is not defined for Keeta, as a token account is itself a single asset.
Should the protocol introduce NFT collections -- token accounts whose individual units are addressable -- a future revision of this profile will specify the `token_id` segment to identify a unit within such a collection.

The Keeta main network is also registered in [SLIP-0044][] as coin type `8887` for use in HD-wallet derivation paths and similar SLIP-0044-indexed contexts.
This profile does not surface SLIP-0044 in [CAIP-19][] form, since on Keeta the base token has a first-class on-chain address that already serves as a canonical [CAIP-19][] reference, and only the main network has a SLIP-0044 entry.

## References

- Keeta [accounts] - defines token accounts and the unified address space for fungible/non-fungible assets.
- Keeta [SDK package][sdk] - `Account.AccountKeyAlgorithm.TOKEN` and `generateBaseAddresses(networkId)` define how a token account's address is constructed.
- [Keeta CAIP-2 Profile][CAIP-2 Profile] - the network portion of the identifier.
- [Keeta CAIP-10 Profile][CAIP-10 Profile] - the address syntax reused for the `<address>` segment.

[CAIP-2 Profile]: ./caip2.md
[CAIP-10 Profile]: ./caip10.md
[accounts]: https://docs.keeta.com/components/accounts
[sdk]: https://www.npmjs.com/package/@keetanetwork/keetanet-client
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[solana-caip19]: https://namespaces.chainagnostic.org/solana/caip19
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
