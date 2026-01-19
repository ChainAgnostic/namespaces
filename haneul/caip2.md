---
namespace-identifier: haneul-caip2
title: Haneul Namespace - Chains
author: Geunhwa Jeong (@GeunhwaJeong)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/168
status: Draft
type: Informational
created: 2026-01-19
updated: 2026-01-19
---

# CAIP-2

_For context, see the [CAIP-2][] specification._

## Introduction

The Haneul namespace in CAIP-2 uses human-readable chain identifiers — such as `mainnet`, `testnet`, and `devnet` — to identify specific Haneul networks. These identifiers are **stable**, **concise**, and **easy to communicate**, and can be resolved to a unique genesis checkpoint digest through a supported Haneul RPC interface.

This design provides both developer ergonomics and cryptographic assurance, allowing developers to work with simple names while still supporting verifiable chain identification.

## Specification

### Semantics

A valid CAIP-2 identifier in the Haneul namespace takes the form:

`haneul:<network>`

Where `<network>` is one of the following reserved, stable identifiers:

- `mainnet`
- `testnet`
- `devnet`

### Syntax

#### Regular Expression

`^haneul:(mainnet|testnet|devnet)$`

Only these exact network identifiers are currently supported.

#### Example

`haneul:testnet`

### Resolution Mechanics

To resolve a CAIP-2 `haneul:<network>` identifier into a unique chain identifier, clients typically query a trusted full node associated with the specified network. While the `haneul_getChainIdentifier` JSON-RPC method is commonly used for this purpose, resolution is not limited to JSON-RPC. Other node interfaces, such as GraphQL, may also support retrieving identifiers pertinent to locating records, such as a genesis checkpoint digest unique to each chain.

**Sample request**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "haneul_getChainIdentifier",
  "params": []
}
```

**Sample response (for testnet):**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "afd5afb7"
}
```

The response returns the first four bytes of the genesis checkpoint digest for the network.

## Rationale

This approach allows developers to use intuitive, readable CAIP-2 identifiers (e.g., `haneul:testnet`) while still achieving unambiguous and verifiable identification of the underlying chain through the genesis checkpoint digest.

The separation of **stable identifiers** (e.g., `haneul:testnet`) from the **unambiguous chain identifier** (e.g., the identifier returned by `haneul_getChainIdentifier`) is particularly important because:

- **`testnet` and `devnet` may be reset** by Haneul maintainers, resulting in a new genesis state.
- When this happens, the **genesis checkpoint digest changes**, meaning the underlying chain identifier is no longer the same.
- If clients depended directly on the digest as the CAIP-2 identifier, each reset would break compatibility or require external coordination.
- By resolving the digest dynamically via RPC, clients can ensure they're talking to the correct chain, without needing to change the CAIP-2 identifier they rely on.

This pattern balances human readability, forward compatibility, and security.

### Backwards Compatibility

There are no legacy identifiers or alternate forms for Haneul chains.

## Test Cases

Below are manually composed examples:

#### Haneul Testnet

- **CAIP-2 Chain ID:** `haneul:testnet`
- **Resolved Chain Identifier:** `afd5afb7`

## References

- [Haneul GitHub] — Official GitHub repository for the Haneul blockchain.
- [Haneul TypeScript SDK] — Official TypeScript SDK for Haneul.
- [CAIP-2] — Chain ID Specification.

[Haneul GitHub]: https://github.com/GeunhwaJeong/haneul
[Haneul TypeScript SDK]: https://github.com/GeunhwaJeong/haneul-ts-sdks
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
