---
namespace-identifier: xync
title: Xync Network Namespace
author: Xync Network (@XyncNet)
status: Draft
type: Informational
created: 2026-07-08
---

# Namespace for Xync Network

**Xync Network** ("xync") is a payments-only Layer-1 blockchain: the
protocol supports exactly two user operations — *send money* and
*request money* — in up to 255 protocol-native currencies plus the
native token XYNC. There is no virtual machine and no general-purpose
smart contracts.

Key architectural facts relevant to cross-chain developers:

- **Finality:** consensusless fastpath (FastPay-style attestation
  quorums, 2f+1 of n validators) finalizes a transfer in one network
  round trip (~0.3 s); a lazy uncertified DAG orders rare system
  events (registrations, validator-set changes, checkpoints).
- **Accounts:** compact integer indexes issued sequentially at paid
  registration (`0` is the genesis operator). Public keys are
  *rotatable* (`rekey`), so the stable account identifier is the
  index, not a key or its hash. This drives the CAIP-10 design.
  Internally an account holds one *currency account* per currency it
  spends from (the pair "user + currency", carrying that currency's
  sequence number); the CAIP-10 address names the user, which is all a
  payer needs — receiving never requires a currency account.
- **Transactions:** the entire transfer packs into 128 bits (= UUID);
  a signed transfer is 80 bytes on the wire.
- **Currencies:** a protocol-level registry of up to 255 currencies
  (fiat-backed by regulated issuers, wrapped coins, loyalty units)
  addressed by a single byte — the basis of the CAIP-19 profile.

Profiles in this namespace:

- [caip2.md](caip2.md) — Blockchain ID (`xync:main`)
- [caip10.md](caip10.md) — Account ID (`xync:main:518-3Y`)
- [caip19.md](caip19.md) — Asset ID (`xync:main/cur:1`)

## Rationale

The namespace addresses everything by the smallest stable number the
protocol already assigns, rather than by a cryptographic artifact:
networks by their genesis `chain_id`, accounts by their integer index,
currencies by their single-byte registry code. Keys are rotatable and
therefore unfit as identifiers; hashes would be verbose and, for
accounts, would require an on-chain reverse index. The three profiles
map onto the protocol's own numbering — a CAIP-10 index is literally the
recipient field of the native 128-bit transaction — so a CAIP identifier
converts to its on-the-wire form without transformation.

## Governance

Network names (CAIP-2 references) and currency codes (CAIP-19
references) are assigned by Xync Network governance and recorded in the
network's canonical, content-addressed genesis file. That file's
SHA-256 is co-signed by the validator checkpoint quorum (2f+1 of n), so
every reference resolves to exactly one genesis and is verifiable
against live checkpoints. Account references are issued by the protocol
itself, sequentially, at registration.

## References

- [Xync Network Yellow Paper][] - full protocol specification
- [XyncPay][] - the live payment product operating on the network

[Xync Network Yellow Paper]: https://xync.net/papers/yellowpaper.en.pdf
[XyncPay]: https://t.me/XyncPayBot

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
