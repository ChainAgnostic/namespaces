---
namespace-identifier: bsv-caip2
title: BSV Blockchain - Networks
author: Deggen (@sirdeggen) <d.kellenschwiler@bsvassociation.org>
discussions-to: ["https://github.com/ChainAgnostic/namespaces/pull/190", "https://github.com/bsv-blockchain/x402/pull/1"]
status: Draft
type: Standard
created: 2026-07-10
requires: ["CAIP-2"]
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

The BSV Chain ID is a human-readable identifier for a BSV network. It is the network
name a BSV node and its client tooling use to describe the chain they operate on —
not the genesis block hash, which BSV shares with BTC and BCH.

## Specification

### Semantics

BSV networks are identified by a stable, well-known network name assigned by the
protocol's reference node implementation (SV Node). Mainnet and testnet are the two
networks in general use; the scaling test network (STN) and regtest exist for testing
and MAY be added to this namespace if cross-chain tooling requires them.

### Syntax

The Chain ID consists of the prefix `bsv:` followed by the network name.

The reference is a case-sensitive string matching the CAIP-2 reference grammar
`[-_a-zA-Z0-9]{1,32}`. This namespace defines two references:

- `mainnet` — the BSV main network
- `testnet` — the BSV test network

A validating regular expression for the fully-qualified Chain ID:

```
bsv:(mainnet|testnet)
```

### Resolution Mechanics

To resolve the network name for a BSV node, send a JSON-RPC `getblockchaininfo`
request; the `chain` field of the result identifies the network. Map the node's
`chain` value to the CAIP-2 reference as follows: `main` → `mainnet`,
`test` → `testnet`.

```jsonc
// Request
{
  "jsonrpc": "1.0",
  "id": 1,
  "method": "getblockchaininfo",
  "params": []
}

// Response (abridged)
{
  "result": {
    "chain": "main"
  }
}
```

Application-layer clients typically resolve the network without a node round-trip: a
[BRC-100][] wallet returns the network directly from its `getNetwork` call
(`{ "network": "mainnet" }` or `{ "network": "testnet" }`), which maps to the CAIP-2
reference unchanged.

## Rationale

BSV descends from the original Bitcoin protocol and therefore shares Satoshi's genesis
block with BTC and BCH. The [bip122][] namespace addresses this by referencing the hash
of a chain's first post-fork block (as it does for Bitcoin Cash), so a BSV entry under
`bip122` is technically possible. This namespace instead uses the network name because
that is the identifier BSV's wallet and infrastructure layer already exchanges — see the
namespace [README][] for the full rationale. This mirrors the [casper][] namespace, which
likewise uses a human-readable Chain ID distinct from the genesis hash.

### Backwards Compatibility

No prior CAIP or namespace assigns BSV identifiers, so there are no legacy identifiers to
maintain. Tooling that prefers a hash-based identifier can independently register BSV under
[bip122][] using its fork-block hash; the two schemes can coexist without collision because
they occupy different namespaces.

## Test Cases

This is a list of manually composed examples:

```
# BSV Mainnet
bsv:mainnet

# BSV Testnet
bsv:testnet
```

## References

- [BRC-100][] - the BSV wallet-to-application interface, whose `getNetwork` method reports the network name
- [bip122][] - the CAIP-2 namespace for Bitcoin-based networks, which identifies forks by fork-block hash
- [casper][] - a CAIP-2 namespace precedent using a human-readable Chain ID rather than a genesis hash
- [README][] - the BSV namespace README with the full rationale

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[BRC-100]: https://github.com/bitcoin-sv/BRCs/blob/master/wallet/0100.md
[bip122]: https://namespaces.chainagnostic.org/bip122/caip2
[casper]: https://namespaces.chainagnostic.org/casper/caip2
[README]: ./README.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
