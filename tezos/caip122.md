---
namespace-identifier: tezos-caip122
title: Tezos Namespace - Sign in With X (SIWx)
author: Carlo van Driesten (@jdsika)
status: Draft
type: Standard
created: 2022-12-06
updated: 2024-02-28
requires: ["CAIP-2", "CAIP-10", "CAIP-122"]
---

## CAIP-122

*For context, see the [CAIP-122][] specification.*

This [CAIP-104][] namespace that enables SIWX for `tezos` provides:

1. a signing algorithm, or a finite set of these, where multiple different signing interfaces might be used,
2. a `type` string(s) that designates each signing algorithm, for inclusion in the `signatureMeta.t` value of each signed response
3. a procedure for creating a signing input from the data model specified in this document for each signing algorithm

The signing algorithm covers:

1. how to sign the signing input,
2. how to verify the signature.

A reference implementation can be found in the [SIWT library][].

## Rationale

Tezos supports three address types with respective key prefixes, `tz1` for [Ed25519][] keys, `tz2` for [Secp256k1][] keys, `tz3` for [NIST P256][] keys, and `tz4` for BLS12-381 keys from the [BLS family][] specified in [CAIP-10][] and the respective `tezos-caip10` specification. This specification provides the signing algorithm to use, the `type` of the signing algorithm to identify it, and a method for signature creation and verification as required by [CAIP-122][].

## Specification

### Abstract Data Model

We start by declaring an abstract data model, which contains all the requisite information, metadata, and security mechanisms to authenticate and authorize with a blockchain account securely. The attribute `address` from [CAIP-122][] is replaced by `account-id` for correctness.

The data model MUST contain the following fields:

| Name              | Type            | REQUIRED | Description                                                                                                                                                                                       |
| ----------------- | --------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `domain`          | string          | ✓         | [RFC 4501][] `dnsauthority` that is requesting the signing.                                                                                                                                       |
| `account-id`      | string          | ✓         | Blockchain account id, as defined by [CAIP-10][], performing the signing; should include [CAIP-2][] chain id namespace                                                                            |
| `uri`             | string          | ✓         | [RFC 3986][] URI referring to the resource that is the subject of the signing i.e. the subject of the claim.                                                                                      |
| `version`         | string          | ✓         | Current version of the message.                                                                                                                                                                   |
| `statement`       | string          |           | Human-readable ASCII assertion that the user will sign. It MUST NOT contain `\n`.                                                                                                                 |
| `nonce`           | string          | ✓         | Randomized token to prevent signature replay attacks.                                                                                                                                             |
| `issued-at`       | string          | ✓         | [RFC 3339][] `date-time` that indicates the issuance time.                                                                                                                                        |
| `expiration-time` | string          |           | [RFC 3339][] `date-time` that indicates when the signed authentication message is no longer valid.                                                                                                |
| `not-before`      | string          |           | [RFC 3339][] `date-time` that indicates when the signed authentication message starts being valid.                                                                                                |
| `request-id`      | string          |           | System-specific identifier used to uniquely refer to the authentication request.                                                                                                                  |
| `resources`       | List of strings |           | List of information or references to information the user wishes to have resolved as part of the authentication by the relying party; express as [RFC 3986][] URIs and separated by `\n`.         |
| `signature`       | bytes           | ✓         | Signature of the message signed by the wallet.                                                                                                                                                    |
| `type`            | string          | ✓         | Type of the signature to be generated, as defined in the namespaces for this CAIP.                                                                                                                |

Here:

- The attributes `issued-at` and `nonce` are set to REQUIRED as it is best practice to use these fields to protect against replay-attacks.

### Signing Algorithm

In Tezos, Ed25519 (`tz1`) is the most commonly used signing algorithm. Tezos
uses prefixed base58 hashes of key material and signatures, with distinct
prefixes to encode the public key, private key and signatures. For Ed25519, the
prefixes are `edpk`, `edsk` and `edsig`. For Secp256k1, the prefixes are `sppk`,
`spsk` and `spsig`. For P256, the prefixes are `p2pk`, `p2sk` and `p2sig`.

