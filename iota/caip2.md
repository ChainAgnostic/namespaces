---
namespace-identifier: iota-caip2
title: IOTA Namespace - Chains
author: Enrico Marconi (@UMR1352)
status: Draft
type: Informational
created: 2025-07-28
updated: 2025-07-28
---

# CAIP-2

_For context, see the [CAIP-2][] specification._

## Introduction

The IOTA namespace in CAIP-2 uses human-readable chain identifiers — such as `mainnet`, `testnet`, and `devnet` — to identify official IOTA networks.
These identifiers are **stable**, **concise**, and **easy to communicate**, and can be resolved to a unique genesis checkpoint digest through a supported IOTA RPC interface.

This design provides both developer ergonomics and cryptographic assurance, allowing developers to work with simple names while still supporting verifiable chain identification.

When addressing unofficial IOTA networks, genesis checkpoint digests can be used instead of the human-readable aliases defined below.

## Specification

### Semantics

A valid CAIP-2 identifier in the IOTA namespace takes the form:

`iota:<network>`

Where `<network>` is either one of the following reserved, stable identifiers:

- `mainnet`
- `testnet`
- `devnet`

or the first 4 hex-encoded bytes of the genesis checkpoint digest (e.g. `6364aad5` for mainnet).

### Syntax

#### Regular Expression

`^iota:(mainnet|testnet|devnet|[a-f0-9]{8})$`

#### Examples

- `iota:mainnet`
- `iota:6364aad5`

### Resolution Mechanics

To resolve a CAIP-2 `iota:<network>` identifier to a unique chain identitier, clients typically query a trusted full node associated with the specified network.
While the `iotax_getChainIdentifier` JSON-RPC method is commonly used for this purpose, resolution is not limited to JSON-RPC.
Other node interfaces, such as GraphQL, may also support retrieving identifiers pertinent to locating records, such as a genesis checkpoint digest unique to each chain.

**Sample request**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "iotax_getChainIdentifier",
  "params": []
}
```

**Sample response (for mainnet):**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "6364aad5"
}
```

The response returns the first four bytes of the genesis checkpoint digest for the network.

## Rationale

This approach allows developers to use intuitive, readable CAIP-2 identifiers (e.g., `iota:mainnet`) while still achieving unambiguous and verifiable identification of the underlying chain through the genesis checkpoint digest.

The separation of **stable identifiers** (e.g., `iota:testnet`) from the **unambiguous chain identifier** (e.g., the identifier returned by `iotax_getChainIdentifier`) is particularly important because:

- **`testnet` and `devnet` may be reset** by IOTA maintainers, resulting in a new genesis state.
- When this happens, the **genesis checkpoint digest changes**, meaning the underlying chain identifier is no longer the same.
- If clients depended directly on the digest as the CAIP-2 identifier, each reset would break compatibility or require external coordination.
- By resolving the digest dynamically via RPC, clients can ensure they’re talking to the correct chain, without needing to change the CAIP-2 identifier they rely on.

This pattern balances human readability, forward compatibility, and security.

### Backwards Compatibility

There are no legacy identifiers or alternate forms for IOTA chains.

## Test Cases

Below are manually composed examples:

#### IOTA Mainnet

- **CAIP-2 Chain ID:** `iota:mainnet`
- **Resolved Chain Identifier:** `6364aad5`

#### IOTA Testnet

- **CAIP-2 Chain ID:** `iota:testnet`
- **Resolved Chain Identifier:** `2304aa97` _(value depends on the current testnet)_

#### IOTA Devnet

- **CAIP-2 Chain ID:** `iota:devnet`
- **Resolved Chain Identifier:** `e678123a` _(value depends on the current devnet)_

## References

- [IOTA Docs] - Developer documentation and concept overviews for building on IOTA.
- [IOTA RPC] - Reference documentation for interacting with IOTA networks via RPC.
- [IOTA GitHub] - Official GitHub repository for the IOTA smart contract platform.
- [IOTA Network Info] - Information regarding IOTA networks and their release schedules.
- [CAIP-2] - Chain ID Specification.

[IOTA Docs]: https://docs.iota.org/
[IOTA RPC]: https://docs.iota.org/references/iota-api-ref
[IOTA GitHub]: https://github.com/iotaledger/iota
[IOTA Network Info]: https://docs.iota.org/developer/network-overview
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
