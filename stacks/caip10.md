---
namespace-identifier: stacks-caip10
title: Stacks Namespace - Addresses
author: Léo Pradel @pradel, Greg Ogunyanwo @gregogun
discussions-to: https://forum.stacks.org/t/caip-2-and-caip-10-stacks-specification/13290
status: Draft
type: Standard
created: 2022-06-07
requires: "CAIP-10"
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

Stacks aligns squarely with the "account" model rather than the "UXTO" model but
uses the format "c32check" to address the "account" model.

## Syntax

Address contains 2 fields, 1 byte version and 20 byte hash of one of the following:
- A single secp256k1 public key (either compressed or uncompressed)
- A Bitcoin p2sh multisig script
- A Bitcoin p2wpkh-p2sh script
- A Bitcoin p2wsh-p2sh script
Valid CAIP-10 `account_id`s in this namespace are represented as c32check-encoded addresses.

A regular expression for validating the `account_id` can be defined as:
```
stacks:S[A-Z0-9]{40}
```

## Test Cases

```
# Stacks mainnet
stacks:1:SP2X0TZ59D5SZ8ACQ6YMCHHNR2ZN51Z32E2CJ173

# Stacks testnet
stacks:2147483648:ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM
```

## References

- [SIP-005][]
- [c32check documentation][]

[SIP-005]: https://github.com/stacksgov/sips/blob/main/sips/sip-005/sip-005-blocks-and-transactions.md
[c32check documentation]: https://github.com/stacks-network/c32check#how-it-works
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
