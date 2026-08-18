---
namespace-identifier: tenzro-caip122
title: Tenzro Namespace - SIWx
author: Hilal Agil (@hilarl)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/184
status: Draft
type: Standard
created: 2026-05-02
updated: 2026-05-02
requires: ["CAIP-122", "CAIP-2", "CAIP-10"]
---

## CAIP-122

For context, see the [CAIP-122](CAIP-122) specification.

## Rationale

Tenzro uses Ed25519 as its native signing algorithm (the same key material backs validator signing, TDIP DIDs, and account-level signing). This specification names the signature type, fixes the message-byte form, and describes verification as required by [CAIP-122](CAIP-122).

## Specification

### Signing Algorithm

Tenzro uses [Ed25519] for signing and verifying messages. Tenzro account public keys are 32-byte Ed25519 public keys, encoded for display either as a `0x`-prefixed lowercase hex string (canonical form) or as a base58btc string.

### Signature Type

We propose the signature type `tenzro:ed25519` to refer to the chain and algorithm uniquely.

### Signature Creation

The abstract data model from CAIP-122 must be converted to an unambiguous string representation, and that string is then encoded as UTF-8 bytes to be signed over.

We adopt the same human-readable layout as [EIP-4361] / Solana's CAIP-122 profile to keep wallet UX uniform across namespaces:

```
${domain} wants you to sign in with your Tenzro account:
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

`${address}` is the Tenzro account in canonical hex form (`0x` + 64 lowercase hex chars).
`${chain-id}` is the CAIP-2 reference for the target Tenzro network (see `caip2.md` in this namespace; e.g. `92bd27db9713293097f0e63476e3911e` for testnet).

Example:

```
service.org wants you to sign in with your Tenzro account:
0x4d7e1c3f5a8b2e9d0c7f3a1b6e9d4c8f2a5b7e0d3c6f9a2b5e8d1c4f7a0b3e6d

I accept the ServiceOrg Terms of Service: https://service.org/tos

URI: https://service.org/login
Version: 1
Chain ID: 92bd27db9713293097f0e63476e3911e
Nonce: 32891757
Issued At: 2026-05-02T16:25:24.000Z
```

The signing input is the UTF-8 byte representation of the string above, signed directly with Ed25519 (no additional pre-hashing — Ed25519 internally hashes the message with SHA-512 per RFC 8032).

### Signature Verification

Verification is standard Ed25519 verification (RFC 8032) over the UTF-8 bytes of the message string. The verification key is the 32-byte Ed25519 public key derived from the displayed address: when the address is in canonical hex form, the public key bytes are exactly the 32 bytes after the `0x` prefix.

Implementations MUST reject low-order public keys and non-canonical scalar encodings, consistent with RFC 8032 §5.1.7 strict-verification rules.

## References

- [EIP-4361]: https://eips.ethereum.org/EIPS/eip-4361
- [CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-2.md
- [CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-10.md
- [CAIP-122]: https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-122.md
- [Ed25519]: https://ed25519.cr.yp.to/
- [RFC 8032]: https://datatracker.ietf.org/doc/html/rfc8032
