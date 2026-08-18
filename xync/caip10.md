---
namespace-identifier: xync-caip10
title: Xync Network - Account ID Specification
author: Xync Network (@XyncNet)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/188
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
index:             0 | [1-9][0-9]{0,9}      (< 1,073,741,824 = 2^30)
checksum:          2 characters of Crockford base32
```

As a single regular expression, the canonical (upper-case) address is
`(0|[1-9][0-9]{0,9})(-[0-9A-HJKMNP-TV-Z]{2})?` — at most 13 characters.
Parsers SHOULD additionally range-check the index against 2^30 - 1,
which a character class cannot express.

Checksum computation:

```
CC = crockford_base32( first 10 bits of SHA-256(chain_id_caip2 + ":" + index) )
# big-endian: byte 0 of the digest, plus the top 2 bits of byte 1, split 5 + 5
# example: SHA-256("xync:main:518") = 1f b3 a3 … -> 0b0001111110 = 126 -> "3Y"
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
  "caip10": "xync:main:518-3Y",
  "pubkey": "…",          // current key; rotatable, NOT part of the address
  ...
}
```

## Rationale

1. *Index, not pubkey:* keys rotate (`rekey`); an address derived from
   a key would break on every rotation. The index maps 1:1 to the
   30-bit recipient field of the native 128-bit transaction format.
2. *Checksum-in-address:* analogous in spirit to [EIP-55][] — a
   canonical plain form and a checksummed display form coexist inside
   CAIP-10's own `account_address` production (`[-.%a-zA-Z0-9]{1,128}`),
   which permits both. Xync itself uses only a narrow subset of that
   production: at most 13 characters, no `.` and no `%`, and the two
   halves have different alphabets — the index is decimal, the checksum
   is exactly two Crockford base32 characters.

### Backwards Compatibility

Not applicable.

## Test Cases

All values below are real outputs of the algorithm above and are usable
as test vectors.

```bash
# mainnet account 518, checksummed (display form)
xync:main:518-3Y

# the same account, canonical plain form (accepted, checksum not verified)
xync:main:518

# genesis operator account
xync:main:0-FH

# largest index representable by the protocol (2^30 - 1)
xync:main:1073741823-TV

# devnet, same index — DIFFERENT checksum than mainnet
xync:dev-1:518-0A

# MUST fail: single-digit typo (3Y belongs to 518, not 519 — whose CC is 9A)
xync:main:519-3Y

# MUST fail: correct index, wrong network (0A is the dev-1 checksum)
xync:main:518-0A

# MUST fail: index beyond the 30-bit address space
xync:main:1073741824-XX

# MUST be accepted (Crockford leniency): lower case, I -> 1
xync:main:1-i2      # canonical form: xync:main:1-12
```

| preimage             | digest[0:2] | top 10 bits | CC  |
|----------------------|-------------|-------------|-----|
| xync:main:0         | 7c 59       | 497         | FH  |
| xync:main:1         | 08 8f       | 34          | 12  |
| xync:main:518       | 1f b3       | 126         | 3Y  |
| xync:main:1073741823 | d6 da      | 859         | TV  |
| xync:dev-1:518      | 02 80       | 10          | 0A  |
| xync:main:519       | 4a 9b       | 298         | 9A  |

## References

- [Xync Network Yellow Paper][] - account model, rekey, transaction format
- [EIP-55][] - the precedent of in-identifier optional checksums

[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[EIP-55]: https://eips.ethereum.org/EIPS/eip-55
[Xync Network Yellow Paper]: https://xync.net/papers/yellowpaper.en.pdf

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
