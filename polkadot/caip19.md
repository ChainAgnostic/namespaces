---
namespace-identifier: polkadot-caip19
title: Polkadot Namespace - Asset Specification
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

A Substrate asset identifier is a key into a storage map in one particular runtime.
Asset id `1984` means "Tether USD" only because it is `1984` *in the `Assets` pallet of Polkadot Asset Hub*; the same integer in another chain's runtime names an unrelated asset, or nothing at all.
The [CAIP-2][] half of a [CAIP-19][] identifier already carries the chain, as a truncated genesis hash, so the asset half never has to repeat any part of the chain's identity.
That is the whole reason this profile composes cleanly: `chain_id` supplies the runtime, and `asset_namespace` plus `asset_reference` supply the key within it.

The Polkadot ecosystem already performs exactly this decomposition in [XCM][].
An XCM `Location` for Asset Hub's USDT reads `(1, [Parachain(1000), PalletInstance(50), GeneralIndex(1984)])`: first the chain, then the pallet instance inside that chain, then the index inside that pallet.
A CAIP-19 for the same asset carries the chain in the CAIP-2, the pallet instance in the `asset_namespace`, and the index in the `asset_reference`.
The mapping is one-to-one for locally-defined assets, which is the strongest argument that the split is the natural one for this namespace.

The part that is easy to get wrong is that a Substrate chain does not have *one* asset index.
It has several, each an independent pallet instance with its own integer key space that starts again at zero.
Polkadot Asset Hub runs `Assets`, `PoolAssets`, `ForeignAssets`, `Nfts` and `Uniques` at the same time, and every one of the 84 ids live in `PoolAssets` is also live in `Assets`, naming something entirely unrelated.
An `asset_namespace` of `asset` alone would therefore be ambiguous for every pool share on the most widely used chain in the namespace, so each index gets its own asset namespace and the rule is stated normatively below.

This profile was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a way to name 175 assets on Polkadot-ecosystem chains.
The authors do not represent the Polkadot ecosystem and offer this for its community to correct, adopt or replace.

## Syntax

After the [CAIP-2][] namespace and chain id, a slash introduces an `asset_namespace` and an `asset_reference`.
For non-fungibles a further slash introduces a `token_id`, as defined in [CAIP-19][].

### Asset Namespaces

| Namespace  | On-chain index                                                            | Reference format                                  |
| :--------- | :------------------------------------------------------------------------ | :------------------------------------------------ |
| `slip44`   | The chain's native unit, where a [SLIP-0044][] coin type is registered      | Decimal coin type, e.g. `354`                      |
| `asset`    | The chain's primary numeric asset index                                    | Decimal `AssetId`                                  |
| `pool`     | The chain's pool-share index                                               | Decimal `AssetId`                                  |
| `foreign`  | The `ForeignAssets` instance of `pallet-assets`, keyed by an XCM `Location` | Lowercase hex of the SCALE-encoded `Location`      |
| `nfts`     | A collection in `pallet-nfts`                                              | Decimal `CollectionId`; `token_id` is the `ItemId` |
| `uniques`  | A collection in `pallet-uniques`                                           | Decimal `CollectionId`; `token_id` is the `ItemId` |

The rule behind the table is that **the asset namespace names the index, and the reference is the key within that index**.
A chain that runs a pallet instance not covered above MUST NOT express it with one of these namespaces; an additional asset namespace should be registered in a follow-up to this profile instead.
This is a hard requirement rather than a stylistic one, because reusing `asset` for a second numeric index reintroduces exactly the collision documented under Collisions and Security Considerations below.

### The primary numeric asset index

`asset` refers to whichever single pallet holds the chain's general-purpose, chain-local, integer-keyed fungible assets.
On chains built from the Polkadot SDK's system parachain templates that is the default instance of `pallet-assets`, conventionally named `Assets`.
On chains that instead run an `asset-registry` pallet, such as Hydration and Bifrost, it is that registry's index.
A chain MUST have at most one index addressed as `asset`; if a runtime carries both a default `pallet-assets` instance and a separate asset registry, only the one that mints the chain's canonical asset ids may use `asset`.

### Decimal reference requirements

References in `asset`, `pool`, `nfts` and `uniques`, and every `token_id`, are unsigned integers rendered in base ten.
They MUST use the shortest form: no leading zeros, no sign, no separators, no `0x` prefix.
`asset:1984` is valid, `asset:01984` is not, and consumers MUST reject the padded form rather than normalising it.
Zero is written `0`, which is a live collection id in `pallet-uniques` on Polkadot Asset Hub and so is not a theoretical case.

