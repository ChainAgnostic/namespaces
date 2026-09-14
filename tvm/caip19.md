---
namespace-identifier: tvm-caip19
title: TVM Namespace - Asset Specification
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

The [TVM namespace][tvm-README] covers the chains running the TON Virtual Machine: TON, Everscale, Venom and Gosh.
All of them share one account model — every asset is a separate smart contract, addressed by a `workchain_id` and a 256-bit `account_id` — and they differ chiefly in which token interface those contracts implement.
TON contracts implement the TEP family ([TEP-74][] jettons, [TEP-62][] NFTs); Everscale, Venom and Gosh contracts implement the TIP family ([TIP-3][] fungible tokens, [TIP-4][] NFTs).

The hard problem this profile has to solve is the address encoding.
A TVM address has two written forms in wide use, and *neither* of them is legal as a [CAIP-19][] `asset_reference` without transformation.
The raw form `0:b113a9…1dfe` contains a colon, which the `asset_reference` charset `[-.%a-zA-Z0-9]{1,128}` excludes.
The TON user-friendly form `EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs` is base64url and so may contain `_`, which the charset also excludes; in its non-URL-safe base64 spelling it may contain `+` and `/`, and `/` is [CAIP-19][]'s own delimiter between an `asset_type` and a `token_id`.
This profile designates the raw form as canonical, percent-encodes its single colon, and specifies the normalisation from the user-friendly form so that the two never produce two identifiers for one asset.

This profile was drafted by the maintainers of FAR, an open cross-reference between [CAIP-19][], CoinGecko and ISO 24165 identifiers, which needs a way to name 215 assets on the chains in this namespace.
The authors do not represent the TON, Everscale, Venom or Gosh ecosystems and offer this for those communities to correct, adopt or replace.

## Syntax

After the [CAIP-2][] namespace and chain ID, a slash introduces an `asset_namespace` and an `asset_reference`.

### Asset Namespaces

| Namespace | Chains | Asset kind | Reference format |
| :--- | :--- | :--- | :--- |
| `slip44` | all | Native coin | the [SLIP-0044][] coin type in decimal |
| `tep74` | TON | Jetton (fungible), [TEP-74][] | jetton master address, canonical raw form |
| `tep62` | TON | NFT, [TEP-62][] | NFT collection address, canonical raw form |
| `extracur` | TON | Extra currency | the 32-bit `currency_id` in decimal |
| `tip3` | Everscale, Venom, Gosh | Fungible token, [TIP-3][] | token root address, canonical raw form |
| `tip4` | Everscale, Venom, Gosh | NFT, [TIP-4][] | NFT collection address, canonical raw form |

`tep62` and `tip4` identify non-fungibles and take a `token_id`; the other four namespaces identify fungible classes and are bare `asset_type`s.

### The canonical address form

A TVM account is a pair of a `workchain_id` and a 256-bit `account_id`.
Nothing else is part of the account's identity.

The **canonical reference form** used by `tep74`, `tep62`, `tip3` and `tip4` is:

```
<workchain_id> "%3A" <account_id>
```

where:

- `workchain_id` is the signed decimal integer of the workchain, with no leading zeroes, no `+` sign, and a leading `-` only when negative.
  In practice it is `0` (the basechain) or `-1` (the masterchain); every asset contract observed on these chains lives in workchain `0`.
- `account_id` is exactly 64 **lowercase** hexadecimal digits, the 32 bytes of the account identifier.
- `%3A` is the percent-encoding of the `:` separator, per [Section 2.1][rfc3986sec2.1] of [RFC 3986][].
  The two hexadecimal digits of the escape are canonically capitalised, as [CAIP-19][] recommends; this is independent of the `account_id`, which is lowercase.

This is the only octet in the canonical form that requires escaping.
The longest possible reference is 78 characters (`-2147483648` + `%3A` + 64 hex digits), well inside the 128-character limit.

Two normalisations are mandatory and both are lossless:

1. Hexadecimal digits are lowercased.
   Some TON libraries emit the raw form with uppercase hex; `0:B113A9…` and `0:b113a9…` are the same account and MUST produce the same identifier.
