---
namespace-identifier: aelf-caip2
title: aelf Namespace - Blockchain ID Specification
author: ["Billy Rennekamp (@okwme)"]
discussions-to: https://github.com/0xcounting/FAR/issues/1
status: Draft
type: Standard
created: 2026-09-14
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

Every aelf chain — the main chain and each side chain — has a chain ID.
The chain ID exists in two forms that an implementer will meet in different places: a signed 32-bit integer used inside the node and the SDKs, and a short base58 string used by the HTTP API, by explorers, and inside displayed addresses.
The two are the same value under a fixed, lossless transformation defined by the reference implementation.
The `aelf` CAIP-2 profile uses the base58 string form as the reference, so aelf MainChain is `aelf:AELF` and its production side chain is `aelf:tDVV`.

## Specification

### Semantics

An aelf chain ID consists of the literal namespace `aelf`, a colon, and a reference holding the chain's base58 chain ID.
Two chains configured with the same chain ID have the same CAIP-2 chain ID by definition.

#### The two forms

The integer form is an `int32`.
The base58 form is the plain base58 encoding — no checksum, no version byte — of the **low three bytes of the integer's little-endian representation**, in big-endian order.
This is defined by `ChainHelper` in the [aelf reference implementation][]:

```csharp
public static string ConvertChainIdToBase58(int chainId)
{
    // Default chain id is 4 base58 chars, bytes size is 3
    var bytes = chainId.ToBytes(false);   // little-endian, 4 bytes
    Array.Resize(ref bytes, 3);           // keep the low three
    return bytes.ToPlainBase58();
}

public static int ConvertBase58ToChainId(string base58String)
{
    var bytes = Base58CheckEncoding.DecodePlain(base58String);
    if (bytes.Length < 4)
        Array.Resize(ref bytes, 4);       // right-pad with zero
    return bytes.ToInt32(false);          // little-endian
}
```

Worked both ways for the main chain:

- `ConvertBase58ToChainId("AELF")` — plain base58 decode gives the three bytes `1B 7A 98`, right-padded to `1B 7A 98 00`, read little-endian as `0x00987A1B` = **9992731**.
- `ConvertChainIdToBase58(9992731)` — little-endian bytes `1B 7A 98 00`, truncated to `1B 7A 98`, plain base58 encoded as **`AELF`**.

The same transformation gives `tDVV` = 1866392 and `tDVW` = 1931928, which match the integers published in aelf's side chain documentation.

Because only three bytes survive the round trip, the usable chain ID space is `0` through `16777215`, and the base58 form is always 3 to 5 characters.
Chain IDs generated for new side chains are constrained by `ChainHelper.GetChainId` to the range whose base58 form is exactly four characters, between `2111` and `zzzz`, which is why every aelf chain ID seen in practice is four characters long.

#### Which form this profile uses, and why

This profile uses the **base58 string**.

It is the form aelf's own HTTP API returns, in the `ChainId` field of `chainStatus`.
It is the form aelf explorers display and the form embedded in aelf's decorated address display `ELF_<address>_<chain ID>`.
It is human-legible, four characters, and already unambiguous inside the ecosystem.
A reader who sees `aelf:tDVV` can match it against an aelf block explorer without conversion; a reader who sees `aelf:1866392` cannot.

The integer form was considered and rejected as the reference.
It is an `int32` that can be negative, its decimal rendering appears in SDK configuration but nowhere a user would see, and it would introduce a second spelling for every chain.
The integer form is documented above so that implementers can convert reliably, not so that it can be used as a reference.

### Syntax

```text
chain_id:  "aelf:" + reference
namespace: aelf
reference: 3*5(base58 character)
```

The reference must match the following regular expression:

```regex
^[1-9A-HJ-NP-Za-km-z]{3,5}$
```

The base58 alphabet excludes `0`, `O`, `I` and `l`.

The regular expression is necessary but not sufficient.
A reference is conformant only if it is **canonical**, meaning it survives a round trip:

```text
ConvertChainIdToBase58(ConvertBase58ToChainId(reference)) == reference
```

