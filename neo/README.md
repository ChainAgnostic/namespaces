---
namespace-identifier: neo
title: Neo
author: Erik Zhang (@erikzhang)
discussions-to: https://github.com/neo-project/proposals/issues/238
status: Draft
type: Informational
created: 2026-07-19
---

# Namespace for Neo blockchains

Neo is an open-source, community-driven blockchain platform for digital assets
and smart contracts.
The `neo` namespace covers blockchains that implement the Neo N3 protocol and
expose its native node and JSON-RPC interfaces.
Individual blockchains in the namespace are identified by their Network Magic
as specified in the [Neo CAIP-2 profile](./caip2.md).

## Rationale

Neo N3 networks share the same transaction and block formats, NeoVM execution
environment, account model, and node interfaces.
A dedicated namespace gives applications a common identifier for these
protocol-level assumptions while allowing MainNet, TestNet, and independently
operated networks to remain distinguishable.

## Governance

Technical standards for Neo are proposed as Neo Enhancement Proposals (NEPs).
[NEP-1][] defines the proposal process and requires proposal authors to build
community consensus around their specifications.

Neo N3 also has on-chain governance in which NEO token holders elect the Neo
Council and consensus nodes.
The initial design of this namespace was discussed publicly in the
[Neo namespace discussion][].

## References

- [Neo documentation][] - Concepts, node operation, and JSON-RPC documentation
- [Neo source code][] - Reference implementation of the Neo N3 protocol
- [NEP-1][] - Neo Enhancement Proposal purpose and guidelines
- [Neo governance][] - Neo N3 governance roles and voting model
- [Neo namespace discussion][] - Community discussion of the namespace and CAIP-2 profile

[Neo documentation]: https://docs.neo.org/docs/n3/
[Neo source code]: https://github.com/neo-project/neo
[NEP-1]: https://github.com/neo-project/proposals/blob/master/nep-1.mediawiki
[Neo governance]: https://docs.neo.org/docs/n3/foundation/governance.html
[Neo namespace discussion]: https://github.com/neo-project/proposals/issues/238

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