2. The colon is escaped as `%3A` and never as `%3a`.

### Normalising the TON user-friendly form

TON additionally publishes a 48-character "user-friendly" address, which is what block explorers, wallets and token lists display.
It is **not** an identifier: it encodes presentation flags that are not part of the account, so one account has four of them, each in two base64 alphabets — eight strings for one asset.
It MUST be converted to the canonical raw form before a [CAIP-19][] identifier is built.

The structure is 36 bytes, base64-encoded without padding:

```
byte  0        tag         0x11 bounceable | 0x51 non-bounceable, OR'd with 0x80 if testnet-only
byte  1        workchain   int8, signed
bytes 2..33    account_id  32 bytes
bytes 34..35   checksum    CRC-16/XMODEM over bytes 0..33, big-endian
```

To normalise:

1. Decode the 48 characters as base64, accepting both the URL-safe alphabet (`-`, `_`) and the standard one (`+`, `/`), to 36 bytes.
2. Verify the CRC-16/XMODEM checksum over the first 34 bytes.
   Reject the address if it does not match.
3. Read `workchain_id` from byte 1 as a signed 8-bit integer, and `account_id` from bytes 2 through 33 as 64 lowercase hexadecimal digits.
4. **Discard the tag byte.**
   Bounceability and the testnet-only flag are routing and display hints; they do not distinguish assets, and preserving them would produce four identifiers for one jetton.
5. Emit `<workchain_id>%3A<account_id>`.

The [toncenter][] `detectAddress` endpoint performs exactly this normalisation and can be used as a reference implementation.

The user-friendly form is a TON addition; Everscale, Venom and Gosh tooling uses the raw form throughout, which is a further reason to make it canonical for the whole namespace.

## RegEx

The RegEx validation strings are as follows:

```sh
asset_id:           asset_type | asset_type + "/" + token_id
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           namespace + ":" + blockchain_id (as defined in [CAIP-2])

asset_namespace:    "slip44" | "tep74" | "tep62" | "extracur" | "tip3" | "tip4"

asset_reference:    slip44_ref | address_ref | extracur_ref
slip44_ref:         [0-9]{1,10}
address_ref:        -?[0-9]{1,10}%3A[0-9a-f]{64}
extracur_ref:       0|[1-9][0-9]{0,9}

token_id:           0|[1-9][0-9]{0,77}
```

`address_ref` is the canonical reference form for `tep74`, `tep62`, `tip3` and `tip4`.
`token_id` applies to `tep62` and `tip4` only.

## Semantics

### Native coins (`slip44`)

The native coin of a TVM chain is identified with the `slip44` asset namespace and the chain's registered coin type, as [CAIP-20][] describes.

Two of the four chains in this namespace are registered in [SLIP-0044][]:

```
| 607        | TON     | TON                               |
| 396        | EVER    | Everscale                         |
```

So Toncoin on TON is `tvm:-239/slip44:607` and EVER on Everscale is `tvm:42/slip44:396`.

**Venom and Gosh have no [SLIP-0044][] registration** as of 2026-09-14, and this profile does not invent one.
Until their communities register a coin type, the native coins of `tvm:1` and of Gosh have no `slip44` identifier, and implementations SHOULD NOT substitute another chain's coin type for them.

### Jettons (`tep74`)

A jetton is TON's fungible token, defined by [TEP-74][].
It is implemented as one **jetton master** contract plus one **jetton wallet** contract per holder, the wallet address being derived from the master and the owner.

The asset is the **master**.
The reference is the jetton master's address in canonical form.

A jetton master is recognised by `get_jetton_data()`, which returns `(int total_supply, int mintable, slice admin_address, cell jetton_content, cell jetton_wallet_code)`.
Metadata (name, symbol, decimals) lives in `jetton_content` per [TEP-64][]; it is mutable, not unique, and not part of the identifier.

### TON NFTs (`tep62`)

[TEP-62][] gives each NFT item its own contract, optionally grouped under a collection contract.
An item exposes `get_nft_data()` returning `(int init?, int index, slice collection_address, slice owner_address, cell individual_content)`; a collection exposes `get_collection_data()` and `get_nft_address_by_index(int index)`.

