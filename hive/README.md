---
namespace-identifier: hive
title: Hive
author: ["@feruzm"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/174
status: Draft
type: Informational
created: 2026-02-25
requires: ["CAIP-2"]
---

# Namespace for Hive

Hive is a delegated-proof-of-stake (DPoS) blockchain focused on social applications, digital publishing, and fast fee-less transactions. It uses account-based identity with human-readable account names.

This document defines the `hive` namespace as a Chain Agnostic Namespace (CAN) to allow standardized identification of Hive networks across multichain tooling using CAIP specifications.

## Rationale

Registering the `hive` namespace enables:

- Standard CAIP-2 chain identifiers for Hive networks
- Use of CAIP-10 account identifiers for Hive account names
- Interoperability with multichain wallets and tooling
- Deterministic identification of Hive networks (mainnet, mirrornet)

Hive networks expose a protocol-defined `chain_id` used in transaction signing to prevent cross-network replay. This makes Hive suitable for deterministic CAIP-2 identification.

## Governance

Hive operates using a Delegated Proof of Stake (DPoS) consensus model. Network upgrades and parameter changes are coordinated by elected block producers ("witnesses") and stakeholders through on-chain governance mechanisms.

## References

- Hive homepage: https://hive.io/
- Hive developer portal: https://developers.hive.io/
- Hive configuration values (includes chain_id):  
  https://developers.hive.io/tutorials-recipes/understanding-configuration-values.html

## Copyright

Copyright and related rights waived via CC0 1.0.
