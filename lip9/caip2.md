---
namespace-identifier: lip9-caip2
title: LIP9 Namespace, aka Lisk - Chains
author: Simon Warta (@webmaster128)
discussions-to: https://github.com/ChainAgnostic/CAIPs/issues/7, https://github.com/ChainAgnostic/CAIPs/pull/1
status: Draft
type: Standard
created: 2019-12-05
updated: 2020-01-16
requires: CAIP-2
supersedes: CAIP-6
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for the Lisk ecosystem as defined in [LIP-9][].

## Semantics

The definition is delegated to LIP9. 

## Syntax

The reference format is a 16 character string extracted from the first 16
characters of the network identifier defined in LIP9 (a 64-character SHA256 hash
in lowercase hex).

### Backwards Compatibility

LIP-9 introduced a hard fork, but no cross-fork/cross-chain replay protection
(or other validating chain identification scheme) predates it.

## Test Cases

This is a list of manually composed examples

```
# Lisk Mainnet (https://github.com/LiskHQ/lips/blob/master/proposals/lip-0009.md#appendix-example)
lip9:9ee11e9df416b18b

# Lisk Testnet (echo -n "da3ed6a45429278bac2666961289ca17ad86595d33b31037615d4b8e8f158bbaLisk" | sha256sum | head -c 16)
lip9:e48feb88db5b5cf5
```

## References

- [LIP-9] - The Lisk Improvement Proposal that defined chain IDs for making
  transactions resistant to cross-chain and cross-fork replay.
 
[LIP-9]: https://github.com/LiskHQ/lips/blob/main/proposals/lip-0009.md#specification

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).