---
namespace-identifier: keeta-caip10
title: Keeta - Account ID Specification
author: ["@sc4l3r", "@xescure"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/183
status: Draft
type: Standard
created: 2026-04-27
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

_For context, see the [CAIP-10][] specification._

## Introduction

Every [account][accounts] on a Keeta network -- whether it is a key-pair-backed account (ECDSA secp256k1/r1, or Ed25519), a token, a storage account, a network account, or a multisig -- is addressed from a single shared address space.
A **keyed account** holds a private key and signs its own blocks.
A **generated account**, also called an identifier account -- a token, storage account, network account, or multisig -- has no private key, and its blocks are signed by a keyed account holding permission over it.
A Keeta address is the account's public key itself with a type byte and a five-byte checksum, all of which is then encoded as base32.
The address alone reveals the account type and signature algorithm.

The same key pair produces the same address on every Keeta network, but account state is per network, so `keeta:21378:<address>` and `keeta:1413829460:<address>` are different accounts.
Generated accounts exist only on the network where they were created (see [Semantics](#semantics)).

Keeta renders every address with the display prefix `keeta_`.
This profile uses the **bare base32 body**, without the prefix, as the [CAIP-10][] `account_address`.

## Specification

### Semantics

The inputs are:

- A Keeta network identifier, as defined in the [Keeta CAIP-2 Profile][CAIP-2 Profile], identifying which network the account lives on.
- A Keeta address as rendered by the SDK, `keeta_<body>`, returned by `account.publicKeyString.toString()` and accepted by `Account.fromPublicKeyString()`.

Only the body is used; the display prefix is discarded (see [Syntax](#syntax)).

The body is the [RFC 4648][rfc4648] base32 encoding, lowercase and without padding, of the following byte sequence:

```
type || key || SHA3-256(type || key)[0..5]
```

- `type` is one byte identifying the account kind: `0` ECDSA secp256k1, `1` Ed25519, `2` network account, `3` token, `4` storage account, `6` ECDSA secp256r1, `7` multisig; the value `5` is unassigned.
- `key` is the 33-byte compressed public key for ECDSA accounts, the 32-byte public key for Ed25519 accounts, or a 32-byte identifier for generated accounts.
- The last five bytes are a checksum over the preceding bytes.

As of `keetanet-client` version `0.18.4` the body is 63 characters for ECDSA accounts and 61 characters for all others.
Keeta may introduce further signing algorithms; the SDK is the authoritative source for the set of type bytes and for encoding and decoding (see [Resolution Mechanics](#resolution-mechanics)).

A keyed address is a valid recipient on any Keeta network before any block has been published to its chain.
A generated account is created by a [`CREATE_IDENTIFIER` operation][generate-identifier], and its identifier is derived from the creating account, the hash of the creating account's previous block on that network, and the index of the operation within that block.
The network account is derived from the network identifier alone, and the base token from the network account.

#### Canonicalization

A Keeta address is **case-insensitive**: per RFC 4648, two base32-encoded bodies that differ only in letter case decode to the same byte sequence and therefore identify the same account.
For [CAIP-10][] purposes the canonical form is **all-lowercase**, and producers MUST lowercase the body before emitting a CAIP-10 string.
An uppercase or mixed-case body does not match the syntax in this profile; consumers MAY accept one by lowercasing it before validation, in which case the lowercased form identifies the same account and SHOULD be the form used as a cache or lookup key.

### Syntax

A Keeta [CAIP-10][] account identifier MUST take the form:

```
keeta:<network>:<address>
```

Where:

- `keeta` is the namespace.
- `<network>` is a Keeta network identifier as defined by the [Keeta CAIP-2 Profile][CAIP-2 Profile].
- `<address>` is the body of the Keeta public key string, **without** the `keeta_` display prefix, in lowercase.

To produce `<address>` from an address as rendered by the SDK, remove the display prefix up to and including the `_` and lowercase the remainder.
To pass `<address>` to the SDK, prepend `keeta_`.

The `<address>` segment MUST match:

```
^[a-z2-7]+$
```

A regex match is necessary but not sufficient for checking address validity as it does not verify the type byte, the checksum, or the length.
Implementations MUST validate addresses using the Keeta SDK or by following the steps in [Resolution Mechanics](#resolution-mechanics).

### Resolution Mechanics

To validate a Keeta CAIP-10 identifier:

1. Split on `:` and verify the namespace is `keeta`.
2. Validate `<network>` against the [Keeta CAIP-2 Profile][CAIP-2 Profile].
3. Lowercase `<address>` to obtain its canonical form; see [Canonicalization](#canonicalization).
4. Prepend `keeta_` and decode the result using the Keeta public-key-string codec; verify the type byte and checksum.
5. Optionally, query a node on the indicated network to confirm the account exists and to retrieve its info:

```ts
import * as KeetaNet from "@keetanetwork/keetanet-client";

const address = "aabfo65nbz4toez4ouzit3ej5elpcjnatv6p6vxtgj5gj4x4cbs3nkytnpniyhi";
const account = KeetaNet.lib.Account.fromPublicKeyString(`keeta_${address}`);
const client = KeetaNet.Client.fromNetwork("test");
const { info } = await client.getAccountInfo(account);
```

Implementations SHOULD validate the checksum by round-tripping through `Account.fromPublicKeyString()` before treating the identifier as well-formed.

Implementations SHOULD use the methods of a Keeta SDK (e.g. `account.isToken()`, `account.isStorage()`) to determine the type of an account.

Note that account _existence_ is not required for a CAIP-10 string to be valid; a keyed address may be a valid recipient before any block has been published to its chain (see [Semantics](#semantics)).

## Rationale

The `keeta_` prefix is omitted because `_` is not a permitted character in a [CAIP-10][] `account_address`, and because the `keeta:` namespace segment already identifies the ecosystem.
The prefix is not part of the encoded bytes or the checksum, so the body alone identifies the account.

The resulting form fits comfortably within the [CAIP-10][] `account_address` length budget of 128 characters: the body is currently 63 characters for compressed ECDSA secp256k1/r1 keys and 61 characters for Ed25519 and generated accounts.
The syntax does not fix these lengths, so a signing algorithm added to Keeta is usable under this profile as soon as the SDK supports it; only implementations that handle accounts of the new kind need to update.

### Backwards Compatibility

This is the first [CAIP-10][] specification for the `keeta` namespace, so there are no legacy identifiers to support.

## Test Cases

Valid (test network, `1413829460`):

```
# Keyed secp256k1 account
keeta:1413829460:aabfo65nbz4toez4ouzit3ej5elpcjnatv6p6vxtgj5gj4x4cbs3nkytnpniyhi
```

Valid forms on other networks:

```
# Main network, keyed Ed25519 account
keeta:21378:ae23cu2wimbyuvib6p77aw7zchgjmfia3fauuhy6mh44xa57buokkhifpsnxo

# Main network, keyed secp256r1 account
keeta:21378:aybzhzcxweiencq2glio3sj6rs5g2sb7qcgmvrumi2y3dmt4sqqvg2zders2ggy

# Main network, token account
keeta:21378:anqdilpazdekdu4acw65fj7smltcp26wbrildkqtszqvverljpwpezmd44ssg

# Main network, storage account
keeta:21378:aqltdal4rshtky5iehd765y3mdjkcmku5d4ulo5fgonzqrxulwepnogq33mle

# Main network, network account
keeta:21378:alwerxoezkupzhifvpo5yvoazlsdqaweov66mokhq7xl4h5ow36v5xu6ek3js

# Main network, multisig account
keeta:21378:a6wiuzcmz4lx3tenp5p24gs76epchg5i22xdkz4r3egopog47onnhhokvqjam
```

Non-conformant but recoverable (does not match the syntax; a consumer MAY lowercase it, after which it identifies the same account as the lowercase form; see [Canonicalization](#canonicalization)):

```
# Uppercase body
keeta:21378:AE23CU2WIMBYUVIB6P77AW7ZCHGJMFIA3FAUUHY6MH44XA57BUOKKHIFPSNXO
```

Invalid:

```
# Display prefix included in the address
keeta:21378:keeta_ae23cu2wimbyuvib6p77aw7zchgjmfia3fauuhy6mh44xa57buokkhifpsnxo

# Wrong namespace casing
Keeta:21378:ae23cu2wimbyuvib6p77aw7zchgjmfia3fauuhy6mh44xa57buokkhifpsnxo

# Hex network identifier (see Keeta CAIP-2 Profile)
keeta:0x5382:ae23cu2wimbyuvib6p77aw7zchgjmfia3fauuhy6mh44xa57buokkhifpsnxo

# Invalid checksum (last character altered)
keeta:21378:ae23cu2wimbyuvib6p77aw7zchgjmfia3fauuhy6mh44xa57buokkhifpsnxa

# Wrong length (one character dropped)
keeta:21378:ae23cu2wimbyuvib6p77aw7zchgjmfia3fauuhy6mh44xa57buokkhifpsnx
```

## Additional Considerations

### Account type prefixes

The type byte occupies the high bits of the encoded body, so the first two characters of the body reflect the account kind.
As of `keetanet-client` version `0.18.4`:

| First two characters   | Account type                     |
| :--------------------- | :------------------------------- |
| `aa`, `ab`, `ac`, `ad` | Keyed account, ECDSA secp256k1   |
| `ae`, `af`, `ag`, `ah` | Keyed account, Ed25519           |
| `ay`, `az`, `a2`, `a3` | Keyed account, ECDSA secp256r1   |
| `ai`, `aj`, `ak`, `al` | Network account                  |
| `am`, `an`, `ao`, `ap` | Token account                    |
| `aq`, `ar`, `as`, `at` | Storage account                  |
| `a4`, `a5`, `a6`, `a7` | Multisig account                 |

This table is illustrative and is **not** normative for type discrimination.
Implementations MUST NOT switch on these prefixes to determine an account's type; instead, parse the address with a Keeta SDK and use `account.isToken()`, `account.isStorage()`, `account.isNetwork()`, and `account.isMultisig()`.

### Security

Keeta addresses encode their type and end in a checksum, so single-character typos and accidental cross-pasting between account types (e.g. sending to a token address instead of a keyed account) are detectable on the client side without a network round-trip.
Implementations SHOULD perform this check before signing a transaction that references a counterparty CAIP-10.

## References

- Keeta [accounts] - account types, generated accounts, and address derivation.
- Keeta [digital signatures][signatures] - the signing algorithms supported by the network.
- Keeta [SDK package][sdk] - `lib/account.d.ts` declares the type bytes and the `PublicKeyString` codec; the reference for encoding and decoding.
- [Keeta CAIP-2 Profile][CAIP-2 Profile] - the network portion of the identifier.
- [RFC 4648][rfc4648] - the base32 alphabet used for the address body.

[CAIP-2 Profile]: ./caip2.md
[accounts]: https://docs.keeta.com/components/accounts
[signatures]: https://docs.keeta.com/security/digital-signatures
[generate-identifier]: https://docs.keeta.com/components/blocks/operations/generateidentifier
[sdk]: https://www.npmjs.com/package/@keetanetwork/keetanet-client
[rfc4648]: https://datatracker.ietf.org/doc/html/rfc4648
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
