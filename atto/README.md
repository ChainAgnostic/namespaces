---
namespace-identifier: atto
title: Atto Ecosystem
author: Felipe Rotilho (@rotilho)
status: Draft
type: Informational
created: 2026-03-18
---

# Namespace for Atto Networks

## Introduction

The `atto` namespace refers to the Atto ecosystem:
a fee-less account-chain payment network where value transfers are represented as native Atto blocks and transactions.

Atto is a native layer-1 system with its own chain model, transaction encoding, and account addressing, all defined by the Atto protocol.

The purpose of this namespace is to provide stable chain identifiers for Atto networks and a neutral reference point for cross-chain tooling built on CAIPs.

## Rationale

Atto needs its own namespace because it introduces a distinct execution and validation model.
Native account-chain semantics, address encoding, and transaction serialization do not fit under existing namespaces such as EVM, Solana, or Stellar.
A dedicated namespace allows tools to refer to Atto deployment environments consistently using human-readable CAIP-2 identifiers.

## Governance

This namespace tracks the public Atto protocol as documented by the ecosystem's maintainers.
Protocol-level changes and governance-relevant decisions should be validated against public Atto materials, especially the whitepaper and official documentation, and against the implementation history in the public GitHub repositories.
Future updates to this namespace should cite those sources when describing changes to network behavior, distribution, staking, or other community-facing protocol decisions.

## References

- [Documentation][] - Official documentation for the Atto ecosystem.
- [Whitepaper][] - Public protocol and governance context, including decentralization and representative voting.
- [Node API Reference][] - Reference for the Atto node RPC and REST interfaces.
- [Integration Guide][] - Overview of Atto components, integration model, and operational guidance.
- [Blog][] - Public announcements and writeups for major ecosystem and protocol changes.
- [GitHub][] - Source code, issues, and pull requests for implementation history and concrete protocol updates.
- [Node Repository][] - Reference implementation of the Atto node and consensus behavior.

[Documentation]: https://atto.cash/docs
[Whitepaper]: https://atto.cash/docs/whitepaper
[Node API Reference]: https://atto.cash/api/node
[Integration Guide]: https://atto.cash/docs/integration
[Blog]: https://atto.cash/blog
[GitHub]: https://github.com/attocash
[Node Repository]: https://github.com/attocash/node

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