Substrate `AssetId` types are at most `u128` and `CollectionId`/`ItemId` are at most `u32`, so a decimal reference is at most 39 characters, well inside the 128-character `asset_reference` limit and the 78-character `token_id` limit.

### Hex reference requirements for `foreign`

The `ForeignAssets` instance is keyed by an XCM `Location`, not by an integer, so there is no number to write.
The reference is the SCALE encoding of that `Location` rendered as lowercase hexadecimal, with no `0x` prefix and an even number of digits.
It is obtained without any re-encoding by the consumer: enumerate the `ForeignAssets::Asset` storage prefix and take the bytes of each key that follow the 16-byte `Blake2_128` hash, which are the `Blake2_128Concat` hasher's verbatim copy of the key.

A `Location` longer than 64 bytes cannot be expressed, because the hex doubles to more than the 128-character `asset_reference` limit.
This is a tighter constraint than it looks.
Polkadot Asset Hub holds 52 `ForeignAssets` entries today whose keys run from 20 to 55 bytes, so the longest is already 110 of the 128 characters available, and an implementation that meets a longer one MUST fail rather than truncate.

### No percent-encoding is required

Every reference form in this profile is drawn from `[0-9]` or `[0-9a-f]`, so none of them can contain an octet outside the `asset_reference` charset, and this profile defines no percent-encoding.
That is a deliberate design constraint rather than a happy accident.
The obvious alternatives all break it: asset symbols and names are arbitrary byte strings on chain — Asset Hub asset `22222005` is named `道阻且长，温暖坚定-爱情/love`, which contains both non-ASCII characters and a `/` — and the human-readable text rendering of an XCM `Location` needs `%2F`, `%28` and `%29` and has no normative grammar to be canonical against.
Binding the reference to the on-chain key rather than to on-chain metadata removes the need for an escape and removes a class of disagreement between implementations at the same time.

## RegEx

The RegEx validation strings are as follows:

```sh
asset_id:           asset_type + "/" + token_id
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           namespace + ":" + blockchain_id (as defined in [CAIP-2])

asset_namespace:    "slip44" | "asset" | "pool" | "foreign" | "nfts" | "uniques"

asset_reference:    slip44_ref | index_ref | foreign_ref
slip44_ref:         0|[1-9][0-9]{0,9}
index_ref:          0|[1-9][0-9]{0,38}
foreign_ref:        ([0-9a-f]{2}){1,64}

token_id:           0|[1-9][0-9]{0,9}
```

`index_ref` is used as the `asset_reference` of `asset`, `pool`, `nfts` and `uniques`.
`token_id` is defined only for `nfts` and `uniques`, whose `ItemId` is a `u32`; the other asset namespaces of this profile are fungible and their identifiers are `asset_type`s with no `token_id`.

## Semantics

### Native tokens

The native unit of a relay chain, solo chain or parachain is identified with the `slip44` asset namespace and the chain's registered [SLIP-0044][] coin type, per [CAIP-20][].
DOT is coin type `354` and KSM is coin type `434`, and many parachain natives are registered too, including GLMR `1284`, MOVR `1285`, ASTR `810`, ACA `787`, BNC `788`, INTR `794`, CFG `747` and KILT `2086`.

Because [CAIP-19][] identifies an asset *on a chain*, the native token of each chain that uses it gets its own identifier.
DOT on the relay chain and DOT teleported to Asset Hub are the same economic asset to a holder, but they are distinct balances in distinct runtimes and so are `polkadot:91b171bb158e2d3848fa23a9f1c25182/slip44:354` and `polkadot:68d56f15f85d3136970ec16946040bc1/slip44:354` respectively.
Consumers that wish to aggregate them must do so themselves; this profile does not collapse them, because collapsing them would discard the chain on which the balance actually exists.

Not every chain's native token has a coin type.
Hydration's HDX has no [SLIP-0044][] registration, and the two SLIP-0044 entries whose symbols resemble it — `609 HYDRA` and `4741444 HYD` — belong to unrelated projects.
Where a chain's native token has no coin type but does appear in the chain's own asset index, as HDX does at Hydration index `0`, the `asset` form is used.
Where it appears in neither, the native token is not expressible under this profile, and the correct fix is to register a coin type with [SLIP-0044][] rather than to invent a reference here.

