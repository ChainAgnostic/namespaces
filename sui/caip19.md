---
namespace-identifier: sui-caip19
title: Sui Namespace - Asset Specification
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

Every asset on Sui is ultimately a Move value, and every Move value is described by a **type tag**.
A type tag is written `address::module::name`, optionally followed by a comma-separated list of type arguments in angle brackets.
Fungible currencies are identified by the type argument `T` of `0x2::coin::Coin<T>`; the canonical example is `0x2::sui::SUI`.
Non-fungible assets are individual Move **objects**, each of which carries both a type tag and a 32-byte object ID.

The [CAIP-19][] `asset_reference` charset is `[-.%a-zA-Z0-9]{1,128}`.
A Move type tag collides with that charset in four places: the `::` separator, the `_` that Move identifiers are permitted to contain, and the `<`, `>` and `,` of a generic argument list.
Because `%` is inside the charset, percent-encoding as defined by [RFC 3986][] is the only escape this profile needs, and this document defines it exactly rather than inventing a Sui-specific one.

Sui accepts an address in a type tag in either a short form (`0x2`) or a zero-padded long form (`0x0000…0002`), which means one asset has two spellings unless a profile picks one.
This profile mandates the long form.
The justification is that the long form is the form Sui itself emits: a live query to the mainnet GraphQL RPC for the type of the SUI currency object returns
`0x0000000000000000000000000000000000000000000000000000000000000002::coin_registry::Currency<0x0000000000000000000000000000000000000000000000000000000000000002::sui::SUI>`.
That string is Move's canonical `TypeTag` serialization, it is fixed-width, and it removes the "how many leading zeros do I strip" question that a short form leaves to every implementer independently.
The cost is 62 extra characters per address, which is paid for in the `Collisions and Security Considerations` section below.

This profile was drafted by the maintainers of FAR, an open cross-reference between [CAIP-19][], CoinGecko and ISO 24165 identifiers, which needs a way to name 151 assets on this chain.
The authors do not represent the Sui ecosystem and offer this for its community to correct, adopt or replace.

## Syntax

After the [CAIP-2][] namespace and chain ID, a slash introduces an `asset_namespace` and an `asset_reference`.

### Asset Namespaces

| Namespace | Description | Reference Format |
| :--- | :--- | :--- |
| `slip44` | Native SUI via the SLIP-0044 registry | `784` |
| `coin` | A fungible currency | Percent-encoded canonical type tag of `T` in `0x2::coin::Coin<T>` |
| `object` | A Move object, i.e. a Sui non-fungible | Percent-encoded canonical type tag of the object's struct; the object ID is the `token_id` |

### Address Normalization

An address inside a type tag, and an object ID used as a `token_id`, MUST be written in the long form.
The long form is `0x` followed by exactly 64 lowercase hexadecimal digits, left-padded with zeros.
Uppercase hexadecimal digits MUST NOT be used, and the `0x` prefix is mandatory.
A short-form address (`0x2`) is a valid input to this profile's construction procedure but is not itself a conformant reference; it MUST be padded before encoding.

### Percent-Encoding

Let `enc(s)` be the function that replaces every octet of `s` that is not in `[-.0-9A-Za-z]` with a percent sign followed by that octet's two-digit uppercase hexadecimal value.
Applied to a canonical Move type tag, `enc` touches exactly the following octets and no others.

| Octet | Character | Escape | Where it occurs |
| :--- | :--- | :--- | :--- |
| `0x3A` | `:` | `%3A` | The `::` separator, always as the pair `%3A%3A` |
| `0x5F` | `_` | `%5F` | Inside a Move module or struct identifier, e.g. `suins_registration` |
| `0x3C` | `<` | `%3C` | Opening a generic argument list |
| `0x3E` | `>` | `%3E` | Closing a generic argument list |
| `0x2C` | `,` | `%2C` | Separating generic arguments |

