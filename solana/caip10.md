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
| Mainnet      | 5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp |
| Devnet       | EtWTRABZaYq6iMfeYKouRu166VU2xqa1 |
| Testnet      | 4uhcVJyU9pJkvQyS88uRDiswHXSCkY3z |

## Test Cases

```
# Solana Mainnet
solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp:7S3P4HxJpyyigGzodYwHtCxZyUQe9JiBMHyRWXArAaKv

# Solana Devnet
solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1:DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK

# Solana Testnet
solana:4uhcVJyU9pJkvQyS88uRDiswHXSCkY3z:6LmSRCiu3z6NCSpF19oz1pHXkYkN4jWbj9K1nVELpDkT
```

## References

[Validating Account Addresses](https://docs.solana.com/integrations/exchange#validating-user-supplied-account-addresses-for-withdrawals)
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md

## Rights

Copyright and related rights waived via CC0.
