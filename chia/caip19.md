---
namespace-identifier: chia-caip19
title: Chia Namespace - Asset Specification
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

Chia is a coin-set chain with no accounts and no token contracts, so an asset here is a *puzzle*, not an address.

Fungible tokens are [Chia Asset Tokens][] (CATs).
A CAT is ordinary Chia value wrapped in the CAT puzzle with a `TAIL_PROGRAM_HASH` curried in, where the TAIL — Token and Asset Issuance Limitations — is the Chialisp program that decides whether units may be minted or melted.
That 32-byte TAIL hash is the CAT's **asset ID**, and because the TAIL is curried into every coin of the token it cannot be changed after issuance: "Once a CAT has been distributed, it is no longer possible to change the TAIL across the entire token supply."
An asset ID is therefore permanent by construction, which is a stronger identity guarantee than an upgradeable contract address gives.

Non-fungible tokens follow [CHIP-0005][] (NFT1) and are singletons.
Each NFT has its own launcher coin, and CHIP-0005 states that "An NFT's ID shall be its launcher, which is a bech32-encoded address with a prefix of `nft`".

Both identifiers are already inside the [CAIP-19][] `asset_reference` charset — hex is alphanumeric, and bech32m is lowercase alphanumeric — so nothing in this profile is percent-encoded.

This profile was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a way to name 4 assets on this chain.
The authors do not represent the Chia ecosystem and offer this for its community to correct, adopt or replace.

## Syntax

After the [CAIP-2][] chain ID, a slash defines an `asset_namespace` and an `asset_reference`.

### Asset Namespaces

