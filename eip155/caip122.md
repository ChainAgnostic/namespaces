---
namespace-identifier: eip155-caip122
title: EVM Namespace - SIWx
author: Haardik (@haardikk21)
discussions-to: TBA
status: Draft
type: Standard
created: 2022-08-19
updated: 2022-08-19
requires: ["CAIP-122", "CAIP-2", "CAIP-10"]
---

## CAIP-122

For context, see the [CAIP-122](CAIP-122) specification.

## Rationale

On Ethereum, [EIP-4361](EIP-4361) Sign-in with Ethereum already exists, which was the inspiration for CAIP-122. This specification highlights how EIP-4361 conforms with CAIP-122.

## Specification

### Signing Algorithm

Ethereum uses the ECDSA signing algorithm for signing and verifying messages. Ethereum addresses are derived from the public ECDSA key.

### Signature Type

We use the signature type `eip191` and `eip1271` when referring to Ethereum Personal Signatures and Contract Signatures respectively, as specified in the EIP-4361 specification.

### Signature Creation

The abstract data model must be converted into a string representation in an unambigious format. We use the format as defined in EIP-4361.

```
${domain} wants you to sign in with your Ethereum account:
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

### Signature Verification

We use signature verification techniques from [EIP-191](EIP-191) and [EIP-1271](EIP-1271) as specified as well as any additional steps specified in [EIP-4361](EIP-4361).

## References

[eip-4361]: https://eips.ethereum.org/EIPS/eip-4361
[caip-10]: https://github.com/ChainAgnostic/CAIPs/blob/8fdb5bfd1bdf15c9daf8aacfbcc423533764dfe9/CAIPs/caip-10.md
[caip-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[caip-122]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-122.md
[eip-191]: https://eips.ethereum.org/EIPS/eip-191
[eip-1271]: https://eips.ethereum.org/EIPS/eip-1271

- [EIP-4361](https://eips.ethereum.org/EIPS/eip-4361): Sign-In with Ethereum
- [CAIP-10](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md): Account ID Specification
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md): Blockchain ID Specification
- [CAIP-122](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-122.md): Sign in With X Specification
- [EIP-191](https://eips.ethereum.org/EIPS/eip-191): Signed Data Standard
- [EIP-1271](https://eips.ethereum.org/EIPS/eip-1271): Standard Signature Validation Method for Contracts
