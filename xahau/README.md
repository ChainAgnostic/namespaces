---
namespace-identifier: xahau
title: Xahau Ecosystem
author: Ekiserrepé (@Ekiserrepe)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/231
status: Draft
type: Informational
created: 2026-09-28
requires: ["CAIP-2", "CAIP-10", "CAIP-19", "CAIP-122"]
---

# Namespace for Xahau Chains

Xahau is a decentralized Layer 1 blockchain derived from the XRP Ledger
protocol.
It is powered by the open-source `xahaud` server and uses XAH as its native
asset.

Xahau extends the XRP Ledger protocol with Hooks, which are small WebAssembly
programs attached to accounts.
Hooks can inspect and control transactions, maintain state, and emit new
transactions.
Xahau also provides network-specific transaction types, ledger objects, and
server definitions for applications that serialize and sign transactions.

## Rationale

The `xahau` namespace distinguishes Xahau chains from other networks based on
the XRP Ledger protocol.
Although Xahau shares its consensus ancestry, address encoding, and much of its
API with the XRP Ledger, its Hooks execution environment, native asset,
transaction types, ledger objects, governance, and dynamically published server
definitions form a distinct application and tooling ecosystem.

Each Xahau chain is identified by the numeric network ID returned by its
`server_info` API response.
The network ID is also included in signed Xahau transactions for replay
protection.

Xahau accounts use checksummed classic addresses beginning with `r`.
The ecosystem supports native XAH, account-issued fungible tokens, and
URI Tokens as its native non-fungible asset type.
Xahau accounts can also authenticate with off-chain services through the
CAIP-122 profile defined by this namespace.

## Governance

The Xahau protocol is implemented in the open-source `xahaud` repository.
Protocol amendments are activated through validator voting, while the Genesis
Hook provides on-ledger governance for network-level responsibilities defined
by the Xahau protocol.

## References

- [Xahau Documentation][] - Official developer and protocol documentation.
- [Xahau Whitepaper][] - Architecture, Hooks, tokenomics, and governance.
- [xahaud][] - Open-source server implementation for the Xahau network.
- [CAIP-2 Profile](./caip2.md) - Xahau blockchain identifiers.
- [CAIP-10 Profile](./caip10.md) - Xahau account identifiers.
- [CAIP-19 Profile](./caip19.md) - Xahau asset identifiers.
- [CAIP-122 Profile](./caip122.md) - Sign-In With Xahau.

[Xahau Documentation]: https://xahau.network/docs/
[Xahau Whitepaper]: https://xahau.network/docs/resources/whitepaper/
[xahaud]: https://github.com/Xahau/xahaud

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
