---
namespace-identifier: polkadot
title: Polkadot Namespace
author: ["Pedro Gomes (@pedrouid)", "Joshua Mir (@joshua-mir)", "Shawn Tabrizi (@shawntabrizi)", "Juan Caballero (@bumblefudge)", "Antonio Antonino (@ntn-x2)"]
status: Draft
type: Informational
created: 2020-04-01
updated: 2023-02-22
replaces: CAIP-13
---

# Polkadot Namespace

## Introduction

These documents define the syntax and canonical references of the CASA URI schemes for the Polkadot namespace. 

It is important for developers new to the Polkadot ecosystem to know that, unlike many other namespaces, the exact execution environment, RPC methods, block sizes and other core features of a Polkadot-based blockchain vary widely in a very layered and modular architecture based on "pallets": components of a blockchain runtime (i.e., VM) composed of storage and a set of functions to operate on that storage.

Polkadot-based blockchains can be of two types: parachains or solo chains.
In the first case, a parachain represents L1 infrastructure with a 12s block time that relies on the security properties of the L0 relay chain its blocks are anchored onto.
The two relaychains currently deployed in a production environment are Polkadot and Kusama, with the latter being only an economically-incentivized canary network.
Relay chains have a 6s block time and are secured by a [Nominated Proof of Stake (NPoS) consensus protocol][polkadot-consensus] which provides deterministic block finalization.

The mentioned architecture creates an environment for complex "cross-chain" use cases between Polkadot-based chains.
Within the framework of the Cross-Chain Messaging [XCM][], cross-chain interactions are enabled by `MultiLocation`s: ways of describing the source and the destination of an XCM message that is agnostic with respect to the consensus system the two actors are part of.
Because with the release of XCM v3 `MultiLocation`s have been updated to always refer to "absolute" locations of source and destination, they represent a suitable starting point for CASA-style addressing.

## References

- [Polkadot documentation][]: Homepage for ecosystem-wide developer documentation
- [Polkadot public RPC endpoints][]: for dev/testing purposes
- [XCM]: Cross Consensus Messaging defies an addressing network across 

[polkadot-consensus]: https://wiki.polkadot.network/docs/learn-consensus
[Polkadot documentation]: https://wiki.polkadot.network/
[Polkadot public RPC endpoints]: https://wiki.polkadot.network/docs/maintain-endpoints
[XCM]: https://wiki.polkadot.network/docs/learn-xcm

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
