---
namespace-identifier: casper-caip10
title: Casper - Addresses
author: <["David Hernando <david.hernando@make.services>", "Adrian Wrona <adrian@casper.network>"]>
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/100
status: Draft
type: Standard
created: 2024-01-12
requires: ["CAIP-10"]

---

<!--You can leave these HTML comments in your merged CAIP and delete the 
 visible duplicate text guides, they will not appear and may be helpful to 
 refer to if you edit it again. This is the suggested template for new CAIPs.
 Note that an CAIP number will be assigned by an editor. When opening a pull
 request to submit your EIP, please use an abbreviated title in the 
 filename, `caipX.md`, all lowercase, no `-` between the CAIP and its 
 number.-->

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

The Casper blockchain uses an on-chain account-based model, uniquely identified by an AccountHash derived from a specific PublicKey. The AccountHash is derived from any of the supported PublicKey variants below to standardize keys that can vary in length.

Casper supports two types of keys for creating accounts and signing transactions:

- Ed25519 keys, which use the Edwards-curve Digital Signature Algorithm (EdDSA).

- Secp256k1 keys, which use the Elliptic Curve Digital Signature Algorithm (ECDSA) with the P-256 curve.


## Syntax

An Account hash is a 32-byte length hash derived from the public key by applying the `blake2b` hash function.

Public key length depends on the key type:

- For Ed25519, length is 66 bytes (the prefix 0x01 and the 64 bytes of the public key).

- For Secp256k1, length is 68 bytes (the prefix 0x02 and the 66 bytes corresponding to the compressed form of the public key).

Keys are usually represented with lowercase letters. However, [CEP-57] introduced an opt-in checksum scheme, based on EIP-55, to protect against copy errors by encoding a checksum in the capitalization of hexadecimal strings.

## Test Cases

Ed25519 public key - checksummed
`01d51D4d7e1Dc8166405EC6fFb21C94434Cfd4D9021Ed6D94A1FF3d7D613046710`

Ed25519 public key - without checksum
`01cd4f2ed572ea555ca46c17c83c43e609d2e916871236f40faa9ba747478e8dee`

AccountHash for previous public key
`account-hash-79c9563deeb7bbd05e91c7dddddec9328717fea1ae846dd54ab9dfeaae015bc0`

Secp256k1 public key - checksummed
`02038a9932973F5632BcF31ff9Ba83e7eB3Bd7457F85af79258bd6b0A1FF06017B5a`

Secp256k1 public key - not checksummed
`02022ade9bd8e06033e99b1bfbf789db4e2db0349045818469bbcaf756996900e838`

AccountHash for previous public key
`account-hash-5b7e450d8b1e58de5f012db6c6e934431a6b6b063e5d4955914675e791797712`

Ed25519 public key - invalid checksum
`01D51D4d7e1Dc8166405EC6fFb21C94434Cfd4D9021Ed6D94a1FF3d7d613046710`

Secp256k1 public key - invalid checksum
`02038A9932973f5632BcF31ff9Ba83e7eB3Bd7457F85af79258bd6b0A1FF06017b5A`

## References
<!--Links to external resources that help understanding the CAIP better. This can e.g. be links to existing implementations.-->
- [Accounts-and-Keys][]
- [CEP-57][]
- [Casper Docs site][]
- [CAIP-10][]

[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CEP-57]: https://github.com/casper-network/ceps/blob/master/text/0057-checksummed-addresses.md
[Accounts-and-Keys]: https://docs.casper.network/concepts/accounts-and-keys/
[Casper Docs site]: https://docs.casper.network/

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
