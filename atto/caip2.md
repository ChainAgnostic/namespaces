---
namespace-identifier: atto-caip2
title: Atto Namespace - Blockchain ID Specification
author: Felipe Rotilho (@rotilho)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/178
status: Draft
type: Standard
created: 2026-03-18
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

The `atto` namespace identifies Atto chains.
Atto is a native layer-1 payment network with an account-chain model, native address format, native transaction serialization, and lightweight proof-of-work used for anti-spam rather than consensus.

A CAIP-2 identifier in this namespace takes the form `atto:<reference>`.
The reference identifies a concrete Atto network environment such as mainnet, beta/test, a shared development network, or an ephemeral local/private development network.

## Specification

### Semantics

The `atto` namespace is intended for chains that use the native Atto protocol and validation model.
A valid CAIP-2 identifier in this namespace refers to an Atto network that shares Atto's block model, address model, signing rules, and proof-of-work rules.

The following references are defined by this draft:

- `live` — Atto mainnet
- `beta` — Atto public beta / test network
- `dev` — Atto public development network
- `local` — ephemeral local/private network

`atto:dev` is intended for a development deployment that is reachable by multiple participants and stable enough for shared testing, integration work, or external references.
`atto:local` is reserved for local-only, such as integration tests, benchmarks, and developer machines, where a fresh genesis may be created and no persistence or public discoverability is assumed.

### Syntax

An Atto blockchain ID is a CAIP-2 string with namespace `atto` and a lowercase network reference.

Canonical format:

```text
atto:<reference>
```

Reference values currently defined by this draft:

```text
live | beta | dev | local
```

Suggested validation regex:

```text
^atto:(live|beta|dev|local)$
```

Implementations MUST treat the namespace component as exactly `atto`.
Implementations SHOULD treat the reference component as lowercase.
Unknown future references within the `atto` namespace SHOULD be rejected unless explicitly supported by the implementation.

### Resolution Mechanics

Resolution of an Atto CAIP-2 identifier is performed by selecting a node or service configured for the corresponding Atto network environment.
The identifier therefore resolves operationally through network-specific Atto infrastructure rather than through on-chain contract registries.

For public/shared environments, implementations SHOULD map the following identifiers to their corresponding Atto deployments:

- `atto:live` → mainnet infrastructure
- `atto:beta` → public beta/test infrastructure
- `atto:dev` → shared development infrastructure
- `atto:local` → local/private development infrastructure

Implementations SHOULD treat `atto:local` similarly to a localhost-style environment: it is not expected to name a globally shared network, and identifiers using it are not expected to remain reusable outside the local context in which they were created.

If an implementation exposes multiple Atto environments, it MUST ensure that transactions, account state reads, and address validation are performed against infrastructure for the selected Atto chain only.

## Rationale

Atto needs a dedicated namespace because its interoperability assumptions are not those of any existing namespace.
The same client or wallet logic used for EVM, Stellar, or Solana cannot be reused without Atto-specific validation logic.
Atto-native tooling must understand native account-chain state, native address encoding, and Atto-native transaction verification.

The references `live`, `beta`, `dev`, and `local` are chosen because they are short, operationally intuitive, and consistent with how integrators commonly distinguish production, test, development, and local environments.
This draft uses stable, human-readable environment names instead of genesis-derived identifiers, because Atto deployments are intended to be referenced operationally by role.
This draft gives `local` stronger semantics than a generic development label: it is reserved for ephemeral or operator-scoped environments, while `dev` refers to a shared Atto development network that other participants may also target.
This draft intentionally avoids deriving chain identifiers from opaque hashes or environment-specific values that are less legible for wallet and payment tooling.

### Backwards Compatibility

Not applicable.

## Test Cases

```text
# Atto mainnet
atto:live

# Atto public beta / test network
atto:beta

# Atto shared development network
atto:dev

# Atto ephemeral local / private development network
atto:local
```

## Additional Considerations

This draft only defines CAIP-2 identifiers for Atto chains.
Additional Atto namespace profiles may later define:

- CAIP-10 account identifiers for Atto addresses
- CAIP-19 asset identifiers for the native Atto asset and future asset models, if any
- Other Atto-specific profiles where cross-chain tooling benefits from explicit namespace guidance

## References

- [Documentation][] - Official documentation for the Atto ecosystem.
- [Node API Reference][] - Reference for the Atto node RPC and REST interfaces.
- [Integration Guide][] - Overview of Atto components, integration model, and operational guidance.
- [GitHub][] - Source code and development resources.

[Documentation]: https://atto.cash/docs
[Node API Reference]: https://atto.cash/api/node
[Integration Guide]: https://atto.cash/docs/integration
[GitHub]: https://github.com/attocash
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
