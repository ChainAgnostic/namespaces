---
namespace-identifier: nano
title: Nano
author: Rai (autonomous AI agent, @PANDeveloper001)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/NANO
status: Draft
type: Informational
created: 2026-09-21
requires: ["CAIP-2"]
---

# Namespace for Nano

Nano is a fee-less, block-lattice digital currency. Each account owns its own chain
of blocks, so there is no global block height and no mining: a "block" is a signed
state change on one account's chain. Accounts are addressed by a 65-character
`nano_`-prefixed string, and there is exactly one public network and one live
test-network lineage to disambiguate.

## Rationale

Nano already appears in cross-chain payment payloads without a CAIP-2 namespace
profile: x402 (the HTTP `402 Payment Required` payment scheme) resources in the wild
declare `network: "nano:mainnet"` today. Because CAIP-2 is the identifier format
those payloads are supposed to use, that string is currently an unstandardised
identifier — implementers must guess at the reference it should carry. This document
supplies the missing namespace profile so `nano:<reference>` has a defined syntax and
a well-known mainnet value.

The `nano` namespace is deliberately chain-agnostic in the same sense as `bip122`:
one namespace covers the Nano protocol's networks.

## Governance

Nano has no foundation-controlled protocol upgrade process. Protocol changes are
proposed as Nano Enhancement Proposals (NEPs) and adopted by node implementation and
network consensus; the reference implementation is `nanocurrency/nano-node`. CAIP
profiles for this namespace should follow the CAIP-104 namespace governance: a
`discussions-to` URL for each profile and editor review via pull request.

## References

- [Nano protocol documentation][nano-docs] - protocol overview and block-lattice model.
- [Nano RPC documentation][nano-rpc] - `block_info`, `block_count` and related calls used below.
- [nano-node][nano-node] - the reference node implementation.
- [CAIP-2][caip-2] - Blockchain ID Specification.
- [CAIP-104][caip-104] - Namespace Reference.

[nano-docs]: https://docs.nano.org/
[nano-rpc]: https://docs.nano.org/commands/rpc-protocol/
[nano-node]: https://github.com/nanocurrency/nano-node
[caip-2]: https://chainagnostic.org/CAIPs/caip-2
[caip-104]: https://chainagnostic.org/CAIPs/caip-104

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
