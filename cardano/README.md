---
namespace-identifier: cardano
title: Cardano
author: ["Billy Rennekamp (@okwme)"]
discussions-to: https://github.com/0xcounting/FAR/issues/1
status: Draft
type: Informational
created: 2026-09-14
---

# Namespace for Cardano blockchains

Cardano is a public proof-of-stake blockchain with an extended UTxO ledger, native multi-asset support, and Plutus smart contracts.
The `cardano` namespace covers blockchains running the Cardano node protocol: the mainnet and the public test networks that share its ledger rules, address format, and node interfaces.
Individual blockchains in the namespace are identified by the pair of network identifiers that Cardano itself uses — the network id and the network magic — as specified in the [Cardano CAIP-2 profile][].

Cardano has two distinct network discriminators, which is the main thing a newcomer needs to know.
The **network magic** is a 32-bit number exchanged in the node-to-node handshake, so two nodes with different magics refuse to talk to each other.
The **network id** is a 4-bit value baked into every address header, where `0` means "some testnet" and `1` means mainnet; it is too small to identify a network on its own, and preprod and preview both carry `0`.

## Rationale

### Why `cardano` and not `cip34`

Cardano's own [CIP-34][] ("Chain ID Registry") defines a human-readable chain identifier of the form `cip34:NetworkId-NetworkMagic`, and it was written with CAIP-2 explicitly in mind.
That string has been used as a de facto CAIP-2 identifier — `cip34:1-764824073` for mainnet — even though no `cip34` namespace has ever been registered with CASA.
This proposal keeps CIP-34's reference format unchanged and proposes `cardano` as the namespace instead.

The reason is that CASA namespaces are named for the ecosystem they bound, and `cip34` names a document rather than an ecosystem.
The two existing document-named namespaces, `eip155` and `bip122`, name specifications that bound *cross-ecosystem families* — every EVM chain, every Bitcoin-derived chain — where no single ecosystem name would have been accurate.
CIP-34's registry has no members outside Cardano, so the ecosystem name is both available and more informative.
A spec-derived name is also fragile here: CIP-34 is still `Proposed` rather than `Active`, its acceptance criteria are unmet, and a future CIP superseding it would leave the namespace pointing at a retired document, whereas `cardano` survives any renumbering.
Migration is mechanical, since only the prefix changes: `cip34:1-764824073` becomes `cardano:1-764824073`.

### Asset addressing, for a future CAIP-19 profile

A native asset on Cardano is identified by a **policy id** — the BLAKE2b-224 digest of its minting script, 28 bytes / 56 hex characters — together with an **asset name**, an arbitrary byte string of up to 32 bytes that need not be valid UTF-8 and may be empty.
Neither component is unique alone: the same asset name may exist under many policies.
Ledger serialisations, explorers, and price aggregators such as CoinGecko commonly present the pair as a single concatenated hex string of up to 120 characters, which does not fit CAIP-19's reference limits without a defined split or truncation.
[CIP-14][] defines the user-facing alternative, an `asset1…` fingerprint that bech32-encodes a BLAKE2b-160 digest of `policyId | assetName`; it is a display aid and is not reversible to the underlying pair.
ADA itself is not a native asset and has no policy id.
This document does not propose a CAIP-19 profile; it records the addressing model so that one can be written on top of this namespace.

### About the authors

This namespace was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a CAIP-2 for this chain in order to name 84 assets that exist on it.
The authors do not represent the Cardano ecosystem.
It is offered as a starting point for the Cardano community to correct, adopt or replace, and the authors would rather it carry a maintainer's name than theirs.

## Governance

Technical standards for Cardano are proposed as Cardano Improvement Proposals (CIPs) in the [cardano-foundation/CIPs][] repository.
[CIP-1][] defines that process, the role of the CIP editors, and the `Proposed` / `Active` / `Inactive` statuses; a CIP reaches `Active` only once the acceptance criteria in its own "Path to Active" section are met.
The CIP process is explicitly not itself a governance mechanism for the protocol.

On-chain governance arrived with the Conway ledger era as specified in [CIP-1694][], under which ADA holders delegate voting power to delegated representatives (DReps) who, together with stake pool operators and a constitutional committee, vote on protocol parameter changes, treasury withdrawals, and hard forks.
Neither process allocates network magics: a magic is chosen in a network's genesis configuration by whoever launches it.

## References

- [Cardano CAIP-2 profile][] - Chain ID specification for this namespace
- [CIP-34][] - Chain ID Registry, source of the `NetworkId-NetworkMagic` reference format
- [CIP-34 registry.json][] - Machine-readable registry of Cardano networks with their ids, magics, and genesis hashes
- [CIP-19][] - Cardano address format, including the 4-bit network tag
- [CIP-30][] - dApp-wallet bridge, whose `getNetworkId()` returns the network id
- [CIP-14][] - User-facing asset fingerprint for policy id plus asset name
- [CIP-1][] - The CIP process
- [CIP-1694][] - On-chain governance in the Conway era
- [cardano-node][] - Reference node implementation and the official network configurations
- [Cardano developer portal][] - Concepts, node operation, and test network documentation

[Cardano CAIP-2 profile]: ./caip2.md
[CIP-34]: https://cips.cardano.org/cip/CIP-34
[CIP-34 registry.json]: https://github.com/cardano-foundation/CIPs/blob/master/CIP-0034/registry.json
[CIP-19]: https://cips.cardano.org/cip/CIP-19
[CIP-30]: https://cips.cardano.org/cip/CIP-30
[CIP-14]: https://cips.cardano.org/cip/CIP-14
[CIP-1]: https://cips.cardano.org/cip/CIP-1
[CIP-1694]: https://cips.cardano.org/cip/CIP-1694
[cardano-foundation/CIPs]: https://github.com/cardano-foundation/CIPs
[cardano-node]: https://github.com/IntersectMBO/cardano-node
[Cardano developer portal]: https://developers.cardano.org/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
