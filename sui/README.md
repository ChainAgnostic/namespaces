---
namespace-identifier: sui
title: Sui Ecosystem
author: William Robertson (@williamrobertson13)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/146
status: Draft
type: Informational
created: 2025-06-18
updated: 2025-06-18
---

# Namespace for Sui Chains

Sui is a smart contract platform that uses a Move-based, object-centric data model and is optimized for parallel execution. Transactions in Sui operate on objects rather than accounts, allowing independent operations to be executed in parallel without coordination. This enables high throughput while preserving safety and determinism.

A Sui network is maintained by a validator committee responsible for processing transactions, reaching consensus, and producing checkpoint digests — cryptographic summaries of network state at fixed intervals. These checkpoints serve as the canonical state and ensure consistency across nodes.

Each network is uniquely identified by its genesis checkpoint digest — the cryptographic hash of the very first checkpoint, signed by the original validator set. This digest anchors the network’s identity in verifiable history and validator consensus.

## Rationale

Because chain identity and state in Sui revolve around checkpoints and objects rather than blocks and accounts, standard CAIP identifiers (e.g., for chains, accounts, and assets) must be adapted accordingly.

This namespace defines how Sui’s architecture maps to cross-chain standards to support consistent and interoperable multi-chain tooling.

## Governance

Sui protocol upgrades and standards are coordinated by the Sui Foundation in collaboration with core contributors and the broader developer community. Changes are proposed through SIPs (Sui Improvement Proposals), with open discussion and reference implementations maintained on GitHub.

## References

- [Sui Docs] — Developer documentation and concept overviews for building on Sui.
- [Sui GitHub] — Official GitHub repository for the Sui smart contract platform.
- [Sui SIPs] — Official GitHub repository for Sui Improvement Proposals.

[Sui Docs]: https://docs.sui.io/
[Sui GitHub]: https://github.com/MystenLabs/sui
[Sui SIPs]: https://github.com/sui-foundation/sips

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
