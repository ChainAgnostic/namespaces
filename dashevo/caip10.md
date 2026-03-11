---
namespace-identifier: dashevo-caip10
title: Dash Platform Namespace - Accounts
author: ["PastaPastaPasta (@PastaPastaPasta)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/177
status: Draft
type: Informational
created: 2026-03-11
updated: 2026-03-11
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Introduction

Dash Platform uses an identity-based account model. Each identity is a
first-class on-chain object that owns cryptographic keys, holds Platform
credits, and can create or update data contracts and documents. This is
fundamentally different from Dash Core's UTXO address model — Platform
identities are persistent entities, not ephemeral transaction outputs.

## Specification

### Semantics

A Dash Platform identity is identified by a 256-bit (32-byte) identifier
derived from the funding outpoint that created it:

```
identity_id = sha256(sha256(funding_outpoint))
```

The `funding_outpoint` is the serialized Dash Core transaction output (txid +
output index) used to fund the identity creation. The double-SHA-256 ensures a
deterministic, collision-resistant mapping from a Layer 1 transaction to a
Platform identity.

The resulting 32-byte identifier is encoded in [base58][] (not base58check —
there is no checksum byte). The typical encoded length is 43-44 characters.

### Syntax

The CAIP-10 identifier for a Dash Platform identity is:

```
dashevo:<chain_id>:<identity_id_base58>
```

Where:
- `<chain_id>` is the Tenderdash chain ID as specified in the [CAIP-2 profile][]
- `<identity_id_base58>` is the base58-encoded 256-bit identity identifier

The regular expression for the account address portion (the `identity_id_base58`
segment) is:

```
[1-9A-HJ-NP-Za-km-z]{43,44}
```

This matches the base58 alphabet (Bitcoin-style, excluding `0`, `O`, `I`, `l`)
with a maximum length of 44 characters (the longest possible base58 encoding of
a 32-byte value).

The full CAIP-10 regular expression is:

```
dashevo:[-a-zA-Z0-9]{1,32}:[1-9A-HJ-NP-Za-km-z]{43,44}
```

### Resolution Mechanics

To verify that an identity exists on a given chain, query the Platform's
identity endpoint via [DAPI][]:

```jsonc
// Request (DAPI gRPC — conceptual representation)
platform.getIdentity({ id: "<identity_id_bytes>" })

// Response
{
  "identity": {
    "id": "EWSqsaghuwHRjtutbXK3nR11KbRkg9a12PNAAkJWRTpY",
    "publicKeys": [ ... ],
    "balance": 1000000,
    "revision": 1
  }
}
```

The identity's `publicKeys` array contains the cryptographic keys authorized to
sign state transitions on behalf of this identity.

## Rationale

The identity-based account model was chosen for Dash Platform because it
supports persistent, key-rotatable identities that can own data contracts and
documents — concepts that do not exist in the UTXO model. The double-SHA-256
derivation from a funding outpoint provides a deterministic link between Layer 1
(Dash Core) and Layer 2 (Dash Platform) without requiring any additional
registration protocol beyond the identity creation state transition.

Base58 encoding (without checksum) is used because Platform identity IDs are
always validated against chain state — the checksum byte used in Dash Core
addresses (base58check) is unnecessary when the canonical identifier is the raw
32 bytes stored on-chain.

## Test Cases

```
# Mainnet identity
dashevo:evo1:EWSqsaghuwHRjtutbXK3nR11KbRkg9a12PNAAkJWRTpY

# Testnet identity
dashevo:dash-testnet-51:GWRSAVFMjXx8HpQFaNJMqBV7MBgMK4br5UESsB4S31Ec
```

## References

- [CAIP-2 Profile][] - Dash Platform CAIP-2 chain identification
- [Dash Platform identity docs][] - Official documentation on Platform identities
- [base58][] - Base58 encoding reference (Bitcoin wiki)
- [DAPI][] - Decentralized API for querying Platform state

[CAIP-2 Profile]: ./caip2.md
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[Dash Platform identity docs]: https://docs.dash.org/projects/platform/en/stable/docs/explanation/identity.html
[base58]: https://en.bitcoin.it/wiki/Base58
[DAPI]: https://docs.dash.org/projects/platform/en/stable/docs/reference/dapi-endpoints.html

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
