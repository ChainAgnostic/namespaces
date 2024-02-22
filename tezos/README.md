---
namespace-identifier: tezos
title: Tezos Namespace
author: Stanly Johnson (@stanly-johnson), Carlo van Driesten (@jdsika)
status: Draft
type: Informational
created: 2020-12-12
updated: 2024-02-20
replaces: CAIP-26
---

# Namespace for Tezos Blockchains

This document defines the applicability of CAIP schemes to the blockchains of
the Tezos ecosystem.

## Syntax

The namespace "tezos" refers to the Tezos open-source blockchain protocol in general. The main implementation is called [Octez][]. The [Tezos test network infrastructure][] provides an overview of the different chains maintained by the community. The Tezos Mainnet can be determined through the genesis block hash: `BLockGenesisGenesisGenesisGenesisGenesisf79b5d1CoW2`.

### Chain IDs

_For context, see the [CAIP-2][] specification and in particular the `tezos-caip2` profile thereof._

| Alias          | Chain ID                         |
| -------------- | -------------------------------- |
| tezos:mainnet  | tezos:NetXdQprcVkpaWU            |
| tezos:ghostnet | tezos:NetXnHfVqm9iesp            |

## References

- [Tezos Website][] - Official project website.
- [Octez][] - Main implementation for the Tezos standard.
- [Octez Documentation][] - How to get started with Tezos.
- [Tezos Foundation][] - Non-profit organization supporting Tezos ecosystem development.
- [CAIP-2][] - Blockchain Chain ID Specification.
- [tzstats.com Tezos Mainnet Genesis Block][] - A Tezos block explorer and the Tezos Mainnet Genesis Block.

[Tezos Website]: https://tezos.com/
[Octez]: https://research-development.nomadic-labs.com/announcing-octez.html
[Octez Documentation]: https://tezos.gitlab.io/
[Tezos Foundation]: https://tezos.foundation/
[Tezos test network infrastructure]: https://teztnets.com/
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[tzstats.com Tezos Mainnet Genesis Block]: https://tzstats.com/0

## Rights

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