Two normalization rules make `enc` injective, and both are mandatory.
Escapes MUST use uppercase hexadecimal (`%3A`, never `%3a`), per [RFC 3986][] section 2.1.
Octets that do not require escaping MUST NOT be escaped: `enc` never produces `%41` for `A`, and a reference containing an unnecessary escape is non-conformant rather than merely unusual.
A canonical type tag contains no whitespace, so generic argument lists are serialized as `A%2CB`, never with a space after the separator.

## RegEx

The RegEx validation strings are as follows.

```sh
asset_id:           asset_type + "/" + token_id
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           "sui:" + ( "mainnet" | "testnet" | "devnet" )   (as defined in [CAIP-2])

asset_namespace:    "slip44" | "coin" | "object"

asset_reference:    slip44_ref | enc_type_tag
slip44_ref:         "784"
token_id:           address

address:            0x[0-9a-f]{64}
enc_identifier:     [A-Za-z]([A-Za-z0-9]|%5F)*
enc_type_tag:       address + "%3A%3A" + enc_identifier + "%3A%3A" + enc_identifier
                    [ "%3C" + enc_type_tag + { "%2C" + enc_type_tag } + "%3E" ]
```

An `enc_type_tag` is additionally bounded by the [CAIP-19][] `asset_reference` limit of 128 characters.
A non-generic type tag encodes to `66 + 6 + len(module) + 6 + len(struct)` characters, where each `_` in an identifier counts as three; the budget left for the two identifiers is therefore 50 characters.
`token_id` is 66 characters, comfortably inside the 78-character limit.

## Semantics

### Native SUI

The native gas and staking token is identified through the SLIP-0044 registry, where line 817 of [SLIP-0044][] reads `| 784 | SUI | Sui |`.

```
sui:mainnet/slip44:784
```

The same asset also exists as a Move currency, `0x2::sui::SUI`, and therefore also has a `coin` form.
See `Collisions and Security Considerations` for which of the two an implementation should emit.

### Coin Types

A Sui currency is a Move type `T` for which a `0x2::coin::TreasuryCap<T>` was created and coin metadata registered.
Balances, transfers and metadata lookups all key on `T`, not on `0x2::coin::Coin<T>`, and this profile follows that convention: the `coin` reference is the encoding of `T` alone.
Writing the wrapper type would double the reference length for no added information and would push most references past the 128-character limit.

Metadata for a coin type is resolved with the `coinMetadata` field of the Sui GraphQL RPC.
The JSON-RPC method `suix_getCoinMetadata` served the same purpose but has been retired on public fullnodes; a live `POST` to `https://fullnode.mainnet.sui.io:443` now answers
`{"code":-32601,"message":"Method not found. JSON-RPC on public fullnodes has been deprecated."}`.

```graphql
{ coinMetadata(coinType: "0x2::sui::SUI") { decimals symbol name } }
```

Sui also defines closed-loop tokens, `0x2::token::Token<T>`, which restrict how a balance may move but do not create a new currency.
A closed-loop token over `T` is the same asset as a coin over `T` and uses the same `coin` reference; the transfer restriction is a property of the holding object, not of the currency.

### Objects and Non-Fungibles

Sui has no single NFT contract standard.
A non-fungible is simply a Move object with the `key` ability, and its identity has two parts: the struct type it was created from, and its 32-byte object ID.
This maps onto the [CAIP-19][] split directly.

The `asset_type` is the `object` namespace plus the encoded struct type, and names the class of objects of that type.
The `asset_id` appends the object ID as the `token_id`, and names one specific object.

```
asset_type: sui:mainnet/object:<enc(type)>
asset_id:   sui:mainnet/object:<enc(type)>/<object_id>
```

An object ID is globally unique and is never reused, so the `token_id` alone is sufficient to dereference the object; the `asset_type` component is retained because [CAIP-19][] requires an `asset_id` to extend an `asset_type`, and because the type is the only class-level handle Sui offers.

### Type Stability Across Package Upgrades

The address component of a type tag is the ID of the package that originally defined the type.
Sui publishes an upgraded package under a new object ID, but existing types keep the defining package's original ID, so a coin's or an object type's [CAIP-19][] identifier does not change when its package is upgraded.

## Examples

