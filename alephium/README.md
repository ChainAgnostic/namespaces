---
namespace-identifier: alephium
title: Alephium Ecosystem
author: Hongchao Liu (@h0ngcha0)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/xxxx
status: Draft
type: Informational
created: 2024-06-19
requires: ["CAIP-2", "CAIP-10", "CAIP-19"]
---

# Namespace for Alephium Blockchains

This document defines the applicability of CAIP schemes to the
blockchains of the Alephium ecosystem. 

Alephium uses the stateful UTXO model where assets are managed by
UTXOs while contract states are managed using account-based
model. Alephium is also a sharded blockchain, its state is divided
into groups, with seperate chains responsible for processing
transactions from one group to another. Alephium's mainnet currently
has 4 groups and 16 blockchains, more groups and blockchains can be
added to increase the throughput.

Understanding these concepts is helpful for interoperability with
other account-based or classic UTXO namespaces.

## Syntax

The namespace `alephium` refers to the Alephium blockchain platform.

## References

- [Official website](https://https://alephium.org/)
- [Alephium Documentation](https://docs.alephium.org/)
- [Stateful UTXO](https://medium.com/@alephium/an-introduction-to-the-stateful-utxo-model-8de3b0f76749)
- [Blockflow](https://medium.com/@alephium/an-introduction-to-blockflow-alephiums-sharding-algorithm-bbbf318c3402)

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).