---
namespace-identifier: tezos-caip10
title: Tezos Namespace - Addresses
author: Qibing Li (@QibingLee)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/40
status: Draft
type: Standard
created: 2022-12-06
updated: 2023-01-17
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

_For context, see the [CAIP-10][] specification._

## Rationale

Tezos supports the use of multiple public-key signature schemes, so the display
address is prefixed with `tz1` (Ed25519 curve), `tz2` (Secp256k1 curve), or
`tz3` (P256 curve). After the prefix, the rest of the account address is a
[base58][] hash of each key's public key.

## Syntax

The syntax of a Tezos address matches the following regular expression (note the
58-character alphabet):

`(tz1|tz2|tz3) [1-9A-HJ-NP-Za-km-z]{33}`

## Chain IDs

_For context, see the [CAIP-2][] specification or the `tezos-caip2` profile thereof._

| Network Name | Chain ID                         |
| ------------ | -------------------------------- |
| Mainnet      | NetXdQprcVkpaWU |
| Delphinet    | NetXm8tYqnMWky1 |

## Test Cases

```
# Tezos Mainnet
tezos:NetXdQprcVkpaWU:tz1MVqWiyfMbSESTaGEPxFjDWdM9zSXy1hcg

# Tezos DelphiNet (Current active testnet)
tezos:NetXm8tYqnMWky1:tz3gN8NTLNLJg5KRsUU47NHNVHbdhcFXjjaB
```

## References

- [Tezos Smart Contract](https://opentezos.com/tezos-basics/smart-contracts#general-definition-of-a-tezos-smart-contract): General definition of a Tezos smart contract
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md): Blockchain ID Specification
- [CAIP-10](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md): Account ID Specification

[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/8fdb5bfd1bdf15c9daf8aacfbcc423533764dfe9/CAIPs/caip-10.md
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[Base58]: https://datatracker.ietf.org/doc/html/draft-msporny-base58-03

## Rights

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
