---
namespace-identifier: iota
title: IOTA
author: Enrico Marconi (@UMR1352)
status: Draft
type: Informational
created: 2025-07-28
---

# Namespace for IOTA networks

IOTA is a smart contract platform that uses a Move-based, object-centric data model and is optimized for
parallel execution.
Transactions in IOTA operate on objects rather than accounts, allowing independent operations to be executed
in parallel without coordination.
This enables high throughput while preserving safety and determinism.

An IOTA network is maintained by a validator committee responsible for processing transactions,
reaching consensus, and producing checkpoint digests — cryptographic summaries of network state at fixed
intervals.
These checkpoints serve as the canonical state and ensure consistency across nodes.

Each network is uniquely identified by its genesis checkpoint digest — the cryptographic hash of the very
first checkpoint, signed by the original validator set. This digest anchors the network’s identity in
verifiable history and validator consensus.

## Rationale

Because chain identity and state in IOTA revolve around checkpoints and objects rather than blocks 
and accounts, standard CAIP identifiers (e.g., for chains, accounts, and assets) must be adapted accordingly.

This namespace defines how IOTA’s architecture maps to cross-chain standards to support consistent and
interoperable multi-chain tooling.

## Governance

IOTA protocol upgrades and standards are coordinated by the IOTA Foundation in collaboration with core
contributors and the broader developer community. Changes are proposed through IIPs (IOTA Improvement
Proposals), with open discussion and reference implementations maintained on GitHub.

## References

- [IOTA Docs] - Developer documentation and cencept overviews for for building on IOTA.
- [IOTA GitHub] - Official GitHub repository for the IOTA smart contract platform.
- [IOTA IIPs] - Official GitHub repository for IOTA Improvement Proposals.

[IOTA Docs]: https://docs.iota.org
[IOTA GitHub]: https://github.com/iotaledger/iota
[IOTA IIPs]: https:/github.com/iotaledger/IIPs

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