For an item that belongs to a collection:

- the `asset_type` is `tep62:` + the **collection** address in canonical form, and
- the `token_id` is the item's `index`, interpreted as the `uint256` that [TEP-62][] declares it to be and rendered in decimal without leading zeroes.

A `uint256` is at most 78 decimal digits, which is exactly the `token_id` limit, so every well-formed index fits.
Because the get-method returns a TVM 257-bit *signed* integer, a resolver MUST reduce the returned value modulo 2^256 and render it unsigned; it MUST NOT emit a negative `token_id`.

Collections are not required to number their items sequentially.
[TEP-62][] uses `next_item_index = -1` to mark a non-sequential collection, and large collections such as TON DNS derive the index from the item's name, producing indices with dozens of digits.

For a **collection-less** item — one whose `collection_address` is `addr_none` — there is no collection to key on, and [TEP-62][] says the item's own index is "arbitrary but constant", so it is not a usable discriminator.
Such an item is identified as a bare `asset_type` whose reference is the **item's own** address in canonical form, with no `token_id`.
This is unambiguous because the item address is globally unique; the Collisions section below explains how a consumer tells the two shapes apart.

### Extra currencies (`extracur`)

TON's `CurrencyCollection` carries, alongside Toncoin, a dictionary of "extra currencies" keyed by a 32-bit `currency_id`.
These are native to the protocol rather than contract-based, so no address exists for them; the reference is the `currency_id` in decimal, between `0` and `4294967295`.

Extra currencies are live on TON mainnet: network config parameter 7 records the volume of each one, and as of 2026-09-14 it carries the ids `239` and `4294967279`.
They are rare, and most tooling ignores them, which is precisely why they need an identifier rather than being silently folded into Toncoin.

### TIP-3 tokens (`tip3`)

[TIP-3][] is the fungible token interface of Everscale, Venom and Gosh.
It is structurally the same design as a jetton: one **TokenRoot** contract plus one TokenWallet per holder.

The asset is the **TokenRoot**, and the reference is its address in canonical form.
A TokenRoot is recognised by the [TIP-6][] interface identifier `0x4371D8ED`, and in practice by its code hash, since the ecosystem deploys a small number of audited TokenRoot builds.

### TIP-4 NFTs (`tip4`)

[TIP-4][] mirrors [TEP-62][]: a Collection contract with `nftAddress(uint256 id)`, and per-item NFT contracts whose `getInfo()` returns `(uint256 id, address owner, address manager, address collection)`.

The `asset_type` is `tip4:` + the collection address in canonical form and the `token_id` is the item's `id` in decimal, with the same `uint256` rules as `tep62`.
The [TIP-6][] interface identifier for `TIP4_1Collection` is `0x1217AAAB`.

## Examples

```sh
# Toncoin, the native coin of TON mainnet
tvm:-239/slip44:607

# EVER, the native coin of Everscale mainnet
tvm:42/slip44:396

# Tether USD (USD₮) jetton on TON
# user-friendly: EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs
tvm:-239/tep74:0%3Ab113a994b5024a16719f69139328eb759596c38a25f59028b146fecdc3621dfe

# Notcoin (NOT) jetton on TON
# user-friendly: EQAvlWFDxGF2lXm67y4yzC17wYKD9A0guwPkMs1gOsM__NOT
tvm:-239/tep74:0%3A2f956143c461769579baef2e32cc2d7bc18283f40d20bb03e432cd603ac33ffc

# TON extra currency 239
tvm:-239/extracur:239

# Whale #3778, item 0 of the Whales Club collection on TON (sequential indices)
tvm:-239/tep62:0%3Aef4453182ddc66bd8dd393e71f58c2ea0e75c5fc47253b6169e30c23df75a194/0

# sexcontact.ton, an item of the TON DNS Domains collection (name-derived index)
tvm:-239/tep62:0%3Ab774d95eb20543f186c06b371ab88ad704f7e256130caf96189368a7d0cb6ccf/243888483260932203507286670066710751810584302796194698527687689304245627

# Wrapped EVER (WEVER), a TIP-3 token root on Everscale
tvm:42/tip3:0%3Aa49cd4e158a9a15555e624759e2e4e766d22600b7800d891e46f9291f044a93d

# Tether USD (USDT), a TIP-3 token root on Everscale
tvm:42/tip3:0%3Aa519f99bb5d6d51ef958ed24d337ad75a1c770885dcd42d51d6663f9fcdacfb2

# A TIP-3 token root on Venom mainnet
tvm:1/tip3:0%3A8d99d8e1910af976b17bb43b2df9682776be41fa2547a03f5e5fd374d6b3f92c
```

