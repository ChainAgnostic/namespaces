---
namespace-identifier: keeta
title: Keeta
author: ["@sc4l3r", "@xescure"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/183
status: Draft
type: Informational
created: 2026-04-27
requires: ["CAIP-2"]
---

# Namespace for Keeta

[Keeta][keeta-home] is a Delegated Proof of Stake (DPoS) Layer-1 designed for high-throughput asset transfers.
Its ledger is a [Directed Acyclic Graph (DAG)][whitepaper] of per-account block chains rather than a single linearly-ordered chain: each account publishes blocks to its own chain, and operations in those blocks reference other accounts' chains, which lets independent accounts publish concurrently.

For developers coming from Bitcoin or the EVM, the following differences shape every identifier in this namespace:

- There are no smart contracts.
  Tokens, storage accounts, and the network itself are [accounts][accounts] in the same address space as key-pair-backed accounts, each with a chain of its own.
- A **keyed account** holds a private key and signs its own blocks.
  A **generated account** (also called an identifier account) -- a token, storage account, network account, or multisig -- has no private key, and its blocks are signed by a keyed account holding permission over it.
- An address is the account's public key itself with a type byte and a checksum, base32-encoded, rather than a hash of the key.
  The address alone reveals the account type and signature algorithm.
- Keeta currently supports three signature algorithms (ECDSA over secp256k1, ECDSA over secp256r1, and Ed25519), and its key format is extensible.
- The same key pair produces the same address on every Keeta network, but balances, permissions, and history are per network.
  Generated accounts exist only on the network where they were created.

A Keeta network is identified by an integer `networkId`.
The public networks are main, test, staging, and dev; a privately-launched network runs the same protocol with its own validators, its own ledger, and its own `networkId`.
A network may host subnets, which are subordinate to it and are not identified by this revision of the namespace (see the [CAIP-2 profile][CAIP-2 Profile]).
Every network has a network account and a base token derived from its `networkId`; the base token of the main network is KTA.

## Rationale

Registering the `keeta` namespace enables standard CAIP-2 chain identifiers for every Keeta network distinguished by its numeric `networkId`.
Because Keeta has no contract addresses, the CAIP profiles in this namespace focus on identifying networks, accounts (keyed and generated), and tokens.

## Governance

Keeta uses Delegated Proof of Stake.
Token holders delegate their balance to representatives, which vote on the validity of [vote staples][vote-stapling] (atomic groups of blocks); the consensus rules are determined by the representatives.
Network-wide policy -- for example, the right to create new tokens or storage accounts -- is expressed as permissions on the network account, a generated account that exists once per network.

Protocol decisions are currently made by Keeta Inc. engineers, with occasional input from ecosystem developers; there is no formal improvement-proposal process yet, and this section should be updated when a long-term process is established.
The block structure is versioned so that the protocol can change without disrupting existing operations.
The reference implementation is published as the [`@keetanetwork/keetanet-client`][sdk] TypeScript SDK; the protocol is described in the [Keeta whitepaper][whitepaper].

## References

- [Keeta home][keeta-home] - public site and ecosystem overview.
- [Keeta whitepaper][whitepaper] - protocol specification, DAG model, consensus, and account model.
- [Keeta documentation][keeta-docs] - developer guide and SDK reference.
- [Keeta SDK package][sdk] - the reference implementation that defines `NetworkIDs`, address encoding, and key algorithms cited by the CAIP profiles in this namespace.
- [Public network resources][official-links] - wallet, block explorer, and faucet endpoints for the public main and test networks.

[keeta-home]: https://keeta.com/
[whitepaper]: https://keeta.com/whitepaper.pdf
[keeta-docs]: https://docs.keeta.com/
[sdk]: https://www.npmjs.com/package/@keetanetwork/keetanet-client
[official-links]: https://docs.keeta.com/other-documentation/official-links
[accounts]: https://docs.keeta.com/components/accounts
[vote-stapling]: https://docs.keeta.com/architecture/consensus/vote-stapling
[CAIP-2 Profile]: ./caip2.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
