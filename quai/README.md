---
namespace-identifier: quai
title: Quai Namespace
author: ["Jonathan Downing (@jdowning100)", "Dr. K (@mechanikalk)"]
status: Draft
type: Informational
created: 2025-06-18
---

# Namespace for Quai Network

Quai is a decentralized, merge-mined, EVM-compatible Layer 1 network of blockchains that leverages a next-generation Proof-of-Work consensus mechanism called Proof-of-Entropy-Minima to eliminate block contention and provide lightning fast finality. Unlike traditional multi-chain systems, Quai uses a single global chain ID (9) for all shards and routes transactions based on address location, not per-chain logic, in which every address deterministically maps to a shard via its first byte. It supports protobuf-encoded transactions rather than RLP-encoded, setting it apart from standard Ethereum-based networks.

## Rationale

Quai’s unique architectural model necessitates a distinct namespace for proper identification and interoperability. While it shares EVM compatibility at the level of contract execution, its divergence in transaction encoding (protobuf), shard-based address space, and shared global chain ID differentiate it from traditional Ethereum forks. Currently, only one shard is active in Quai, so integration is relatively simple.

This namespace ensures that cross-chain tools such as WalletConnect, DID methods, and asset resolvers can interpret Quai’s model accurately — especially given the single-chain ID model combined with a sharded execution environment.

## Governance

Quai protocol upgrades and standards are driven by the Quai Foundation in coordination with the Quai developer community. Improvement proposals are documented via QIPs (Quai Improvement Proposals), with reference implementations and discussion led through the official GitHub repositories and Discord. Final decisions for protocol-level changes are currently stewarded by core contributors, with an aim toward more decentralized governance in future roadmap stages.

All RPC compatibility, chain metadata, and transaction standards are maintained openly at [docs.qu.ai](https://docs.qu.ai) and the [QIPs github repository](https://github.com/quai-network/qips). Developers are encouraged to participate in network design and contribute implementations via the quais.js SDK and go-quai node software repositories.

## References

- [Quai Docs][] - Official Quai documentation including address sharding, quais.js SDK and Proof-of-Entropy-Minima (PoEM) reference
- [Quai Docs: JSON-RPC][] - JSON-RPC Reference
- [go-quai Github][] - Source code repository for the node protocol implementation
- [Quai Improvement Proposals Github][] - Repository for QIPs and protocol design, including address sharding, Qi energy-based flatcoin controller design, and dynamic network expansion
- [PoEM: A Better Proof-of-Work Fork Choice Rule][] - PoEM security proof, incentive design, and selfish mining analysis
- [Quaiscan][] - Quai block explorer, currently running on shard 0, also known as cyprus-1
- [Pelagus Wallet][] - Browser extension-based wallet that allows users to hold QUAI and interact with Quai mainnet and testnet dApps
- [quais.js][] - SDK for deploying contracts and building dApps that interact with Quai

[Quai Docs]: https://docs.qu.ai
[Quai Docs: JSON-RPC]: https://docs.qu.ai/build/playground/overview#json-rpc-overview
[go-quai Github]: https://github.com/dominant-strategies/go-quai
[Quai Improvement Proposals Github]: https://github.com/quai-network/qips
[PoEM: A Better Proof-of-Work Fork Choice Rule]: https://eprint.iacr.org/2024/200
[Quaiscan]: https://quaiscan.io
[Pelagus Wallet]: https://pelgauswallet.io
[quais.js]: https://github.com/dominant-strategies/quais.js

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
