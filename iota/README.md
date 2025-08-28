---
namespace-identifier: iota
title: IOTA
author: Enrico Marconi (@UMR1352)
status: Draft
type: Informational
created: 2025-07-28
---

# Namespace for IOTA networks

IOTA is a Move-based smart contract platform designed for high performance. Unlike traditional blockchains
that use accounts and process transactions sequentially, IOTA uses an object-centric data model.
This allows transactions to operate on individual objects, enabling them to be executed in parallel without
needing to be coordinated. This architecture ensures high throughput while maintaining security and consistency.

The IOTA network is maintained by a committee of validators. These validators are responsible for processing
transactions and creating checkpoint digests, which are cryptographic summaries of the network's state at regular
intervals. These checkpoints are crucial because they serve as the official, canonical state of the network.

Each IOTA network has a unique identity, established by its genesis checkpoint digest. This is the cryptographic
hash of the very first checkpoint, signed by the original validators. This digest acts as a verifiable anchor for
the network’s identity.

## Rationale

This distinct design - which focuses on checkpoints and objects instead of blocks and accounts - requires a special
approach to integrate with standard cross-chain identifiers (CAIPs).

This new namespace provides the necessary framework to map [IOTA's architecture][IOTA Docs] to these standards, ensuring
compatibility and interoperability with multi-chain tools.

## Governance

The IOTA Foundation coordinates protocol upgrades and standards by working with core contributors and the developer
community. Proposed changes go through an open process called [IOTA Improvement Proposals][IOTA IIPs] (IIPs), with discussions
and reference implementations maintained on [GitHub][IOTA Github].

## References

- [IOTA Docs] - Developer documentation and cencept overviews for for building on IOTA.
- [IOTA GitHub] - Official GitHub repository for the IOTA smart contract platform.
- [IOTA IIPs] - Official GitHub repository for IOTA Improvement Proposals.

[IOTA Docs]: https://docs.iota.org
[IOTA GitHub]: https://github.com/iotaledger/iota
[IOTA IIPs]: https:/github.com/iotaledger/IIPs

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
