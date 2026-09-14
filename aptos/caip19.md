---
namespace-identifier: aptos-caip19
title: Aptos Namespace - Asset Specification
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

Aptos carries two fungible-token standards at once, and they are not two spellings of one thing.

The older one, `0x1::coin`, identifies a currency by a Move **type tag** written `address::module::name`, of which `0x1::aptos_coin::AptosCoin` is the canonical example.
The newer one, the Fungible Asset standard of [AIP-21][], identifies a currency by the **address of a metadata object**, a bare 32-byte address with no type tag at all.
Non-fungibles split the same way: the Digital Asset standard of [AIP-11][] gives every token its own object address, while the legacy `0x3::token` standard identifies a token by the tuple of creator address, collection name, token name and property version.

That is four reference grammars with nothing in common, so this profile defines four asset namespaces plus `slip44`, and the `Collisions and Security Considerations` section documents the places where two of them name the same economic asset.

The type-tag grammar collides with the [CAIP-19][] `asset_reference` charset `[-.%a-zA-Z0-9]{1,128}` in two places: the `::` separator and the `_` that Move identifiers are permitted to contain, both of which appear in `0x1::aptos_coin::AptosCoin`.
Because `%` is inside the charset, percent-encoding as defined by [RFC 3986][] is the spec-legal escape, and this document defines it exactly.
The object-address grammars need no escaping at all.

The namespace abbreviations `fa` and `ft` would be the obvious names for Fungible Assets, and both are illegal: [CAIP-19][] requires an `asset_namespace` of 3 to 8 characters.
This profile instead names the two object standards after the AIPs that define them, `aip21` and `aip11`, following the precedent set by the Stellar profile's `cap38` and `sep41`.
The alternative, descriptive names such as `fungible` and `digital`, was rejected because those words describe a property that several of these namespaces share rather than the standard that fixes the reference format.

This profile was drafted by the maintainers of FAR, an open cross-reference between [CAIP-19][], CoinGecko and ISO 24165 identifiers, which needs a way to name 64 assets on this chain.
The authors do not represent the Aptos ecosystem and offer this for its community to correct, adopt or replace.

## Syntax

After the [CAIP-2][] namespace and chain ID, a slash introduces an `asset_namespace` and an `asset_reference`.

### Asset Namespaces

| Namespace | Standard | Description | Reference Format |
| :--- | :--- | :--- | :--- |
| `slip44` | [SLIP-0044][] | Native APT | `637` |
| `coin` | `0x1::coin` | Legacy Coin currency | Percent-encoded type tag of `T` in `0x1::coin::Coin<T>` |
| `aip21` | [AIP-21][] | Fungible Asset | Metadata object address |
| `aip11` | [AIP-11][] | Digital Asset (NFT) | Collection object address; the token object address is the `token_id` |
| `tokenv1` | `0x3::token` | Legacy Token V1 (NFT) | `TokenDataId` digest; the property version is the `token_id` |

### Address Normalization

Aptos publishes an address-format standard, [AIP-40][], which defines a `LONG` form of `0x` plus exactly 64 hexadecimal digits and a `SHORT` form with leading zeros trimmed, and calls an address **special** when it matches `^0x0{63}[0-9a-f]$`.
This profile applies [AIP-40][] in the two contexts it distinguishes, and the two contexts do not use the same form.

**A bare address used as an `aip21`, `aip11` or `tokenv1` reference, or as an `aip11` `token_id`**, MUST use [AIP-40][] display format: `SHORT` if the address is special, `LONG` otherwise.
This is what the fullnode REST API returns.
Live, the APT metadata object is `0xa` and Circle's native USDC metadata object is `0xbae207659db88bea0cbead6da0ed00aac12edcdda169e591cd41c94180b46f3b`.

**An address inside a `coin` type tag** MUST use `SHORT` form, with all leading zeros trimmed, whether or not the address is special.
This is not the [AIP-40][] display rule, and the divergence is deliberate: it is what the Move VM and every Aptos API actually emit for a type tag.
Live, a REST query for `0x1::coin::CoinInfo<0x7fd500c11216f0fe3095d0c4b8aa4d64a4e2e04f83758462f2b127255643615::thl_coin::THL>` echoes the type back with that 63-digit address unchanged, and the flagship type is `0x1::aptos_coin::AptosCoin`, not `0x0000…0001::aptos_coin::AptosCoin`.
Requiring `LONG` here would make every [CAIP-19][] reference differ from the string the chain, the explorers and the SDKs all print.