### Address round trip

Every one of the following strings names the same TON account — the Tether USD jetton master — and all of them normalise to the same reference:

```sh
# user-friendly, bounceable, base64url        (the form wallets and explorers show)
EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs
# user-friendly, non-bounceable, base64url
UQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_p0p
# user-friendly, bounceable, testnet-only flag
kQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_ntm
# user-friendly, non-bounceable, testnet-only flag
0QCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_iaj
# user-friendly, bounceable, standard base64
EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id/sDs
# raw
0:b113a994b5024a16719f69139328eb759596c38a25f59028b146fecdc3621dfe
# raw, uppercase hex, as some libraries emit it
0:B113A994B5024A16719F69139328EB759596C38A25F59028B146FECDC3621DFE

# all seven normalise to:
0%3Ab113a994b5024a16719f69139328eb759596c38a25f59028b146fecdc3621dfe
# giving:
tvm:-239/tep74:0%3Ab113a994b5024a16719f69139328eb759596c38a25f59028b146fecdc3621dfe
```

Percent-encoding is used in exactly one place in this profile, for the `:` in the raw address, and a conforming implementation needs no percent-decoder beyond a fixed `%3A` at a known offset.

## Collisions and Security Considerations

### The user-friendly form is not an identifier

An implementation that builds references from TON user-friendly addresses will emit up to eight distinct [CAIP-19][] strings for one jetton, because the tag byte and the base64 alphabet both vary while the account does not.
The standard-base64 spellings are not merely non-canonical but actively dangerous, because `/` is [CAIP-19][]'s own delimiter.
The Tether USD jetton master, written in standard base64, is `EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id/sDs`, and the string

```
tvm:-239/tep74:EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id/sDs
```

satisfies every production in [CAIP-19][]: it is a well-formed `asset_id` whose `asset_reference` is a truncated address and whose `token_id` is `sDs`.
It does not fail validation, it silently names a different thing.
Notcoin shows the same hazard doubled — the Notcoin jetton master's user-friendly address is the vanity string `EQAvlWFDxGF2lXm67y4yzC17wYKD9A0guwPkMs1gOsM__NOT`, spelled `EQAvlWFDxGF2lXm67y4yzC17wYKD9A0guwPkMs1gOsM//NOT` in standard base64 — with two illegal `_` characters in one form and two delimiter collisions in the other.
This is the concrete reason the raw form is mandated here.

### The `index` of a TEP-62 item is reported inconsistently

[TEP-62][] declares the NFT index a `uint256`, but at least one widely used TON indexer truncates it to its low 64 bits and renders that as a signed `int64`.
For the TON DNS item `sexcontact.ton`, the contract's own `get_nft_data()` returns

```
243888483260932203507286670066710751810584302796194698527687689304245627
```

while the indexer reports `-8293690280373418629`, which is the low 64 bits of that value read as a signed integer.
The truncated form is not just non-canonical, it is **not injective**: any two items in a large name-derived collection whose indices agree in their low 64 bits would receive the same `token_id`.
Implementations MUST take the index from the get-method or from a source that preserves all 256 bits.

### Jetton wallets are not jettons

`get_wallet_address(owner)` on a jetton master returns a per-holder wallet contract address, and TIP-3 has the same TokenRoot/TokenWallet split.
Those wallet addresses appear in transfer messages and in naive indexer output, and they are ordinary TVM addresses, so they will pass every syntactic check in this profile.
A `tep74` or `tip3` reference MUST be the master or root address; a wallet address would name a different asset for every holder of the same token.

### Collection addresses and collection-less item addresses share a namespace

