---
namespace-identifier: nano-caip2
title: Nano Namespace - Networks
author: ["Frank Kilkelly (@kilkelly)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/242
status: Draft
type: Standard
created: 2026-11-26
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

The Nano ecosystem consists of multiple networks maintained by the Nano
Foundation and the wider community:

- `mainnet` – the production network with real economic value
- `betanet` – experimental network used for load testing, performance testing,
  and early feature/release-candidate testing (funds have no value)
- `testnet` – network intended for basic integration and development testing
  (funds have no value)

Each network is completely independent and has its own genesis block.
Transactions signed for one network are invalid on another.

Because the networks are identified by well-known, human-readable names in all
official documentation, the CAIP-2 reference
uses these canonical names directly.

## Specification

### Semantics

The namespace is `nano`.

The reference is one of the following lowercase strings:

- `mainnet`
- `betanet`
- `testnet`

Full CAIP-2 identifiers therefore take the form:

```
nano:mainnet
nano:betanet
nano:testnet
```

### Syntax

#### Regular Expression

```
^nano:(mainnet|betanet|testnet)$
```

Only these exact network identifiers are currently defined.

#### Example

```
nano:mainnet
```

### Resolution Mechanics

To resolve the current network of a Nano node, make a JSON-RPC request with the
`version` action:

```json
{
  "action": "version"
}
```

Example response (mainnet):

```json
{
  "rpc_version": "1",
  "store_version": "22",
  "protocol_version": "19",
  "node_vendor": "Nano V28.2",
  "store_vendor": "LMDB 0.9.25",
  "network": "live"
}
```

Mapping from the `network` field returned by the node:

| Node `network` value | CAIP-2 reference |
|----------------------|------------------|
| `live`               | `mainnet`        |
| `beta`               | `betanet`        |
| `test`               | `testnet`        |

The `network` field is the canonical way to identify which network a node is
connected to.

## Rationale

The reference values follow the canonical names used throughout the official
Nano documentation. Mapping the node's internal `live` / `beta` / `test` labels
to the more widely understood CAIP-style `mainnet` / `betanet` / `testnet` names
improves clarity  while remaining fully deterministic.

### Backwards Compatibility

This is the first CAIP-2 specification for the `nano` namespace, so there are no
legacy identifiers to support.

## Test Cases

```
# Mainnet
nano:mainnet

# Betanet
nano:betanet

# Testnet
nano:testnet
```

## References

- [Nano documentation][nano-docs]
- [Nano node source code][nano-github]
- [Nano official website][nano-home]

[nano-docs]: https://docs.nano.org/
[nano-github]: https://github.com/nanocurrency/nano-node
[nano-home]: https://nano.org/
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).