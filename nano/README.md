---
namespace-identifier: nano
title: Nano Namespace
author: Frank Kilkelly (@kilkelly)
status: Draft
type: Informational
created: 2026-11-26
---

# Namespace for Nano

The `nano` namespace gives software a consistent way to distinguish Nano network
environments from one another and from other blockchain ecosystems.
For example, `nano:mainnet` identifies Nano Mainnet, while
`nano:testnet` identifies Nano Testnet.

## Rationale

Nano is a Layer 1 protocol using a block-lattice data structure with distinct Mainnet, Betanet, and
Testnet networks. Each network has its own genesis block and is completely
independent; transactions signed for one network are invalid on another.

## Governance

Nano protocol and public-network upgrades are coordinated by the Nano Foundation
and communicated through official Nano announcements and developer
documentation. Node operators and infrastructure providers adopt the
corresponding software and configuration updates for each network.

## References

- [Nano documentation][nano-docs]
- [Nano node source code][nano-github]
- [Nano official website][nano-home]

[nano-docs]: https://docs.nano.org/
[nano-github]: https://github.com/nanocurrency/nano-node
[nano-home]: https://nano.org/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).