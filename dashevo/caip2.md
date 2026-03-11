---
namespace-identifier: dashevo-caip2
title: Dash Platform Namespace - Chains
author: ["PastaPastaPasta (@PastaPastaPasta)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/177
status: Draft
type: Informational
created: 2026-03-11
updated: 2026-03-11
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

Dash Platform chains are identified by string-based chain IDs assigned at
genesis by [Tenderdash][], a Dash fork of Tendermint. Each network (mainnet,
testnet, devnet) has a distinct `chain_id` that is returned by every node in
that network. This is the same pattern used by the Cosmos ecosystem, but with a
separate namespace because Dash Platform is an independent consensus layer with
its own identity and data contract system.

## Specification

### Semantics

The `chain_id` is a string identifier set in the Tenderdash genesis
configuration. It uniquely identifies a Dash Platform network. The value is
immutable for the lifetime of a network — if a network is reset, a new
`chain_id` is assigned.

Known chain IDs:

| Network  | chain_id           |
|----------|--------------------|
| Mainnet  | `evo1`             |
| Testnet  | `dash-testnet-51`  |

These values are sourced from the [Platform source code][chain-id-source]
(`getMainnetConfigFactory.js` and `getTestnetConfigFactory.js`).

### Syntax

The CAIP-2 identifier for Dash Platform chains is formed by prefixing the
namespace `dashevo:` to the Tenderdash `chain_id`:

```
dashevo:<chain_id>
```

The `chain_id` (used as the CAIP-2 `reference`) matches the following regular
expression:

```
[-a-zA-Z0-9]{1,32}
```

This is the same character class as Cosmos direct references, reflecting the
shared Tendermint heritage.

### Resolution Mechanics

To verify a chain ID, query any Tenderdash node's status endpoint. The
`chain_id` appears in the `network` field of the node info response.

```jsonc
// Request (Tenderdash RPC)
curl -sS https://seed-1.testnet.networks.dash.org:1443/status | jq .result.node_info

// Response (relevant fields)
{
  "network": "dash-testnet-51",
  "version": "1.3.0",
  ...
}
```

For mainnet, query a mainnet Tenderdash node using the same `/status` path.
The `network` field in the response can be used directly as the `reference`
portion of the CAIP-2 identifier.

Note: These are documentation endpoints for chain verification. They are not
required by the WalletConnect relay protocol and are not embedded in session
proposals.

## Rationale

Dash Platform chain IDs follow the Tendermint convention of human-readable
string identifiers set at genesis. The `evo1` mainnet identifier and
`dash-testnet-51` testnet identifier are simple strings that fit within the
32-character limit of CAIP-2 references and match the `[-a-zA-Z0-9]{1,32}`
pattern without requiring hashing.

The namespace `dashevo` was chosen to distinguish Dash Platform from Dash Core
(which uses the `bip122` namespace). "Evo" is the community name for Dash
Platform (short for "Evolution"), making `dashevo` immediately recognizable to
Dash ecosystem participants.

## Test Cases

```
# Mainnet
dashevo:evo1

# Testnet
dashevo:dash-testnet-51
```

## References

- [Tenderdash][] - Tenderdash consensus engine repository
- [Dash Platform docs][] - Official Dash Platform documentation
- [DAPI endpoints][] - DAPI endpoint reference for querying Platform state
- [chain-id-source][] - Platform source code where chain IDs are defined

[Tenderdash]: https://github.com/dashpay/tenderdash
[Dash Platform docs]: https://docs.dash.org/
[DAPI endpoints]: https://docs.dash.org/projects/platform/en/stable/docs/reference/dapi-endpoints.html
[chain-id-source]: https://github.com/dashpay/platform
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
