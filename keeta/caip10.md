---
namespace-identifier: keeta-caip10
title: Keeta - Account ID Specification
author: ["@sc4l3r"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/XXXX
status: Draft
type: Standard
created: 2026-04-27
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

_For context, see the [CAIP-10][] specification._

## Introduction

Every [account][accounts] on a Keeta network -- whether it is a key-pair-backed account (ECDSA secp256k1, ECDSA secp256r1, or Ed25519), a token, a storage account, a network account, or a multisig -- is addressed by a single base32-encoded **public key string** with the prefix `keeta_`.

The body of the address self-identifies its account type via its first base32 characters (e.g. `aa` is a secp256k1 keyed account, `am` is a token, `aq` is a storage account, `ai` is a Network Account), and ends in a checksum.

This profile uses the full canonical `keeta_...` form as the [CAIP-10][] `account_address`.

## Specification

### Semantics

The inputs are:

- A Keeta `networkId` (defined in the [Keeta CAIP-2 Profile][CAIP-2 Profile]) identifying which network the account lives on.
- A Keeta canonical address string, of the form `keeta_<base32 body>`, returned by the SDK as `account.publicKeyString.toString()` (or accepted by `Account.fromPublicKeyString()`).

The body of a Keeta address is the [RFC 4648][rfc4648] base32 encoding of a byte sequence that encodes an account-type indicator, the public key material, and a truncated hash checksum.
RFC 4648 base32 is case-insensitive; the canonical form on Keeta and in this profile is lowercase with no padding (see [Canonicalization](#canonicalization)).
The exact byte layout may change in future protocol versions; the SDK is the authoritative source for encoding and decoding (see [Resolution Mechanics](#resolution-mechanics)).

The account-type indicator occupies the high bits of the encoded body, so the characters immediately following `keeta_` reflect the account's key algorithm and identifier type.
The following two-character prefixes are reserved by the SDK for the account types listed below as of `keetanet-client` version `0.16.1`:

| First chars (after `keeta_`) | Account type                           |
| :--------------------------- | :------------------------------------- |
| `aa`, `ab`, `ac`, `ad`       | Keyed account, ECDSA secp256k1         |
| `ae`, `af`, `ag`, `ah`       | Keyed account, Ed25519                 |
| `ay`, `az`, `a2`, `a3`       | Keyed account, ECDSA secp256r1 (P-256) |
| `ai`, `aj`, `ak`, `al`       | Network Account (one per network)      |
| `am`, `an`, `ao`, `ap`       | Token account                          |
| `aq`, `ar`, `as`, `at`       | Storage account                        |
| `a4`, `a5`, `a6`, `a7`       | Multisig identifier account            |

This table is illustrative and reflects the current SDK encoding; it is **not** normative for type discrimination.
Implementations MUST NOT switch on these prefixes to determine an account's type; instead, parse the address with a Keeta SDK and use `account.isToken()`, `account.isStorage()`, `account.isNetwork()`, and `account.isMultisig()` (see [Resolution Mechanics](#resolution-mechanics)).

#### Canonicalization

A Keeta address is **case-insensitive**: per RFC 4648, two base32-encoded bodies that differ only in letter case decode to the same byte sequence and therefore identify the same account.
For [CAIP-10][] purposes the canonical form is **all-lowercase**, and producers MUST lowercase the body before emitting a CAIP-10 string.
Consumers MUST treat differently-cased CAIP-10 strings whose lowercased forms are equal as identifiers for the same account, and SHOULD lowercase incoming CAIP-10 strings before using them as cache or lookup keys.
The literal prefix `keeta_` is always lowercase.

### Syntax

A Keeta [CAIP-10][] account identifier MUST take the form:

```
keeta:<networkId>:<address>
```

Where:

- `keeta` is the namespace.
- `<networkId>` is a CAIP-2 reference for a Keeta network as defined by the [Keeta CAIP-2 Profile][CAIP-2 Profile].
- `<address>` is the canonical Keeta public key string, **including** its `keeta_` prefix.

The `<address>` segment MUST match:

```
^keeta_[a-z2-7]+$
```

A regex match is necessary but not sufficient for validity as it does not verify the type indicator, checksum, or body length.
Implementations MUST validate addresses using the Keeta SDK or by following the steps in [Resolution Mechanics](#resolution-mechanics).

### Resolution Mechanics

To validate a Keeta CAIP-10 identifier:

1. Split on `:` and verify the namespace is `keeta`.
2. Validate `<networkId>` against the [Keeta CAIP-2 Profile][CAIP-2 Profile].
3. Lowercase the body of `<address>` (the part after `keeta_`) to obtain its canonical form; see [Canonicalization](#canonicalization).
4. Decode `<address>` using the Keeta public-key-string codec; verify the type byte and checksum.
5. Optionally, query a node on the indicated network to confirm the account exists and to retrieve its info:

```ts
import * as KeetaNet from "@keetanetwork/keetanet-client";

const account = KeetaNet.lib.Account.fromPublicKeyString(
  "keeta_aabfo65nbz4toez4ouzit3ej5elpcjnatv6p6vxtgj5gj4x4cbs3nkytnpniyhi",
);
const client = KeetaNet.Client.fromNetwork("test");
const { info } = await client.getAccountInfo(account);
```

Implementations SHOULD validate the checksum by round-tripping through `Account.fromPublicKeyString()` before treating the identifier as well-formed.

Implementations SHOULD use the methods of a Keeta SDK (e.g. `account.isToken()`, `account.isStorage()`) to determine the type of an account.

Note that account _existence_ is not required for a CAIP-10 string to be valid -- Keeta accounts come into existence when their first block is published, and a freshly-derived keyed address may be a perfectly valid recipient before any block has ever been published to its chain.

## Rationale

Keeta addresses are designed to be self-describing: the `keeta_` prefix and the algorithm-tag prefix are part of the canonical form everywhere -- wallet UIs, block explorers, the SDK, and on-chain metadata.
Stripping `keeta_` to "save space" inside a CAIP-10 string would force every consumer to reattach it before handing the address to the SDK, and would cause CAIP-10 strings to disagree with how the same address is rendered everywhere else in the ecosystem.

The resulting form fits comfortably within the [CAIP-10][] `account_address` length budget of 128 characters: the currently longest possible Keeta address is `keeta_` (6 chars) plus a 63-char body for compressed ECDSA secp256k1 / secp256r1 keys = 69 chars total; Ed25519 and identifier accounts are 67 chars total.

### Backwards Compatibility

This is the first [CAIP-10][] specification for the `keeta` namespace, so there are no legacy identifiers to support.

## Test Cases

Valid (test network, `networkId = 1413829460`):

```
# Keyed secp256k1 account
keeta:1413829460:keeta_aabfo65nbz4toez4ouzit3ej5elpcjnatv6p6vxtgj5gj4x4cbs3nkytnpniyhi
```

Valid forms on other networks:

```
# Mainnet, keyed Ed25519 account
keeta:21378:keeta_ae23cu2wimbyuvib6p77aw7zchgjmfia3fauuhy6mh44xa57buokkhifpsnxo

# Mainnet token account
keeta:21378:keeta_anqdilpazdekdu4acw65fj7smltcp26wbrildkqtszqvverljpwpezmd44ssg

# Mainnet storage account
keeta:21378:keeta_aqltdal4rshtky5iehd765y3mdjkcmku5d4ulo5fgonzqrxulwepnogq33mle

# Mainnet Network Account
keeta:21378:keeta_alwerxoezkupzhifvpo5yvoazlsdqaweov66mokhq7xl4h5ow36v5xu6ek3js
```

Non-canonical (decode to a valid account but MUST be lowercased before being used as a CAIP-10 identifier; see [Canonicalization](#canonicalization)):

```
# Uppercase body — same account as the lowercase form
keeta:21378:keeta_AE23CU2WIMBYUVIB6P77AW7ZCHGJMFIA3FAUUHY6MH44XA57BUOKKHIFPSNXO
```

Invalid:

```
# Missing keeta_ prefix on the address
keeta:21378:ae23cu2wimbyuvib6p77aw7zchgjmfia3fauuhy6mh44xa57buokkhifpsnxo

# Wrong namespace casing
Keeta:21378:keeta_ae23cu2wimbyuvib6p77aw7zchgjmfia3fauuhy6mh44xa57buokkhifpsnxo

# Hex networkId (see Keeta CAIP-2 Profile)
keeta:0x5382:keeta_ae23cu2wimbyuvib6p77aw7zchgjmfia3fauuhy6mh44xa57buokkhifpsnxo
```

## Additional Considerations

### Security

Keeta addresses encode their algorithm and type in the leading body characters and end in a checksum, so single-character typos and accidental cross-pasting between account types (e.g. sending to a token address instead of a keyed account) are detectable on the client side without a network round-trip.
Implementations SHOULD perform this check before signing a transaction that references a counterparty CAIP-10.

The same key pair derives to the same `keeta_...` address on every Keeta network, but the `<networkId>` segment of a CAIP-10 string is not redundant: the on-chain _state_ of an account (balances, permissions, certificates, history) is per-network, and applications MUST treat `keeta:21378:keeta_...` and `keeta:1413829460:keeta_...` as different accounts even when the address bodies are identical.

## References

- Keeta [accounts] - account types, identifier accounts, and address derivation.
- Keeta [SDK source][sdk] - `lib/account.d.ts` defines the `keeta_` prefix, the algorithm tag bytes, and the `PublicKeyString` codec.
- [Keeta CAIP-2 Profile][CAIP-2 Profile] - the network-id portion of the identifier.
- [RFC 4648][rfc4648] - the base32 alphabet used for the address body.

[CAIP-2 Profile]: ./caip2.md
[accounts]: https://docs.keeta.com/components/accounts
[sdk]: https://github.com/KeetaNetwork/keetanet-client
[rfc4648]: https://datatracker.ietf.org/doc/html/rfc4648
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