The `0x` prefix is mandatory in every form, and hexadecimal digits MUST be lowercase.

### Percent-Encoding

Let `enc(s)` be the function that replaces every octet of `s` that is not in `[-.0-9A-Za-z]` with a percent sign followed by that octet's two-digit uppercase hexadecimal value.
Applied to an Aptos type tag, `enc` touches exactly the following octets.

| Octet | Character | Escape | Where it occurs |
| :--- | :--- | :--- | :--- |
| `0x3A` | `:` | `%3A` | The `::` separator, always as the pair `%3A%3A` |
| `0x5F` | `_` | `%5F` | Inside a Move module or struct identifier, e.g. `aptos_coin` |
| `0x3C` | `<` | `%3C` | Opening a generic argument list |
| `0x3E` | `>` | `%3E` | Closing a generic argument list |
| `0x2C` | `,` | `%2C` | Separating generic arguments |

Escapes MUST use uppercase hexadecimal (`%3A`, never `%3a`), per [RFC 3986][] section 2.1.
Octets that do not require escaping MUST NOT be escaped, so that `enc` is injective and one currency has exactly one reference.
A type tag is serialized without whitespace, so a generic argument list is `A%2CB` and never carries a space after the separator.

## RegEx

The RegEx validation strings are as follows.

```sh
asset_id:           asset_type + "/" + token_id
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           "aptos:" + [0-9]+        (as defined in [CAIP-2])

asset_namespace:    "slip44" | "coin" | "aip21" | "aip11" | "tokenv1"

asset_reference:    slip44_ref | enc_type_tag | display_address | digest
slip44_ref:         "637"

display_address:    special_address | long_address
special_address:    0x[0-9a-f]
long_address:       0x[0-9a-f]{64}
short_address:      0x[0-9a-f]{1,64}         (no leading zero unless the whole address is 0x0)
digest:             0x[0-9a-f]{64}

enc_identifier:     [A-Za-z]([A-Za-z0-9]|%5F)*
enc_type_tag:       short_address + "%3A%3A" + enc_identifier + "%3A%3A" + enc_identifier
                    [ "%3C" + enc_type_tag + { "%2C" + enc_type_tag } + "%3E" ]

token_id:           display_address          (for aip11)
                  | [0-9]+                   (for tokenv1, the property version)
```

`asset_reference` is additionally bounded at 128 characters and `token_id` at 78, both of which every form above satisfies.

## Semantics

### Native APT

The native gas and staking token is identified through the SLIP-0044 registry, where line 670 of [SLIP-0044][] reads `| 637 | APTOS | Aptos |`.

```
aptos:1/slip44:637
```

APT also exists as a Coin type and as a Fungible Asset, so it has three identifiers in total.
See `Collisions and Security Considerations` for which one to emit.

### Coin

`0x1::coin` is the original Aptos fungible standard.
A currency is a Move type `T`; the chain stores its metadata in a `0x1::coin::CoinInfo<T>` resource under the account that published `T`.
The `coin` reference is the encoding of `T`, not of the wrapper `0x1::coin::Coin<T>`, matching how balances, transfers and every Aptos API address a currency.

Metadata is resolved with a REST call to a fullnode, in which the Aptos API itself percent-encodes the angle brackets of the resource type.

```bash
curl 'https://fullnode.mainnet.aptoslabs.com/v1/accounts/0x1/resource/0x1::coin::CoinInfo%3C0x1::aptos_coin::AptosCoin%3E'
# {"type":"0x1::coin::CoinInfo<0x1::aptos_coin::AptosCoin>",
#  "data":{"decimals":8,"name":"Aptos Coin","symbol":"APT", ...}}
```

### Fungible Asset

[AIP-21][] replaces the type-tag model with an object model.
A currency is a Move object carrying a `0x1::fungible_asset::Metadata` resource, and its identity is that object's address.
There is no type tag, so there is nothing to percent-encode.

