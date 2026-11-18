---
namespace-identifier: mvx-caip19
title: MultiversX Namespace - Asset Specification
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

Every issued asset on MultiversX is an ESDT, and every ESDT is identified by a **token identifier**: an uppercase alphanumeric ticker, a hyphen, and six lowercase hexadecimal characters assigned at issuance.
`WEGLD-bd4d79` and `ASH-a642d1` are real mainnet examples.
Non-fungible, semi-fungible and Meta-ESDT instances extend that with a third segment, the instance nonce in hexadecimal: `CGEM-a75db0-01746c`.

The [CAIP-19][] `asset_reference` charset is `[-.%a-zA-Z0-9]{1,128}` and the `token_id` charset is `[-.%a-zA-Z0-9]{1,78}`.
**An ESDT identifier is already a strict subset of both**, and it is worth saying so explicitly rather than leaving it implicit.
The hyphen is in the charset, the ticker is `[A-Z0-9]`, the random suffix and the nonce are `[0-9a-f]`, and the whole identifier is at most 17 characters against a 128-character budget.
This profile therefore defines **no percent-encoding**, no truncation and no hashing: an `mvx` asset reference is byte-for-byte the string the chain and its APIs already print.
That is the opposite situation to Move-based chains, where a type tag's `::` and `_` must be escaped, and it is the main reason this profile can be short.

MultiversX treats fungible ESDTs, NFTs, SFTs and Meta-ESDTs as one token system differentiated by a `type` field rather than as separate identifier spaces, and a fungible ESDT is simply an ESDT whose instances all have nonce zero.
This profile follows that and defines a single `esdt` asset namespace.
The collection-versus-instance distinction that the third segment expresses is exactly the [CAIP-19][] `asset_type`-versus-`asset_id` distinction, so it is carried by the `token_id` rather than by a second namespace.

This profile was drafted by the maintainers of FAR, an open cross-reference between [CAIP-19][], CoinGecko and ISO 24165 identifiers, which needs a way to name 35 assets on this chain.
The authors do not represent the MultiversX ecosystem and offer this for its community to correct, adopt or replace.

## Syntax

After the [CAIP-2][] namespace and chain ID, a slash introduces an `asset_namespace` and an `asset_reference`.

### Asset Namespaces

| Namespace | Description | Reference Format |
| :--- | :--- | :--- |
| `slip44` | Native EGLD via the SLIP-0044 registry | `508` |
| `esdt` | Any issued ESDT | `{ticker}-{random}`; an instance nonce, where one exists, is the `token_id` |

### Token Identifier Requirements

A token identifier is the ticker chosen at issuance, a hyphen, and a six-character suffix.
The [MultiversX token documentation][MultiversX Tokens] states the two halves precisely: "Token Ticker: length between 3 and 10 characters alphanumeric UPPERCASE only", and "The random string starts with `-` and has 6 more random characters (3 bytes - 6 characters hex encoded)."

- The ticker MUST be preserved in uppercase and the suffix in lowercase.
- The suffix is exactly six lowercase hexadecimal characters and MUST NOT be trimmed or re-cased.
- The identifier MUST NOT be abbreviated to the ticker alone.

This grammar was checked against live data rather than taken from the documentation alone: 2000 consecutive fungible tokens and 500 consecutive collections returned by the public API all match `^[A-Z0-9]{3,10}-[0-9a-f]{6}$`, with no exceptions.

### Nonce Requirements

The `token_id` is the instance nonce, encoded exactly as the chain encodes it in the third segment of a native instance identifier: the nonce as a big-endian integer, minimal-length byte representation, hex-encoded in lowercase.

- The encoding is byte-aligned, so its length is always even and always at least two characters.
- Leading zeros within the final byte are significant: nonce 95340 is `01746c`, never `1746c`.
- The `token_id` MUST NOT be written in decimal.

Hexadecimal is mandated over decimal so that `reference + "-" + token_id` reproduces the native identifier by concatenation, with no arithmetic and no chance of a re-encoding mismatch.
The decimal nonce remains available from the API for display.

This too was checked live: for 1500 consecutive NFT, SFT and Meta-ESDT instances returned by the public API, the third segment is even-length lowercase hexadecimal and decodes to exactly the `nonce` field the API reports, in every case.

## RegEx

The RegEx validation strings are as follows.

```sh
asset_id:           asset_type + "/" + token_id
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           "mvx:" + ( "1" | "D" | "T" )      (as defined in [CAIP-2])

asset_namespace:    "slip44" | "esdt"

asset_reference:    slip44_ref | esdt_ref
slip44_ref:         "508"
esdt_ref:           ticker + "-" + random
ticker:             [A-Z0-9]{3,10}
random:             [0-9a-f]{6}

token_id:           ([0-9a-f]{2})+                    (nonce, big-endian, minimal bytes)
```

An `esdt_ref` is at most 17 characters against the 128-character `asset_reference` limit, and a nonce is a `uint64`, so its `token_id` is at most 16 characters against the 78-character limit.
Neither limit can be approached, let alone reached, so this namespace needs no documented truncation.

