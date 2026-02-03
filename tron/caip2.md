---
namespace-identifier: tron-caip2
title: Tron Namespace - Blockchain ID Specification
author: Ignacio Rivera (@riveign), Daniel Rocha (@danroc)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/XXX
status: Draft
type: Standard
created: 2026-01-27
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

Tron uses hexadecimal chain IDs derived from the last 4 bytes of the genesis block hash, as specified in [TIP-474][].
This approach provides several benefits:
- Deterministic derivation from the immutable genesis block
- Compatibility with EVM tooling and infrastructure
- Replay protection across different Tron networks
- Integration with existing blockchain registries like ChainList

The chain ID mechanism was introduced to enable cross-chain compatibility and provide unique, verifiable identifiers for each Tron network.

## Syntax

The namespace "tron" refers to the Tron blockchain platform and its associated networks.

### Reference Definition

The reference format for Tron chains uses the hexadecimal representation of the chain ID, prefixed with `0x`.
This chain ID is derived from the last 4 bytes of the genesis block hash.

**Format**: `tron:0x{chainId}` where `chainId` is an 8-character hexadecimal string (4 bytes)

### Semantics

The chain ID derivation follows this algorithm:
1. Query the genesis block (block height 0)
2. Extract the block hash
3. Take the last 4 bytes (8 hexadecimal characters) of the genesis block hash
4. Use this as the chain ID with `0x` prefix

### Resolution Method

Tron chain IDs are derived from the last 4 bytes of the genesis block hash and are static for each network.
Applications should use the following pre-determined chain IDs:

| Network | Chain ID | Genesis Hash (last 4 bytes) |
|---------|----------|----------------------------|
| Mainnet | `0x2b6653dc` | `...2b6653dc` |
| Shasta  | `0xcd8690dc` | `...cd8690dc` |
| Nile    | `0x94a9059e` | `...94a9059e` |

These chain IDs are deterministically derived and do not change. For verification purposes, you can query the genesis block to confirm the derivation, but the chain IDs themselves are constants that should be used for network identification.

**Note**: Applications should use Tron-native RPC methods with the `tron_` prefix (e.g., `tron_getBalance`, `tron_signTransaction`). While Tron implements some EVM-compatible JSON-RPC endpoints (including `eth_chainId`) for tooling compatibility, these are secondary interfaces. The chain ID values remain the same regardless of which RPC interface is used.

## Test Cases

This is a list of manually composed and validated examples:

```bash
# Tron Mainnet
tron:0x2b6653dc

# Tron Shasta Testnet (mainnet-compatible testing)
tron:0xcd8690dc

# Tron Nile Testnet (bleeding-edge features)
tron:0x94a9059e
```

### Chain ID Verification

| Network | Chain ID (Hex) | Chain ID (Decimal) | Genesis Hash (last 4 bytes) |
|---------|----------------|--------------------|-----------------------------|
| Mainnet | `0x2b6653dc` | `728126428` | `...2b6653dc` |
| Shasta  | `0xcd8690dc` | `3448148188` | `...cd8690dc` |
| Nile    | `0x94a9059e` | `2494104990` | `...94a9059e` |

### RPC Endpoints for Resolution

- **Mainnet**: `https://api.trongrid.io/jsonrpc`
- **Shasta**: `https://api.shasta.trongrid.io/jsonrpc`
- **Nile**: `https://nile.trongrid.io/jsonrpc`

## Backwards Compatibility

Prior to TIP-474, Tron did not have a standardized chain ID mechanism for cross-chain identification.
The introduction of hexadecimal chain IDs maintains compatibility with:
- Existing EVM tooling and wallets (MetaMask, etc.)
- Blockchain registries (ChainList, ChainID.network)
- Cross-chain protocols and bridges

Legacy integrations that predate TIP-474 should migrate to using the standardized hexadecimal chain IDs.

## Additional Considerations

### Genesis Block Hash Format

The full genesis block hashes for reference:

**Mainnet**:
```
0x00000000000000001ebf88508a03865c71d452e25f4d51194196a1d22b6653dc
```

**Shasta Testnet**:
```
0x0000000000000000d698d4192c56cb6be724a558448e2684802de4d6cd8690dc
```

**Nile Testnet**:
```
0x0000000000000000de1aa88295e1fcf982742f773e0419c5a9c134c994a9059e
```

### Registry Information

Tron chain IDs are registered in:
- [ChainList][]: Public registry of EVM and EVM-compatible chains
- [ChainID.network][]: Community-maintained chain ID database

### Network Selection

Applications should use:
- **Mainnet** for production deployments
- **Shasta** for testing with mainnet-compatible parameters
- **Nile** for testing bleeding-edge features before mainnet deployment

## References

- [CAIP-2][]: Chain ID Specification
- [TIP-474][]: Tron Improvement Proposal for chain ID optimization
- [Tron Developer Hub - Networks][]: Official network documentation
- [Tron Developer Hub - eth_chainId][]: Chain ID RPC method documentation
- [ChainList][]: Tron chain listings
- [TronGrid][]: Official Tron API service
- [Tronscan][]: Tron blockchain explorer

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[TIP-474]: https://github.com/tronprotocol/tips/blob/master/tip-474.md
[Tron Developer Hub - Networks]: https://developers.tron.network/docs/networks
[Tron Developer Hub - eth_chainId]: https://developers.tron.network/reference/eth_chainid
[ChainList]: https://chainlist.org/
[ChainID.network]: https://chainid.network/
[TronGrid]: https://www.trongrid.io/
[Tronscan]: https://tronscan.org/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
