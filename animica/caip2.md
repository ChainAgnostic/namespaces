---
namespace-identifier: animica-caip2
title: Animica Namespace - Chains
author: Animica (@animicaorg)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/200
status: Draft
type: Standard
created: 2026-08-22
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

Every Animica network is configured with an unsigned 32-bit integer chain id.
The `animica` CAIP-2 profile identifies a network by encoding that value as a canonical unsigned decimal string.
The mainnet identifier `animica:1` is already in production use by Animica's [x402][] ANM settlement lane and MCP tooling; this profile documents that existing usage.

## Specification

### Semantics

An Animica chain id consists of the literal namespace `animica`, a colon, and a reference containing the network's integer chain id.
The chain id is the value a node returns from `chain.getChainId`, and the `chainId` field of `chain.getChainIdentity`, `chain.getHead`, and every block and transaction view.
The same chain id is committed to in the signing domain of every transaction, so a transaction signed for one chain id is not valid on a network with a different one.

Animica's [chain parameters][Chain Parameters] assign `1` to mainnet, `2` to the public testnet, and `1337` to local development networks.
Only the mainnet (`animica:1`) is a public network with a public RPC endpoint at the time of writing.

### Syntax

```text
chain_id:  "animica:" + reference
namespace: animica
reference: 0 | [1-9][0-9]{0,9}
```

The reference must match the following regular expression:

```regex
^(0|[1-9][0-9]{0,9})$
```

The parsed value must additionally be in the unsigned 32-bit integer range `0` through `4294967295`, inclusive; the regular expression alone is not sufficient to enforce the upper bound.
The reference uses ASCII decimal digits without a sign, base prefix, separators, surrounding whitespace, or leading zeroes.
The value `0` is syntactically representable but is not assigned to any Animica network and has no special meaning; applications SHOULD NOT use it.

### Resolution Mechanics

To resolve the chain id reported by an Animica JSON-RPC endpoint, call `chain.getChainId`:

```jsonc
// Request
{ "jsonrpc": "2.0", "id": 1, "method": "chain.getChainId", "params": [] }

// Response
{ "jsonrpc": "2.0", "id": 1, "result": 1 }
```

Serialize the result in canonical unsigned decimal form and prefix it with `animica:`.
The example response therefore resolves to `animica:1`.

An integer chain id does not by itself prove which chain an endpoint serves, because a future or private network could be configured with the same value.
Clients that need a trusted chain identity SHOULD instead call `chain.getChainIdentity`, which returns the chain id together with the genesis hash and the fork id that the network's signing domain commits to:

```jsonc
// Request
{ "jsonrpc": "2.0", "id": 1, "method": "chain.getChainIdentity", "params": [] }

// Response (from a mainnet node, 2026-08-22)
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "chainId": 1,
    "genesisHash": "0xa0892158cf997c56e91d0aa12e60c36037dae34800a2b54111a8fa17ec88b7de",
    "genesisHeaderHash": "0xa0892158cf997c56e91d0aa12e60c36037dae34800a2b54111a8fa17ec88b7de",
    "genesisBlockHash": "0xa0892158cf997c56e91d0aa12e60c36037dae34800a2b54111a8fa17ec88b7de",
    "forkId": 3511060514,
    "consensusId": "consensus/68e4e2ad4c547dce744181cedeabe028920cae052eb8095a6f18d351bf68dc74",
    "protocolVersion": "1.0"
  }
}
```

For `animica:1`, clients SHOULD verify that `genesisHash` equals `0xa0892158cf997c56e91d0aa12e60c36037dae34800a2b54111a8fa17ec88b7de` before treating the endpoint as Animica mainnet.
The `forkId` (`3511060514` on mainnet) is part of the transaction signing domain and changes with protocol upgrades, so it should be read from the node at signing time rather than hard-coded as a chain identifier.

## Rationale

The integer chain id is the native network discriminator in Animica's chain parameters, is exposed directly by the standard JSON-RPC interface, and is bound into every transaction signature.
Using it requires no additional registry or transformation and matches the `animica:<chainId>` form that Animica's own documentation, payment lane, and tooling already use.

Decimal encoding matches the JSON-RPC representation and avoids multiple textual forms for the same value, such as hexadecimal, signed, or zero-padded representations.
The genesis-hash cross-check described above follows the precedent of other namespaces whose chain references are operator-configurable integers and exist to defeat a later chain reusing the same id.

### Backwards Compatibility

There was no previously registered CAIP-2 profile for Animica.
This profile does not change Animica's native chain ids.
The identifier `animica:1` is already in use by deployed Animica software, and this profile is compatible with that usage.

## Test Cases

### Valid identifiers

| Identifier | Reason |
| --- | --- |
| `animica:1` | Animica mainnet (genesis 2026-04-06, public RPC `https://rpc.animica.org/rpc`) |
| `animica:2` | Reference reserved for the public testnet in the chain parameters |
| `animica:1337` | Reference reserved for local development networks |
| `animica:4294967295` | Upper `uint32` boundary |

### Invalid identifiers

| Identifier | Reason |
| --- | --- |
| `animica:` | Empty reference |
| `animica:01` | Leading zero |
| `animica:0x1` | Hexadecimal representation |
| `animica:-1` | Signed value |
| `animica:mainnet` | Reference must be the decimal chain id, not a name |
| `animica:4294967296` | Above the `uint32` maximum |
| `animica: 1` | Leading whitespace |
| `ANIMICA:1` | Incorrect namespace casing |
| `eip155:1` | Ethereum mainnet; Animica is not an `eip155` chain even though its chain id is also `1` |

## Security Considerations

Resolving a chain id through `chain.getChainId` only establishes what the queried endpoint reports.
It does not authenticate that endpoint or prevent another network from being configured with the same integer.
Applications that rely on a trusted chain identity should corroborate the result with the `genesisHash` returned by `chain.getChainIdentity`, as described in the [Resolution Mechanics section](#resolution-mechanics).

## References

- [CAIP-2][] - Blockchain ID specification
- [Chain Parameters][] - Animica chain ids, units, and network parameters
- [Encoding Specification][] - Defines `chainId` as a `u32` and lists the registered ids
- [Public RPC][] - Public JSON-RPC 2.0 endpoint for mainnet
- [Explorer][] - Mainnet block explorer
- [Animica source repository][] - Node and reference implementations
- [x402][] - Payment protocol whose Animica lane uses `animica:1` as its network id

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[Chain Parameters]: https://github.com/animicaorg/all/blob/36f995f241cd3e54f66c7a5a6f373d4587bbc60d/docs/spec/CHAIN_PARAMS.md
[Encoding Specification]: https://github.com/animicaorg/all/blob/36f995f241cd3e54f66c7a5a6f373d4587bbc60d/docs/spec/ENCODING.md
[Public RPC]: https://rpc.animica.org/rpc
[Explorer]: https://explorer.animica.org
[Animica source repository]: https://github.com/animicaorg/all
[x402]: https://github.com/x402-foundation/x402

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