### Assets in the primary numeric index

`asset` names an entry in the chain's primary numeric asset index, as defined in the Syntax section.
On Polkadot Asset Hub these are the `pallet-assets` ids that wallets and explorers already show: `1984` is Tether USD, `1337` is USD Coin, `23` is PINK.
On Hydration the same asset namespace addresses the `asset-registry` index: `0` is HDX, `5` is DOT, `10` is USDT, `16` is GLMR.

Two chains numbering the same underlying token differently is normal and is not a defect.
Asset Hub's USDT is index `1984` and Hydration's is index `10`; both identifiers are correct, they name different on-chain balances, and the chain half of each identifier is what distinguishes them.

### Pool shares

`pool` names an entry in the chain's pool-share index: the `PoolAssets` instance of `pallet-assets`, which holds the liquidity-provider tokens minted by `pallet-asset-conversion`.
These are ordinary fungible balances and are transferable, but they are minted and burned by the AMM rather than by an asset owner, and they carry no `pallet-assets` metadata, so they cannot be resolved to a name or symbol the way an `asset` entry can.
`PoolAssets` numbers its entries from its own counter, entirely independently of `Assets`, which is the collision documented below.

### Foreign assets

`foreign` names an entry in the `ForeignAssets` instance of `pallet-assets`, which holds assets whose canonical home is another consensus system and which are keyed by the XCM `Location` of that home rather than by a local integer.
On Polkadot Asset Hub this covers both assets bridged from other parachains and assets bridged from Ethereum over Snowbridge.

The reference is opaque by design, and that is the right trade-off here.
A `Location` is already the ecosystem's canonical name for a foreign asset, the storage key is the runtime's own byte-for-byte rendering of it, and reproducing those bytes requires no encoder, no XCM version negotiation and no agreement about how to print a junction.

### Non-fungible collections

`nfts` and `uniques` name a collection in `pallet-nfts` and `pallet-uniques` respectively.
The `asset_reference` is the `CollectionId` and the `token_id` is the `ItemId`, so a collection without a `token_id` is an `asset_type` naming the collection as a class, and a collection with a `token_id` is an `asset_id` naming one item.

`pallet-uniques` is superseded by `pallet-nfts`, but it has not been removed and both pallets hold live state on Polkadot Asset Hub today, with overlapping collection ids.
Both asset namespaces are therefore required, and an implementation MUST NOT treat `uniques` as an alias for `nfts`.

### Assets this profile deliberately does not define

**Bittensor subnet alpha tokens.**
Bittensor is reachable under this namespace — its `finney` mainnet is `polkadot:2f0555cc76fc2840a25a6ea3b9637146` — and since Dynamic TAO each subnet has an alpha token that holders can acquire, hold and unstake, so it is tempting to write a `subnet` asset namespace whose reference is the subnet's `netuid`.
This profile does not define one, for three reasons.

First, and decisively, a `netuid` is a reusable slot rather than a permanent name.
`SubnetLimit` is `128`, and when the table is full a new subnet registration prunes the non-immune subnet with the lowest moving alpha price and the freed `netuid` is taken by the incoming subnet, with [BIT-0004][] specifying that dissolution removes all of the old subnet's network storage.
The chain is at that limit now: `SubtensorModule::TotalNetworks` reads `129`, which is the 128-subnet ceiling plus the root network.
An identifier that silently begins naming a different asset after an unrelated third party registers a subnet is not an asset identifier, and it is worse than an ordinary rebasing risk because the reassignment is a routine and forced consequence of the table being full, not a rare voluntary act by the asset's own owner.

Second, a subnet's own symbol cannot stand in for the `netuid`.
Symbols are assigned positionally from a fixed glyph sequence and are single non-ASCII characters — subnet `1` is `α`, subnet `17` is `ρ`, subnet `128` is `න` — so they are neither ASCII nor independent of the reusable index.

Third, alpha is held as a share in a per-subnet staking pool attached to a hotkey, not as a balance in an asset index, so there is no index for the "names the index, keys within it" rule of this profile to point at.

If the Bittensor community wants these identifiers, the constructive form is a reference that pins the registration as well as the slot — a `netuid` paired with the subnet's `NetworkRegisteredAt` block, for example `17-2840556`, both of which are readable from chain state today — and it should be specified by that community rather than assumed here.

