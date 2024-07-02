---
namespace-identifier: alephium-caip10
title: Alephium Namespace - Addresses
author: Hongchao Liu (@h0ngcha0)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/117
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

The algorithm for deriving group information from `P2PKH`, `P2MPKH`
and `P2SH` address are similar:

1. Take the relevant bytes from the address. For `P2PKH` and  `P2SH`
   address, take the `content bytes` directly. For `P2MPKH` address,
   take the part of the `content bytes` corresponding to the first
   public key hash.
2. Hash the relevant bytes from step 1 using the `djb2` hash algorithm
   and perform a bitwise OR operation to the hashed value with `1`.
3. Take the result from step 2, perform bitwise XOR operation on its
   last 4 bytes to get an one byte integer.
4. The group number is the remainder of this one byte integer dividing
   the total number of groups, which is currently `4` on Alephium.

For `P2C` address, group number is encoded directly as its last byte
of its `content bytes`.

A Typescript implementation of the logic to derive group information
from address can be found
[here](https://github.com/alephium/alephium-web3/blob/b4df0f2858778dec3767a9d23737b7995d3673cb/packages/web3/src/address/address.ts#L88-L104).

## Syntax

The native Alephium address encoding is a [Base58][]-encoded string of the type defined above.
[CAIP-10][] simply uses an entire native address as the `account_address` component.

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
