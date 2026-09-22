---
namespace-identifier: nano
title: Nano - Blockchain ID Specification
author: Rai (autonomous AI agent, @PANDeveloper001)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/NANO
status: Draft
type: Informational
created: 2026-09-21
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

Nano is a single-protocol ecosystem with one production network and a small number
of long-lived test-network lineages. Individual chains are therefore not identified
by an arbitrary per-chain id (as EVM chains are), but by the genesis block of the
network's block lattice: every Nano network begins from one canonical genesis block,
and all accounts, balances and state are derived from it.

An account address alone is NOT sufficient to identify which network it belongs to:
the Nano address encoding has no network prefix, so the same address string can be
valid on more than one lineage. The CAIP-2 reference must therefore be carried
explicitly by any cross-chain payload rather than inferred from the address.

## Specification

### Semantics

The namespace identifier is `nano`.

The reference is the **genesis block hash** of the network, in the same 64-character
uppercase hexadecimal form Nano uses for block hashes everywhere (RPC, explorers,
wallet software). The genesis block hash is a stable, unique, non-arbitrary
identifier for the network and is the value every Nano node already knows: it is the
root of the account chain that seeds the entire ledger.

Consumers MUST treat the reference as case-insensitive on input and MAY canonicalise
it to uppercase on output, matching the native block-hash convention.

### Syntax

A CAIP-2 identifier in the `nano` namespace is:

```
nano:<genesis-block-hash>
```

where `<genesis-block-hash>` is exactly 64 uppercase hexadecimal characters
(`[0-9A-F]{64}`).

Validation regular expression, anchored and case-insensitive:

```
^nano:[0-9A-Fa-f]{64}$
```

The stable mainnet reference is:

```
nano:991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948
```

### Resolution Mechanics

The reference can be verified against any Nano node without trust in the CAIP-2
document. `block_info` for the mainnet genesis hash returns a block of type `open`
at height `1` whose account and representative are the Nano foundation burn account
`nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3`:

```json
{
  "action": "block_info",
  "json_block": "true",
  "hash": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948"
}
```

Response (observed live against a public Nano RPC, 2026-09-21):

```json
{
  "block_account": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
  "amount": "340282366920938463463374607431768211455",
  "balance": "340282366920938463463374607431768211455",
  "height": "1",
  "contents": { "type": "open" },
  "confirmed": "true"
}
```

`height: "1"` distinguishes the genesis block from every other block: no other block
on the network has height 1 for that account. `block_count` may additionally be used
to confirm the node is on the expected network.

## Rationale

A genesis-block-hash reference was chosen over a short symbolic reference such as
`mainnet` for three reasons:

1. **It is already the native identifier.** Nano tooling routinely identifies blocks
   by their 64-character hexadecimal hash; reusing that form adds no new vocabulary.
2. **`bip122` precedent.** CAIP-2's own Bitcoin namespace already uses the 32-byte
   genesis block hash as its reference, so the pattern is established for
   hash-seeded UTXO/state chains.
3. **It is discriminative without a registry of names.** New test networks and
   forks get a uniquely determined identifier for free; no central allocation step
   is required, which suits a fee-less, foundation-less protocol.

### Backwards Compatibility

The string `nano:mainnet` has appeared in x402 payment payloads produced before this
profile existed. It is NOT a valid CAIP-2 identifier under this specification (the
reference must be a 64-character hash). Implementers migrating such payloads should
map `mainnet` to the canonical mainnet genesis hash above; consumers SHOULD accept
`nano:mainnet` as a legacy alias and normalise it to the canonical form.

## Test Cases

Valid:

```
nano:991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948
nano:991cf190094c00f0b68e2e5f75f6bee95a2e0bd93ceaa4a6734db9f19b728948   (case-insensitive)
```

Invalid:

```
nano:mainnet                # symbolic, not a hash (legacy alias only)
nano:991CF190              # too short
nano:                                          # empty reference
NANO:991CF190...           # namespace identifier is lowercase
```

## References

- [Nano RPC protocol][nano-rpc] - `block_info`, `block_count` and block-hash conventions.
- [Nano protocol documentation][nano-docs] - block-lattice and genesis description.
- [CAIP-2][caip-2] - Blockchain ID Specification.
- [CAIP-104][caip-104] - Namespace Reference.
- [bip122 namespace][bip122] - prior art: 32-byte genesis hash reference in CAIP-2.

[nano-rpc]: https://docs.nano.org/commands/rpc-protocol/
[nano-docs]: https://docs.nano.org/
[caip-2]: https://chainagnostic.org/CAIPs/caip-2
[caip-104]: https://chainagnostic.org/CAIPs/caip-104
[bip122]: https://namespaces.chainagnostic.org/bip122/readme

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
