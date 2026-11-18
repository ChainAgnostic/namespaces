---
namespace-identifier: casper-caip19
title: Casper Namespace - Asset Specification
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

Casper has a native token, CSPR, and two token standards layered on top of contracts: [CEP-18][] for fungible tokens and [CEP-78][] for non-fungible ones.
Three asset namespaces cover all of it, and this profile stays short because there is not much more to say.

The one decision that matters is *which* hash identifies a token contract.
A Casper contract is deployed inside a **contract package**, and the package holds a list of versions each mapping to a different **contract hash**; upgrading a token mints a new contract hash and disables the old one, while the package hash never changes.
Wrapped CSPR on mainnet is a live example: package `8df5d26790e18cf0404502c62ce5dc9025800ad6975c97466e20506c39c505b6` currently lists three versions, of which the first two are disabled, and its current contract hash is `aeda05e72070084e21677852d6b45e1a2c892f0884fb1c04cbfc62ba53d9fad1`.
An identifier built on the contract hash would therefore have named a different string before that upgrade and will name another one after the next, for what holders and the ledger both regard as one asset.
This profile uses the **contract package hash**, which is also what `cspr.live` uses in its URLs and what wallets display.

This profile was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a way to name 1 asset on Casper.
The authors do not represent the Casper ecosystem and offer this for its community to correct, adopt or replace.

## Syntax

After the [CAIP-2][] namespace and chain id, a slash introduces an `asset_namespace` and an `asset_reference`.
For non-fungibles a further slash introduces a `token_id`, as defined in [CAIP-19][].

### Asset Namespaces

| Namespace | Description                              | Reference format                                     |
| :-------- | :--------------------------------------- | :--------------------------------------------------- |
| `slip44`  | Native CSPR via [SLIP-0044][]            | `506`, Casper's registered coin type                  |
| `cep18`   | A [CEP-18][] fungible token              | Contract package hash, 64 lowercase hex digits        |
| `cep78`   | A [CEP-78][] non-fungible collection     | Contract package hash; `token_id` identifies the item |

### Contract package hash

The reference for `cep18` and `cep78` is the contract package hash as 64 lowercase hexadecimal digits.
The `hash-` prefix that Casper's own `Key` serialisation carries is **not** part of the reference and MUST be stripped, since it is constant and conveys nothing.
The hash MUST NOT be the contract hash of a particular version, for the reason given in the Rationale.

### Token id

[CEP-78][] fixes a collection's `identifier_mode` at installation and never changes it, so a collection's `token_id` form is stable even though the form differs between collections:

- `Ordinal` mode: a `u64`, written in base ten with no leading zeros.
- `Hash` mode: by default the base16 blake2b hash of the item's metadata, 64 lowercase hex digits; optionally a custom string chosen at mint.

A custom `Hash`-mode identifier is an arbitrary string and so is the only place in this profile that can contain an octet outside the `token_id` charset.
Such an identifier MUST be percent-encoded: encode the string as UTF-8, then replace every octet that is not in `[-.A-Za-z0-9]` with `%` followed by its two uppercase hexadecimal digits, `%` itself included as `%25`.
Percent-encoding expands, so a custom identifier whose encoded form exceeds 78 characters cannot be expressed as a [CAIP-19][] `token_id` and an implementation that meets one MUST fail rather than truncate.

## RegEx

The RegEx validation strings are as follows:

```sh
asset_id:           asset_type + "/" + token_id
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           namespace + ":" + blockchain_id (as defined in [CAIP-2])

asset_namespace:    "slip44" | "cep18" | "cep78"

asset_reference:    slip44_ref | package_ref
slip44_ref:         "506"
package_ref:        [0-9a-f]{64}

token_id:           ordinal_id | hash_id | custom_id
ordinal_id:         0|[1-9][0-9]{0,19}
hash_id:            [0-9a-f]{64}
custom_id:          ([-.A-Za-z0-9]|%[0-9A-F]{2}){1,78}
```

## Semantics

### Native CSPR

CSPR is the native token of the network, used for gas and for staking, and is identified with coin type `506` as registered in [SLIP-0044][].
It is held in purses rather than in a token contract, and it has no contract package hash.

### CEP-18 fungible tokens

