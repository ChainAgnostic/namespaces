---
namespace-identifier: xync-caip2
title: Xync Network - Blockchain ID Specification
author: Xync Network (@XyncNet)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/188
status: Draft
type: Informational
created: 2026-07-08
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

Xync Network is a payments-only Layer-1 blockchain. Networks in the
"xync" namespace are identified by a short human-readable network name
declared in the network's genesis file (`chain_id`). The genesis file
is canonical and content-addressed: its SHA-256 hash is co-signed by
the validator quorum in every checkpoint, so a reference resolves
unambiguously to one genesis.

## Specification

### Semantics

The reference is the `chain_id` field of the network's genesis file:
`main` for the production network, `test-N` / `dev-N` for test and
development networks. The reference intentionally excludes the
namespace name (no `xync-` prefix) to avoid stutter.

### Syntax

```
chain_id:    namespace + ":" + reference
namespace:   xync
reference:   [-_a-zA-Z0-9]{1,32}
```

### Resolution Mechanics

Query any validator's public API:

```jsonc
// GET https://<node>/status
{
  "chain": "main",
  "caip2": "xync:main",
  "genesis_sha256": "9f2c…",   // co-signed by the checkpoint quorum
  ...
}
```

A client validates that `caip2` matches the expected identifier and
MAY verify `genesis_sha256` against the published genesis file and the
latest checkpoint signatures (2f+1 of the validator set).

## Rationale

Named references (like `hedera:mainnet`) rather than genesis-hash
references (like `solana`): the genesis hash is still verifiable via
resolution, while the identifier stays short and human-readable —
consistent with the network's compact-identifier design philosophy
(a whole transaction is 128 bits). Network names are unique within the
namespace and assigned by namespace governance.

### Backwards Compatibility

Not applicable (the namespace launches with this specification).

## Test Cases

```bash
# Xync mainnet
xync:main

# Xync development network
xync:dev-1
```

## References

- [Xync Network Yellow Paper][] - protocol specification (network
  model, genesis, checkpoints)
- [XyncPay][] - the live payment product on the network

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[Xync Network Yellow Paper]: https://xync.net/papers/yellowpaper.en.pdf
[XyncPay]: https://t.me/XyncPayBot

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