**XC-20s on EVM parachains.**
Moonbeam, Moonriver and other Frontier-based parachains expose their cross-chain assets as ERC-20 contracts, and they also have an `eip155` chain id: Moonbeam answers `eth_chainId` with `0x504`, or `1284`.
Such assets are already addressable as `eip155:1284/erc20:0x…`, and implementations SHOULD prefer that form rather than inventing a second identifier for the same token under this namespace.
Note that the same chain has two valid CAIP-2 identifiers as a result, `eip155:1284` and `polkadot:fe58ea77779b7abda7da4ec526d14db9`, which is a property of those chains rather than of this profile.

## Examples

```sh
# DOT, the native token of the Polkadot relay chain
polkadot:91b171bb158e2d3848fa23a9f1c25182/slip44:354

# KSM, the native token of the Kusama relay chain
polkadot:b0a8d493285c2df73290dfb7e61f870f/slip44:434

# DOT held on Polkadot Asset Hub -- the same token, a different chain, a different identifier
polkadot:68d56f15f85d3136970ec16946040bc1/slip44:354

# Tether USD (USDt), Assets pallet id 1984 on Polkadot Asset Hub
polkadot:68d56f15f85d3136970ec16946040bc1/asset:1984

# USD Coin (USDC), Assets pallet id 1337 on Polkadot Asset Hub
polkadot:68d56f15f85d3136970ec16946040bc1/asset:1337

# PINK, Assets pallet id 23 on Polkadot Asset Hub
polkadot:68d56f15f85d3136970ec16946040bc1/asset:23

# UNION, Assets pallet id 56 on Polkadot Asset Hub
polkadot:68d56f15f85d3136970ec16946040bc1/asset:56

# The asset-conversion pool share with PoolAssets id 56 on Polkadot Asset Hub
# -- the same integer as UNION above, a different pallet instance, a different asset
polkadot:68d56f15f85d3136970ec16946040bc1/pool:56

# Staked USDe (sUSDe), bridged from Ethereum, keyed by the XCM Location
# (2, [GlobalConsensus(Ethereum{chain_id:1}), AccountKey20(0x9d39a5de...)])
polkadot:68d56f15f85d3136970ec16946040bc1/foreign:020209070403009d39a5de30e57443bff2a8307a4256c8797a3497

# Wrapped Ether (WETH), bridged from Ethereum to Polkadot Asset Hub
polkadot:68d56f15f85d3136970ec16946040bc1/foreign:02020907040300c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2

# Equilibrium (EQ), keyed by the XCM Location (1, [Parachain(2011)])
polkadot:68d56f15f85d3136970ec16946040bc1/foreign:0101006d1f

# HDX, Hydration's native token, which has no SLIP-0044 coin type,
# addressed through Hydration's own asset registry at index 0
polkadot:afdc188f45c71dacbaa0b62e16a91f72/asset:0

# DOT as registered on Hydration
polkadot:afdc188f45c71dacbaa0b62e16a91f72/asset:5

# USDT as registered on Hydration -- index 10, not 1984
polkadot:afdc188f45c71dacbaa0b62e16a91f72/asset:10

# A pallet-nfts collection on Polkadot Asset Hub, as a class
polkadot:68d56f15f85d3136970ec16946040bc1/nfts:752

# One item in that collection
polkadot:68d56f15f85d3136970ec16946040bc1/nfts:752/47

# A pallet-uniques collection on Polkadot Asset Hub, and one item in it
polkadot:68d56f15f85d3136970ec16946040bc1/uniques:2022
polkadot:68d56f15f85d3136970ec16946040bc1/uniques:2022/1

# Collection id zero is live in pallet-uniques and is written without padding
polkadot:68d56f15f85d3136970ec16946040bc1/uniques:0
```

## Collisions and Security Considerations

### The same integer in two pallet instances

This is the collision this profile exists to prevent, and on the namespace's most used chain it is not a corner case but the normal state of affairs.
Polkadot Asset Hub currently holds 762 `Assets` entries with ids from `0` to `50000547`, and 84 `PoolAssets` entries with ids from `0` to `83` — and **every one of those 84 pool ids is also a live `Assets` id**.
`Assets` id `56` is a token called UNION while `PoolAssets` id `56` is an asset-conversion pool share; `Assets` id `81` is a token called GAVIN while `PoolAssets` id `81` is another pool share; and so on for all 84.
`pallet-nfts` and `pallet-uniques` likewise number their collections independently, and both have live collections on the same chain.
A consumer that flattens these into a single `asset:<n>` form will merge unrelated assets, and merging is worse than failing because the result looks like a successful resolution.
Implementations MUST carry the asset namespace through resolution and MUST NOT infer it from the reference.

