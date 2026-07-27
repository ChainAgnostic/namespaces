---
namespace-identifier: kaspa-caip2
title: Kaspa Namespace - Chains
author: Luke Dunshea (@elldeeone)
discussions-to: https://kas-smiths.org/t/kaspa-x402-pay-per-request-kas-payments-for-apis-and-ai-agents/15
status: Draft
type: Standard
created: 2026-07-27
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

In [CAIP-2][] a general blockchain identification scheme is defined.
This is the implementation of CAIP-2 for Kaspa.
Blockchains in the `kaspa` namespace are identified by the network names defined by the Rusty Kaspa `NetworkId` implementation.
The reference node exposes the same identifier through RPC with a `kaspa-` prefix.

Kaspa has its own blockDAG consensus, node RPC, and native network identification.
It does not use the Bitcoin-family resolution method defined by the `bip122` namespace.

## Syntax

The namespace `kaspa` refers to the Kaspa open-source blockchain platform.

### Reference Definition

The initial references are:

| Network | Native `NetworkId` | RPC `networkName` | CAIP-2 identifier |
|---------|--------------------|-------------------|-------------------|
| Mainnet | `mainnet` | `kaspa-mainnet` | `kaspa:mainnet` |
| Testnet 10 | `testnet-10` | `kaspa-testnet-10` | `kaspa:testnet-10` |

Only the references listed in this profile are conformant.
Local `simnet` and `devnet` names are not included because they do not identify globally unique public networks.
A future public network can be added with a distinct reference and genesis block.

The registered genesis hashes are:

| Network | Genesis block hash |
|---------|--------------------|
| Mainnet | `58c2d4199e21f910d1571d114969cecef48f09f934d42ccb6a281a15868f2999` |
| Testnet 10 | `f896a3034873be1739fc4359236899fd3d65d2bc94f9780df0d0da3eb1cc4370` |

### Resolution Method

To resolve a blockchain reference for the Kaspa namespace, call `getBlockDagInfo` on a Kaspa node.

```jsonc
// Response excerpt
{
  "networkName": "kaspa-testnet-10",
  "blockCount": 123456,
  "headerCount": 123456
}
```

The returned `networkName` maps directly to the corresponding entry in the reference table.
For example, `kaspa-testnet-10` resolves to `kaspa:testnet-10`.
Implementations that require an immutable network fingerprint can also compare the configured genesis hash with the table above.

### Backwards Compatibility

Not applicable.

## Test Cases

This is a list of manually composed examples:

```text
# Kaspa mainnet
kaspa:mainnet

# Kaspa public testnet 10
kaspa:testnet-10
```

## References

- [Network ID Implementation][] - Native network parsing and serialization
- [Network Parameters][] - Public-network parameter selection
- [Genesis Configuration][] - Mainnet and testnet genesis constants
- [Kaspa RPC Protocol][] - `getBlockDagInfo` and `networkName`
- [Rusty Kaspa][] - Kaspa reference-node implementation

[Network ID Implementation]: https://github.com/kaspanet/rusty-kaspa/blob/78257f273a26c4be085bab0f79437dee99ca8835/consensus/core/src/network.rs
[Network Parameters]: https://github.com/kaspanet/rusty-kaspa/blob/78257f273a26c4be085bab0f79437dee99ca8835/consensus/core/src/config/params.rs
[Genesis Configuration]: https://github.com/kaspanet/rusty-kaspa/blob/78257f273a26c4be085bab0f79437dee99ca8835/consensus/core/src/config/genesis.rs
[Kaspa RPC Protocol]: https://github.com/kaspanet/rusty-kaspa/blob/78257f273a26c4be085bab0f79437dee99ca8835/rpc/grpc/core/proto/rpc.proto
[Rusty Kaspa]: https://github.com/kaspanet/rusty-kaspa
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
