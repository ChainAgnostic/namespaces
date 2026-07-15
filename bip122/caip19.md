---
namespace-identifier: bip122-caip19
title: BIP122 Namespace - Assets (Ordinals Inscriptions)
author: ordspv (https://github.com/ordspv)
status: Draft
type: Standard
created: 2026-07-11
requires: ["CAIP-19", "BIP-122"]
---

## CAIP-19

*For context, see the [CAIP-19][] specification.*

This profile defines the `ordinals` asset namespace for addressing **ordinals
inscriptions** (content inscribed in Bitcoin transaction witnesses per the
[ordinals protocol][ord-docs] as assets within [BIP-122][] chains.

## Syntax

```
asset_type:      chain_id + "/ordinals:" + inscription_id
chain_id:        per the BIP-122 CAIP-2 profile
                 (e.g. bip122:000000000019d6689c085ae165831e93 for mainnet)
inscription_id:  txid + "i" + index
txid:            64 lowercase hex characters (display-order reveal txid)
index:           decimal envelope index, no leading zeros (0 allowed)
```

An inscription id is **self-certifying**: the txid commits to the reveal transaction whose witness carries the envelope at the given index, so the asset reference can be verified against Bitcoin consensus data without any trusted indexer (SPV-grade verification levels are specified in the companion [verification spec][spec-verification].

`asset_namespace` = `ordinals` (8 chars, within CAIP-19's `[-a-z0-9]{3,8}`).
`asset_reference` = the inscription id (66–75 chars, within CAIP-19's
`[-.%a-zA-Z0-9]{1,128}`; the only non-hex character is the literal `i`).
No `token_id` component is used: an inscription is a singleton asset, not a class with instances.

### Canonicalization

- txid hex MUST be lowercase; the index MUST be canonical decimal (no leading zeros, no `+`).
- Consumers MUST treat two asset ids differing only in txid case as the same asset but SHOULD emit lowercase only.

### Out of scope

- **Sat (ordinal-number) addressing is explicitly out of scope.** A satpoint or sat number designates a *location* tracked by an ord indexer's transfer history: a trusted-index artifact, not a self-certifying reference. This profile addresses the inscribed ASSET; where an application needs "the current location of inscription X", that is an indexer query, not an asset id.
- Inscription **numbers** (`#123`, negative for cursed) are display aliases assigned by indexer policy and MUST NOT appear in asset ids.
- Runes and other Bitcoin metaprotocols are separate namespaces.

## Rationale

Inscriptions are a major class of non-native Bitcoin assets; wallets and marketplaces exchanging chain-agnostic asset descriptors (CAIP-19 consumers: WalletConnect, indexer APIs, token lists) currently have no standard way to name one. The `ordinals` namespace reuses the ecosystem's existing canonical identifier verbatim, the same id used by `ord:` URIs, ord server endpoints, and recursive inscriptions, so no mapping layer is required and the reference remains verifiable end-to-end.

## Test Cases

```
# inscription 0, Bitcoin mainnet
bip122:000000000019d6689c085ae165831e93/ordinals:6fb976ab49dcec017f1e201e84395983204ae1a7c2abf7ced0a85d692e442799i0

# a batch-minted inscription at envelope index 665
bip122:000000000019d6689c085ae165831e93/ordinals:11d3f4b39e8ab97995bab1eacf7dcbf1345ec59c07261c0197e18bf29b88d8dai665

# INVALID: inscription number, not an id
bip122:000000000019d6689c085ae165831e93/ordinals:0
# INVALID: sat addressing out of scope
bip122:000000000019d6689c085ae165831e93/ordinals:1252201400444387
# INVALID: uppercase txid (non-canonical)
bip122:000000000019d6689c085ae165831e93/ordinals:6FB976ABi0
```

## References

- [CAIP-19][]: Asset Type and Asset ID Specification
- [BIP-122][]: URI scheme for blockchain references (chain ids)
- [bip122 CAIP-2 profile][bip122-caip2]: chain id derivation
- [ordinals protocol docs][ord-docs]: inscription ids, envelopes
- [`ord:` URI draft][ord-uris] and the companion [verification spec][spec-verification]

[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-19.md
[BIP-122]: https://github.com/bitcoin/bips/blob/master/bip-0122.mediawiki
[bip122-caip2]: https://namespaces.chainagnostic.org/bip122/caip2
[ord-docs]: https://docs.ordinals.com/inscriptions.html
[ord-uris]: https://docs.ordinals.com/inscriptions/uris.html
[spec-verification]: https://github.com/ordspv/ordspv/blob/master/docs/spec/SPEC-VERIFICATION.md
