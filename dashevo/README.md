---
namespace-identifier: dashevo
title: Dash Platform (Evo)
author: ["PastaPastaPasta (@PastaPastaPasta)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/177
status: Draft
type: Informational
created: 2026-03-11
updated: 2026-03-11
requires: ["CAIP-2", "CAIP-10"]
---

# Namespace for Dash Platform

[Dash Platform][] is an application layer built on top of the [Dash][] payment network.
It uses [Tenderdash][] (a Dash fork of Tendermint) for consensus and provides a decentralized identity and data contract system.
Unlike Dash Core, which operates on a UTXO-based payment model under the [bip122][] namespace, Dash Platform uses an identity-based account model where users register identities, deploy data contracts, and create documents on a separate consensus layer.

## Rationale

A separate namespace is required because Dash Platform differs fundamentally
from Dash Core (bip122) in every dimension relevant to chain addressing:

- **Consensus engine**: Tenderdash (Tendermint fork) vs Bitcoin-derived PoW/PoSe
- **Account model**: Identity-based (256-bit identifiers) vs UTXO-based addresses
- **State model**: Data contracts and documents vs transactions and outputs
- **Transport**: gRPC via [DAPI][] vs Bitcoin JSON-RPC
- **Chain IDs**: Tenderdash string identifiers (e.g. `evo1`) vs block hash genesis references

These differences mean that CAIP-2 chain references, CAIP-10 account
identifiers, and any higher-level CAIPs would have entirely incompatible
semantics if forced into the [bip122][] namespace.

## Governance

Dash Platform is governed through the [Dash Improvement Proposal][DIP] process.
Protocol changes are proposed as DIPs, discussed by the community, and implemented by [Dash Core Group][DCG].
The Tenderdash consensus layer inherits governance from the broader Dash masternode network, where masternodes vote on proposals and protocol upgrades.

## References

- [Dash][] - Dash project homepage
- [Dash Platform docs][] - Official Dash Platform documentation
- [Dash Platform][] - Dash Platform monorepo (source code)
- [Tenderdash][] - Tenderdash consensus engine (Dash fork of Tendermint)
- [DAPI][] - Decentralized API for Dash Platform
- [DIP][] - Dash Improvement Proposals
- [DCG][] - Dash Core Group
- [bip122][] - BIP122 namespace used by Dash Core for payment transactions

[Dash]: https://www.dash.org/
[Dash Platform docs]: https://docs.dash.org/
[Tenderdash]: https://github.com/dashpay/tenderdash
[DAPI]: https://docs.dash.org/projects/platform/en/stable/docs/reference/dapi-endpoints.html
[DIP]: https://github.com/dashpay/dips
[Dash Platform]: https://github.com/dashpay/platform
[DCG]: https://www.dash.org/dcg/
[bip122]: https://github.com/ChainAgnostic/namespaces/tree/main/bip122
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