This single rule rejects every non-canonical spelling without needing to enumerate them.
For example, `1AELF` matches the regular expression and decodes to the integer `-1736828160`, but that integer re-encodes to `136H`, not to `1AELF`, so `1AELF` is not a conformant reference.
Likewise `2` decodes to `1`, which re-encodes to `LUw`.
Implementations MUST apply the round-trip check, and MUST compare references as case-sensitive strings, since base58 distinguishes `AELF` from `AELf`.

### Resolution Mechanics

To resolve the chain ID reported by an aelf node, issue a `GET` against the chain API:

```http
GET /api/blockChain/chainStatus HTTP/1.1
Accept: application/json
```

The following is an abbreviated response from a MainChain node at `https://aelf-public-node.aelf.io`:

```json
{
  "ChainId": "AELF",
  "GenesisBlockHash": "73b6d1064013c0b34e6b4783d04a7c550863c95bd78e9b372fe8372577e290e8",
  "GenesisContractAddress": "pykr77ft9UUKJZLVq15wCH8PinBSjVRQ12sD1Ayq92mKFsJ1i",
  "BestChainHeight": 354157264
}
```

Take `ChainId` verbatim, verify that it is canonical under the round-trip rule above, and prefix it with `aelf:`.
The example response therefore resolves to `aelf:AELF`.

A node on the `tDVV` side chain at `https://tdvv-public-node.aelf.io` returns `"ChainId": "tDVV"` with `GenesisBlockHash` `f29548aa57863ca2f0b09673e6821be83b5beabb3c1be341c446a5d149b305dc`, resolving to `aelf:tDVV`.

## Rationale

The chain ID is the value aelf uses to route cross-chain messages, to scope token symbols, and to decorate displayed addresses, so it is the identifier the ecosystem already treats as naming a chain.
Using it requires no registry and no truncation: four characters fit comfortably inside CAIP-2's 32-character reference limit.

The genesis block hash was considered as an alternative reference, because it would be globally unique where the chain ID is not (see below).
It was rejected as the primary reference for two reasons.
It is 32 bytes, so it would need a documented truncation of the kind `bip122` and `hive` define, and the truncated form carries none of the legibility that makes `aelf:tDVV` useful.
More importantly, it would not match anything an aelf user, explorer, or SDK ever displays, which would leave every implementer converting between a CAIP-2 identifier and the identifier aelf itself uses.

## Well-Known Chains

The following table allows clients to label well-known chains without an API round trip.
It is informative; the resolution method above remains authoritative.

| Chain | Chain ID | Integer form | CAIP-2 chain ID |
| --- | --- | ---: | --- |
| MainNet main chain | `AELF` | `9992731` | `aelf:AELF` |
| MainNet side chain | `tDVV` | `1866392` | `aelf:tDVV` |
| TestNet main chain | `AELF` | `9992731` | `aelf:AELF` |
| TestNet side chain | `tDVW` | `1931928` | `aelf:tDVW` |

The two MainNet rows were read from live nodes for this document.
The two TestNet rows are taken from aelf's documentation; the public TestNet endpoints returned HTTP 522 at the time of writing, so those rows are documented but not independently confirmed by the authors.

`tDVV` was previously also the name of a TestNet side chain, which aelf retired in favour of `tDVW`; the `tDVV` chain that exists today is the MainNet side chain.
Documents written before that migration may use `tDVV` to mean a test chain.

## Collisions

**aelf's TestNet main chain is documented as using the same chain ID, `AELF`, as MainNet's main chain.**
If that is correct, `aelf:AELF` does not distinguish MainNet from TestNet, and no choice of encoding in this profile can fix that, because the collision is in aelf's own identifier rather than in its rendering.

Consumers that must distinguish the two have three options, in decreasing order of preference:

1. Carry the network out of band, as aelf's own tooling does by configuring a MainNet or TestNet endpoint.
2. Corroborate with `GenesisBlockHash` from `chainStatus`, which differs between the two and is the value that actually pins a chain's identity.
3. Refuse to resolve a chain ID from an endpoint that has not been established as MainNet or TestNet.

Side chain IDs are allocated by the main chain's cross-chain contract when a side chain is created, and are derived from a serial number, so two side chains on the same main chain will not collide with one another.
The collision above is specifically between separate aelf deployments — MainNet and TestNet — that each run their own main chain.