```sh
# Native SUI on mainnet, via SLIP-0044
sui:mainnet/slip44:784

# SUI as a coin type
sui:mainnet/coin:0x0000000000000000000000000000000000000000000000000000000000000002%3A%3Asui%3A%3ASUI

# Circle-issued native USDC on mainnet (decimals 6, symbol USDC)
sui:mainnet/coin:0xdba34672e30cb065b1f93e3ab55318768fd6fef66c15942c9f7cb846e2f900e7%3A%3Ausdc%3A%3AUSDC

# The Prime Machin NFT type -- the class of all Prime Machin objects
sui:mainnet/object:0x034c162f6b594cb5a1805264dd01ca5d80ce3eca6522e6ee37fd9ebfb9d3ddca%3A%3Afactory%3A%3APrimeMachin

# Prime Machin #2550 -- one specific object
sui:mainnet/object:0x034c162f6b594cb5a1805264dd01ca5d80ce3eca6522e6ee37fd9ebfb9d3ddca%3A%3Afactory%3A%3APrimeMachin/0x0003cf33a2555e1b47eeb00ba24d9d37a8ec128e00477f33830cd9b0bf0fabd5

# A SuiNS name registration -- note the underscore in the module name
sui:mainnet/object:0xd22b24490e0bae52676651b4f56660a5ff8022a2576e0089f79b3c88d44e08f0%3A%3Asuins%5Fregistration%3A%3ASuinsRegistration/0x00000c873385ec0533ec694114d0824ff1bfbe4f02d5fadcce0aa828b085fb7e

# Native SUI on testnet
sui:testnet/slip44:784
```

### Round Trip

The full round trip for the flagship coin type, from the short form a user is most likely to paste to the reference and back.

```sh
# 1. input, short form as printed by the Sui CLI and explorer
0x2::sui::SUI

# 2. normalize the address to the long form (left-pad to 64 hex digits)
0x0000000000000000000000000000000000000000000000000000000000000002::sui::SUI

# 3. apply enc(): four ":" octets become "%3A"; nothing else changes
0x0000000000000000000000000000000000000000000000000000000000000002%3A%3Asui%3A%3ASUI

# 4. prepend the CAIP-2 chain ID and the asset namespace
sui:mainnet/coin:0x0000000000000000000000000000000000000000000000000000000000000002%3A%3Asui%3A%3ASUI

# 5. to reverse, strip the prefix and percent-decode
0x0000000000000000000000000000000000000000000000000000000000000002::sui::SUI

# 6. optionally re-shorten for display only; this form is NOT a conformant reference
0x2::sui::SUI
```

Step 5 is what a client sends to an RPC.
Both step 2 and step 6 are accepted by a Sui fullnode: a live `coinMetadata` query for each returns the same result, `{"decimals":9,"symbol":"SUI","name":"Sui"}`.
The encoded reference in step 3 is 84 characters and the one in the USDC example is 86, both inside the 128-character limit.

## Collisions and Security Considerations

### Short and long address forms are both accepted by the chain

This is the single largest source of duplicate identifiers on Sui, and it was verified live rather than assumed.
A `coinMetadata` query for `0x2::sui::SUI` and one for `0x0000…0002::sui::SUI` both succeed and return the same currency.
An indexer that normalizes inconsistently will therefore hold the same asset under two [CAIP-19][] identifiers that no string comparison relates.
Only the long form is conformant here, and a consumer receiving a short-form reference SHOULD reject it rather than silently pad it, because silent padding hides the producer's bug.

### The currency type, not the wrapper

`coin:0x…::sui::SUI` and a hypothetical `coin:0x…::coin::Coin%3C0x…::sui::SUI%3E` would name the same currency.
Only the former is conformant.

### The 128-character ceiling is reachable