### Signature Type

We propose using any of the three signature types (`tezos:ed25519`,
`tezos:secp256k1` and `tezos:p256`) to allow Tezos wallets to sign with `tz1`,
`tz2` or `tz3` addresses for off-chain authentication purposes.

### Signature Creation

The abstract data model must be converted into a string representation in an
unambigious format, and then the string converted to a byte array to be signed
over.

The proposed string representation format, adapted from [EIP-4361][], should be as such:

```text
${domain} wants you to sign in with your ${namespace(account-id)} account:
${account_address(account-id)}

${statement}

URI: ${uri}
Version: ${version}
Nonce: ${nonce}
Issued At: ${issued-at}
Expiration Time: ${expiration-time}
Not Before: ${not-before}
Request ID: ${request-id}
Chain ID: ${chain_id(account-id)}
Resources:
- ${resources[0]}
- ${resources[1]}
...
- ${resources[n]}
```

Here:

- The data model in [CAIP-122][] defines the attribute `address` which is here correctly replaced by the [CAIP-10][] term `account-id`,
- `account_address(account-id)` is the `pkh` segment of a [CAIP-10][] `account-id`,
- `chain_id(account-id)` is the `chain_id` segment of the `account-id` defined in [CAIP-2][],
- `namespace(account-id)` is the `namespace` segment of `account-id` of the data model represented by a human-readable name of the ecosystem the user can recognize which is here `tezos`.
- A wallet provider MAY use an alias for the `chain_id` like `mainnet` as defined in [CAIP-2][] if the user experience is enhanced. It is RECOMMENDED to use a separate chain registry to map an alias to the chain ID.

### Signature Verification

Tezos signatures and public keys are base58 encoded with prefixes. Once these have been removed, we can use standard signature verification methods. Note that the signature and the signing public key should be sent together to verifiers, because there is no solution to recover the public key from `tz1`, `tz2`, `tz3`, or `tz4` signatures.

## Examples


## References

- [CAIP-2][] - Chain ID Specification.
- [CAIP-10][] - Account ID Specification.
- [CAIP-104][] - CAIP namespace definition.
- [CAIP-122][] - Sign in With X (SIWx).
- [EIP-4361][] - Sign-In with Ethereum.
- [RFC 3339][]: Date and Time on the Internet: Timestamps.
- [RFC 4501][]: Domain Name System Uniform Resource Identifiers
- [RFC 3986][]: Uniform Resource Identifier (URI): Generic Syntax
- [Ed25519][] - Ed25519: high-speed high-security signatures.
- [Secp256k1][] - Elliptic curve used in Bitcoin's public-key cryptography.
- [NIST P256][] - One of the most used elliptic curves including native support in some mobile devices.
- [BLS family][] - BLS12-381 is a pairing-friendly elliptic curve construction from the BLS family, with embedding degree 12.
- [SIWT library][] - A reference implementation adhering to the CAIP specifications.


[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[CAIP-104]: https://chainagnostic.org/CAIPs/caip-104
[CAIP-122]: https://chainagnostic.org/CAIPs/caip-122
[EIP-4361]: https://eips.ethereum.org/EIPS/eip-4361
[RFC 3339]: https://datatracker.ietf.org/doc/html/rfc3339#section-5.6
[RFC 3986]: https://www.rfc-editor.org/rfc/rfc3986
[RFC 4501]: https://www.rfc-editor.org/rfc/rfc4501.html
[Ed25519]: https://ed25519.cr.yp.to/
[Secp256k1]: https://en.bitcoin.it/wiki/Secp256k1
[NIST P256]: https://csrc.nist.gov/csrc/media/events/workshop-on-elliptic-curve-cryptography-standards/documents/papers/session6-adalier-mehmet.pdf
[BLS family]: https://eprint.iacr.org/2002/088
[SIWT library]: https://siwt.xyz/

## Rights

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
