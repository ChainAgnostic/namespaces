---
namespace-identifier: tron
title: Tron Ecosystem
author: Ignacio Rivera (@riveign), Daniel Rocha (@danroc)
status: Draft
type: Informational
created: 2026-01-27
---

# Namespace for Tron Chains

This document describes the syntax and structure of the Tron namespace.
Tron is a decentralized blockchain platform that utilizes Delegated Proof of Stake (DPoS) consensus and features the Tron Virtual Machine (TVM), which is compatible with the Ethereum Virtual Machine (EVM).

## Introduction

Tron is a blockchain-based decentralized platform founded in 2017 that aims to build a free, global digital content entertainment system utilizing blockchain and distributed storage technology.
The Tron network supports smart contracts through its TVM (Tron Virtual Machine) and provides high throughput with approximately 2,000 transactions per second and 3-second block times.

The Tron ecosystem includes:
- **Mainnet**: Production network for live applications
- **Shasta Testnet**: Testing environment compatible with mainnet parameters
- **Nile Testnet**: Bleeding-edge testing network for new features

## Blockchain Identification

Tron chains are identified using hexadecimal chain IDs derived from the last 4 bytes of their genesis block hashes, as specified in TIP-474.
This approach provides:
- Deterministic chain identification from genesis block
- Compatibility with EVM tooling through `eth_chainId` method
- Replay protection across networks
- Integration with existing blockchain infrastructure

## Token Standards

Tron supports multiple token standards:
- **TRC-20**: Fungible token standard (similar to ERC-20)
- **TRC-10**: Native token standard with lower transaction costs
- **TRC-721**: Non-fungible token (NFT) standard

## Address Format

Tron uses Base58Check encoding for addresses:
- All addresses start with the letter `T`
- Addresses are exactly 34 characters long
- Example: `TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL`

## Network Information

### Mainnet
- **RPC Endpoint**: `https://api.trongrid.io`
- **JSON-RPC Endpoint**: `https://api.trongrid.io/jsonrpc`
- **Explorer**: `https://tronscan.org`
- **Native Currency**: TRX (6 decimals, 1 TRX = 1,000,000 SUN)

### Shasta Testnet
- **RPC Endpoint**: `https://api.shasta.trongrid.io`
- **JSON-RPC Endpoint**: `https://api.shasta.trongrid.io/jsonrpc`
- **Explorer**: `https://shasta.tronscan.org`
- **Faucet**: Available at https://www.trongrid.io/shasta

### Nile Testnet
- **RPC Endpoint**: `https://nile.trongrid.io`
- **JSON-RPC Endpoint**: `https://nile.trongrid.io/jsonrpc`
- **Explorer**: `https://nile.tronscan.org`

## References

- [Tron Developer Hub][]: Official Tron development documentation
- [TIP-474][]: Tron Improvement Proposal specifying chain ID derivation
- [TronGrid][]: Official Tron API service
- [TronWeb][]: JavaScript SDK for Tron blockchain
- [Tronscan][]: Tron blockchain explorer

[Tron Developer Hub]: https://developers.tron.network/
[TIP-474]: https://github.com/tronprotocol/tips/blob/master/tip-474.md
[TronGrid]: https://www.trongrid.io/
[TronWeb]: https://tronweb.network/
[Tronscan]: https://tronscan.org/
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md

## Rights

Copyright and related rights waived via CC0.
