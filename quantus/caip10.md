---
namespace-identifier: quantus-caip10
title: Quantus Namespace - Addresses
author: ["Nikolaus Heger (@n13)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/228
status: Draft
type: Standard
created: 2026-09-17
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

A Quantus account is identified on-chain by a 32-byte account ID.
For accounts controlled by a key, the account ID is the [Poseidon][] hash of the ML-DSA public key.
Both ML-DSA-87 and ML-DSA-65 keys are supported, and the account ID does not reveal which was used.
The public key itself is 2592 bytes for ML-DSA-87 or 1952 bytes for ML-DSA-65 and is never used as an address; it is only revealed inside a signed transaction.
Other account IDs, such as multisig and pallet-derived accounts, are 32-byte values with no corresponding key.

Account IDs are presented to users in [SS58][] encoding with the network prefix `189`, which is registered to Quantus in the [SS58 registry][].
Every Quantus network uses the same prefix, so a given account ID has the same address string on mainnet and on Planck.
The CAIP-2 chain ID is what distinguishes the two.

## Syntax

An SS58 address with prefix `189` is the base58btc encoding of:

1. the two prefix bytes `0x6f 0x40` (the SS58 encoding of `189`),
2. the 32-byte account ID,
3. a 2-byte checksum: the first two bytes of `blake2b-512("SS58PRE" || prefix bytes || account ID)`.

The result is always 49 characters long and always starts with `qz`.
The `account_address` segment of a Quantus CAIP-10 is that string, unchanged.

```
account_id:        chain_id + ":" + account_address
chain_id:          "quantus:" + [a-z0-9]{3,32}
account_address:   "qz" + [1-9A-HJ-NP-Za-km-z]{47}
```

A regular expression for validating the syntax, without verifying the checksum, is:

```
^quantus:[a-z0-9]{3,32}:qz[1-9A-HJ-NP-Za-km-z]{47}$
```

Full validation decodes the address, checks that the prefix bytes are `0x6f40` and recomputes the checksum.
Any SS58 library that accepts a numeric prefix can do this with prefix `189`.

### Backwards Compatibility

Not applicable.

## Test Cases

This is a list of manually composed examples. Each account ID is shown in hex followed by its address on both networks:

```
# Account ID 0xbe13a189f99c44a959e26694ffe5e4ba223092f3edbe8259c1d45ad08edb403d
quantus:mainnet:qzokTZkdWXxMgSXyF86ECHxG8o8yRX5ibrX2Uw8YmqkHRdj1V
quantus:planck:qzokTZkdWXxMgSXyF86ECHxG8o8yRX5ibrX2Uw8YmqkHRdj1V

# Account ID 0x586c2cc8b99325a0455f20485fce964f040670a810ee4639e5f6ce9b85215c66
quantus:mainnet:qzmTAz3UUw1WGUuVh8nbFmPwcftomduwy6twq6NDR6y9qqtEs
quantus:planck:qzmTAz3UUw1WGUuVh8nbFmPwcftomduwy6twq6NDR6y9qqtEs

# Account ID 0x3179fa8be95211111e314411647708c64227ef4bdcb26ea1a5026a4542363a23
quantus:mainnet:qzka7DZXAT7GnzgXQfxiSwrPKRWgW6m6G89QRsQiLThThZ6Cw
quantus:planck:qzka7DZXAT7GnzgXQfxiSwrPKRWgW6m6G89QRsQiLThThZ6Cw
```

## References

- [Quantus documentation][] - developer documentation for Quantus Network
- [Post-quantum cryptography in Quantus][] - how ML-DSA keys and Poseidon account derivation work
- [SS58][] - the address encoding
- [SS58 registry][] - the registry in which prefix `189` is assigned to Quantus
- [FIPS 204][] - the ML-DSA signature standard

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[Quantus documentation]: https://docs.quantus.com/
[Post-quantum cryptography in Quantus]: https://docs.quantus.com/deep-dives/pqc/
[SS58]: https://docs.polkadot.com/polkadot-protocol/parachain-basics/accounts/#address-formats
[SS58 registry]: https://github.com/paritytech/ss58-registry
[FIPS 204]: https://csrc.nist.gov/pubs/fips/204/final
[Poseidon]: https://eprint.iacr.org/2019/458

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