## Semantics

### Native EGLD

EGLD is the native coin: it pays gas, it is staked, and it is not an ESDT.
It is identified through the SLIP-0044 registry, where line 541 of [SLIP-0044][] reads `| 508 | EGLD | MultiversX |`.

```
mvx:1/slip44:508
```

Wrapped EGLD is a different asset, an ordinary fungible ESDT issued by a smart contract, and takes an `esdt` identifier.
See `Collisions and Security Considerations` for the pseudo-identifier `EGLD-000000`, which MUST NOT be used here.

### Fungible ESDT

A fungible ESDT has a supply, a decimal count and no per-instance state.
All of its units carry nonce zero.

A fungible ESDT is an `asset_type` and MUST be written **without** a `token_id`.
Nonce zero MUST NOT be spelled as `/00` or `/0`, because that would give one asset two identifiers.

```bash
curl https://api.multiversx.com/tokens/WEGLD-bd4d79
# {"type":"FungibleESDT","identifier":"WEGLD-bd4d79","name":"WrappedEGLD",
#  "ticker":"WEGLD","decimals":18, ...}
```

### NFT, SFT and Meta-ESDT

These three types share one identifier shape: a **collection** identifier plus an instance **nonce**.
The collection identifier is itself a `ticker-random` string, indistinguishable in form from a fungible ESDT identifier, and the API exposes it as the `collection` field of every instance.

The `asset_type` is the `esdt` namespace plus the collection identifier, and names the collection.
The `asset_id` appends the nonce as the `token_id`, and names one instance.

```
asset_type: mvx:1/esdt:{collection}
asset_id:   mvx:1/esdt:{collection}/{nonce}
```

The three types differ in what an instance holds, not in how it is named.

| API `type` | Instance supply | Decimals | Example |
| :--- | :--- | :--- | :--- |
| `NonFungibleESDT` | exactly 1 | 0 | `CGEM-a75db0-01746c` |
| `SemiFungibleESDT` | 1 or more, interchangeable within the nonce | 0 | `VESTING-72b753-03f8` |
| `MetaESDT` | fractional, with decimals | as issued | `XMEX-fda355-2f` |

Because SFT and Meta-ESDT instances are quantifiable, an `asset_id` in this namespace does not always denote something non-fungible in the strict sense.
It denotes one instance, which may be semi-fungible.
This is the same role `token_id` plays for ERC-1155 and is consistent with [CAIP-19][].

A consumer that needs to know which of the three it is holding MUST resolve the `type` field on chain; the identifier does not carry it.

```bash
curl https://api.multiversx.com/nfts/XMEX-fda355-2f
# {"identifier":"XMEX-fda355-2f","collection":"XMEX-fda355","nonce":47,
#  "type":"MetaESDT","ticker":"XMEX","decimals":18, ...}
```

## Examples

```sh
# Native EGLD on mainnet
mvx:1/slip44:508

# Wrapped EGLD, a fungible ESDT (decimals 18, name "WrappedEGLD")
mvx:1/esdt:WEGLD-bd4d79

# AshSwap governance token, a fungible ESDT (decimals 18, name "AshSwap")
mvx:1/esdt:ASH-a642d1

# An NFT collection
mvx:1/esdt:CGEM-a75db0

# One NFT in it -- "Uncommon Chipped Ruby", nonce 95340 = 0x01746c
mvx:1/esdt:CGEM-a75db0/01746c

# One SFT instance -- "Pulsar.Money Vesting", nonce 1016 = 0x03f8
mvx:1/esdt:VESTING-72b753/03f8

# One Meta-ESDT instance -- xMEX, nonce 47 = 0x2f, decimals 18
mvx:1/esdt:XMEX-fda355/2f

# Native EGLD on devnet
mvx:D/slip44:508

# Wrapped EGLD on devnet -- same ticker, different issuance, different suffix
mvx:D/esdt:WEGLD-a28c59
```

### Round Trip

There is no encoding step to undo, which is the point.

```sh
# 1. input, as returned by https://api.multiversx.com/nfts/CGEM-a75db0-01746c
CGEM-a75db0-01746c

# 2. split on the last hyphen into collection and nonce
CGEM-a75db0   +   01746c

# 3. prepend the CAIP-2 chain ID and the asset namespace
mvx:1/esdt:CGEM-a75db0/01746c

# 4. to reverse, replace the last "/" with "-"
CGEM-a75db0-01746c

# 5. the nonce in decimal, for display only
int("01746c", 16) == 95340   # matches the API's "nonce" field
```

Step 2 splits on the **last** hyphen, never the first, because a ticker may itself contain digits but never a hyphen; the identifier has exactly two hyphens for an instance and exactly one for a collection.
Every character in step 3 is already inside `[-.%a-zA-Z0-9]`, so no octet is escaped anywhere in this profile.

## Collisions and Security Considerations

