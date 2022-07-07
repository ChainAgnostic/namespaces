---
namespace-identifier: solana-caip122
title: Solana Namespace - SIWx
author: Haardik (@haardikk21)
discussions-to: TBA
status: Draft
type: Standard
created: 2022-07-06
updated: 2022-07-06
requires: ["CAIP-122", "CAIP-2", "CAIP-10"]
---

## CAIP-122

For context, see the [CAIP-122](CAIP-122) specification.

## Rationale

In Solana, signatures can only be made over raw bytes, `Uint8Arrays` in Javascript. This specification provides the signing algorithm to use, the `type` of the signing algorithm to identify it, and a method for signature creation and verification as required by [CAIP-122](CAIP-122).

## Specification

### Signing Algorithm

Solana uses the [Ed25519](Ed25519) signing algorithm for signing and verifying messages. Solana keypairs are also just Ed25519 public/private keypairs.

### Signature Type

We propose using the signature type `solana:ed25519` to refer to the chain and algorithm used uniquely.

### Signature Creation

The abstract data model must be converted into a string representation in an unambigious format, and then the string converted to a byte array to be signed over.

We propose the following string format, inspired from [EIP-4361](EIP-4361).

```
${domain} wants you to sign in with your Solana account:
${address}

${statement}

URI: ${uri}
Version: ${version}
Nonce: ${nonce}
Issued At: ${issued-at}
Expiration Time: ${expiration-time}
Not Before: ${not-before}
Request ID: ${request-id}
Chain ID: ${chain-id}
Resources:
- ${resources[0]}
- ${resources[1]}
...
- ${resources[n]}
```

For example,

```
service.org wants you to sign in with your Solana account:
GwAF45zjfyGzUbd3i3hXxzGeuchzEZXwpRYHZM5912F1

I accept the ServiceOrg Terms of Service: https://service.org/tos

URI: https://service.org/login
Version: 1
Nonce: 32891757
Issued At: 2021-09-30T16:25:24.000Z
Chain ID: 1
Resources:
- ipfs://Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu
- https://example.com/my-web2-claim.json
```

which should then be converted into raw bytes (encoded as base64url for brevity).

```
c2VydmljZS5vcmcgd2FudHMgeW91IHRvIHNpZ24gaW4gd2l0aCB5b3VyIFNvbGFuYSBhY2NvdW50OgpHd0FGNDV6amZ5R3pVYmQzaTNoWHh6R2V1Y2h6RVpYd3BSWUhaTTU5MTJGMQoKSSBhY2NlcHQgdGhlIFNlcnZpY2VPcmcgVGVybXMgb2YgU2VydmljZTogaHR0cHM6Ly9zZXJ2aWNlLm9yZy90b3MKClVSSTogaHR0cHM6Ly9zZXJ2aWNlLm9yZy9sb2dpbgpWZXJzaW9uOiAxCk5vbmNlOiAzMjg5MTc1NwpJc3N1ZWQgQXQ6IDIwMjEtMDktMzBUMTY6MjU6MjQuMDAwWgpDaGFpbiBJRDogMQpSZXNvdXJjZXM6Ci0gaXBmczovL1FtZTdzczNBUlZneHY2clhxVlBpaWtNSjh1Mk5MZ21nc3pnMTNwWXJES0VvaXUKLSBodHRwczovL2V4YW1wbGUuY29tL215LXdlYjItY2xhaW0uanNvbg
```

Depending on the method used for signatures, this conversion may or may not happen automatically. For example, when using Phantom Wallet client-side, it performs the conversion automatically. However, if doing something server-side, you likely need to do this conversion yourself.

### Signature Verification

Signature verification behaves similarly. We can use standard Ed25519 signature verification. We convert the input message to a bytes representation of the string format, then verify the signature over that. The verification public key should be the Solana wallet address, which is just a `base58` encoded Ed25519 public key.

## References

[eip-4361]: https://eips.ethereum.org/EIPS/eip-4361
[caip-10]: https://github.com/ChainAgnostic/CAIPs/blob/8fdb5bfd1bdf15c9daf8aacfbcc423533764dfe9/CAIPs/caip-10.md
[caip-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[caip-122]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-122.md
[ed25519]: https://ed25519.cr.yp.to/

- [EIP-4361](https://eips.ethereum.org/EIPS/eip-4361): Sign-In with Ethereum
- [CAIP-10](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md): Account ID Specification
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md): Blockchain ID Specification
- [CAIP-122](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-122.md): Sign in With X Specification
- [Ed25519](https://ed25519.cr.yp.to/): Ed25519: high-speed high-security signatures