```bash
curl 'https://fullnode.mainnet.aptoslabs.com/v1/accounts/0xa/resource/0x1::fungible_asset::Metadata'
# {"type":"0x1::fungible_asset::Metadata",
#  "data":{"decimals":8,"name":"Aptos Coin","symbol":"APT", ...}}
```

A Fungible Asset may be paired with a legacy Coin type, in which case the two are two views of one balance, or it may be FA-native, in which case no Coin type exists for it.
Both cases occur on mainnet and both are resolvable on chain; see below.

### Digital Asset

[AIP-11][] models a non-fungible as a Move object holding a `0x4::token::Token` resource, which points at a collection object holding a `0x4::collection::Collection` resource.
That is a genuine class-and-instance pair and maps onto the [CAIP-19][] split without invention.

The `asset_type` is the `aip11` namespace plus the **collection** object address.
The `asset_id` appends the **token** object address as the `token_id`.

```
asset_type: aptos:1/aip11:<collection_object_address>
asset_id:   aptos:1/aip11:<collection_object_address>/<token_object_address>
```

A token object address is globally unique on its own, so the `token_id` alone suffices to dereference the token; the collection address is retained because [CAIP-19][] requires an `asset_id` to extend an `asset_type`, and because the collection is the only class-level handle the standard offers.

### Token V1

`0x3::token` predates objects and identifies a token by a `TokenId`, which is a `TokenDataId` of `(creator_address, collection_name, token_name)` plus a numeric `property_version`.
Collection and token names are unbounded UTF-8 strings.
They are therefore not directly representable: percent-encoding a multi-byte character costs three characters per octet, and a real mainnet collection named `It's an Aptos thing` already spends nine characters on one apostrophe, with a 66-character creator address and a second name still to come inside a 128-character budget.

This profile instead uses the digest that the Aptos indexer publishes as `token_data_id`, which is
`sha256("<creator_address>::<collection_name>::<token_name>")` over the [AIP-40][] `LONG` creator address and the raw UTF-8 names.
The derivation was verified rather than assumed: for creator `0xaec259d962b5b975a3147df3683a954a582382a704846e8b660894050153d293`, collection `LFB` and token `LFB #33554`, that SHA-256 is `09c2834a9a55fdcd01acc1b51d14ec512827504ae1c8777e22d9dd258dd1b0a2`, which is exactly the `token_data_id` the public indexer returns for it.

The `asset_type` is the `tokenv1` namespace plus that digest, prefixed `0x`.
The `asset_id` appends the `property_version` in decimal as the `token_id`, which is the right split because a `TokenData` with a maximum above one and `property_version` zero is semi-fungible, exactly the role [CAIP-19][] `token_id` plays for ERC-1155.

A `tokenv1` reference is a digest and **not an address**.
Nothing is deployed at it; a REST query for resources at `0x09c2834a9a55fdcd01acc1b51d14ec512827504ae1c8777e22d9dd258dd1b0a2` returns `[]`.
It MUST NOT be dereferenced as an account or object address.

## Examples

```sh
# Native APT via SLIP-0044
aptos:1/slip44:637

# APT as a legacy Coin type
aptos:1/coin:0x1%3A%3Aaptos%5Fcoin%3A%3AAptosCoin

# APT as a Fungible Asset -- 0xa is special, so AIP-40 SHORT form
aptos:1/aip21:0xa

# Circle-issued native USDC, FA-native with no Coin type (decimals 6, symbol USDC)
aptos:1/aip21:0xbae207659db88bea0cbead6da0ed00aac12edcdda169e591cd41c94180b46f3b

# LayerZero-bridged USD Coin, a legacy Coin type (decimals 6, name "USD Coin")
aptos:1/coin:0x5e156f1207d0ebfa19a9eeff00d62a282278fb8719f4fab3a586a0a2c0fffbea%3A%3Acoin%3A%3AT

# Thala Token -- note both the underscore and the 63-digit SHORT address
aptos:1/coin:0x7fd500c11216f0fe3095d0c4b8aa4d64a4e2e04f83758462f2b127255643615%3A%3Athl%5Fcoin%3A%3ATHL

# The "It's an Aptos thing" Digital Asset collection
aptos:1/aip11:0x9a6f1b16323c428756b439553ab2a6a4cbdd46ade55d0da17f3a7c7d3e4c6ac8

# One token in it
aptos:1/aip11:0x9a6f1b16323c428756b439553ab2a6a4cbdd46ade55d0da17f3a7c7d3e4c6ac8/0x016243d52923adac2c86dcc4cb83e9b8e270f20c63954555acf5792a4ab9814e

# A Token V1 asset, "LFB #33554", property version 0
aptos:1/tokenv1:0x09c2834a9a55fdcd01acc1b51d14ec512827504ae1c8777e22d9dd258dd1b0a2/0

# APT on testnet
aptos:2/slip44:637
```

