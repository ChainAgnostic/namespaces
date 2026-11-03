---
namespace-identifier: radix
title: Radix DLT
author: ["Avaunt (@AVaunt-consulting)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/198
status: Draft
type: Informational
created: 2026-07-28
requires: ["CAIP-2", "CAIP-10", "CAIP-19"]
---

# Namespace for Radix DLT

Radix is a layer-1 network purpose-built for decentralized finance, currently
running the "Babylon" protocol generation (live since September 2023). It is
not EVM-compatible: transactions execute in the Radix Engine, an
asset-oriented execution environment in which tokens ("resources") are native
primitives held in accounts rather than balances inside contract storage.
Transactions are expressed as human-readable "transaction manifests" over an
intent-based transaction model, and are signed by zero or more signatories
before being notarized and submitted.

Radix uses deterministic finality (HotStuff-style BFT): committed transactions
are final, and there are no probabilistic forks. The ledger is a stream of
transactions broken into epochs of roughly five minutes rather than blocks.

All Radix entity addresses (accounts, resources, components, packages) are
bech32m-encoded strings whose human-readable part (HRP) is the concatenation
of an *entity specifier* (e.g. `account_`, `resource_`) and a *network
specifier* (`rdx` for mainnet, `tdx_2_` for the Stokenet public testnet),
making every address self-describing and network-bound.

## Rationale

The namespace identifier `radix` is the network's common name, used across its
documentation, tooling, and deep links (e.g. the `radix:<address>` deposit QR
convention). Networks in this namespace are the Radix Babylon networks: one
production mainnet and a small, governed set of test networks, each defined by
a numeric network ID, a logical name, and an address HRP suffix:

| Network  | Network ID | Logical name | HRP network specifier |
| -------- | ---------- | ------------ | --------------------- |
| Mainnet  | `1`        | `mainnet`    | `rdx`                 |
| Stokenet | `2`        | `stokenet`   | `tdx_2_`              |

The earlier "Olympia" network generation (2021–2023) was retired when its end
state was migrated into Babylon's genesis; Olympia used different address
encodings and is out of scope for this namespace.

## Governance

The Radix protocol and its reference node implementation were originally developed by RDX Works and stewarded by the Radix Foundation. RDX Works has since disbanded and protocol changes are now governed and maintained by the Radix Foundation. Note: As of 3rd August 2026 a Marshall Islands DAO is currently being created with the intention of the Radix Foundation handing over IP, Crypto assets and relevant accounts to the Marshall Islands DAO. The creation of the DAO is expected to be completed before the end of 2026.
Protocol changes ship as named "protocol updates" (e.g. "Anemone", "Bottlenose", "Cuttlefish") which are
enacted at epoch boundaries once a supermajority of validator stake signals
readiness. There is no on-chain permissionless improvement-proposal process;
specifications and integrator guidance are published in the official
documentation and the open-source node and toolkit repositories.

## References

- [Radix Documentation][] - official developer and integrator documentation.
- [Radix Integrator Concepts][] - addresses, networks, transactions, and API guidance for integrators.
- [Well-Known Addresses][] - canonical registry of native addresses (XRD, badges, packages) per network, including each network's ID and HRP suffix.
- [Address Concepts][] - bech32m address structure: entity specifier, network specifier, and 30-byte payload.
- [Babylon Node][] - reference node implementation (Java/Rust).
- [Radix Engine Toolkit][] - offline transaction construction and address derivation/validation library (Rust core; TypeScript, Python and other bindings).
- [Gateway API][] - indexed network API used by wallets and dashboards.
- [Core API][] - node-local API for integrators running their own node.
- [Radix Dashboard][] - the network explorer.

[Radix Documentation]: https://docs.radixdlt.com/
[Radix Integrator Concepts]: https://docs.radixdlt.com/docs/concepts
[Well-Known Addresses]: https://docs.radixdlt.com/docs/well-known-addresses
[Address Concepts]: https://docs.radixdlt.com/docs/concepts
[Babylon Node]: https://github.com/radixdlt/babylon-node
[Radix Engine Toolkit]: https://github.com/radixdlt/radix-engine-toolkit
[Gateway API]: https://radix-babylon-gateway-api.redoc.ly/
[Core API]: https://radix-babylon-core-api.redoc.ly/
[Radix Dashboard]: https://dashboard.radixdlt.com/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
