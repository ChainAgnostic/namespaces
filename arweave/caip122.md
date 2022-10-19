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

Arweave signatures are 512 byte arrays which are `Base64URL` encoded for transmission over HTTP. This specification provides the signing algorithm to use, the `type` of the signing algorithm to identify it, and a method for signature creation and verification as required by [CAIP-122](CAIP-122).

## Specification

### Signing Algorithm

Arweave wallets are RSA key pairs and use the private and public keys for signing and verifying signatures. Arweave wallet addresses are the SHA-256 hash of the RSA public key.

### Signature Type

Arweave signatures use the RSA-PSS signing algorithm to sign data and verify signatures. Hence, the type of the signature would be represented as `arweave:rsa-pss` in the cacao object.

### Signature Creation

The abstract data model must be converted into a string representation in an unambigious format. We use the format as defined in EIP-4361 as reference.

An informal template of the full message is presented below. The field descriptions are provided in the order they must appear as follows:
- `domain` is the RFC 3986 authority that is requesting the signing.
- `address` is the Arweave address performing the signing.
- `statement` (optional) is a human-readable ASCII assertion that the user will sign, and it must not contain '\n'.
- `uri` is an RFC 3986 URI referring to the resource that is the subject of the signing (as in the subject of a claim).
- `version` is the current version of the message, which MUST be 1 for this specification.
- `chain-id` (optional) is the Arweave Chain ID to which the session is bound, and the network where Contract Accounts MUST be resolved.
- `nonce` (optional) is a randomized token typically chosen by the relying party and used to prevent replay attacks, at least 8 alphanumeric characters.
- `timestamp` (optional) is the unix time stamp of when the request was created.
- `expiration-time` (optional) is the ISO 8601 datetime string that, if present, indicates when the signed authentication message is no longer valid.
- `not-before` (optional) is the ISO 8601 datetime string that, if present, indicates when the signed authentication message will become valid.
- `request-id` (optional) is an system-specific identifier that may be used to uniquely refer to the sign-in request.
- `resources` (optional) is a list of information or references to information the user wishes to have resolved as part of authentication by the relying party. They are expressed as RFC 3986 URIs separated by "\n- " where \n is the byte 0x0a.
- `type` of the signature to be generated, as defined in the namespaces for this CAIP.
- `signature` is the result of concatenation and signing of the other field descriptions by the wallet.

```
${domain} wants you to sign in with your Arweave account:
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

Type: ${type}
Signature: ${signature}
```

The signature creation process on Arweave is done through the `arweave-js` library. The message data model is expressed in string format. This string is signed using the RSA-PSS algorithm through a manual call to the `sign()` method from the `arweave-js` library. The signature is returned as a Uint8Array of bytes which is then Base64Url encoded by calling `arweave.utils.bufferTob64Url()`.

### Signature Verification

The signature is encoded in Base64URL format. It must be decoded to an array of bytes before being verified using the RSA algorithm.

## References

- [EIP-4361](https://eips.ethereum.org/EIPS/eip-4361)
- [Arweave](https://github.com/ArweaveTeam/arweave-standards)
- [Arweave Transaction Signing](https://docs.arweave.org/developers/server/http-api#transaction-signing)
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md)
- [CAIP-10](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md)
- [CAIP-122](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-122.md)



## Rights

Copyright and related rights waived via CC0.