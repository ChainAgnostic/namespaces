---
namespace-identifier: xrpl-caip10
title: XRP Ledger Namespace - Addresses
author: Anton Dalgren (@antondalgren)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/57/
status: Draft
type: Standard
created: 2023-02-23
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

In CAIP-10, a string-based general account address scheme is defined. XRPL
supports two address formats:

### Classic Addresses (r-addresses)

Classic XRPL addresses are identified by an address in the XRP Ledger's [base58btc][]
encoding. The address is derived from an account's master public key. A classic XRPL
address is a string with the following characteristics:

* It is between 25 and 35 characters long, inclusive.
* It starts with the character `r`
* It uses alphanumerical characters [excluding][base58btc] number `0`, lowercase
  letter `"l"` and capital letters `["O", "I"]`.
* It is case-sensitive
* It includes a 4-byte checksum making the probabilty of generating a valid address from random characters approximately 1 in 2<sup>32</sup>
* It may optionally include a destination tag appended with a hyphen (`-`) separator

### X-Addresses

X-addresses are a newer format that encode both the destination address and an
optional destination tag into a single string. An X-address has the following characteristics:

* It starts with the character `X`
* It uses base58 encoding (same character set as r-addresses)
* It is case-sensitive
* It encodes both the classic address and destination tag in a single value
* It includes a checksum for validation

### Syntax

The `account_id` is a case-sensitive string in the form:

```
account_id:        chain_id + ":" + account_address
chain_id:          See [CAIP-2][]
account_address:   classic_address | x_address
classic_address:   r[1-9a-hj-zA-HJ-NP-Z]{24,34} + optional_tag
optional_tag:      ("-" + [0-9]+)?
x_address:         X[1-9a-hj-zA-HJ-NP-Z]{46,47}
```

### Semantics

The `chain_id` is specified by the [CAIP-2][] which describes the blockchain id.

The `account_address` represents an account on the XRPL and can be expressed in two formats:

1. **Classic Address (r-address)**: A base58-encoded address optionally followed by a destination tag. The destination tag is a numeric identifier (0 to 2^32-1) used to identify a specific recipient or purpose at the destination address. When included, the tag is separated from the address by a hyphen (`-`).

2. **X-Address**: A compact format that encodes both the classic address and destination tag (if any) into a single base58-encoded string starting with `X`. X-addresses eliminate the need for separate tag handling and reduce user error.

## Test Cases

This is a list of manually composed examples

```
# Livenet classic address (without tag)
xrpl:0:r4FTvnahbUfhe1WK2EK5Jz4cNvdFvT8Dzt

# Testnet classic address (without tag)
xrpl:1:rEBakx2WdNsmRb5tm5KmhsqKAqvLJrRoiU

# Devnet classic address (without tag)
xrpl:2:rUgna78QFFeixu8v9ZqwtViWnknXYtHG2X

# Classic address with destination tag
xrpl:0:rPEPPER7kfTD9w2To4CQk6UCfuHM9c6GDY-495

# X-address (Livenet)
xrpl:0:XV5sbjUmgPpvXv4ixFWZ5ptAYZ6PD2q1qM6owqNbug8W6KV

# X-address (Testnet)
xrpl:1:TVE26TYGhfLC7tQDno7G8dGtxSkYQnSy8W3wYu
```

## Backwards Compatibility

Not applicable

## References

- [XRPL Address Definition][] - The explanation of a XRPL Address, what it consists of and what limitations it has.
- [XRPL Base58 Encoding][] - Explains how a public key is encoded to a XRPL address.
- [X-Address Format][] - Specification for the X-address format that encodes both address and destination tag.
- [Destination Tags][] - Explanation of destination tags and their use in XRPL.


[CAIP-2]: ./caip2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[base58btc]: https://en.bitcoin.it/wiki/Base58Check_encoding#Base58_symbol_chart
[XRPL Address Definition]: https://xrpl.org/accounts.html#addresses
[XRPL Base58 Encoding]: https://xrpl.org/base58-encodings.html
[X-Address Format]: https://xrpaddress.info/
[Destination Tags]: https://xrpl.org/source-and-destination-tags.html

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
