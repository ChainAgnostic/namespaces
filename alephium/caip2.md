---
namespace-identifier: alephium-caip2
title: Alephium Blockchain ID Specification
author: Hongchao Liu (@h0ngcha0)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/xxxx
status: Draft
type: Standard
created: 2024-06-19
updated: 2024-06-19
---


## Abstract

In CAIP-2 a general blockchain identification scheme is defined. 
This is the implementation of CAIP-2 for Alephium network.

## Rationale

Alephium is a sharded blockchain that organizes addresses and states
into distinct groups groups. The blockchain id includes both the
network id and the group information.

The Network id can be one of three values: `mainnet`, `testnet` and
`devnet`. 

Currently, Alephium has 4 groups. The group component of the
blockchain id can take one of five values: `0`, `1`, `2` and `3` which
correspond to groups `0` through `3`, and `-1` which represents any
group.

### Syntax

The `chain_id` is a case-insensitive string in the form

```
chain_id:    alephium + ":" + network_id + "/" + group
network_id:  mainnet, testnet or devnet
group:       0, 1, 2, 3 or -1
```

## Test Cases

This is a list of manually composed examples

```
# Alephium mainnet, group 1
alephium:mainnet/1

# Alephium testnet, any group
alephium:testnet/-1

```

## References

- [Blockflow](https://medium.com/@alephium/an-introduction-to-blockflow-alephiums-sharding-algorithm-bbbf318c3402)
- [API Endpoints](https://node.mainnet.alephium.org/docs/)

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
