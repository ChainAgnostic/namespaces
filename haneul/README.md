---
namespace-identifier: haneul
title: Haneul Ecosystem
author: Geunhwa Jeong (@GeunhwaJeong)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/XXX
status: Draft
type: Informational
created: 2026-01-19
updated: 2026-01-19
---

# Namespace for Haneul Chains

Haneul is a Layer 1 smart contract platform that uses a Move-based, object-centric data model and is optimized for parallel execution. Transactions in Haneul operate on objects rather than accounts, allowing independent operations to be executed in parallel without coordination. This enables high throughput while preserving safety and determinism.

A Haneul network is maintained by a validator committee responsible for processing transactions, reaching consensus, and producing checkpoint digests — cryptographic summaries of network state at fixed intervals. These checkpoints serve as the canonical state and ensure consistency across nodes.

Each network is uniquely identified by its genesis checkpoint digest — the cryptographic hash of the very first checkpoint, signed by the original validator set. This digest anchors the network's identity in verifiable history and validator consensus.

## Rationale

Because chain identity and state in Haneul revolve around checkpoints and objects rather than blocks and accounts, standard CAIP identifiers (e.g., for chains, accounts, and assets) must be adapted accordingly.

This namespace defines how Haneul's architecture maps to cross-chain standards to support consistent and interoperable multi-chain tooling.

## Governance

Haneul protocol upgrades and standards are coordinated by Haneul Labs in collaboration with core contributors and the broader developer community. Changes are proposed through HIPs (Haneul Improvement Proposals), with open discussion and reference implementations maintained on GitHub.

## References

- [Haneul GitHub] — Official GitHub repository for the Haneul blockchain.
- [Haneul TypeScript SDK] — Official TypeScript SDK for Haneul.

[Haneul GitHub]: https://github.com/GeunhwaJeong/haneul
[Haneul TypeScript SDK]: https://github.com/GeunhwaJeong/haneul-ts-sdks

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
