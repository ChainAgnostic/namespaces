---
namespace-identifier: pinet
title: Pi Network Ecosystem
author: Hakkyung Lee (@hklee93)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/199
status: Draft
type: Informational
created: 2026-08-19
requires: ["CAIP-2"]
---

# Namespace for Pi Network Chains

The `pinet` namespace gives software a consistent way to distinguish Pi Network
chains from one another and from other blockchain ecosystems.
For example, `pinet:mainnet` identifies Pi Network Mainnet, while
`pinet:testnet` identifies Pi Network Testnet.

## Rationale

Pi Network is a Layer 1 blockchain with distinct Mainnet and Testnet
environments.
Although its protocol and transaction model are derived from Stellar, Pi
Network has its own governance, validator set, native asset, public
infrastructure, and network passphrases.
Reusing the `stellar` namespace would therefore obscure the operational and
trust boundaries between the ecosystems and could cause software to resolve a
Pi chain as a Stellar network.

The `pinet` namespace keeps those boundaries explicit while retaining short,
human-readable chain references.
Each reference maps deterministically to an exact, case-sensitive Pi Network
passphrase exposed by the network's Horizon API.
Wallets, applications, and cross-chain systems can use that mapping to verify
which Pi Network environment they are connected to before processing accounts,
assets, or transactions.
The mapping and its resolution procedure are defined in the
[Pi Network CAIP-2 Profile][].

## Governance

Pi Network protocol and public-network upgrades are coordinated by the Pi Core
Team and communicated through official Pi Network announcements and developer
documentation.
Node operators and infrastructure providers adopt the corresponding software
and configuration updates for each network.

Changes to this namespace follow the review process of the Chain Agnostic
`namespaces` repository.
A new chain reference should be added only when Pi Network exposes a stable
environment with a distinct network passphrase and deterministic resolution
mechanics.
Temporary or private deployments should not be assigned a shared reference
unless they become persistent interoperability targets.

## References

- [Pi Network CAIP-2 Profile][] - Defines Pi Network chain identifiers and
  their resolution mechanics.
- [CAIP-2][] - Defines the chain-agnostic blockchain identifier format.
- [Pi Whitepaper][] - Introduces the Pi Network protocol, ecosystem, and
  governance model.
- [Pi Developer Documentation][] - Documents Pi Network application and
  blockchain integration.
- [Pi Network Updates][] - Publishes protocol and public-network upgrade
  announcements.

[Pi Network CAIP-2 Profile]: ./caip2.md
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[Pi Whitepaper]: https://minepi.com/white-paper/
[Pi Developer Documentation]: https://developers.minepi.com/
[Pi Developer JS SDK]: https://github.com/pi-apps/pi-platform-docs/
[Pi Network Updates]: https://minepi.com/category/update/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