Long-form addresses cost 66 characters each, and a generic type tag carries at least two.
`0x2::coin::Coin<0xdba34672…::usdc::USDC>` encodes to 178 characters and is therefore **not representable** as a [CAIP-19][] `asset_reference`.
No currency in this profile needs a generic reference, because the `coin` namespace takes `T` alone, but a generic *object* type always does: two long-form addresses alone cost 132 characters, so an NFT type of the shape `0xA::pkg::Fren<0xB::kind::Kind>` is over the limit before a single module or struct name is written.
Such assets have no identifier under this profile.
The SuiNS example above, at 115 characters, shows how little headroom even a single non-generic type with one underscored identifier leaves.
A future revision could define a digest-based reference for the overflow case; this profile deliberately does not, because a hash is not reversible and would break the round trip that is the point of the encoding.

### A Move type is not a curated collection

An `object` `asset_type` is a *type-level* class, which is weaker than the contract-level class an ERC-721 address provides.
A launchpad or a shared NFT framework that mints many logical collections from one generic struct produces one `asset_type` for all of them.
Conversely a single logical collection that migrated between modules has two.
Consumers MUST NOT assume that one `object` `asset_type` corresponds to exactly one marketplace collection, and SHOULD carry the collection's own on-chain handle, such as its Kiosk or its `0x2::display::Display` record, alongside the [CAIP-19][] identifier when that distinction matters.

### Case and over-encoding

Move identifiers are case-sensitive, so `::USDC` and `::usdc` are different types and different references.
Hexadecimal in addresses MUST be lowercase, hexadecimal in percent escapes MUST be uppercase, and no octet outside the table above may be escaped.
Without these three rules `enc` is not injective and a single asset again acquires several spellings.

### Symbols are not identifiers

Coin metadata `symbol` is attacker-chosen and unconstrained.
Two distinct coin types on Sui mainnet both report `{"decimals":6,"symbol":"USDC","name":"USD Coin"}`: the Circle-issued `0xdba34672…::usdc::USDC` above, and the Wormhole-bridged `0x5d4b302506645c37ff133b98c4b50a5ae14841659738d6d733d59d0d217a93bf::coin::COIN`.
Only the type tag identifies the asset.

## Backwards Compatibility

There is no prior asset-identifier convention in the `sui` namespace to be compatible with, so this profile introduces no breaking change.

The convention it does have to respect is the ecosystem's own habit of writing type tags in short form, which appears throughout Sui documentation, the Sui CLI and Sui Explorer.
This profile treats that form as an accepted *input* and a permitted *display* form, and requires normalization to the long form only at the point where a [CAIP-19][] identifier is constructed.

Metadata resolution moved from the JSON-RPC method `suix_getCoinMetadata` to the GraphQL `coinMetadata` field, and metadata storage itself is moving into `0x2::coin_registry`.
Neither change affects the identifiers defined here, because both are lookups keyed on the same type tag.

## References

- [CAIP-2][] - Blockchain ID Specification, and the `sui` chain IDs used above
- [CAIP-19][] - Asset Type and Asset ID Specification
- [SLIP-0044][] - Registered coin types, line 817 for Sui
- [RFC 3986][] - URI Generic Syntax, section 2.1 for percent-encoding
- [Sui Docs][] - Developer documentation and concept overviews for building on Sui
- [Sui GraphQL RPC][] - The interface used to verify every coin type and object in this document
- [Sui JSON-RPC Migration][] - Notice of the deprecation of JSON-RPC on public fullnodes
- [Sui Coin Standard][] - The `0x2::coin` currency model
- [Sui Package Upgrades][] - Why a type's defining package address is stable
- [Move Type Tags][] - The `address::module::name` grammar and its canonical serialization

[CAIP-2]: ./caip2.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[RFC 3986]: https://www.rfc-editor.org/rfc/rfc3986#section-2.1
[Sui Docs]: https://docs.sui.io/
[Sui GraphQL RPC]: https://docs.sui.io/references/sui-graphql
[Sui JSON-RPC Migration]: https://docs.sui.io/develop/accessing-data/json-rpc-migration
[Sui Coin Standard]: https://docs.sui.io/standards/coin
[Sui Package Upgrades]: https://docs.sui.io/concepts/sui-move-concepts/packages/upgrade
[Move Type Tags]: https://move-book.com/reference/primitive-types/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
