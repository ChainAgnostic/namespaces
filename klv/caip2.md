---
namespace-identifier: klv-caip2
title: Klever Namespace - Chains
author: Nicollas Gabriel da Silva (@nickgs1337)
discussions-to: https://forum.klever.org/, https://github.com/klever-io/klever-go/discussions
status: Draft
type: Standard
created: 2026-05-13
requires: ["CAIP-2"]
---

# CAIP-2

_For context, see the [CAIP-2][] specification._

## Abstract

In [CAIP-2][] a general blockchain identification scheme is defined. This
document is the implementation of CAIP-2 for the Klever blockchain.

### Klever Namespace

The namespace `klv` refers to the wider Klever ecosystem.

## Rationale

The Klever protocol runs a production network (Mainnet), a testing network
(Testnet) and a development network (Devnet). More may be canonically
addressed in the future. Each network is identified on-chain by an integer
`klv_chain_id` assigned at genesis; that integer is the canonical CAIP-2
reference.

## Syntax

An identifier for a Klever chain consists of the namespace prefix `klv:`
followed by the chain's integer `klv_chain_id`.

### Reference Definition

The reference is the network's integer chain ID, rendered in base 10 with no
leading zeros:

- `108` for Mainnet
- `109` for Testnet
- `100001` for Devnet

References are within the case-sensitive `[-a-zA-Z0-9]{1,32}` envelope
mandated by [CAIP-2][].

### Resolution Method

To resolve a blockchain reference for the Klever namespace, query the
`/node/status` endpoint on any public Klever node, e.g. the official mainnet
node:

```jsonc
// Request
curl -sS https://node.mainnet.klever.org/node/status

// Response (formatted, excerpt)
{
  "data": {
    "metrics": {
      "klv_chain_id": 108
      // ... other live chain metrics
    }
  },
  "code": "successful"
}
```

The `klv_chain_id` field inside `data.metrics` is the value used directly as
the `reference` section of a CAIP-2 or CAIP-10.

## Backwards Compatibility

Not applicable.

## Test Cases

```
# Klever Mainnet
klv:108

# Klever Testnet
klv:109

# Klever Devnet
klv:100001
```

## References

- [Klever node status endpoint][klever-status] — REST endpoint that returns
  the live chain ID and other chain identity metrics.
- [Klever Connect SDK][klever-connect] — Implements chain-id-aware
  transaction signing.

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[klever-status]: https://node.mainnet.klever.org/node/status
[klever-connect]: https://github.com/klever-io/klever-connect

## Rights

Copyright and related rights waived via CC0.
