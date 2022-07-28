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

Address string concatenates 2 fields without whitespace or dividers: a 1-byte version prefix and a 20-byte hash of any one of the following:
- A single secp256k1 public key (either compressed or uncompressed)
- A Bitcoin p2sh multisig script
- A Bitcoin p2wpkh-p2sh script
- A Bitcoin p2wsh-p2sh script
Valid CAIP-10 `account_id`s in this namespace are represented as [c32check][]-encoded addresses. The addresses are always all-caps.

A regular expression for validating the `account_id` can be defined as:
```
stacks:S[A-Z0-9]{30-40}
```

## Test Cases

```
# Stacks mainnet, p2pkh input = a46ff88886c2ef9762d970b4d2c63678835bd39d
stacks:1:SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7

# Stacks testnet
stacks:2147483648:ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM
```

## References

- [SIP-005][]
- [c32check][] documentation
- [c32check typescript implementation][] on github

[SIP-005]: https://github.com/stacksgov/sips/blob/main/sips/sip-005/sip-005-blocks-and-transactions.md
[c32check]: https://github.com/stacks-network/c32check#how-it-works
[c32check typescript implementation]: https://github.com/stacks-network/c32check
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
