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
a feeless account-chain payment network where value transfers are represented as native Atto blocks and transactions.

Atto is a native layer-1 system with its own chain model, transaction encoding, and account addressing, all defined by the Atto protocol.

The purpose of this namespace is to provide stable chain identifiers for Atto networks and a neutral reference point for cross-chain tooling built on CAIPs.

## Rationale

Atto needs its own namespace because it introduces a distinct execution and validation model.
Native account-chain semantics, address encoding, and transaction serialization do not fit under existing namespaces such as EVM, Solana, or Stellar.
A dedicated namespace allows tools to refer to Atto deployment environments consistently using human-readable CAIP-2 identifiers.

## Governance

This namespace tracks the Atto protocol and its network identifiers as defined by the Atto ecosystem maintainers.
Future CAIP profiles for Atto should follow this namespace to document account IDs, asset IDs, and other ecosystem-specific conventions.
Public network naming should remain stable over time to ensure long-term interoperability.

## References

- [Documentation][] - Official documentation for the Atto ecosystem.
- [Node API Reference][] - Reference for the Atto node RPC and REST interfaces.
- [Integration Guide][] - Overview of Atto components, integration model, and operational guidance.
- [GitHub][] - Source code and development resources.

[Documentation]: https://atto.cash/docs
[Node API Reference]: https://atto.cash/api/node
[Integration Guide]: https://atto.cash/docs/integration
[GitHub]: https://github.com/attocash

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
