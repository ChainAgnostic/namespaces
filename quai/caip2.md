---
namespace-identifier: quai-caip2
title: Quai Namespace - Chains
author: ["Jonathan Downing (@jdowning100)", "Dr. K (@mechanikalk)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/145
status: Draft
type: Standard
created: 2025-06-18
requires: ["CAIP-2"]
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale
Quai is a merge-mined, EVM-compatible, horizontally scalable Layer 1 blockchain that leverages a novel Proof-of-Work consensus mechanism (PoEM) and address-based sharding for throughput scaling. Unlike traditional multi-chain ecosystems, Quai maintains a **single global chain ID** (`9`) across all shards, relying on address prefixing to determine shard routing.

This CAIP-2 profile defines the valid chain identifiers in the `quai` namespace, including testnet and future devnet/mainnet configurations.

The `quai` namespace requires a distinct CAIP-2 specification to:

- Encode unique blockchain references for use in WalletConnect, DID methods, and asset registries.
- Support the shared global chain ID (EIP-155: 9) model.
- Identify and distinguish Quai networks (testnet, mainnet) without needing different chain IDs for shards.
- Enable forward compatibility with Quai's expanding shard topology.

This approach ensures backward-compatible interop with Ethereum tooling while preserving Quai’s unique scalability model.

## Semantics

- **Namespace**: `quai`
- **Reference**: A short numeric identifier matching the `chainId` used by EVM-compatible clients (e.g. `9` for mainnet, `15000` for Orchard testnet, etc).
- **Address Routing**: All mainnet chains use the same global chain ID (9), but routing and execution are determined by the address prefix (see QIP-2).
- **Sharding Model**: The shard is not encoded in the chain reference but inferred from the address itself.

## Syntax

A valid `quai` CAIP-2 blockchain ID must match the pattern:
- `quai:9` — Quai Mainnet
- `quai:15000` — Quai Testnet (Orchard)

Quai does not use separate chain IDs per shard — instead, each account is routed to a shard based on its address prefix (see QIP-2). The reference is not the name of a shard or zone. Instead, it refers to a **logical environment** with its own genesis block (e.g., Quai Orchard Testnet vs Quai Mainnet). Separate chain IDs are used for mainnet (9) and Orchard testnet (15000). Thus, `<reference>` uniquely identifies the logical Quai network.

These two logical environments can also be treated as "chains" in the EVM namespaces, i.e., they can be addressed from EVM contexts unaware of sharding as [eip155][] references. For example:
- `eip155:9` - Quai Mainnet
- `eip155:15000` - Quai Testnet (Orchard)

### Resolution Mechanics

To resolve a chain identifier like `quai:15000`, a client should:

1. **Identify the network environment**: 
   - `quai:9` → Quai Mainnet
   - `quai:15000` → Quai Testnet (Orchard)

2. **Use the correct chain ID in transactions**:
   - Mainnet: `9`
   - Testnet: `15000`

3. **Connect to the appropriate RPC endpoint**:
   - Mainnet: `https://rpc.quai.network/cyprus1` (currently routes to cyprus-1)
   - Testnet: `https://orchard.rpc.quai.network/cyprus1` (currently routes to cyprus-1)

**Current State**: With only one active shard (cyprus-1), the chain ID is sufficient to determine the RPC endpoint. **Future State**: As the network expands and additional shards activate, clients will need address-based shard routing (see [CAIP-10 profile](./caip10.md) for shard resolution mechanics).

Sample request:

```json
{
  "jsonrpc": "2.0",
  "method": "quai_chainId",
  "params": [],
  "id": 1
}
```

Sample response (mainnet):

```json
{
  "jsonrpc": "2.0",
  "result": "0x9",
  "id": 1
}
```


### Backwards Compatibility

There are no legacy references or alternate namespace versions at this time. All prior Quai environments use the single chain ID `9` and follow the sharded address space logic described in QIP-2.

## Test Cases

| Blockchain   | CAIP-2 ID    | Chain ID | Notes              |
| ------------ | ------------ | -------- | ------------------ |
| Quai Mainnet | `quai:9`     | 9        | Production network |
| Quai Testnet | `quai:15000` | 15000    | "Orchard" testnet  |


## References

- [CAIP-2][]
- [Quai Docs][] - Official Quai documentation including address sharding, quais.js SDK and Proof-of-Entropy-Minima (PoEM) reference
- [Quai Docs: JSON-RPC][] - JSON-RPC Reference
- [go-quai Github][] - Source code repository for the node protocol implementation
- [Quai Improvement Proposals Github][] - Repository for QIPs and protocol design, including address sharding, Qi energy-based flatcoin controller design, and dynamic network expansion
- [PoEM: A Better Proof-of-Work Fork Choice Rule][] - PoEM security proof, incentive design, and selfish mining analysis
- [Quaiscan][] - Quai block explorer, currently running on shard 0, also known as cyprus-1
- [Pelagus Wallet][] - Browser extension-based wallet that allows users to hold QUAI and interact with Quai mainnet and testnet dApps
- [quais.js][] - SDK for deploying contracts and building dApps that interact with Quai


[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[Quai Docs]: https://docs.qu.ai
[Quai Docs: JSON-RPC]: https://docs.qu.ai/build/playground/overview#json-rpc-overview
[go-quai Github]: https://github.com/dominant-strategies/go-quai
[Quai Improvement Proposals Github]: https://github.com/quai-network/qips
[PoEM: A Better Proof-of-Work Fork Choice Rule]: https://eprint.iacr.org/2024/200
[Quaiscan]: https://quaiscan.io
[Pelagus Wallet]: https://pelgauswallet.io
[quais.js]: https://github.com/dominant-strategies/quais.js
[eip155]: https://github.com/ChainAgnostic/namespaces/blob/main/eip155/caip2.md

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
