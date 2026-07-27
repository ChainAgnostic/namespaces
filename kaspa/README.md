---
namespace-identifier: kaspa
title: Kaspa Ecosystem
author: Luke Dunshea (@elldeeone)
discussions-to: https://kas-smiths.org/t/kaspa-x402-pay-per-request-kas-payments-for-apis-and-ai-agents/15
status: Draft
type: Informational
created: 2026-07-27
requires: ["CAIP-2", "CAIP-10"]
---

# Namespace for Kaspa chains

## Introduction

Blockchains in the `kaspa` namespace are identified by the network names defined by the Rusty Kaspa `NetworkId` implementation.
Kaspa is a proof-of-work Layer 1 that orders blocks using blockDAG consensus and uses a native UTXO transaction model.
It has its own consensus protocol, RPC interfaces, transaction serialization, and address encoding.

Although Kaspa uses UTXOs, it does not implement Bitcoin or the BIP-122 chain-identification method.
The `kaspa` namespace therefore identifies Kaspa networks directly rather than placing them in the `bip122` namespace.

## Syntax

The namespace `kaspa` refers to the Kaspa open-source blockchain platform.
The initial profiles cover Kaspa mainnet and the stable public testnet-10 network.

## References

- [Kaspa][] - Kaspa project website
- [Rusty Kaspa][] - Kaspa reference-node implementation
- [Kaspa Community Discussion][] - Community review of the identifier convention

[Kaspa]: https://kaspa.org/
[Rusty Kaspa]: https://github.com/kaspanet/rusty-kaspa
[Kaspa Community Discussion]: https://kas-smiths.org/t/kaspa-x402-pay-per-request-kas-payments-for-apis-and-ai-agents/15

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