### Numeric ids are reusable

`pallet-assets` lets an asset be destroyed, after which its id is free and can be created again by a different owner with different metadata.
Nothing in the runtime binds an id to the asset that first held it, so a CAIP-19 identifier in the `asset` or `pool` namespace is stable only for as long as the underlying entry is not destroyed.
Consumers holding long-lived records SHOULD store the block height at which an identifier was resolved, and SHOULD re-resolve rather than assume that an id seen years ago still names the same asset.
This is the same failure mode that keeps Bittensor's subnet netuids out of this profile, the difference being one of frequency rather than of kind: destruction of an Asset Hub asset requires its owner to act and its accounts to be empty, whereas a Bittensor netuid is recycled as a routine consequence of the subnet table being full.

### Metadata is not an identifier

On-chain `name` and `symbol` are arbitrary bounded byte strings, unvalidated and non-unique.
Asset Hub asset `22222005` is named `道阻且长，温暖坚定-爱情/love`, and the symbol `USDT` is claimed by different entries on different chains and could be claimed twice on one chain.
Metadata MUST NOT be used to construct or to match a CAIP-19 identifier; it is a display hint.

### Truncated genesis hashes

This profile inherits the [CAIP-2][] reference format for the namespace, which is the first 16 bytes of the genesis hash rather than the whole 32.
Two chains with a colliding 16-byte prefix would collide in every asset identifier built on top, and no asset-level rule can repair that.
The risk is the same one the chain profile already accepts, and this profile does not add to it.

### Cross-chain aliasing is intentional

A single economic asset commonly has several identifiers under this profile: DOT on the relay chain and on Asset Hub, USDT as Asset Hub `asset:1984` and as Hydration `asset:10`, Ether as Asset Hub `foreign:0202…c756cc2` and as `eip155:1/slip44:60`.
These are distinct on-chain balances with distinct issuers and distinct redemption risk, and treating them as one asset is an accounting decision that belongs to the consumer, not a normalisation that belongs in the identifier.

## Backwards Compatibility

No [CAIP-19][] profile previously existed for this namespace, so nothing is superseded and no existing identifier changes meaning.
The [CAIP-2][] and [CAIP-10][] profiles for `polkadot` are unaffected.

`pallet-uniques` is deprecated in favour of `pallet-nfts` but continues to hold live state, so the `uniques` asset namespace is required for as long as that state exists and is not merely a historical alias.

## References

- [CAIP-19][]: Asset Type and Asset ID Specification
- [CAIP-20][]: Asset Reference for the SLIP44 Asset Namespace
- [SLIP-0044][]: Registered coin types for BIP-0044, the source of the `slip44` references above
- [XCM][]: Cross-Consensus Messaging, whose `Location` type this profile mirrors
- [pallet-assets][]: The FRAME pallet behind the `asset`, `pool` and `foreign` namespaces
- [pallet-nfts][] and [pallet-uniques][]: The FRAME pallets behind the non-fungible namespaces
- [Polkadot Hub Assets][]: Ecosystem documentation for Asset Hub's asset pallets and their XCM locations
- [Polkadot public RPC endpoints][]: for dev/testing purposes
- [BIT-0004][]: Bittensor subnet deregistration, the source of the netuid-reuse behaviour described above

[CAIP-2]: ./caip2.md
[CAIP-10]: ./caip10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-20]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-20.md
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[XCM]: https://wiki.polkadot.network/docs/learn-xcm
[pallet-assets]: https://paritytech.github.io/polkadot-sdk/master/pallet_assets/index.html
[pallet-nfts]: https://paritytech.github.io/polkadot-sdk/master/pallet_nfts/index.html
[pallet-uniques]: https://paritytech.github.io/polkadot-sdk/master/pallet_uniques/index.html
[Polkadot Hub Assets]: https://docs.polkadot.com/reference/polkadot-hub/assets/
[Polkadot public RPC endpoints]: https://wiki.polkadot.network/docs/maintain-endpoints
[BIT-0004]: https://github.com/opentensor/bits/blob/main/bits/BIT-0004-subnet-deregistration.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
