---
namespace-identifier: xahau-caip122
title: Xahau Namespace - Sign-In With X
author: Ekiserrepé (@Ekiserrepe)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/231
status: Draft
type: Standard
created: 2026-09-28
requires: ["CAIP-2", "CAIP-10", "CAIP-122"]
---

# CAIP-122

*For context, see the [CAIP-122][] specification.*

## Introduction

This profile defines Sign-In With Xahau message serialization, signature types,
and verification for Xahau accounts.
It supports the two account key types implemented by `xahaud`: secp256k1 and
Ed25519.

## Specification

### Signing Input

The CAIP-122 abstract data model MUST be serialized as the following
human-readable string.
Lines are separated by a single line-feed byte (`0x0A`), including blank lines,
the final line is not followed by a line feed, and the resulting string is
encoded as UTF-8 without a byte-order mark.
Optional labeled fields that are absent MUST be omitted together with their
complete line.
The blank line after `account_address` is always present.
When `statement` is present, it is followed by one additional blank line.
When `resources` is absent or empty, the `Resources:` line and all resource
entries are omitted.

```text
${domain} wants you to sign in with your Xahau account:
${account_address}

${statement}

URI: ${uri}
Version: ${version}
Nonce: ${nonce}
Issued At: ${issued-at}
Expiration Time: ${expiration-time}
Not Before: ${not-before}
Request ID: ${request-id}
Chain ID: ${chain_id}
Resources:
- ${resources[0]}
- ${resources[1]}
...
- ${resources[n]}
```

`account_address` MUST be the classic address from the Xahau CAIP-10 account ID.
It MUST NOT contain the CAIP-2 prefix, a destination tag, or an X-address.
`chain_id` MUST be the CAIP-2 chain reference, which is the decimal network ID
such as `21337`, following the convention of [CAIP-122][] and [EIP-4361][].
The `xahau` namespace is implied by the message header, so verifiers MUST
reconstruct the full CAIP-2 identifier as `xahau:` followed by this reference.

The requesting wallet MUST verify that `domain` matches the origin of the
request before asking the user to sign.

### Signing Algorithms and Signature Types

Xahau supports two signature types:

| Key type | Signature type | Signing procedure |
| --- | --- | --- |
| secp256k1 | `xahau:secp256k1` | Sign the SHA-512Half digest of the UTF-8 signing input with deterministic ECDSA and canonical low-S DER encoding. |
| Ed25519 | `xahau:ed25519` | Sign the UTF-8 signing input bytes directly with Ed25519. |

SHA-512Half means the first 32 bytes of the SHA-512 digest.
No Xahau transaction-signing prefix is added because a CAIP-122 authentication
message is not a transaction.

### Signature Metadata

The signature metadata MUST include the hexadecimal public key used to create
the signature:

```text
type SignatureMeta struct {
  SigningPubKey String
}
```

Ed25519 public keys are 33 bytes and begin with `ED`.
Compressed secp256k1 public keys are 33 bytes and begin with `02` or `03`.
Signers MUST encode hexadecimal public keys and signatures with uppercase
characters.
Verifiers SHOULD accept either case when decoding them.

### Signature Verification

A verifier MUST:

1. validate the CAIP-2 chain ID and CAIP-10 account ID;
2. reconstruct the exact UTF-8 signing input;
3. select the algorithm from the declared signature type and confirm it agrees
   with the public-key prefix;
4. verify the signature using the procedure above;
5. derive the public key's classic address by calculating
   `RIPEMD-160(SHA-256(public_key_bytes))` and applying Xahau's account-address
   Base58Check encoding; and
6. verify that the derived address is authorized for the claimed account.

The derived address is authorized when it is the claimed account's master
address, unless that account has disabled its master key, or when it matches the
account's current `RegularKey` value.
Verifiers MUST query validated state on the chain named by `chain_id` when
account settings are needed for this authorization check.

This profile does not define a CAIP-122 aggregation format for Xahau signer-list
quorums.
A single signature from one signer-list member MUST NOT be treated as control of
the multisigned account.

## Example

```text
service.org wants you to sign in with your Xahau account:
r9cZA1mLK5R5Am25ArfXFmqgNwjZgnfk59

I accept the ServiceOrg Terms of Service: https://service.org/tos

URI: https://service.org/login
Version: 1
Nonce: 32891757
Issued At: 2026-09-28T12:00:00Z
Chain ID: 21337
Resources:
- ipfs://Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu
- https://example.com/my-web2-claim.json
```

The UTF-8 signing input is 374 bytes and has the following SHA-512Half digest:

```text
06DBD28145086FDAFEBD140EB4395897C68A88277498EEA9D36EC8DD1CC6D6E6
```

This digest is the secp256k1 signing input.
An Ed25519 signer signs the original 374 UTF-8 bytes instead.

## Security Considerations

Verifiers MUST validate the domain, nonce, issuance time, optional validity
window, URI, and chain ID according to CAIP-122.
A signature valid for one Xahau chain MUST NOT be accepted for another chain.

The public key is necessary because a classic address is a hash of a public key
and does not permit public-key recovery for both supported algorithms.
Applications MUST perform the authorization check described above instead of
only verifying the cryptographic signature.

This profile requires a wallet that can sign arbitrary message bytes with the
account key.
Sign-in flows in which a wallet signs a Xahau transaction or a wallet-specific
payload instead of the signing input defined above are outside the scope of
this profile and do not produce `xahau:secp256k1` or `xahau:ed25519`
signatures.

## Backwards Compatibility

There are no known legacy CAIP-122 signature types in the `xahau` namespace.

## References

- [CAIP-2 Profile][] - Xahau chain ID specification.
- [CAIP-10 Profile][] - Xahau account ID specification.
- [CAIP-122][] - Sign-In With X specification.
- [EIP-4361][] - Sign-In with Ethereum, from which the CAIP-122 message format is adapted.
- [Xahau Binary Format][] - Canonical signing and supported signature algorithms.
- [Xahau Transaction Common Fields][] - Public-key authorization for master and regular keys.
- [Xahau AccountRoot][] - Master-key and regular-key account state.
- [xahau-py Keypairs][] - Official key derivation, signing, and verification implementation.
- [xahaud Public Key Source][] - Protocol implementation of key-type detection and signature verification.

[CAIP-2 Profile]: ./caip2.md
[CAIP-10 Profile]: ./caip10.md
[CAIP-122]: https://chainagnostic.org/CAIPs/caip-122
[EIP-4361]: https://eips.ethereum.org/EIPS/eip-4361
[Xahau Binary Format]: https://xahau.network/docs/protocol-reference/binary-format/
[Xahau Transaction Common Fields]: https://xahau.network/docs/protocol-reference/transactions/transaction-common-fields/
[Xahau AccountRoot]: https://xahau.network/docs/protocol-reference/ledger-data/ledger-objects-types/accountroot/
[xahau-py Keypairs]: https://github.com/Xahau/xahau-py
[xahaud Public Key Source]: https://github.com/Xahau/xahaud/blob/dev/src/libxrpl/protocol/PublicKey.cpp

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
