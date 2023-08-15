---
namespace-identifier: xrpl-caip122
title: XRP Ledger Namespace - SIWx
author: Anton Dalgren (@antondalgren)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/57/
status: Draft
type: Standard
created: 2023-08-12
requires: ["CAIP-122", "CAIP-2", "CAIP-10"]
---

## CAIP-122

For context, see the [CAIP-122][CAIP-122] specification.

## Rationale

This specification provides the signing algorithm to use, the `type` of the signing algorithm to identify it, and a method for signature creation and verification as required by [CAIP-122][CAIP-122].

## Specification

### Signing Algorithm

XRPL uses the ECDSA [secp256k1][secp256k1] or  EdDSA [Ed25519][Ed25519] signing algorithm for signing and verifying messages depending on the type of the keypair that is being used. A [secp256k1][secp256k1] keypair will be using the [secp256k1][secp256k1] algorithm and a [Ed25519][Ed25519] keypair will be using the [Ed25519][Ed25519] algorithm.

Prior to the message being signed using [secp256k1][secp256k1], it needs to be hashed using the SHA-512/2 algorithm. Correspondingly it needs to be converted to bytes prior to signing it using the [Ed25519][Ed25519] algorithm.

### Signature Type

We propose using the signature type `xrpl:secp256k1` and `xrpl:ed25519` to refer to the chain and algorithm used uniquely.

### Signature Creation

The abstract data model must be converted into a string representation in an unambigious format, and then the string converted to the proper format mentioned in [signing algorithm](#signing-algorithm) to be signed over with the proper algorithm.
Depending on the method used for signatures, this conversion may or may not happen automatically. For example, if using [ripple-keypairs][ripple-keypairs] you need to convert it to a byte representation before signing using [Ed25519][Ed25519] and for [secp256k1][secp256k1] the library will handle hashing and signing.

We propose the following string format, inspired by [EIP-4361][EIP-4361].

```
${domain} wants you to sign in with your XRPL account:
${address}

${statement}

URI: ${uri}
Version: ${version}
Chain ID: ${chain-id}
Nonce: ${nonce}
Issued At: ${issued-at}
Expiration Time: ${expiration-time}
Not Before: ${not-before}
Request ID: ${request-id}
Resources:
- ${resources[0]}
- ${resources[1]}
...
- ${resources[n]}
```

For example,

```
service.org wants you to sign in with your XRPL account:
r4FTvnahbUfhe1WK2EK5Jz4cNvdFvT8Dzt

I accept the ServiceOrg Terms of Service: https://service.org/tos

URI: https://service.org/login
Version: 1
Chain ID: 0
Nonce: 32891757
Issued At: 2021-09-30T16:25:24.000Z
Resources:
- ipfs://Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu
- https://example.com/my-web2-claim.json
```

The preceeding example would be hashed to `4beb3f7d5c8bf8deab467de033628274a9053f688f82e0f023cddcb0564cfc9a` prior to being signed using the [secp256k1][secp256k1] algorithm.

The conversion to bytes prior to signing with [Ed25519][Ed25519] would be:
```
736572766963652e6f72672077616e747320796f7520746f207369676e20696e207769746820796f7572205852504c206163636f756e743a0a72344654766e6168625566686531574b32454b354a7a34634e766446765438447a740a0a49206163636570742074686520536572766963654f7267205465726d73206f6620536572766963653a2068747470733a2f2f736572766963652e6f72672f746f730a0a5552493a2068747470733a2f2f736572766963652e6f72672f6c6f67696e0a56657273696f6e3a20310a436861696e2049443a20300a4e6f6e63653a2033323839313735370a4973737565642041743a20323032312d30392d33305431363a32353a32342e3030305a0a5265736f75726365733a0a2d20697066733a2f2f516d653773733341525667787636725871565069696b4d4a3875324e4c676d67737a673133705972444b456f69750a2d2068747470733a2f2f6578616d706c652e636f6d2f6d792d776562322d636c61696d2e6a736f6e
```
### Signature Verification

Signature verification behaves similarly. We can use standard [secp256k1][secp256k1]/[Ed25519][Ed25519] signature verification. We convert the input message to a bytes representation of the string format, then verify the signature over that using the public key. These verification methods are also available in the [ripple-keypairs][ripple-keypairs] library.

## References

[EIP-4361]: https://eips.ethereum.org/EIPS/eip-4361
[caip-10]: https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-10.md
[caip-2]: https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-2.md
[caip-122]: https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-122.md
[ed25519]: https://ed25519.cr.yp.to/
[secp256k1]: https://en.bitcoin.it/wiki/Secp256k1
[ripple-keypairs]: https://www.npmjs.com/package/ripple-keypairs

- [EIP-4361][]: Sign-In with Ethereum
- [CAIP-10](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-10.md): Account ID Specification
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-2.md): Blockchain ID Specification
- [CAIP-122](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-122.md): Sign in With X Specification
- [Ed25519](https://ed25519.cr.yp.to/): Ed25519: high-speed high-security signatures
- [secp256k1](https://en.bitcoin.it/wiki/Secp256k1): secp256k1 algorithm.
- [ripple-keypairs](https://www.npmjs.com/package/ripple-keypairs): Ripple keypairs
