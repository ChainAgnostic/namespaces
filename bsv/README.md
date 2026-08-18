---
namespace-identifier: bsv
title: BSV Blockchain
author: Deggen (@sirdeggen) <d.kellenschwiler@bsvassociation.org>
status: Draft
type: Informational
created: 2026-07-10
requires: ["CAIP-2"]
---

# Namespace for the BSV Blockchain

BSV is a proof-of-work UTXO blockchain descended from the original Bitcoin protocol.
This namespace identifies BSV networks by their human-readable network name, mirroring
how BSV wallets and application infrastructure already refer to the network they
operate on.

Registered networks:

- `bsv:mainnet` — BSV main network
- `bsv:testnet` — BSV public test network
- `bsv:ttn` — Teranode Test Net (public Teranode scaling test network / Teratestnet)
- `bsv:tstn` — Teranode Scaling Test Net (private, per-deployment scaling test network)

## Rationale

BSV shares its genesis block with BTC and BCH, all three tracing back to Satoshi's
2009 genesis block. The [bip122][] namespace disambiguates such forks by using the
hash of the first block *after* divergence rather than the genesis hash — Bitcoin Cash,
for example, is registered as `bip122:000000000000000000651ef99cb9fcbe`. A BSV
identifier could in principle be constructed the same way, from BSV's fork block.

This namespace exists for a different reason. The BSV application layer — BRC-100
wallets, overlay services, ARC transaction broadcasters, and SPV clients — universally
identifies a network by a stable human-readable name, never by a fork-block hash.
A BRC-100 wallet self-reports its network via a `getNetwork` call; SV Node's
`getblockchaininfo` returns a `chain` field of `main` or `test`. A CAIP-2 identifier
that mirrors this name lets cross-chain tooling (payment protocols such as x402,
CAIP-10 account references, CAIP-19 asset references) map directly onto the
identifiers applications already exchange, without a full-node RPC round-trip to
recover a fork-block hash. Following the precedent set by the [casper][] namespace,
whose Chain ID "should not be confused with the genesis_hash," this namespace uses
the network name as the CAIP-2 reference.

`ttn` and `tstn` are included so high-throughput payment protocols can exercise
Teranode test environments without overloading `bsv:testnet` or inventing ad-hoc
names that later need client migration.

## Governance

The BSV protocol is stewarded by the [BSV Association][], a Switzerland-based
non-profit that maintains the network's technical standards and the reference node
implementation. Application-layer standards are published through the openly editable
[BRC (Bitcoin Request for Comment)][BRCs] process, which defines wallet interfaces
(BRC-100), key derivation (BRC-42/BRC-43), payment protocols (BRC-29), and transaction
serialization (BRC-62/BRC-95), among others. Changes to this namespace should be
discussed with the BSV Association and the BRC maintainers.

## References

- [BSV Association][] - the non-profit stewarding the BSV protocol and its standards
- [BRCs][] - the Bitcoin Request for Comment repository defining BSV application standards
- [bip122][] - the CAIP-2 namespace for Bitcoin-based networks, which identifies forks by fork-block hash
- [casper][] - a CAIP-2 namespace precedent using a human-readable Chain ID rather than a genesis hash

[BSV Association]: https://www.bsvblockchain.org/
[BRCs]: https://github.com/bitcoin-sv/BRCs
[BRC-100]: https://github.com/bitcoin-sv/BRCs/blob/master/wallet/0100.md
[bip122]: https://namespaces.chainagnostic.org/bip122/README
[casper]: https://namespaces.chainagnostic.org/casper/README

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
