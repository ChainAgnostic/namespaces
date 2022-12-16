---
namespace-identifier: tezos-caip122
title: Tezos Namespace - SIWx
author: Qibing Li (@QibingLee)
discussions-to: TBA
status: Draft
type: Standard
created: 2022-12-06
updated: 2022-12-15
requires: ["CAIP-122", "CAIP-2", "CAIP-10"]
---

## CAIP-122

For context, see the [CAIP-122][] specification.

## Rationale

Tezos supports three types of keys, `tz1` for Ed25519 keys, `tz2` for Secp256k1 keys and `tz3` for P256 keys. This specification provides the signing algorithm to use, the `type` of the signing algorithm to identify it, and a method for signature creation and verification as required by [CAIP-122][].

## Specification

### Signing Algorithm

In Tezos, Ed25519 (`tz1`) is the most commonly used signing algorithm. Tezos uses the base58 with different prefixes to encode the public key, private key and signature. For Ed25519, the prefixes are `edpk`, `edsk` and `edsig`. For Secp256k1, the prefixes are `sppk`, `spsk` and `spsig`. For P256, the prefixes are `p2pk`, `p2sk` and `p2sig`.

### Signature Type

We propose using the signature type `tezos:ed25519`, `tezos:secp256k1` and `tezos:p256` to refer to the Tezos chain and different signing algorithms for `tz1`, `tz2` and `tz3`.

### Signature Creation

The abstract data model must be converted into a string representation in an unambigious format, and then the string converted to a byte array to be signed over.

We propose the following string format, inspired from [EIP-4361][].

```
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

Tezos signatures and public keys are base58 encoded with prefixes, which should be removed before verification. Then we can use standard signature verification once we get the signature and public key. Note that the signature and public key should be sent together to verifiers, because there is no solution to recover the public key from `tz` addresses.

## References

[EIP-4361]: https://eips.ethereum.org/EIPS/eip-4361
[CAIP-122]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-122.md

- [EIP-4361](https://eips.ethereum.org/EIPS/eip-4361): Sign-In with Ethereum
- [CAIP-10](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md): Account ID Specification
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md): Blockchain ID Specification
- [CAIP-122](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-122.md): Sign in With X Specification
- [Ed25519](https://ed25519.cr.yp.to/): Ed25519: high-speed high-security signatures
