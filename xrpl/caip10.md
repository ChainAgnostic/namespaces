---
namespace-identifier: xrpl-caip10
title: XRP Ledger Namespace - Addresses
author: Anton Dalgren (@antondalgren)
status: Draft
type: Standard
created: 2023-02-23
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

In CAIP-10, a string-based general account address scheme is defined. XRPL addresses are identified by an address in the XRP Ledger's base58 encoding. The address is derived from an account's master public key. An XRPL address is a string with the following characteristics.
* It is between 25 and 35 characters long.
* It starts with the character `r`
* It uses alpanumerical characters excluding number `0`, lowercase letter `"l"` and capital letters `["O", "I"]`.
* It is case-sensitive
* It includes a 4-byte checksum making the probabilty of generating a valid address from random characters approximately 1 in 2<sup>32</sup>

### Syntax

The `account_id` is a case-sensitive string in the form:

```
account_id:        chain_id + ":" + account_address
chain_id:          See [CAIP-2][]
account_address:   r[1-9a-hj-zA-HJ-NP-Z]{24,34}
```

### Semantics

The `chain_id` is specified by the [CAIP-2][] which describes the blockchain id.
The `account_address` is the address to an account on the XRPL.

## Test Cases

This is a list of manually composed examples

```
# Livenet address
xrpl:0:r4FTvnahbUfhe1WK2EK5Jz4cNvdFvT8Dzt

# Testnet address
xrpl:1:rEBakx2WdNsmRb5tm5KmhsqKAqvLJrRoiU

# Devnet address
xrpl:2:rUgna78QFFeixu8v9ZqwtViWnknXYtHG2X
```

## Backwards Compatibility

Not applicable

## References

- [XRPL Address Definition][] - The explanation of a XRPL Address, what it consists of and what limitations it has.
- [XRPL Base58 Encoding][] - Explains how a public key is encoded to a XRPL address.


[CAIP-2]: ./caip2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[XRPL Address Definition]: https://xrpl.org/accounts.html#addresses
[XRPL Base58 Encoding]: https://xrpl.org/base58-encodings.html

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

