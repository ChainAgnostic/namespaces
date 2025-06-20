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

The Sui namespace in CAIP-2 defines chain identifiers based on the **genesis checkpoint digest**, a cryptographically unique and immutable value derived from the first checkpoint of a Sui network. This ensures that identifiers are stable, verifiable, and unambiguous.

## Specification

### Semantics

A valid CAIP-2 identifier in the Sui namespace takes the form:

```
sui:<genesis_checkpoint_digest>
```

Where `<genesis_checkpoint_digest>` is the first 4 bytes (8 hex characters) of the network’s genesis checkpoint digest.

### Syntax

#### Regular Expression

```
^sui:[0-9a-fA-F]{8}$
```

#### Example

```
sui:35834a8a
```

### Resolution Mechanics

To resolve a CAIP-2 chain identifier, clients query a trusted full node associated with the specified network. While the `suix_getChainIdentifier` JSON-RPC method is commonly used for this purpose, resolution is not limited to JSON-RPC. Other interfaces, such as GraphQL, may also support retrieving the corresponding genesis checkpoint digest.

**Sample request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "suix_getChainIdentifier",
  "params": []
}
```

**Sample response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "35834a8a"
}
```

## Rationale

This approach advocates for the exclusive use of unambiguous chain identifiers for identifying Sui chains in CAIP-2 format.

While human-readable identifiers like `sui:mainnet` or `sui:testnet` are intuitive, they are not stable over time. Networks like testnet and devnet may be reset by Sui maintainers, resulting in a new genesis state. When this happens, the associated digest changes, meaning the underlying chain is no longer the same, even if the CAIP-2 identifier remains unchanged.

Using the digest-based identifier directly avoids this ambiguity by ensuring all references point to a specific, verifiable chain instance. This eliminates reliance on potentially outdated or re-used labels and simplifies validation logic.

By relying solely on unambiguous identifiers, we prioritize long-term compatibility, security, and correctness. This ensures that clients consistently interact with the intended chain, even as network environments evolve.

### Backwards Compatibility

There are no legacy identifiers or alternate forms for Sui chains.

## Test Cases

Below are manually composed examples:

```
# CAIP-2 Chain ID for Mainnet**
sui:35834a8a

# CAIP-2 Chain ID for Testnet**
sui:4c78adac

# CAIP-2 Chain ID for Devnet**
sui:aba3e445
```

## References

- [Sui Docs] - Developer documentation and concept overviews for building on Sui.
- [Sui RPC] - Reference documentation for interacting with Sui networks via RPC.
- [Sui GitHub] - Official GitHub repository for the Sui smart contract platform.
- [CAIP-2] - Chain ID Specification.

[Sui Docs]: https://docs.sui.io/
[Sui RPC]: https://docs.sui.io/references/sui-api
[Sui GitHub]: https://github.com/MystenLabs/sui
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
