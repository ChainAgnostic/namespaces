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

Although Kaspa uses UTXOs, it does not implement Bitcoin or the [BIP-122][] chain-identification method.
The `kaspa` namespace therefore identifies Kaspa networks directly rather than placing them in the [BIP-122 Namespace][].

## Syntax

The namespace `kaspa` refers to the Kaspa open-source blockchain platform.
The initial profiles cover Kaspa mainnet and the stable public testnet-10 network.

## Governance

Kaspa is a decentralized proof-of-work network with no single governing organization or authority.
Protocol changes are developed openly and take effect through adoption by independent network participants, including node operators and miners.
The resources referenced in this profile document the network and its implementation; they are not governing authorities.

This namespace profile documents identifiers already used across the Kaspa ecosystem for interoperability.
Changes to this profile are reviewed through the CASA namespace process and should be informed by public Kaspa community discussion and implementation evidence.

## References

- [Kaspa][] - Kaspa ecosystem website
- [Kaspa Docs][] - Kaspa builder documentation
- [Rusty Kaspa][] - Kaspa full-node implementation and related SDK libraries
- [Kaspa Community Discussion][] - Community review of the identifier convention
- [BIP-122][] - Bitcoin-family URI and chain-identification method
- [BIP-122 Namespace][] - CASA namespace profile for BIP-122 chains

[Kaspa]: https://kaspa.org/
[Kaspa Docs]: https://docs.kaspa.org/
[Rusty Kaspa]: https://github.com/kaspanet/rusty-kaspa
[Kaspa Community Discussion]: https://kas-smiths.org/t/kaspa-x402-pay-per-request-kas-payments-for-apis-and-ai-agents/15
[BIP-122]: https://github.com/bitcoin/bips/blob/master/bip-0122.mediawiki
[BIP-122 Namespace]: https://namespaces.chainagnostic.org/bip122/README

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