### A ticker is not an identifier

The ticker alone is not unique and was never intended to be.
The [MultiversX token documentation][MultiversX Tokens] is explicit: "Anyone else is free to create a new token with the same token name and the same token ticker", and the six-character random suffix exists solely to separate them.

This is live on mainnet, not hypothetical.
`WXMEX-794dbd` and `WXMEX-19a835` are two distinct Meta-ESDT collections, both with ticker `WXMEX` and both named `WrappedXMEX`.
Any system that keys on the ticker, or that renders only the ticker to a user approving a transfer, merges them.
The full identifier MUST be carried end to end, and a user-facing display SHOULD show the suffix.

### `EGLD-000000` is not an ESDT

The public API answers `GET /tokens/EGLD-000000` with a record that looks like a fungible ESDT and is not one.
Its own description says what it is: "EGLD-000000 is the identifier used when wanting to transfer EGLD via a MultiESDTNFTTransfer."
It is a transfer-encoding convention for the native coin, with zero supply, zero minted and no issuer.

Native EGLD MUST be identified as `mvx:1/slip44:508`.
`mvx:1/esdt:EGLD-000000` MUST NOT be emitted, and a consumer that receives it SHOULD map it to `slip44:508` rather than treat it as a distinct asset.
Note that `EGLD-000000` *does* satisfy this profile's `esdt_ref` grammar — `EGLD` is a legal ticker and `000000` is legal hexadecimal — so no validator will reject it.
The exclusion has to be stated as a rule because syntax cannot express it.

### Nonce encoding is where an implementation will go wrong

Three distinct mistakes produce a wrong or duplicate identifier, and none of them will fail a naive length check.

- Stripping the leading zero of the final byte: `1746c` instead of `01746c`.
- Writing the nonce in decimal: `95340` instead of `01746c`, which is also a syntactically valid `token_id` and so will not be rejected.
- Uppercasing the hexadecimal: `01746C`, a second spelling of one instance.

[CAIP-19][] references and token IDs are case-sensitive and are compared as strings, so each of these is a silent duplicate rather than an error.

### Case sensitivity across the whole identifier

The ticker is uppercase and the suffix is lowercase, and both MUST be preserved exactly.
`wegld-bd4d79` is not `WEGLD-bd4d79`.
A pipeline that upper- or lower-cases identifiers for storage will produce references that no other implementation recognizes.

### The same identifier can exist on more than one network

Identifiers are assigned per network, so nothing prevents mainnet and devnet from holding tokens whose identifiers coincide, and tickers certainly recur: mainnet's wrapped EGLD is `WEGLD-bd4d79` while devnet's is `WEGLD-a28c59`.
The [CAIP-2][] chain ID is the only thing separating them, and an `esdt` reference MUST NOT be moved between chain IDs.

### Identifiers are stable, token properties are not

The identifier is fixed at issuance and never changes.
Everything else can: a token issued with `canUpgrade` set may later have its properties altered by its owner, and `canMint`, `canBurn`, `canPause` and `canWipe` determine whether the issuer can inflate, freeze or destroy a holder's balance.
`WEGLD-bd4d79` currently reports `canUpgrade`, `canMint`, `canBurn` and `canChangeOwner` all true.
A [CAIP-19][] identifier asserts identity, not safety, and consumers SHOULD resolve these properties rather than infer them.

## Backwards Compatibility

There is no prior asset-identifier convention in the `mvx` namespace, so this profile introduces no breaking change.

More usefully, there is nothing to be compatible *with* at the string level: the `esdt` reference is the native identifier unchanged, so a [CAIP-19][] identifier can be split back into a form the MultiversX API accepts with a single substitution, and an existing MultiversX-native database needs no re-encoding to adopt it.

The MultiversX token model has been extended over time, from fungible ESDT to NFT, SFT and Meta-ESDT, without changing the identifier grammar.
The `esdt` namespace inherits that: a future instance type that reuses the `ticker-random[-nonce]` shape is representable here without a new namespace.

## References

- [CAIP-2][] - Blockchain ID Specification, and the `mvx` chain IDs used above
- [CAIP-19][] - Asset Type and Asset ID Specification
- [SLIP-0044][] - Registered coin types, line 541 for MultiversX
- [MultiversX Tokens][] - The ticker, random-suffix and nonce grammar quoted above
- [MultiversX NFT Tokens][] - NFT, SFT and Meta-ESDT issuance and the instance nonce
- [MultiversX REST API][] - The interface used to verify every identifier in this document
- [MultiversX Specifications][] - Protocol-level ESDT specifications

[CAIP-2]: ./caip2.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[MultiversX Tokens]: https://docs.multiversx.com/tokens/fungible-tokens/
[MultiversX NFT Tokens]: https://docs.multiversx.com/tokens/nft-tokens/
[MultiversX REST API]: https://docs.multiversx.com/sdk-and-tools/rest-api/
[MultiversX Specifications]: https://github.com/multiversx/mx-specs

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
