---
namespace-identifier: flow-caip2
title: Flow Namespace - Chains
author: Hao Fu
discussions-to: https://github.com/ChainAgnostic/namespaces/issues/163
status: Draft
type: Informational
created: 2026-01-13
requires: CAIP-2
---

# CAIP-2

_For context, see the [CAIP-2][] specification._

## Introduction

The Flow namespace uses short, human-readable network identifiers.
These identifiers are stable and map to distinct Flow networks.

## Specification

### Semantics

A valid Flow CAIP-2 identifier takes the form:

`flow:<network>`

Where `<network>` is one of the following reserved identifiers:

- `mainnet`
- `testnet`

### Syntax

#### Regular Expression

`^flow:(mainnet|testnet)$`

#### Example

`flow:mainnet`

### Resolution Mechanics

Clients should resolve a Flow network identifier by querying the Flow REST API network parameters endpoint for the target network and verifying the returned `chain_id`.

**Sample request (mainnet):**

`GET https://rest-mainnet.onflow.org/v1/network/parameters`

**Sample response:**

```json
{
  "chain_id": "flow-mainnet"
}
```

## Rationale

Stable, human-readable network names provide a simple and consistent way to identify Flow networks across tooling.

### Backwards Compatibility

There are no legacy identifiers for Flow networks in this namespace.

## Test Cases

- **Flow Mainnet:** `flow:mainnet`
- **Flow Testnet:** `flow:testnet`

## References

- [Flow] - Official Flow website and documentation portal.
- [CAIP-2] - Chain ID Specification.

[Flow]: https://flow.com
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
