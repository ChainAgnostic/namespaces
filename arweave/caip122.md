---
namespace-identifier: arweave-caip122
title: Arweave Namespace - SIWx
author: Rohit Pathare (@ropats16), Phil Billingsby (@pbillingsby), Dan MacDonald (@DanMacDonald)
discussions-to: TBA
status: Draft
type: Standard
created: 2022-09-01
requires: ["CAIP-122", "CAIP-2", "CAIP-10"]
---

## CAIP-122

For context, see the [CAIP-122](CAIP-122) specification.

## Rationale

On Arweave, [EIP-4361](EIP-4361) Sign-in with Arweave already exists, which was the inspiration for CAIP-122. This specification highlights how EIP-4361 conforms with CAIP-122.

## Specification

### Signing Algorithm

Arweave wallets are RSA key pairs and use the private and public keys for signing and verifying signatures. Arweave wallet addresses are the SHA-256 hash of the RSA public key.

### Signature Type

Arweave signatures use the RSA-PSS signing algorithm to sign data and verify signatures.

### Signature Creation

The abstract data model must be converted into a string representation in an unambigious format. We use the format as defined in EIP-4361 as reference.

An informal template of the full message is presented below. The field descriptions are provided in the order they must appear as follows:
- `domain` is the RFC 3986 authority that is requesting the signing.
- `address` is the Arweave address performing the signing.
- `uri` is an RFC 3986 URI referring to the resource that is the subject of the signing (as in the subject of a claim).
- `version` is the current version of the message, which MUST be 1 for this specification.
- `type` of the signature to be generated, as defined in the namespaces for this CAIP.
- `signature` is the result of concatenation and signing of the other field descriptions by the wallet.

Each message field is separated by a line feed (LF).

```
Domain: ${domain} LF
Address: ${address} LF
URI: ${uri} LF
Version: ${version} LF
Chain ID: ${chain-id} LF
Type: ${type} LF
Signature: ${signature} LF
```

### Signature Verification

The signature is encoded in Base64URL format. It must be decoded to an array of bytes before being verified using the RSA algorithm.

## References

- [EIP-4361](https://eips.ethereum.org/EIPS/eip-4361): Sign-In with Arweave
- [Arweave](https://github.com/ArweaveTeam/arweave-standards)
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md)
- [CAIP-10](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md)
- [CAIP-122](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-122.md): Sign in With X 



## Rights

Copyright and related rights waived via CC0.