---
namespace-identifier: bsv-caip2
title: BSV Blockchain - Networks
author: Deggen (@sirdeggen) <d.kellenschwiler@bsvassociation.org>
discussions-to: ["https://github.com/ChainAgnostic/namespaces/pull/190", "https://github.com/x402-foundation/x402/pull/2890"]
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

BSV networks are identified by a stable, well-known network name. This namespace
registers the networks in general use for production and public/private scaling
tests. Classic mainnet and testnet remain the baseline networks; Teranode Test Net
(`ttn`) and Teranode Scaling Test Net (`tstn`) identify the Teranode-era scaling
test networks. Local-only environments such as regtest/mockchain are out of scope
for this registration.

### Syntax

The Chain ID consists of the prefix `bsv:` followed by the network name.

The reference is a case-sensitive string matching the CAIP-2 reference grammar
`[-_a-zA-Z0-9]{1,32}`. This namespace defines four references:

- `mainnet` — the BSV main network
- `testnet` — the BSV public test network
- `ttn` — Teranode Test Net (public Teranode scaling test network; also known as Teratestnet)
- `tstn` — Teranode Scaling Test Net (private, per-deployment Teranode scaling test network)

A validating regular expression for the fully-qualified Chain ID:

```
bsv:(mainnet|testnet|ttn|tstn)
```

### Resolution Mechanics

To resolve the network name for a BSV node, send a JSON-RPC `getblockchaininfo`
request; the `chain` field of the result identifies the network. Map the node's
`chain` value to the CAIP-2 reference as follows where applicable: `main` →
`mainnet`, `test` → `testnet`. Teranode deployments that self-identify as `ttn`
or `tstn` map to those references unchanged.

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
(e.g. `{ "network": "mainnet" }` or `{ "network": "testnet" }`), which maps to the
CAIP-2 reference for mainnet/testnet. Wallets and services that operate on Teranode
test networks SHOULD report `ttn` or `tstn` so the CAIP-2 reference matches the
application-layer identifier without translation.

## Rationale

BSV descends from the original Bitcoin protocol and therefore shares Satoshi's genesis
block with BTC and BCH. The [bip122][] namespace addresses this by referencing the hash
of a chain's first post-fork block (as it does for Bitcoin Cash), so a BSV entry under
`bip122` is technically possible. This namespace instead uses the network name because
that is the identifier BSV's wallet and infrastructure layer already exchanges — see the
namespace [README][] for the full rationale. This mirrors the [casper][] namespace, which
likewise uses a human-readable Chain ID distinct from the genesis hash.

`ttn` and `tstn` are registered now so payment and cross-chain tooling (e.g. x402) can
target Teranode test environments without overloading `bsv:testnet` or inventing
ad-hoc identifiers that later need migration.

### Backwards Compatibility

No prior CAIP or namespace assigns BSV identifiers, so there are no legacy identifiers to
maintain. Tooling that prefers a hash-based identifier can independently register BSV under
[bip122][] using its fork-block hash; the two schemes can coexist without collision because
they occupy different namespaces. Clients MUST NOT treat a `bip122` identifier that only
names the shared genesis block as a BSV network — that reference is ambiguous across the
BTC/BCH/BSV split.

## Test Cases

This is a list of manually composed examples:

```
# BSV Mainnet
bsv:mainnet

# BSV Testnet
bsv:testnet

# BSV Teranode Test Net (Teratestnet)
bsv:ttn

# BSV Teranode Scaling Test Net
bsv:tstn
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
