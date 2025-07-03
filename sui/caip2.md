---
namespace-identifier: sui-caip2
title: Sui Namespace - Chains
author: William Robertson (@williamrobertson13)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/146
status: Draft
type: Informational
created: 2025-06-18
updated: 2025-06-18
---

# CAIP-2

_For context, see the [CAIP-2][] specification._

## Introduction

The Sui namespace in CAIP-2 uses human-readable chain identifiers — such as `mainnet`, `testnet`, and `devnet` — to identify specific Sui networks. These identifiers are **stable**, **concise**, and **easy to communicate**, and can be resolved to a unique genesis checkpoint digest through a supported Sui RPC interface.

This design provides both developer ergonomics and cryptographic assurance, allowing developers to work with simple names while still supporting verifiable chain identification.

## Specification

### Semantics

A valid CAIP-2 identifier in the Sui namespace takes the form:

`sui:<network>`

Where `<network>` is one of the following reserved, stable identifiers:

- `mainnet`
- `testnet`
- `devnet`

### Syntax

#### Regular Expression

`^sui:(mainnet|testnet|devnet)$`

Only these exact network identifiers are currently supported.

#### Example

`sui:mainnet`

### Resolution Mechanics

To resolve a CAIP-2 `sui:<network>` identifier into a unique chain identitier, clients typically query a trusted full node associated with the specified network. While the `suix_getChainIdentifier` JSON-RPC method is commonly used for this purpose, resolution is not limited to JSON-RPC. Other node interfaces, such as GraphQL, may also support retrieving identifiers pertinent to locating records, such as a genesis checkpoint digest unique to each chain.

**Sample request**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "suix_getChainIdentifier",
  "params": []
}
```

**Sample response (for mainnet):**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "35834a8a"
}
```

The response returns the first four bytes of the genesis checkpoint digest for the network.

## Rationale

This approach allows developers to use intuitive, readable CAIP-2 identifiers (e.g., `sui:mainnet`) while still achieving unambiguous and verifiable identification of the underlying chain through the genesis checkpoint digest.

The separation of **stable identifiers** (e.g., `sui:testnet`) from the **unambiguous chain identifier** (e.g., the identifier returned by `suix_getChainIdentifier`) is particularly important because:

- **`testnet` and `devnet` may be reset** by Sui maintainers, resulting in a new genesis state.
- When this happens, the **genesis checkpoint digest changes**, meaning the underlying chain identifier is no longer the same.
- If clients depended directly on the digest as the CAIP-2 identifier, each reset would break compatibility or require external coordination.
- By resolving the digest dynamically via RPC, clients can ensure they’re talking to the correct chain, without needing to change the CAIP-2 identifier they rely on.

This pattern balances human readability, forward compatibility, and security.

### Backwards Compatibility

There are no legacy identifiers or alternate forms for Sui chains.

## Test Cases

Below are manually composed examples:

#### Sui Mainnet

- **CAIP-2 Chain ID:** `sui:mainnet`
- **Resolved Chain Identifier:** `35834a8a`

#### Sui Testnet

- **CAIP-2 Chain ID:** `sui:testnet`
- **Resolved Chain Identifier:** `4c78adac` _(value depends on the current testnet)_

#### Sui Devnet

- **CAIP-2 Chain ID:** `sui:devnet`
- **Resolved Chain Identifier:** `aba3e445` _(value depends on the current devnet)_

## References

- [Sui Docs] - Developer documentation and concept overviews for building on Sui.
- [Sui RPC] - Reference documentation for interacting with Sui networks via RPC.
- [Sui GitHub] - Official GitHub repository for the Sui smart contract platform.
- [Sui Network Info] - Information regarding Sui networks and their release schedules.
- [CAIP-2] - Chain ID Specification.

[Sui Docs]: https://docs.sui.io/
[Sui RPC]: https://docs.sui.io/references/sui-api
[Sui GitHub]: https://github.com/MystenLabs/sui
[Sui Network Info]: https://sui.io/networkinfo
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
