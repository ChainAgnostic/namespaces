---
namespace-identifier: iota-caip19
title: IOTA Namespace - Asset Specification
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

### Which IOTA this profile is for

IOTA has had two incompatible asset models, and a CAIP-19 profile has to say which one it describes.
Under the Stardust protocol, tokens were foundry outputs identified by a 38-byte foundry ID; under IOTA Rebased, IOTA is an object-based Move network and a token is a Move coin type.
These produce entirely different identifiers, so guessing would have been unacceptable.

The question is settled by this namespace's own [CAIP-2][] profile, which defines the chain reference as "the first 4 hex-encoded bytes of the genesis checkpoint digest (e.g. `6364aad5` for mainnet)" and resolves it through `iotax_getChainIdentifier`.
Checkpoint digests and that RPC exist only on the Move network.
Querying `https://api.mainnet.iota.cafe` confirms it directly: `iota_getChainIdentifier` returns `6364aad5`, matching the profile's mainnet example, and the same node answers `iotax_getCoinMetadata` for `0x2::iota::IOTA` with 9 decimals.
(In passing: that node answers `iota_getChainIdentifier` but returns `-32601 Method not found` for the `iotax_getChainIdentifier` spelling the [CAIP-2][] profile gives, which that profile's authors may want to correct.)

**This profile is for the Move network**, and no conditional drafting is needed.
The IOTA EVM chain (`eth_chainId` 0x2276, decimal 8822) is a separate execution environment addressed under `eip155`, and its ERC-20s are not in this namespace.

### The `::` problem

A Move type tag is `address::module::struct`, and `:` is one of the characters [CAIP-19][] explicitly excludes from `asset_reference`.
Move module and struct names also permit `_`, which is likewise outside the charset — and this is not hypothetical: IOTA mainnet carries live coins such as `…::demo_coin::DEMO_COIN` and the migrated Stardust foundries, whose module names are generated in the form `foundry_y1ti9yf`.

CAIP-19 already names the remedy, recommending "URL encoding (% + 2-character codes, canonically capitalized) as per Section 2 of RFC 3986" for exactly this case, and `%` is in the charset.
This profile therefore percent-encodes the type tag and defines precisely which octets are encoded.
The same treatment should apply to Sui, whose namespace has a chain-ID profile but no asset profile yet; the two ecosystems share the Move type-tag grammar and ought not diverge here.
This profile therefore uses namespace names (`coin`, `object`), an address normalization rule and an escape table that a Sui asset profile could adopt unchanged, so that one Move identifier does not acquire two spellings depending on which chain it is on.

This profile was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a way to name 4 assets on this chain.
The authors do not represent the IOTA ecosystem and offer this for its community to correct, adopt or replace.

## Syntax

After the [CAIP-2][] chain ID, a slash defines an `asset_namespace` and an `asset_reference`.

### Asset Namespaces

| Namespace | Description | Reference Format | `token_id` |
| :--- | :--- | :--- | :--- |
| `slip44` | Native IOTA via [SLIP-0044][] | `4218` (IOTA's coin type) | never |
| `coin` | A Move coin, i.e. the `T` of a `0x2::coin::Coin<T>` | percent-encoded type tag of `T` | never |
| `object` | A Move object, i.e. an IOTA non-fungible | percent-encoded type tag of the object's struct | **required** |

### Type tag canonicalization

Before encoding, a type tag **MUST** be normalized:

1. The address is written as `0x` followed by the full 32-byte address in lowercase hex, **zero-padded to 64 digits**.
   The node accepts `0x2::iota::IOTA` and `0x0000…0002::iota::IOTA` interchangeably — both were confirmed to resolve to the same coin metadata — but only the padded form is unique, so it is the canonical one.
   Consumers **MUST** accept abbreviated addresses on input and left-pad them before comparison.
2. Module and struct names are copied verbatim.
   Move identifiers are case-sensitive and `0x2::iota::iota` is not a type; the RPC returns `null` for it.

### Percent-encoding

Exactly five characters are encoded, with uppercase hex digits per RFC 3986:

| Character | Encoded | Where it occurs |
| :--- | :--- | :--- |
| `:` | `%3A` | the two `::` separators |
| `_` | `%5F` | module and struct names |
| `<` | `%3C` | opening a generic type argument list |
| `>` | `%3E` | closing one |
| `,` | `%2C` | separating generic type arguments |

Everything else in a normalized type tag — `0`-`9`, `a`-`z`, `A`-`Z`, `x` — is already in the charset and **MUST NOT** be encoded.
Decoding is plain percent-decoding and round-trips exactly.

```
0xd3b63e603a78786facf65ff22e79701f3e824881a12fa3268d62a75530fe904f::vusd::VUSD
  -> 0xd3b63e603a78786facf65ff22e79701f3e824881a12fa3268d62a75530fe904f%3A%3Avusd%3A%3AVUSD
  -> 0xd3b63e603a78786facf65ff22e79701f3e824881a12fa3268d62a75530fe904f::vusd::VUSD
```

### Object ID

An `object` `token_id` is the object's ID: `0x` followed by 64 lowercase hex digits, 66 characters, within the 78-character `token_id` limit.

## RegEx

```sh
asset_id:           asset_type | asset_type + "/" + token_id
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           "iota:" + blockchain_id (as defined in [CAIP-2])

asset_namespace:    "slip44" | "coin" | "object"

asset_reference:    slip44_ref | encoded_type_tag
slip44_ref:         "4218"
encoded_type_tag:   address + "%3A%3A" + identifier + "%3A%3A" + identifier [ generics ]
address:            0x[0-9a-f]{64}
identifier:         [A-Za-z]([A-Za-z0-9]|%5F)*
generics:           "%3C" encoded_type_tag ("%2C" encoded_type_tag)* "%3E"

token_id:           0x[0-9a-f]{64}
```

## Semantics

### Native Asset (IOTA)

The native token is identified with the `slip44` namespace and coin type `4218`, registered in [SLIP-0044][] as `| 4218 | IOTA | IOTA |`.
It has 9 decimals and a total supply of 4,981,117,335,291,855,045 base units, and it pays gas.

Example: `iota:mainnet/slip44:4218`

The same asset also has a Move coin type, `0x2::iota::IOTA`, and so is expressible as a `coin` reference.
`slip44:4218` is the canonical form and producers **MUST** emit it for the native token; the `coin` form is listed in the examples only so that a consumer normalizing third-party data knows what it is looking at.

### Move Coins

A `coin` asset type names the phantom type parameter `T` of `0x2::coin::Coin<T>`, which is what `iotax_getCoinMetadata`, `iotax_getTotalSupply` and `iotax_getAllBalances` all key on.
The reference names `T` itself, never the wrapper: `0x2::coin::Coin<…>` **MUST NOT** appear in a `coin` reference.

Metadata (symbol, decimals, name) lives in a `CoinMetadata` object created at publication and is resolved, not encoded:

```json
{"jsonrpc":"2.0","id":1,"method":"iotax_getCoinMetadata",
 "params":["0xd3b63e603a78786facf65ff22e79701f3e824881a12fa3268d62a75530fe904f::vusd::VUSD"]}
// {"decimals":6,"name":"Virtue USD","symbol":"VUSD", ...}
```

### Non-Fungible Objects

IOTA has no single NFT standard; an NFT is a Move object with `key` ability and, usually, a `display` definition.
Its Move *type* is the closest analogue of an ERC-721 contract and takes the `asset_type` position; its *object ID* is unique chain-wide and takes the `token_id` position.

```
# a migrated Stardust NFT, type 0x107a::nft::Nft
iota:mainnet/object:0x000000000000000000000000000000000000000000000000000000000000107a%3A%3Anft%3A%3ANft/0x0ec1ae658596b7e44adf3c7f6c0cb384ed1947deae3f12a6c8e1481fd322c3dd
```

Because a Move type is not a per-collection deployment — one generic `Nft` type can back many unrelated collections — the `asset_type` alone is weak as a collection identifier, and consumers **SHOULD NOT** treat two NFTs sharing a type as belonging to one collection.

### Known limitation: generic types can exceed 128 characters

`asset_reference` is capped at 128 characters.
A non-generic coin type usually fits: the VUSD reference above is 86 characters, though the migrated foundry coin below is already 112 and a package with long module and struct names would pass 128 on its own.
A *generic* type does not fit at all.
The live IOTA type `0x107a::nft_output::NftOutput<0x2::iota::IOTA>`, normalized and encoded, is 191 characters and is unrepresentable under this profile.
Liquidity-pool share coins parameterised by two user-published coin types are worse.

This is a real gap and this profile does not paper over it: implementations **MUST** fail rather than truncate, abbreviate the address, or substitute a hash.
Three resolutions are plausible — permit abbreviated addresses for the reserved framework addresses (`0x1`, `0x2`, `0x3`, `0x107a`), which brings the example above to 68 characters; address such assets by their `CoinMetadata` object ID instead; or raise the CAIP-19 limit.
The authors have no standing to pick one and flag it for the IOTA community and the CASA editors.

## Examples

```sh
# Native IOTA on mainnet -- canonical form
iota:mainnet/slip44:4218

# The same asset written as a Move coin type (0x2::iota::IOTA) -- non-canonical
iota:mainnet/coin:0x0000000000000000000000000000000000000000000000000000000000000002%3A%3Aiota%3A%3AIOTA

# Virtue USD (VUSD), 6 decimals, the Virtue protocol stablecoin
iota:mainnet/coin:0xd3b63e603a78786facf65ff22e79701f3e824881a12fa3268d62a75530fe904f%3A%3Avusd%3A%3AVUSD

# Twin (TWIN), 9 decimals
iota:mainnet/coin:0xedfde36ab409ebb6f543d6ac54de142411fca335e9dfc1624af53c592c07cc4f%3A%3Atwin%3A%3ATWIN

# A coin whose module and struct names contain underscores
iota:mainnet/coin:0x182d011ea38737ad0217e09efa223c32ed05013efd9775a06a872786a568a380%3A%3Ademo%5Fcoin%3A%3ADEMO%5FCOIN

# A Stardust-migrated foundry token, module name generated as foundry_<suffix>
iota:mainnet/coin:0xd6eda59c9891925ed0c5825a86cd46b892a374dace56db569ae76f4846a941fd%3A%3Afoundry%5Fy1ti9yf%3A%3AFOUNDRY%5FY1TI9YF

# A non-fungible object: type 0x107a::nft::Nft, object 0x0ec1ae65...
iota:mainnet/object:0x000000000000000000000000000000000000000000000000000000000000107a%3A%3Anft%3A%3ANft/0x0ec1ae658596b7e44adf3c7f6c0cb384ed1947deae3f12a6c8e1481fd322c3dd

# Native IOTA on testnet
iota:testnet/slip44:4218
```

## Security Considerations

### Module and struct names are not unique

A Move type is unique because of its package address, and nothing else about it is.
IOTA mainnet currently carries coins of type `…::btc::BTC` published by at least three distinct packages — `0x49baadcb29843f1a690455946bbd243eb9d707e4253d6230b94afe5db7ac69c0`, `0x6af1002e9693764e59cd172194d63b753a01e6d33b5607578353957715c815a9` and `0xb3d9b02ae559b4255f4324b5d1bbb4daee0d9599919b1a9a502267146509c64f` — and three unrelated `…::katzo::KATZO` coins from three more.
A single account holds 2,100,000,000,000,000 base units of the first of those, which reads as 21,000,000 BTC at eight decimal places to anyone matching on the struct name.
Only the full type tag, address included, may be treated as identity, and a consumer **MUST NOT** resolve an IOTA asset by symbol, struct name, or module name.

### Address abbreviation is a homograph surface

`0x2` and `0x0000…0002` are the same address; `0x20` is not.
Because IOTA tooling routinely prints abbreviated addresses, an identifier copied from a UI can be ambiguous in a way the padded canonical form is not.
Producers **MUST** pad; consumers **MUST** pad before comparing, and **MUST NOT** compare abbreviated forms lexically.

### Two identifiers for the native token

`slip44:4218` and the `0x2::iota::IOTA` coin form denote the same asset.
Consumers that ingest data from several sources **SHOULD** normalize the `coin` form to `slip44:4218` rather than carrying both, which would otherwise double-count the largest balance in any portfolio.

### Chain reference stability

The [CAIP-2][] profile's `testnet` and `devnet` aliases survive network resets while the underlying genesis checkpoint digest does not.
An asset identifier inherits that: `iota:testnet/coin:…` may refer to a package that no longer exists after a reset.
Mainnet is unaffected.

## Backwards Compatibility

Stardust native tokens were not carried over as foundry IDs.
Migration wrapped each foundry as a Move coin with a generated module name of the form `foundry_<suffix>`, so a Stardust foundry ID has no direct CAIP-19 form in this namespace and mapping one requires the migration record, not a string transformation.
Stardust NFT outputs were migrated to `0x107a::nft_output::NftOutput<…>` and `0x107a::nft::Nft` objects, which is why the length limitation above is a live concern rather than a theoretical one.

## References

- [IOTA Docs][] - developer documentation for the Move-based IOTA network
- [IOTA Coin Standard][] - the `0x2::coin` module and the `Coin<T>` / `CoinMetadata` model
- [IOTA JSON-RPC][] - `iota_getChainIdentifier`, `iotax_getCoinMetadata`, `iotax_getTotalSupply`, `iotax_getAllBalances`
- [IOTA Stardust Migration][] - how foundry and NFT outputs became Move objects
- [RFC 3986][] - percent-encoding, as recommended by CAIP-19
- [SLIP-0044][] - registered coin types, `4218` for IOTA
- [CAIP-2][] - the IOTA chain ID profile in this namespace
- [CAIP-19][] - Asset Type and Asset ID Specification

[CAIP-2]: ./caip2.md
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[IOTA Docs]: https://docs.iota.org/
[IOTA Coin Standard]: https://docs.iota.org/developer/standards/coin
[IOTA JSON-RPC]: https://docs.iota.org/references/iota-api
[IOTA Stardust Migration]: https://docs.iota.org/developer/stardust/migration-process
[RFC 3986]: https://www.rfc-editor.org/rfc/rfc3986#section-2.1

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