`cep18` names a fungible token implementing the [CEP-18][] standard, identified by its contract package hash.
The token's `name`, `symbol` and `decimals` are named keys on the package's current contract version and are display metadata only: they are chosen freely by the deployer, are not unique, and MUST NOT be used to construct or to match an identifier.

### CEP-78 non-fungible tokens

`cep78` names a collection implementing the [CEP-78][] standard, identified by its contract package hash.
Without a `token_id` the identifier is an `asset_type` naming the collection as a class; with a `token_id` it is an `asset_id` naming one item, in whichever identifier mode the collection was installed with.

Casper's earlier NFT standard, CEP-47, is not covered by this profile.
Contracts implementing it remain on chain, and an additional asset namespace should be registered for them if the community needs their identifiers.

## Examples

```sh
# Native CSPR on Casper Mainnet
casper:casper/slip44:506

# Native CSPR on Casper Testnet
casper:casper-test/slip44:506

# Wrapped CSPR (WCSPR), a CEP-18 token on Casper Mainnet
casper:casper/cep18:8df5d26790e18cf0404502c62ce5dc9025800ad6975c97466e20506c39c505b6

# Staked CSPR (sCSPR), a CEP-18 token on Casper Mainnet
casper:casper/cep18:a4f6d5e6ce046b7e8e32356b1395b69573ba2481fc86b85f9183f149366b60f1

# Shiboo (SHIBOO), a CEP-18 token on Casper Mainnet
casper:casper/cep18:94b4ce46711aa9a778bf472dd257f25588e5d326623a125c5d1d8ceec7455b89

# A CEP-78 collection, as a class, and item 42 of it in Ordinal identifier mode
casper:casper/cep78:<package_hash>
casper:casper/cep78:<package_hash>/42

# The same collection in Hash identifier mode, addressing one item by the
# base16 blake2b hash of its metadata
casper:casper/cep78:<package_hash>/<metadata_blake2b_hash>

# A Hash-mode collection with a custom string identifier "Token #7",
# percent-encoded because a space and a "#" are outside the token_id charset
casper:casper/cep78:<package_hash>/Token%20%237
```

The `cep18` package hashes above were read from Casper Mainnet global state.
No concrete `cep78` package hash is given: at the time of writing the authors could not reach an index of mainnet CEP-78 collections to cite one from, so the `<package_hash>` placeholder marks a form that has not been verified against a live collection, and it should be replaced with a real collection before this profile is finalised.

## Collisions and Security Considerations

### Package hash versus contract hash

The two hashes are indistinguishable as strings — both are 64 hex digits — so a producer that emits a contract hash where a package hash is expected creates a well-formed identifier that resolves to nothing, or, after a later upgrade, to a disabled contract version.
Consumers SHOULD verify that a `cep18` or `cep78` reference resolves to a `ContractPackage` rather than to a `Contract`, which a single `query_global_state` on the `hash-` key answers.

### Chain id, not genesis hash

As the [CAIP-2][] profile for this namespace notes, the Casper chain id is the human-readable chainspec name and is not the chain's genesis hash.
Every identifier here inherits that, so `casper:casper` and `casper:casper-test` are distinguished by a name an operator chose, and an asset identifier is only as trustworthy as the chain id in front of it.

### Metadata is not an identifier

Two different CEP-18 packages may both call themselves `USDC`, and a `Hash`-mode CEP-78 identifier derived from metadata will collide for two items minted with byte-identical metadata in the same collection.
The first is a reason never to match on symbol; the second is a property of CEP-78's content-addressed mode that this profile inherits and cannot repair.

## Backwards Compatibility

No [CAIP-19][] profile previously existed for this namespace, so no existing identifier changes meaning.
The [CAIP-2][] and [CAIP-10][] profiles for `casper` are unaffected.

## References

- [CAIP-19][]: Asset Type and Asset ID Specification
- [SLIP-0044][]: Registered coin types, where Casper is coin type `506`
- [CEP-18][]: The Casper fungible token standard
- [CEP-78][]: The Casper enhanced NFT standard, including its `NFTIdentifierMode` modality
- [Casper Docs site][]: Contract packages, versions and global state

[CAIP-2]: ./caip2.md
[CAIP-10]: ./caip10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[CEP-18]: https://github.com/casper-ecosystem/cep18
[CEP-78]: https://github.com/casper-ecosystem/cep-78-enhanced-nft
[Casper Docs site]: https://docs.casper.network/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