### Round Trip

The full round trip for the flagship Coin type.

```sh
# 1. input, as printed by the chain, the explorers and the SDKs
0x1::aptos_coin::AptosCoin

# 2. normalize: the address is already SHORT, so nothing changes here

# 3. apply enc(): four ":" become "%3A" and one "_" becomes "%5F"
0x1%3A%3Aaptos%5Fcoin%3A%3AAptosCoin

# 4. prepend the CAIP-2 chain ID and the asset namespace
aptos:1/coin:0x1%3A%3Aaptos%5Fcoin%3A%3AAptosCoin

# 5. to reverse, strip the prefix and percent-decode
0x1::aptos_coin::AptosCoin
```

The encoded reference is 36 characters; the longest in the examples above, the Thala type, is 90.
Step 5 is the exact string a REST or view call takes as a type argument.

## Collisions and Security Considerations

### One asset, a Coin identifier and a Fungible Asset identifier

This is the defining hazard of the Aptos namespace and it affects the flagship asset.
`aptos:1/coin:0x1%3A%3Aaptos%5Fcoin%3A%3AAptosCoin` and `aptos:1/aip21:0xa` are the same APT.
Both report `{"decimals":8,"symbol":"APT","name":"Aptos Coin"}`, and the pairing is not inferred from that but stated on chain in both directions.

```bash
curl -X POST https://fullnode.mainnet.aptoslabs.com/v1/view -H 'Content-Type: application/json' \
  -d '{"function":"0x1::coin::paired_metadata","type_arguments":["0x1::aptos_coin::AptosCoin"],"arguments":[]}'
# [{"vec":[{"inner":"0xa"}]}]

curl -X POST https://fullnode.mainnet.aptoslabs.com/v1/view -H 'Content-Type: application/json' \
  -d '{"function":"0x1::coin::paired_coin","type_arguments":[],"arguments":["0xa"]}'
# [{"vec":[{"account_address":"0x1","module_name":"0x6170746f735f636f696e","struct_name":"0x4170746f73436f696e"}]}]
# module_name and struct_name are hex-encoded "aptos_coin" and "AptosCoin"
```

The rule this profile adopts is that when `0x1::coin::paired_metadata<T>` returns a metadata object `m`, the **`aip21:m` form is canonical** and `coin:T` SHOULD be emitted only where the record is specifically about a legacy `CoinStore` balance.
Pairing is widespread, not exceptional: live, the LayerZero `…fffbea::coin::T` pairs to `0x54fc0d5fa5ad975ede1bf8b1c892ae018745a1afd4a4da9b70bb6e5448509fc0` and Thala's `thl_coin::THL` pairs to `0x377adc4848552eb2ea17259be928001923efe12271fef1667e2b784f04a7cf3a`.

The inverse does not hold.
`0x1::coin::paired_coin` for Circle's USDC metadata object returns `[{"vec":[]}]`, meaning that asset is FA-native and has no `coin` identifier at all.
An implementation that assumes every fungible asset has a Coin type will silently drop FA-native assets, which now include most newly issued stablecoins.

### The same address in two forms

Aptos accepts a non-special address in a type tag in either `LONG` or `SHORT` form, and normalizes its own echo to `SHORT`.
Verified live: a REST resource query written with `0x07fd500c11216f0fe3095d0c4b8aa4d64a4e2e04f83758462f2b127255643615` (64 digits) succeeds and returns the type spelled `0x7fd500c11216f0fe3095d0c4b8aa4d64a4e2e04f83758462f2b127255643615` (63 digits).
[AIP-40][] exists precisely because of this, and this profile's two normalization rules exist to collapse it to one spelling per asset.
A consumer receiving a `coin` reference whose address carries a leading zero, or an `aip21` reference whose non-special address is shorter than 64 digits, SHOULD reject it rather than silently re-normalize, because silent repair hides the producer's bug.

