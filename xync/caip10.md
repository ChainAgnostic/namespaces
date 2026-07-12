---
namespace-identifier: xync-caip10
title: Xync Network - Account ID Specification
author: Xync Network (@XyncNet)
discussions-to: TODO-PR-URL
status: Draft
type: Informational
created: 2026-07-08
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Introduction

Xync accounts are compact non-negative integer indexes issued
sequentially by the protocol at registration (account `0` is the
genesis operator). Public keys are rotatable (`rekey` operation), so
the stable identifier of an account is its index — NOT a key or a hash
of one. An optional 2-character checksum suffix protects against typos
and cross-network confusion; it is REQUIRED in user-facing contexts.

## Specification

### Semantics

The address is the account index in decimal, optionally followed by
`-CC` where CC is a checksum. Because the index space is dense (most
small integers are existing accounts), a mistyped address usually hits
a *real* account — unlike sparse hash-address namespaces. Wallets,
QR codes and deep links MUST therefore render the checksummed form;
parsers MUST validate the checksum when present. Exchanges SHOULD
require the checksummed form for withdrawals.

### Syntax

```
account_id:        chain_id + ":" + address
address:           index | index + "-" + checksum
index:             0 | [1-9][0-9]{0,8}      (< 268,435,456 in format v1)
checksum:          2 characters of Crockford base32
```

Checksum computation:

```
CC = crockford_base32( first 10 bits of SHA-256(chain_id_caip2 + ":" + index) )
# example: SHA-256("xync:main:518") -> first 10 bits -> "K7"
```

Crockford base32 alphabet (`0123456789ABCDEFGHJKMNPQRSTVWXYZ`);
parsing is case-insensitive and maps `I`/`L`→`1`, `O`→`0`. Binding the
CAIP-2 identifier into the hash makes a testnet address fail checksum
validation on mainnet and vice versa.

### Resolution Mechanics

```jsonc
// GET https://<node>/account/518
{
  "index": 518,
  "caip10": "xync:main:518-K7",
  "pubkey": "…",          // current key; rotatable, NOT part of the address
  ...
}
```

## Rationale

1. *Index, not pubkey:* keys rotate (`rekey`); an address derived from
   a key would break on every rotation. The index maps 1:1 to the
   28-bit address field of the native 128-bit transaction format.
2. *Checksum-in-address:* analogous in spirit to [EIP-55][] — a
   canonical plain form and a checksummed display form coexist within
   one CAIP-10 grammar (`[-.%a-zA-Z0-9]{1,128}` permits both).

### Backwards Compatibility

Not applicable.

## Test Cases

```bash
# mainnet account 518, checksummed (display form)
xync:main:518-K7

# the same account, canonical plain form (accepted, checksum not verified)
xync:main:518

# genesis operator account
xync:main:0

# devnet account (same index, DIFFERENT checksum than mainnet)
xync:dev-1:518-9Q
```

(Checksum values above are illustrative; compute per the algorithm.)

## References

- [Xync Network Yellow Paper][] - account model, rekey, transaction format
- [EIP-55][] - the precedent of in-identifier optional checksums

[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[EIP-55]: https://eips.ethereum.org/EIPS/eip-55
[Xync Network Yellow Paper]: https://xync.net/papers/yellowpaper.en.pdf

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