| Namespace | Description | Reference Format |
| :--- | :--- | :--- |
| `slip44` | Native XCH via [SLIP-0044][] | `8444` (Chia's coin type) |
| `cat` | A CAT2 Chia Asset Token | the 32-byte asset ID (TAIL hash), 64 lowercase hex characters |
| `nft` | An NFT1 non-fungible token | the launcher ID in bech32m, `nft1…` |

### CAT Asset ID

A `cat` reference **MUST** be the asset ID as 64 lowercase hexadecimal characters, with the `0x` prefix stripped.
This matches how this namespace's [CAIP-2][] profile already renders the genesis challenge, and how Chia wallets and the `get_stray_cats` RPC render asset IDs.
Uppercase hex **MUST NOT** be produced and **SHOULD** be accepted and lowercased on input.

### NFT Launcher ID

An `nft` reference **MUST** be the bech32m encoding of the NFT's launcher ID with the human-readable part `nft`, exactly as CHIP-0005 defines the NFT's ID, and is 62 characters.

The two namespaces disagree on encoding on purpose.
CHIP-0005 makes the `nft1…` string normative for NFTs, and its bech32m checksum catches transcription errors in an identifier that users copy and paste by hand.
No equivalent encoding has been standardised for CAT asset IDs, which the ecosystem renders as bare hex everywhere, so inventing a `cat1…` form here would be this profile making up a Chia standard rather than profiling one.
Each asset kind is written the way its own standard writes it.

## RegEx

```sh
asset_id:           asset_type
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           "chia:" + blockchain_id (as defined in [CAIP-2])

asset_namespace:    "slip44" | "cat" | "nft"

asset_reference:    slip44_ref | cat_ref | nft_ref
slip44_ref:         "8444"
cat_ref:            [0-9a-f]{64}
nft_ref:            nft1[023456789acdefghjklmnpqrstuvwxyz]{58}
```

The `nft_ref` character class is the bech32 charset (`qpzry9x8gf2tvdw0s3jn54khce6mua7l`) expressed as a range; a validator **SHOULD** verify the bech32m checksum rather than rely on the pattern.

## Semantics

### Native Asset (XCH)

XCH is identified with the `slip44` namespace and coin type `8444`, registered in [SLIP-0044][] as `| 8444 | XCH | Chia |`.
It is the unwrapped form of Chia value: a CAT is XCH inside the CAT puzzle, and melting a CAT returns XCH.
The smallest unit is the mojo, 10^-12 XCH.

Example: `chia:ccd5bb71183532bff220ba46c268991a/slip44:8444`

### CATs

A `cat` asset type names the TAIL, and therefore the set of all coins that can ever be issued under it.

CAT precision is not part of the identifier and is not a per-token parameter: Chia fixes the ratio at 1 CAT to 1,000 mojos for every CAT, giving three decimal places, and the official wallet does not support any other ratio.
Ticker and name (`SBX`, `wUSDC`) live in off-chain registries such as taildatabase and dexie and are neither unique nor on-chain; no part of this profile admits them.

### NFTs

An `nft` asset type names one NFT1 singleton.

Chia NFTs are not organised by an on-chain collection contract.
A collection is an off-chain metadata field defined by [CHIP-0007][], asserted by the minter in the NFT's metadata file, and not enforced by consensus — two unrelated NFTs may claim the same collection, and an NFT may claim none.
There is therefore no meaningful container to put in the `asset_type` position, and this profile does **not** use CAIP-19's `token_id` component for Chia: the launcher ID alone is unique chain-wide, so asset type and asset ID coincide.
This follows the precedent of the Solana profile, where each NFT is likewise named by its own mint account with no `token_id`.

A collection-scoped alternative — `nft:<collection_id>/<launcher_id>`, with the CHIP-0007 collection ID as the type — was considered and rejected because it would make an NFT's identifier depend on a claim its minter can make falsely, and would leave collection-less NFTs unnameable.
Reviewers who believe the collection belongs in the identifier should say so; the tradeoff is legibility against forgeability.

Decentralized Identifiers (`did:chia:…`) are also Chia singletons but are identities rather than assets and are out of scope.

## Examples

```sh
# Native XCH on mainnet
chia:ccd5bb71183532bff220ba46c268991a/slip44:8444

# wUSDC, warp.green bridged USD Coin
chia:ccd5bb71183532bff220ba46c268991a/cat:bbb51b246fbec1da1305be31dcf17151ccd0b8231a1ec306d7ce9f5b8c742b9e

# Spacebucks (SBX)
chia:ccd5bb71183532bff220ba46c268991a/cat:a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913

# dexie bucks (DBX)
chia:ccd5bb71183532bff220ba46c268991a/cat:db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20

# Chia Friends #21, an NFT1 singleton
chia:ccd5bb71183532bff220ba46c268991a/nft:nft1pd66xktppqlxkzjduwardg7rnxtthknw5tgyjcp4ekmff2c7du5snlr03r

# Native TXCH on testnet10
chia:ae83525ba8d1dd3f09b277de18ca3e43/slip44:8444
```

## Security Considerations

### An asset ID does not say CAT1 or CAT2

The asset ID is the TAIL program hash, and the CAT1-to-CAT2 migration replaced the *outer* CAT puzzle, not the TAIL.
Asset IDs did not change across that migration, so the same 64-hex string names both a token's CAT1 coins and its CAT2 coins.
CAT1 coins still exist on-chain but stopped being supported at the end-of-life block 2,311,760 and are not the asset anybody means.

`cat` in this profile means CAT2.
A consumer that finds a balance under a `cat` reference **MUST** confirm the coin's outer puzzle is CAT2 before treating it as the named asset; the identifier cannot carry that distinction and this profile does not pretend otherwise.

### Tickers are off-chain and collide

CAT tickers are assigned by community registries with no uniqueness guarantee and no link to the TAIL.
`wUSDC` and `wUSDC.b` are two different bridged USD Coins (from Ethereum and Base respectively) with different asset IDs, and nothing prevents a third issuance from taking either code.
Only the asset ID may be treated as identity.

### A bad TAIL is a bad asset under a perfectly good identifier

The Chialisp documentation is explicit that "If the TAIL is programmed incorrectly, the tokens may be issued by attackers, rendering the asset worthless", and that there is no way to patch a TAIL once distributed.
The identifier's permanence is a property of the puzzle hash, not a statement about the puzzle's soundness.

### Hex case and prefixes

Chia RPCs return hashes with a `0x` prefix (`"0xccd5bb71…"`) and some tools uppercase hex.
Producers **MUST** strip `0x` and emit lowercase; consumers **SHOULD** normalise both before comparison, since `0X…`, `0x…` and uppercase variants would otherwise silently fail equality checks on the same asset.

## Backwards Compatibility

CAT2 has been the live CAT standard since block 2,311,760 in July 2022 and NFT1 since CHIP-0005 reached Final status, so both namespaces describe current standards rather than legacy ones.
CAT1 is addressed above and is deliberately not given a namespace of its own.

## References

- [Chia Asset Tokens][] - the CAT primitive, the TAIL, and the fixed 1,000-mojo CAT ratio
- [CAT2 Intro and FAQ][] - the CAT1 end-of-life block and the CAT1-to-CAT2 transition
- [CHIP-0005][] - the NFT1 standard, including the `nft1…` bech32m NFT ID
- [CHIP-0007][] - off-chain metadata format for NFT1, where collection membership is asserted
- [Chia RPC Reference][] - full-node and wallet RPCs used to resolve asset IDs and launcher IDs
- [dexie API][] - the asset registry queried to verify the CAT asset IDs in this document
- [MintGarden API][] - the NFT indexer queried to verify the launcher ID in this document
- [SLIP-0044][] - registered coin types, `8444` for XCH
- [CAIP-2][] - the Chia chain ID profile in this namespace
- [CAIP-19][] - Asset Type and Asset ID Specification

[CAIP-2]: ./caip2.md
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[Chia Asset Tokens]: https://chialisp.com/cats/
[CAT2 Intro and FAQ]: https://docs.chia.net/guides/cat2-intro/
[CHIP-0005]: https://github.com/Chia-Network/chips/blob/main/CHIPs/chip-0005.md
[CHIP-0007]: https://github.com/Chia-Network/chips/blob/main/CHIPs/chip-0007.md
[Chia RPC Reference]: https://docs.chia.net/rpc
[dexie API]: https://api.dexie.space/v1/assets
[MintGarden API]: https://api.mintgarden.io/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
