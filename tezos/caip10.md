---
namespace-identifier: tezos-caip10
title: Tezos Namespace - Addresses
author: Qibing Li (@QibingLee)
discussions-to: TBA
status: Draft
type: Standard
created: 2022-12-06
updated: 2022-12-06
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

_For context, see the [CAIP-10][] specification._

## Rationale

Tezos account is linked to a manager, which owns the public key. The hash of the public key outputs an address. Tezos supports the use of multiple public-key signature schemes, so the address prefix starts with `tz1` (Ed25519 curve), `tz2` (Secp256k1 curve), or `tz3` (P256 curve).

## Syntax

The syntax of a Tezos address matches the following regular expression:

`(tz1|tz2|tz3) [1-9A-HJ-NP-Za-km-z]{33}`

## Chain IDs

_For context, see the [CAIP-2][] specification._

| Network Name | Chain ID                         |
| ------------ | -------------------------------- |
| Mainnet      | NetXdQprcVkpaWU |
| Devnet       | NetXm8tYqnMWky1 |


## Test Cases

```
# Tezos Mainnet
tezos:NetXdQprcVkpaWU:tz1MVqWiyfMbSESTaGEPxFjDWdM9zSXy1hcg

# Tezos DelphiNet (Current active testnet)
tezos:NetXm8tYqnMWky1:tz3gN8NTLNLJg5KRsUU47NHNVHbdhcFXjjaB
```

## References

[Tezos Smart Contract](https://opentezos.com/tezos-basics/smart-contracts#general-definition-of-a-tezos-smart-contract)
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md

## Rights

Copyright and related rights waived via CC0.