Within `tep62` (and `tip4`), a reference that carries a `token_id` is a collection address and a bare reference is a collection-less item address.
The shapes are distinguishable by their arity, but a consumer that drops a `token_id` turns a valid item identifier into a valid-looking, wrong one.
A resolver can always settle the question on-chain: `get_collection_data()` succeeds on a collection and fails on an item, and `get_nft_data()` does the reverse.
Implementations SHOULD reject a bare `tep62` reference whose contract answers `get_collection_data()`.

### Names and tickers are not identifiers

Jetton and TIP-3 metadata is mutable and unconstrained.
The Tether USD jetton's on-chain symbol is `USD₮` — with U+20AE TUGRIK SIGN, not an ASCII `T` — which is representable in [TEP-64][] metadata and not representable in an `asset_reference` at all.
Identifiers in this profile are derived only from addresses and protocol-assigned integers, never from metadata.

### `global_id` is not centrally registered

The [CAIP-2][] profile for this namespace notes that there is no central registry preventing two chains from claiming the same `global_id`.
That risk is inherited here in full: an asset reference is only as unique as the chain ID it is qualified by.
Consumers handling assets from more than one TVM chain SHOULD pin each `global_id` to a known endpoint set rather than treating the integer as globally authoritative.

## Backwards Compatibility

This is the first asset specification for the `tvm` namespace, so there is no prior [CAIP-19][] profile to be compatible with.

Existing TON tooling overwhelmingly exchanges the base64url user-friendly form, and existing Everscale, Venom and Gosh tooling overwhelmingly exchanges the raw form.
The normalisation above accepts both and is lossless in the direction that matters, since the discarded tag byte carries no asset identity.
Reconstructing a display address from a canonical reference requires choosing a tag, and implementations SHOULD default to bounceable (`0x11`) with the testnet flag clear, which is the form TON explorers use for contracts.

[TEP-74][] jettons, [TEP-62][] NFTs, [TIP-3][] tokens and [TIP-4][] NFTs are all live standards with deployed contracts predating this document; nothing here requires an on-chain change.

## References

- [CAIP-2][]: Blockchain ID Specification
- [CAIP-19][]: Asset Type and Asset ID Specification
- [CAIP-20][]: Asset Reference for the SLIP44 Asset Namespace
- [SLIP-0044][]: Registered coin types for BIP-0044
- [TEP-74][]: Fungible tokens (Jettons) standard
- [TEP-62][]: NFT standard
- [TEP-64][]: Token data standard
- [TIP-3][]: Fungible token interface for Everscale, Venom and Gosh
- [TIP-4][]: Non-fungible token interface
- [TIP-6][]: Standard interface detection
- [TON Addresses][]: The raw and user-friendly address forms
- [toncenter][]: TON HTTP API, including `detectAddress` and `runGetMethod`
- [tonapi][]: TON indexer API
- [Everscale GraphQL][]: Everscale node GraphQL endpoint
- [Venom GraphQL][]: Venom node GraphQL endpoint
- [TIP3 Tokens List][]: Curated Everscale TIP-3 token manifest
- [RFC 3986][]: Uniform Resource Identifier (URI): Generic Syntax

[CAIP-2]: ./caip2.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-20]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-20.md
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[tvm-README]: ./README.md
[TEP-74]: https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md
[TEP-62]: https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md
[TEP-64]: https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md
[TIP-3]: https://docs.everscale.network/standard/TIP-3
[TIP-4]: https://docs.everscale.network/standard/TIP-4
[TIP-6]: https://docs.everscale.network/standard/TIP-6
[TON Addresses]: https://docs.ton.org/v3/documentation/smart-contracts/addresses
[toncenter]: https://toncenter.com/api/v2/
[tonapi]: https://tonapi.io/
[Everscale GraphQL]: https://dapp01.itgold.io/graphql
[Venom GraphQL]: https://gql.venom.foundation/graphql
[TIP3 Tokens List]: https://github.com/broxus/ton-assets
[RFC 3986]: https://www.rfc-editor.org/rfc/rfc3986
[rfc3986sec2.1]: https://www.rfc-editor.org/rfc/rfc3986#section-2.1

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
