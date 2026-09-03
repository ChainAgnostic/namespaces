---
namespace-identifier: xync-caip19
title: Xync Network - Asset ID Specification
author: Xync Network (@XyncNet)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/188
status: Draft
type: Informational
created: 2026-07-08
requires: ["CAIP-2", "CAIP-19"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Introduction

Xync carries up to 255 protocol-native currencies (fiat units backed
by regulated issuers, wrapped coins, loyalty units) plus the native
token XYNC. Currencies are not contracts: they are single-byte codes
in an on-chain registry that also stores the display name, decimal
scale and issuer. Every asset therefore addresses with one byte.

## Specification

### Semantics

The asset namespace is `cur`; the asset reference is the registry code
(0–255). Code `0` is permanently the native token XYNC. The registry
entry (resolvable below) carries `name` and `scale` — amounts on the
wire are integers in minimal units of the given scale.

### Syntax

```
asset_id:        chain_id + "/" + "cur" + ":" + code
code:            0 | [1-9][0-9]{0,2}     (0..255)
```

### Resolution Mechanics

```jsonc
// GET https://<node>/currencies
{
  "0": {"name": "XYNC", "scale": 6},
  "1": {"name": "USD",  "scale": 3, "issuer_acct": 8},
  ...
}
```

## Rationale

A currency is a registry number, not a deployed contract: zero
attack surface and identical behavior for every asset. The registry code
is a single byte; the native 128-bit transaction does not carry it
directly — a transfer names the sender's *currency account* (the pair
"user + currency", which owns the sequence number), and the currency is
read from that account. A CAIP-19 reference therefore maps 1:1 onto the
currency half of every account in the ledger.

### Backwards Compatibility

A `slip44:` asset namespace alias for the native token MAY be added
after a SLIP-44 coin type is assigned to XYNC; `cur:0` remains
canonical.

## Test Cases

```bash
# native token XYNC on mainnet
xync:main/cur:0

# protocol-native USD (issuer-backed) on mainnet
xync:main/cur:1

# a currency on the development network
xync:dev-1/cur:3
```

## References

- [Xync Network Yellow Paper][] - the currency registry, issuers,
  proof-of-reserves

[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[Xync Network Yellow Paper]: https://xync.net/papers/yellowpaper.en.pdf

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
