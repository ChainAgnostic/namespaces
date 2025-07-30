---
namespace-identifier: quai-caip10
title: Quai Namespace - Addresses
author: ["Jonathan Downing (@jdowning100)", "Dr. K (@mechanikalk)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/145
status: Draft
type: Standard
created: 2025-07-22
requires: ["CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

Quai Network implements a unique sharded address space where every address deterministically routes to a specific shard based on its first byte prefix. Unlike traditional multi-chain systems that require separate chain IDs, Quai uses a single global chain ID (9 for mainnet, 15000 for testnet) across all shards, with address-based routing determining transaction execution location. The first byte encodes both the shard location (region and zone) and the ledger type (Quai account-based or Qi UTXO-based), making addresses self-describing for routing purposes.

## Rationale

Quai's address space requires specialized CAIP-10 handling due to its unique sharded architecture. Traditional blockchain addresses are simply identifiers within a single state space, but Quai addresses encode routing information that determines which shard processes transactions. The first byte of every Quai address contains:

- **Bits 0-3**: Region number (0-15)
- **Bits 4-7**: Zone number within region (0-15) 
- **Bit 8**: Ledger identifier (0=Quai accounts, 1=Qi UTXO)

This creates a deterministic address space where `0x00...` addresses route to region-0/zone-0 (cyprus-1), `0x01...` to region-0/zone-1, etc. Currently only shard 0 (cyprus-1) is active on mainnet, so all addresses begin with `0x00`. As network demand grows, additional shards will activate with their corresponding address prefixes. This specification enables proper interpretation of Quai addresses for cross-chain tools, wallets, and asset registries while maintaining compatibility with EVM tooling through checksummed hex encoding.

## Semantics

- **Namespace**: `quai`
- **Chain ID**: References a specific Quai network environment (9 for mainnet, 15000 for testnet)
- **Address**: A 20-byte hex-encoded address with EIP-55 checksumming, where the first byte determines shard routing
- **Address Prefix**: The first byte encodes shard location and ledger type according to QIP-2
- **Ledger Types**: Quai (account-based, bit 8=0) or Qi (UTXO-based, bit 8=1)
- **Shard Routing**: Determined by address prefix, not chain ID
- **Location Encoding**: `(region << 4) | zone` for bits 0-7, plus ledger bit

## Syntax

Quai CAIP-10 addresses follow the format:

```
quai:<chain_id>:<checksummed_address>
```

Where:
- `<chain_id>` is `9` (mainnet) or `15000` (testnet)
- `<checksummed_address>` is a 40-character hex string (20 bytes) with EIP-55 checksumming

**Regular Expression**:
```
^quai:(9|15000):0x[a-fA-F0-9]{40}$
```

**Address Format**:
```
0x[PB][LB][34 hex chars]
```
Where:
- `PB` = Prefix byte encoding shard location `(region << 4) | zone`
- `LB` = Ledger byte (bit 0/first bit indicates ledger: 0=Quai, 1=Qi)
- Remaining 18 bytes = Standard address data

**Ledger Detection**:
- Third hex character `0-7` → Quai ledger (account-based)
- Third hex character `8-F` → Qi ledger (UTXO-based)

**Prefix Byte Calculation**:
```
prefix_byte = (region << 4) | zone
```

**Valid Examples**:
- `quai:9:0x00841c4349dbC3CD16098ef0aF2780BA0F7f5C02` (mainnet, cyprus-1 shard)
- `quai:15000:0x004d2Ee5f59c0A7Df5C54d6C9d5a4f3e3b8E1d2F` (testnet, cyprus-1 shard)

### Resolution Mechanics

To resolve and validate a Quai CAIP-10 address:

1. **Parse the chain reference** to determine network (9=mainnet, 15000=testnet)
2. **Extract the address prefix** (first byte) to determine shard routing
3. **Validate EIP-55 checksum** using standard Ethereum checksumming
4. **Route to appropriate RPC endpoint** based on shard location

**Shard Resolution Example**:
```javascript
// Address: 0x00841c4349dbC3CD16098ef0aF2780BA0F7f5C02
const firstByte = 0x00;
const region = (firstByte & 0xF0) >> 4;  // 0
const zone = firstByte & 0x0F;           // 0
const isQi = (secondByte & 0x80) > 0;    // false (Quai ledger)
// Routes to: cyprus-1 (region-0, zone-0)
```

**RPC Validation**:
```json
{
  "jsonrpc": "2.0",
  "method": "quai_getBalance",
  "params": ["0x00841c4349dbC3CD16098ef0aF2780BA0F7f5C02", "latest"],
  "id": 1
}
```

**Response**:
```json
{
  "jsonrpc": "2.0", 
  "result": "0x1b1ae4d6e2ef500000",
  "id": 1
}
```

**Shard-to-Port Mapping**:

When running a local Quai node, each shard operates on a specific port. The address prefix determines which shard (and thus which port) to use:

| Shard      | HTTP RPC Port | Address Prefix | Status |
|------------|---------------|----------------|---------|
| `zone-0-0` (cyprus-1) | 9200 | `0x00`, `0x01` | Active |
| `zone-0-1` (cyprus-2) | 9201 | `0x10`, `0x11` | Inactive |
| `zone-1-0` (paxos-1)  | 9220 | `0x20`, `0x21` | Inactive |
| `zone-1-1` (paxos-2)  | 9221 | `0x30`, `0x31` | Inactive |
| ... | ... | ... | Future expansion |

**Note**: When using quais.js and/or Pelagus wallet with the mainnet RPC, developers and users are abstracted away from the shard-port mapping. If developers run their own node, the shard-port mapping may be a useful reference.

### Backwards Compatibility

Quai addresses maintain full backwards compatibility with Ethereum address formats and tooling:

- **EIP-55 Checksumming**: All Quai addresses use standard Ethereum checksumming
- **20-byte Format**: Identical to Ethereum address length and structure
- **Hex Encoding**: Standard 0x-prefixed hex representation
- **EVM Compatibility**: Addresses work directly with existing Ethereum tooling

##### Note: If a transaction is sent from a Quai address to a Qi address, it will be interpreted as a Quai->Qi conversion. It is therefore highly recommended to check the recipient address before sending a transaction! If a transaction is sent to a Quai address on a different shard, and that shard is not active, the transaction will fail. 

**Legacy Considerations**:
- Pre-mainnet testnets may have used different address formats - these are deprecated
- Early documentation may reference different shard numbering - current spec follows QIP-2
- Address validation should always check current network state for active shards

## Test Cases

### Mainnet Examples (quai:9)

| Address Type | CAIP-10 Address | Shard | Ledger | Notes |
|--------------|-----------------|-------|-----------|-------|
| Cyprus-1 Quai | `quai:9:0x000DEAdbeEFCafE0000000000000000000000000` | region-0, zone-0 | Quai | Active shard |
| Cyprus-1 Qi | `quai:9:0x008fb5C7919B14a1Cd9c2e5f8D3e4B2a7f6c9D0e` | region-0, zone-0 | Qi | UTXO ledger |
| Future Cyprus-2 | `quai:9:0x014c3e5f1B2A4D6F8e0C9a7b5D3F1e4C2a0b8d6f` | region-0, zone-1 | Quai | Inactive |
| Future Paxos-1 | `quai:9:0x102a4D6f8e0c9A7b5d3f1e4C2a0b8d6f1C3e5f1b` | region-1, zone-0 | Quai | Inactive |

### Testnet Examples (quai:15000)

| Address Type | CAIP-10 Address | Shard | Ledger | Notes |
|--------------|-----------------|-------|-----------|-------|
| Testnet Cyprus-1 | `quai:15000:0x004d2EE5F59c0a7dF5C54D6C9D5a4F3E3B8e1d2f` | region-0, zone-0 | Quai | Orchard testnet |
| Testnet Qi | `quai:15000:0x00B2f4C6e8a0D2F4E6a8b0D2F4C6e8A0B2F4c6E8` | region-0, zone-0 | Qi | UTXO testnet |

### Invalid Examples

| Invalid Address | Issue | Correct Format |
|-----------------|-------|----------------|
| `quai:1:0x00...` | Wrong chain ID | `quai:9:0x00...` |
| `quai:9:0x00841c...` | Truncated address | Must be 40 hex chars |
| `quai:9:0x00841C...` | Wrong checksum | Use EIP-55 checksum |
| `ethereum:1:0x00...` | Wrong namespace | Use `quai` namespace |

## Additional Considerations

**Shard Expansion**: As Quai network grows, new shards will activate with corresponding address prefixes. Address validation should check current network state for active shard ranges.

**Cross-shard Transactions**: Future QIPs may define cross-shard transaction formats that could affect address interpretation and routing.

**Dynamic Expansion**: QIP-2 defines a deterministic shard expansion schedule. CAIP-10 implementations should be prepared for new address prefixes as the network scales.

**Ledger Interoperability**: Conversion between Quai (account) and Qi (UTXO) ledgers may require special address handling in future protocol versions.

## References

- [CAIP-10][] - Account ID specification for blockchain agnostic account addressing
- [QIP-2][] - Quai Improvement Proposal defining sharded ledger and address space
- [EIP-55][] - Mixed-case checksum address encoding standard
- [Quai Docs][] - Official documentation including address sharding and network details
- [go-quai][] - Reference implementation of Quai protocol with address handling
- [quais.js][] - JavaScript SDK for Quai development with address utilities
- [Quaiscan][] - Block explorer showing address format examples

[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[QIP-2]: https://github.com/quai-network/qips/blob/master/qip-0002.md
[EIP-55]: https://eips.ethereum.org/EIPS/eip-55
[Quai Docs]: https://docs.qu.ai
[go-quai]: https://github.com/dominant-strategies/go-quai
[quais.js]: https://github.com/dominant-strategies/quais.js
[Quaiscan]: https://quaiscan.io

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
