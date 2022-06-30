---
namespace-identifier: solana-caip10
title: Solana Namespace - Addresses
author: Haardik (@haardikk21)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/26
status: Draft
type: Standard
created: 2022-06-08
updated: 2022-06-08
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

_For context, see the [CAIP-10][] specification._

## Rationale

Solana "addresses" are base-58 encoded 256-bit Ed25519 public keys with length varying from 32 to 44 characters.

## Syntax

The syntax of a Solana address matches the following regular expression:

`[1-9A-HJ-NP-Za-km-z]{32,44}`

## Chain IDs

_For context, see the [CAIP-2][] specification._

| Network Name | Chain ID                         |
| ------------ | -------------------------------- |
| Mainnet      | 4sGjMW1sUnHzSxGspuhpqLDx6wiyjNtZ |
| Devnet       | 8E9rvCKLFQia2Y35HXjjpWzj8weVo44K |

## Test Cases

```
# Solana Mainnet
solana:4sGjMW1sUnHzSxGspuhpqLDx6wiyjNtZ:7S3P4HxJpyyigGzodYwHtCxZyUQe9JiBMHyRWXArAaKv

# Solana Devnet
solana:8E9rvCKLFQia2Y35HXjjpWzj8weVo44K:DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK
```

## References

[Validating Account Addresses](https://docs.solana.com/integrations/exchange#validating-user-supplied-account-addresses-for-withdrawals)
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md

## Rights

Copyright and related rights waived via CC0.
