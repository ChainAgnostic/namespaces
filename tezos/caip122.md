---
namespace-identifier: tezos-caip122
title: Tezos Namespace - Sign in With X (SIWx)
author: Qibing Li (@QibingLee), Carlo van Driesten (@jdsika)
discussions-to: TBA
status: Draft
type: Standard
created: 2022-12-06
updated: 2024-02-20
requires: ["CAIP-2", "CAIP-10", "CAIP-122"]
---

## CAIP-122

For context, see the [CAIP-122][] specification.

## Rationale

Tezos supports three address types with respective key prefixes, `tz1` for [Ed25519][] keys, `tz2` for [Secp256k1][] keys and `tz3` for [NIST P256][] keys specified in [CAIP-10][] and the respective `tezos-caip10` specification. This specification provides the signing algorithm to use, the `type` of the signing algorithm to identify it, and a method for signature creation and verification as required by [CAIP-122][].

## Specification

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

We propose the following string format, inspired by [EIP-4361][].

```text
${domain} wants you to sign in with your Tezos account:
${address}

${statement}

URI: ${uri}
Version: ${version}
Chain ID: ${chain-id}
Nonce: ${nonce}
Issued At: ${timestamp}
Expiration Time: ${expiration-time}
Not Before: ${not-before}
Request ID: ${request-id}
Resources:
- ${resources[0]}
- ${resources[1]}
...
- ${resources[n]}
```

### Signature Verification

Tezos signatures and public keys are base58 encoded with prefixes. Once these
have been removed, we can use standard signature verification methods. Note that
the signature and the signing public key should be sent together to verifiers,
because there is no solution to recover the public key from `tz1`, `tz2`, OR
`tz3` signatures.

## References

- [CAIP-2][] - Blockchain ID Specification.
- [CAIP-10][] - Account ID Specification.
- [CAIP-122][] - Sign in With X (SIWx).
- [EIP-4361][] - Sign-In with Ethereum.
- [Ed25519][] - Ed25519: high-speed high-security signatures.
- [Secp256k1][] - Elliptic curve used in Bitcoin's public-key cryptography.
- [NIST P256][] - One of the most used elliptic curves including native support in some mobile devices.

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[CAIP-122]: https://chainagnostic.org/CAIPs/caip-122
[EIP-4361]: https://eips.ethereum.org/EIPS/eip-4361
[Ed25519]: https://ed25519.cr.yp.to/
[Secp256k1]: https://en.bitcoin.it/wiki/Secp256k1
[NIST P256]: https://csrc.nist.gov/csrc/media/events/workshop-on-elliptic-curve-cryptography-standards/documents/papers/session6-adalier-mehmet.pdf

## Rights

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).