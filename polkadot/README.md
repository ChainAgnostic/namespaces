---
namespace-identifier: polkadot
title: Polkadot Namespace
author: ["Pedro Gomes (@pedrouid)", "Joshua Mir (@joshua-mir)", "Shawn Tabrizi (@shawntabrizi)", "Juan Caballero (@bumblefudge)"]
status: Draft
type: Informational
created: 2020-04-01
updated: 2022-03-27
replaces: CAIP-13
---

# Polkadot Namespace

## Introduction

These documents defines the syntax and canonical references of the CASA URI schemes
for the Polkadot namespace. 

It is important for developers new to the ecosystem to know that unlike other
namespaces, the exact execution environment, RPC methods, block sizes and other
core features of a blockchain vary widely in a very layered and modular
architecture based on "pallets" (Rust crates that extend the virtual machine and
consensus). This creates an environment for complex "cross-chain" development
between polkadots chains that may have shared security or common resources via
coordination chains but also may not. Within the framework of the
Cross-Consensus Messaging [XCM][], cross-chain interactions are enabled but a
polkadot-wide meta-chain data model; moving beyond the "relative addressing" of
earlier forms of the Polkadot-wide `Multilocation` type, addressing in the
"absolute mode" introduced by XCM v3 is the starting point for CASA-style
addressing. 

## References

- [Polkadot documentation][]: Homepage for ecosystem-wide developer documentation
- [Polkadot-ENS tutorial][]: A tutorial for native Kusama address support in the ENS front-end
- [Polkadot public RPC endpoints][]: for dev/testing purposes
- [Polkadot identity system][]: Introduction to on-chain identity registrars 
- [Polkadot address explainer][]: A quick overview of how network-specific,
      self-describing addresses can derive from the same private key
- [Polkadot subscan tool][]: A tool for transforming addresses according to SS58 across polkadot networks
- [XCM]: Cross Consensus Messaging defies an addressing network across 

[Polkadot address explainer]: https://www.quora.com/How-do-different-wallet-addresses-work-on-Polkadot-and-Kusama
[Polkadot identity system]: https://wiki.polkadot.network/docs/learn-identity
[Polkadot public RPC endpoints]: https://wiki.polkadot.network/docs/maintain-endpoints
[Polkadot documentation]: https://wiki.polkadot.network/
[Polkadot subscan tool]: https://polkadot.subscan.io/tools/ss58_transform?
[Polkadot-ENS tutorial]: https://wiki.polkadot.network/docs/ens
[SS58]: https://docs.substrate.io/v3/advanced/ss58/
[SS58 registry]: https://github.com/paritytech/ss58-registry/blob/main/ss58-registry.json
[multiaddress]: https://github.com/multiformats/multiaddr#specification
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-21]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-21.md
[CAIP-22]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-22.md
[EIP155]: https://eips.ethereum.org/EIPS/eip-155
[ERC20]: https://eips.ethereum.org/EIPS/eip-20
[ERC721]: https://eips.ethereum.org/EIPS/eip-721

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
