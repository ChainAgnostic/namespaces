---
namespace-identifier: acknacki-caip2
title: Acki Nacki Blockchain - Chain ID Specification
author: Mitja Goroshevsky (@Futurizt)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/XXX
status: Draft
type: Standard
created: 2026-04-07
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

Acki Nacki is a layer-1 blockchain identified by a `global_id` integer stored
in every block header. Each network (mainnet, shellnet) has a unique
`global_id` assigned at genesis.

## Specification

### Semantics

Each Acki Nacki network is uniquely identified by its `global_id`, a signed
32-bit integer present in every block. This value is set at genesis and remains
constant for the lifetime of the network.

### Syntax

The `global_id` is used directly as the CAIP-2 reference:

```
acknacki:<global_id>
```

The reference is the decimal string representation of `global_id`.

Validation regex:

```
acknacki:[-]?[0-9]{1,10}
```

### Resolution Mechanics

The `global_id` can be retrieved from any block via the GraphQL API:

```graphql
query {
  blocks(limit: 1) {
    global_id
  }
}
```

**Mainnet endpoint:** `https://mainnet.ackinacki.org/graphql`
**Shellnet endpoint:** `https://shellnet.ackinacki.org/graphql`

Example response:

```json
{
  "data": {
    "blocks": [
      { "global_id": 0 }
    ]
  }
}
```

The returned `global_id` value is the CAIP-2 reference for that network.

## Rationale

Using `global_id` from the block header follows the same pattern as the `tvm`
namespace (which uses the identical field for Everscale and TON). This provides
a simple, deterministic, on-chain verifiable identifier that requires no
external registry.

### Backwards Compatibility

This is the initial specification. No legacy identifiers exist.

## Test Cases

```
# Acki Nacki Mainnet (global_id = 0)
acknacki:0

# Acki Nacki Shellnet / Testnet (global_id = 1)
acknacki:1
```

## References

- [Acki Nacki Documentation][docs] - Official documentation
- [Acki Nacki Developer Portal][dev] - Developer guides, GraphQL API
- [Acki Nacki GitHub][github] - Node software and contracts
- [CAIP-2][] - Blockchain ID Specification

[docs]: https://docs.ackinacki.com
[dev]: https://dev.ackinacki.com
[github]: https://github.com/ackinacki/ackinacki
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
