---
namespace-identifier: tron-caip2
title: Tron Namespace - Blockchain ID Specification
author: Ignacio Rivera (@riveign), Daniel Rocha (@danroc)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/170
status: Draft
type: Standard
created: 2026-01-27
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

Tron chain IDs are derived from the last 4 bytes of the genesis block hash, as specified in [TIP-474][], and are expressed in decimal, following the same convention as the `eip155` namespace.
This approach provides several benefits:
- Deterministic derivation from the immutable genesis block
- Compatibility with EVM tooling and infrastructure
- Replay protection across different Tron networks
- Integration with existing blockchain registries like ChainList

The chain ID mechanism was introduced to enable cross-chain compatibility and provide unique, verifiable identifiers for each Tron network.

## Syntax

The namespace "tron" refers to the Tron blockchain platform and its associated networks.

### Reference Definition

The reference format for Tron chains is the decimal representation of the chain ID, an unsigned 32-bit integer.
This chain ID is the numeric value of the last 4 bytes of the genesis block hash.

**Format**: `tron:{chainId}` where `chainId` is the chain ID rendered in decimal, without leading zeroes

### Semantics

The chain ID derivation follows this algorithm:
1. Query the genesis block (block height 0)
2. Extract the block hash
3. Take the last 4 bytes (8 hexadecimal characters) of the genesis block hash
4. Interpret those 4 bytes as a big-endian unsigned 32-bit integer
5. Render that integer in decimal

### Resolution Method

Tron chain IDs are derived from the last 4 bytes of the genesis block hash and are static for each network.
Applications should use the following pre-determined chain IDs:

| Network | Chain ID | Genesis Hash (last 4 bytes) |
|---------|----------|----------------------------|
| Mainnet | `728126428` | `...2b6653dc` |
| Shasta  | `2494104990` | `...94a9059e` |
| Nile    | `3448148188` | `...cd8690dc` |

These chain IDs are deterministically derived and do not change. For verification purposes, you can query the genesis block to confirm the derivation, but the chain IDs themselves are constants that should be used for network identification.

These values are published by the Tron Foundation in [Tron Developer Hub - eth_chainId][], which is the authoritative source should the table above fall out of date. They can also be confirmed at any time by calling `eth_chainId` or reading the genesis block on each network.

**Note**: Applications should use Tron-native RPC methods with the `tron_` prefix (e.g., `tron_getBalance`, `tron_signTransaction`). While Tron implements some EVM-compatible JSON-RPC endpoints (including `eth_chainId`) for tooling compatibility, these are secondary interfaces. The chain ID values remain the same regardless of which RPC interface is used.

When resolving via `eth_chainId`, the response is a base-16-encoded integer (e.g. `0x2b6653dc`) and must be converted to base 10 to form a CAIP-2 reference, as in the `eip155` namespace.

## Test Cases

This is a list of manually composed and validated examples:

```bash
# Tron Mainnet
tron:728126428

# Tron Shasta Testnet (mainnet-compatible testing)
tron:2494104990

# Tron Nile Testnet (bleeding-edge features)
tron:3448148188
```

### Chain ID Verification

| Network | Chain ID (Decimal) | Genesis Hash (last 4 bytes) | Hexadecimal Equivalent |
|---------|--------------------|-----------------------------|------------------------|
| Mainnet | `728126428` | `...2b6653dc` | `0x2b6653dc` |
| Shasta  | `2494104990` | `...94a9059e` | `0x94a9059e` |
| Nile    | `3448148188` | `...cd8690dc` | `0xcd8690dc` |

The hexadecimal column is informative only; it shows the derivation from the genesis hash and is not a valid CAIP-2 reference.

### RPC Endpoints for Resolution

Endpoint URLs change over time.
The authoritative list is maintained by the Tron Foundation in [Tron Developer Hub - Networks][]; the values below are current at the time of writing.

- **Mainnet**: `https://api.trongrid.io/jsonrpc`
- **Shasta**: `https://api.shasta.trongrid.io/jsonrpc`
- **Nile**: `https://nile.trongrid.io/jsonrpc`

## Backwards Compatibility

Prior to [TIP-474], Tron did not have a standardized chain ID mechanism for cross-chain identification.

Both a decimal and a `0x`-prefixed hexadecimal rendering of the same 4-byte value have circulated in the ecosystem.
This specification designates the decimal form as canonical, which keeps the namespace consistent with:
- The underlying type of the chain ID, which [TIP-474][] and the `CHAINID` opcode treat as an integer rather than a byte string
- Tron's existing registrations in [ethereum-lists/chains][] and [ChainList][] (`728126428` for Mainnet)
- Existing wallet implementations, including MetaMask and `tronwallet-adapter`
- The `eip155` namespace, which uses decimal references

The decimal form was agreed as the canonical CAIP-2 representation for Tron in TRON Wallet Dev Community Call #5 on 2026-08-19; see [tronprotocol/pm#229][].

Implementations that previously emitted the hexadecimal form should treat it as a deprecated alias: accept `tron:0x2b6653dc` on input, normalise it to `tron:728126428`, and emit only the decimal form.
The underlying chain ID value is unchanged, so no address-level or on-chain migration is required.

## Additional Considerations

### Genesis Block Hash Format

The full genesis block hashes for reference:

**Mainnet**:
```
0x00000000000000001ebf88508a03865c71d452e25f4d51194196a1d22b6653dc
```

**Shasta Testnet**:
```
0x0000000000000000de1aa88295e1fcf982742f773e0419c5a9c134c994a9059e
```

**Nile Testnet**:
```
0x0000000000000000d698d4192c56cb6be724a558448e2684802de4d6cd8690dc
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
[ethereum-lists/chains]: https://github.com/ethereum-lists/chains/blob/master/_data/chains/eip155-728126428.json
[tronprotocol/pm#229]: https://github.com/tronprotocol/pm/issues/229
[TronGrid]: https://www.trongrid.io/
[Tronscan]: https://tronscan.org/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
