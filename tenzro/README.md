---
namespace-identifier: tenzro
title: Tenzro Ecosystem
author: Tenzro Engineering (eng@tenzro.com)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/184
status: Draft
type: Informational
created: 2026-05-02
updated: 2026-05-02
---

# Namespace for Tenzro chains

## Introduction

Blockchains in the "tenzro" namespace are validated by their genesis block hash.
Tenzro is an L1 settlement layer designed for AI-age applications: each chain in
the namespace runs HotStuff-2 BFT consensus over a multi-VM execution layer
(EVM, SVM, and Canton/DAML) with a single shared native balance per asset (the
Sei-V2-style pointer model). The namespace covers all networks operated under
this protocol regardless of which VM façade a wallet or dApp interacts with.

## Syntax

The namespace "tenzro" refers to the Tenzro Network protocol — see the
project repository at <https://github.com/tenzro/tenzro-network> and the
whitepaper at <https://tenzro.com>. Implementations of this namespace expose
both an EVM-compatible JSON-RPC surface (`eth_*`, `chain_id` integer) and a
Tenzro-native namespace (`tenzro_*`, including multi-VM scope methods).

## Multi-VM façades

A single Tenzro chain (one `tenzro:<reference>` identifier) hosts three
execution-layer façades over a shared state:

- **EVM** — reachable via `eth_*` JSON-RPC; the integer `chain_id` returned
  by `eth_chainId` is exposed for compatibility with EVM tooling but is
  **not** a separate CAIP-2 reference.
- **SVM** — Solana VM bytecode runs natively. SPL Token instructions are
  mapped to the Tenzro native token registry; SPL amounts are 9-decimal
  values that get truncated to match the underlying token's stored
  precision.
- **Canton/DAML** — DAML 3.x contracts execute against the same shared
  state; CIP-56 holdings are first-class.

Each façade reads and writes the same balances and storage. SVM and Canton
account references therefore resolve under `tenzro:`, not under `solana:`
or any Canton-specific namespace; the underlying chain is identified by
its Tenzro genesis hash regardless of which façade a caller uses.

## References

- [Tenzro Network repository][repo]
- [HotStuff-2 BFT][hs2] — consensus algorithm
- [Sei V2 pointer model][sei2] — basis for Tenzro's multi-VM token architecture

[repo]: https://github.com/tenzro/tenzro-network
[hs2]: https://eprint.iacr.org/2023/397.pdf
[sei2]: https://blog.sei.io/sei-v2-the-first-parallelized-evm/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
