---
namespace-identifier: stacks-caip122
title: Stacks Namespace - SIWx
author: Léo Pradel @pradel
discussions-to: https://forum.stacks.org/t/caip-2-and-caip-10-stacks-specification/13290
status: Draft
type: Standard
created: 2023-01-08
requires: ["CAIP-122", "CAIP-2", "CAIP-10"]
---

## CAIP-122

For context, see the [CAIP-122][] specification.

## Rationale

This specification provides the signing algorithm to use, the `type` of the
signing algorithm to identify it, and a method for signature creation and
verification as required by [CAIP-122][].

## Specification

### Signing Algorithm

Stacks uses the ECDSA secp256k1 signing algorithm for signing and verifying
messages. The message is hashed with SHA256 before being used as an input for
signing.

### Signature Type

We propose using the signature type `stacks:secp256k1` to refer to the chain and
algorithm used uniquely.

### Signature Creation

The abstract data model defined by CAIP-122 must be converted into a string
representation in an unambigious format, and then the string converted to a byte
array to be signed over.

We propose the following string format, inspired by [EIP-4361][].

```
${domain} wants you to sign in with your Stacks account:
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

As in other secp256k1 systems, the public key from which an address is derived
can be recovered by smart contracts or elsewhere from a signature and the
signing address, via the Stacks equivalent of the [ECRecover][] pattern.  With
the signature and public key, the message can be verified using the same
algorithm as for signature creation. The message needs to be hashed with SHA256
before being used as an input for verification.

## References

[EIP-4361]: https://eips.ethereum.org/EIPS/eip-4361
[CAIP-122]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-122.md
[SIP-018]: https://github.com/stacksgov/sips/pull/57
[ECRecover]: https://docs.stacks.co/docs/write-smart-contracts/clarity-language/language-functions#secp256k1-recover

- [EIP-4361](https://eips.ethereum.org/EIPS/eip-4361): Sign-In with Ethereum
- [CAIP-10](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md): Account ID Specification
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md): Blockchain ID Specification
- [CAIP-122](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-122.md): Sign in With X Specification