Privately operated aelf networks choose their own chain IDs and are not covered by any registry.
If two distinct chains use the same chain ID, this profile cannot distinguish them and their CAIP-2 chain IDs collide.

The authors flag this as the single most likely thing in this draft to need correction by the aelf community, and would welcome a normative answer from maintainers.

## Backwards Compatibility

There was no previously registered CAIP-2 profile for aelf.
This profile does not change any native aelf identifier.

## Test Cases

### Valid identifiers

| Identifier | Reason |
| --- | --- |
| `aelf:AELF` | aelf main chain, confirmed on a live MainNet node |
| `aelf:tDVV` | aelf MainNet side chain, confirmed on a live node |
| `aelf:tDVW` | aelf TestNet side chain |
| `aelf:111` | Canonical encoding of chain ID `0`, the shortest possible reference |
| `aelf:2UzHL` | Canonical encoding of `16777215`, the largest representable chain ID |

### Invalid identifiers

| Identifier | Reason |
| --- | --- |
| `aelf:` | Empty reference |
| `aelf:1AELF` | Non-canonical: decodes to `-1736828160`, which re-encodes to `136H` |
| `aelf:2` | Non-canonical: decodes to `1`, which re-encodes to `LUw` |
| `aelf:12` | Non-canonical: decodes to `256`, which re-encodes to `15R` |
| `aelf:9992731` | Integer form, seven characters, outside the 3-to-5 length |
| `aelf:aelf` | Contains `l`, which is not in the base58 alphabet |
| `aelf:AELF0` | Contains `0`, which is not in the base58 alphabet |
| `aelf:ELF_JRmBduh4nXWi1aXgdUsj5gJrzeZb2LxmrAbf7W99faZSvoAaE_AELF` | Decorated address display form, not a chain ID |
| `aelf: AELF` | Leading whitespace |
| `AELF:AELF` | Incorrect namespace casing |

## Additional Considerations

A CAIP-19 profile for this namespace must not key fungible assets on a contract address.
Every token on a given aelf chain lives inside that chain's single MultiToken system contract, so token identity is the symbol within `(chain ID, symbol)`; see the [namespace README][] for the detail and for the confirmed MultiToken addresses.

A CAIP-10 profile will need to decide whether to accept aelf's decorated address form `ELF_<address>_<chain ID>` on input, and should normalise to the bare base58 address, since the decorated form already duplicates the CAIP-2 reference.

## Security Considerations

Resolving a chain ID through `chainStatus` establishes only what the queried endpoint reports.
It does not authenticate the endpoint, and, given the MainNet/TestNet chain ID collision described above, it does not on its own establish which aelf deployment is being addressed.
Applications that depend on a trusted chain identity should use authenticated endpoints and corroborate `ChainId` against the expected `GenesisBlockHash` in the same response.

## References

- [CAIP-2][] - Blockchain ID specification
- [aelf chain ID helper][] - `ChainHelper`, the normative chain ID encoding and decoding quoted above
- [aelf reference implementation][] - The C# node
- [chain API][] - SDK reference documenting the `/api/blockChain/chainStatus` endpoint used above
- [ELF token][] - Published MultiToken contract addresses and chain IDs for `AELF` and `tDVV`
- [aelf side chains][] - Side chain setup, including the integer form of `tDVV`
- [aelf integration guide][] - TestNet endpoints and chain IDs
- [namespace README][] - aelf namespace overview, side chains, and the shared MultiToken model

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[aelf chain ID helper]: https://github.com/AElfProject/AElf/blob/dev/src/AElf.Types/Helper/ChainHelper.cs
[aelf reference implementation]: https://github.com/AElfProject/AElf
[chain API]: https://docs.aelf.com/tools/chain-sdk/javascript-sdk/
[ELF token]: https://docs.aelf.com/about-aelf/elf-token/
[aelf side chains]: https://docs.aelf.com/quick-start/node-operators/set-up-a-side-chain/
[aelf integration guide]: https://docs.aelf.com/resources/integration-guide/
[namespace README]: ./README.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
