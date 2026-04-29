---
namespace-identifier: keeta
title: Keeta
author: ["@sc4l3r"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/XXXX
status: Draft
type: Informational
created: 2026-04-27
requires: ["CAIP-2"]
---

# Namespace for Keeta

[Keeta][keeta-home] is a Delegated Proof of Stake (DPoS) Layer-1 designed for high-throughput asset transfers, real-world asset tokenization, and built-in compliance primitives (KYC, sanctions, ACLs).
The protocol uses a [Directed Acyclic Graph (DAG)][whitepaper] of per-account block chains rather than a single linearly-ordered ledger, which lets independent accounts publish concurrently and lets the network achieve sub-second finality.

The `keeta` namespace describes both the public Keeta main network and any of its sibling networks -- the test, staging, and dev networks, and any privately-launched **sub-network** (a private instance that runs the same protocol but with isolated transaction visibility and its own validator set).
All networks share the same key-pair format, address encoding, and operation set, so a single Keeta key pair can be used across networks and the only thing that distinguishes one from another in CAIP terms is its `networkId`.

## Rationale

Registering the `keeta` namespace enables standard CAIP-2 chain identifiers for every Keeta network distinguished by their numeric `networkId`.
Keeta does not run an EVM or similar and has no smart-contract addresses.
Therefore, CAIP profiles in this namespace focus on identifying networks, accounts (keyed and identifier-style), and tokens, not contracts.

## Governance

Keeta uses Delegated Proof of Stake.
Token holders elect representatives, which vote on the validity of vote staples (atomic groups of blocks).
Network-wide policy -- for example, the right to create new tokens or storage accounts -- is expressed as permissions on the [Network Account][accounts], a deterministically-generated identifier account that exists once per network.

Protocol changes are coordinated by Keeta Token Genesis LLC and the validator set.
The reference implementation is published as the [`@keetanetwork/keetanet-client`][sdk] TypeScript SDK; the protocol specification is described in the [Keeta whitepaper][whitepaper].

## References

- [Keeta home][keeta-home] - public site and ecosystem overview.
- [Keeta whitepaper][whitepaper] - protocol specification, DAG model, consensus, and account model.
- [Keeta documentation][keeta-docs] - developer guide, SDK reference, and anchor framework.
- [Keeta SDK source][sdk] - the canonical reference implementation that defines `NetworkIDs`, address encoding, and key algorithms cited by the CAIP profiles in this namespace.
- [Public network resources][official-links] - wallet, block explorer, and faucet endpoints for the public main and test networks.

[keeta-home]: https://keeta.com/
[whitepaper]: https://keeta.com/whitepaper.pdf
[keeta-docs]: https://docs.keeta.com/
[sdk]: https://github.com/KeetaNetwork/keetanet-client
[official-links]: https://docs.keeta.com/other-documentation/official-links
[accounts]: https://docs.keeta.com/components/accounts

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
