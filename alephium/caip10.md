---
namespace-identifier: alephium-caip10
title: Alephium Namespace - Addresses
author: Hongchao Liu (@h0ngcha0)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/xxxx
status: Draft
type: Standard
created: 2024-06-19
updated: 2024-06-19
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

An address on Alephium is a unique identifier that represents an
account or a contract. All networks share the same address format.

There are 4 different address types on Alephium:

* 0x00 - Pay to public key hash (P2PKH)
* 0x01 - Pay to multiple public key Hash (P2MPKH)
* 0x02 - Pay to script hash (P2SH)
* 0x03 - Pay to contract (P2C)

For each address type, `content bytes` are defined as follows:

- **P2PKH** - serialized public key hash
- **P2MPKH** - serialized public key hashes and multisig threshold
- **P2SH** - serialized script hash
- **P2C** - serialized contract id

Hash algorithm used is blake2b.

Constructing an address:

- **address** = `address type || content bytes`

Each address on Alephium belongs to a group, which can be derived
deterministically from the address.

## Syntax

Alephium address is represented as a Base58 encoded string.

## Test Cases

```
# P2PKH address
15EM5rGtt7dPRZScE4Z9oL2EDfj84JnoSgq3NNgdcGFyu

# P2MPKH address
2jW1n2icPtc55Cdm8TF9FjGH681cWthsaZW3gaUFekFZepJoeyY3ZbY7y5SCtAjyCjLL24c4L2Vnfv3KDdAypCddfAY

# P2C address
w7oLoY2txEBb5nzubQqrcdYaiM8NcCL9kMYXY67YfnUo

# P2SH address
ibsc1yJLJxxVcsPfSDJoR3mzrasrZq2Rn63dFQGcDAYE
```

## References

- [Alephium Documentation](https://docs.alephium.org/)
- [base58btc](https://en.bitcoin.it/wiki/Base58Check_encoding#Base58_symbol_chart)

[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
