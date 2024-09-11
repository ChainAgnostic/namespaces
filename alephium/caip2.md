---
namespace-identifier: alephium-caip2
title: Alephium Blockchain ID Specification
author: Hongchao Liu (@h0ngcha0)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/117
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
into distinct groups. The blockchain id includes both the network id
and the group information.

Each transaction has an origin and destination group. All transactions
from by addresses in group `G1` to addresses in group `G2` will be
included in chain `G1 -> G2`. If there are `G` groups on Alephium,
there will be `G`*`G` chains inside of it. In Alephium, groups are
like cities and chains are like roads connecting them.

Both contract and address belong to a group. A contract deployed in
one group can only be interacted with directly with an address from
the same group. Therefore it is common for a dApp deployed in one
group to request connection to an address within the same
group. However a dApp deployed in all groups might request connection
with an address from any group.

The Network id can be one of three values: `mainnet`, `testnet` and
`devnet`.

Currently, Alephium has 4 groups. The group component of the
blockchain id can take one of five values: `0`, `1`, `2` and `3` which
correspond to groups `0` through `3`, and `-1` which represents any
group.

### Syntax

The `chain_id` is a case-insensitive string in the form

```
chain_id:    alephium + ":" + group + "_" + network_id
network_id:  mainnet, testnet or devnet
group:       0, 1, 2, 3 or -1
```

For information that is not network or group specific, there is a
special chain id `alephium:universal`.

## Test Cases

This is a list of manually composed examples

```
# Alephium mainnet, group 0
alephium:0_mainnet

# Alephium testnet, any group
alephium:-1_testnet

```

## References

- [Blockflow](https://medium.com/@alephium/an-introduction-to-blockflow-alephiums-sharding-algorithm-bbbf318c3402)
- [API Endpoints](https://node.mainnet.alephium.org/docs/)

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