### Fungible Assets, tokens and collections share one address space

An `aip21` reference, an `aip11` reference, an `aip11` `token_id` and an Aptos account address are all 32-byte addresses drawn from the same space, and nothing in the string says which kind it is.
The `asset_namespace` is the only disambiguator, so a bare address moved between systems without it is meaningless.
The kind is resolvable on chain by asking which resource the object holds: `0x1::fungible_asset::Metadata` for `aip21`, `0x4::token::Token` for an `aip11` token, `0x4::collection::Collection` for an `aip11` collection.
Implementations SHOULD perform that check before trusting a namespace assignment from an untrusted source.

### Symbols are not identifiers

Three distinct assets on Aptos mainnet report symbol `USDC` with 6 decimals: the LayerZero Coin type `0x5e156f…::coin::T`, the Wormhole Coin type `0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa::asset::USDC`, and Circle's FA-native `0xbae207…`.
Keying on symbol merges them.
Note also that the first two are named `USD Coin` and differ from each other only in their type tag.

### Token V1 digests are not addresses and not preimage-bound

A `tokenv1` reference cannot be dereferenced on chain, and it cannot be reversed to recover the creator, collection and token name.
Any system that needs those must carry them alongside the identifier.
Two Token V1 assets collide only if their `(creator, collection, name)` triples collide under SHA-256, which is not a practical concern, but a consumer cannot *verify* a `tokenv1` reference without already holding the preimage.

### Case sensitivity

Move identifiers are case-sensitive, so `::USDC` and `::usdc` are different types.
Address hexadecimal MUST be lowercase and percent escapes MUST be uppercase; mixing either produces a second spelling of one asset.

## Backwards Compatibility

There is no prior asset-identifier convention in the `aptos` namespace, so this profile introduces no breaking change.

Within the chain, the migration from `0x1::coin` to [AIP-21][] Fungible Assets is ongoing rather than complete, which is why this profile keeps both namespaces rather than deprecating `coin`.
Historical records that predate an asset's pairing can only be expressed as `coin:T`, and that form remains conformant indefinitely.
The canonicalization preference stated above is a `SHOULD` for new records, not a rewrite of old ones.

The same applies to `tokenv1`: Token V1 assets are not migrated to [AIP-11][] automatically, so both NFT namespaces describe assets that exist on mainnet today.

## References

- [CAIP-2][] - Blockchain ID Specification, and the `aptos` chain IDs used above
- [CAIP-19][] - Asset Type and Asset ID Specification
- [SLIP-0044][] - Registered coin types, line 670 for Aptos
- [RFC 3986][] - URI Generic Syntax, section 2.1 for percent-encoding
- [AIP-11][] - Digital Assets, tokens as objects
- [AIP-21][] - Fungible Assets
- [AIP-40][] - Address Standard v1, the source of the `LONG`/`SHORT`/special definitions
- [Aptos REST API][] - The interface used to verify every coin, Fungible Asset and object in this document
- [Aptos Indexer API][] - The source of the `token_data_id` digest used by `tokenv1`
- [Aptos Coin and FA Standards][] - Developer documentation on the two fungible standards

[CAIP-2]: ./caip2.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[RFC 3986]: https://www.rfc-editor.org/rfc/rfc3986#section-2.1
[AIP-11]: https://github.com/aptos-foundation/AIPs/blob/main/aips/aip-011-digital-assets-tokens-as-objects.md
[AIP-21]: https://github.com/aptos-foundation/AIPs/blob/main/aips/aip-021-fungible-assets.md
[AIP-40]: https://github.com/aptos-foundation/AIPs/blob/main/aips/aip-040-address-standard-v1.md
[Aptos REST API]: https://aptos.dev/en/network/nodes/aptos-api-spec
[Aptos Indexer API]: https://aptos.dev/en/build/indexer
[Aptos Coin and FA Standards]: https://aptos.dev/en/build/smart-contracts/fungible-asset

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
