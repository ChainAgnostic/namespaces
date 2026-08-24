---
namespace-identifier: canton-caip2
title: Canton Namespace - Chains
author: Marc Juchli (@mjuchli-da) <marc.juchli@digitalasset.com>
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/201
status: Draft
type: Standard
created: 2026-08-21
requires: CAIP-2
---

# CAIP-2

For context, see the [CAIP-2](https://chainagnostic.org/CAIPs/caip-2) specification.


## Syntax

CAIP‑2 identifiers follow:

```
chain_id:    namespace + ":" + reference
namespace:   [-a-z0-9]{3,8}
reference:   [-_a-zA-Z0-9]{1,32}
```

CAIP-2 constrains the blockchain reference component to a maximum length of 32 characters and restricts the set of permitted characters. As Canton Synchronizer identifiers do not conform to these constraints, they cannot be used directly as CAIP-2 blockchain identifiers.

### Namespace

The namespace is set to `canton`.

### Reference

To provide a compliant and stable `reference`, Canton Synchronizer IDs **MUST** define a unique network identifier (alias) that satisfies the CAIP-2 reference requirements. This identifier serves as the blockchain reference in the CAIP-2 chain identifier and **MUST** uniquely resolve to the corresponding Synchronizer.

The mapping between a network identifier and its Synchronizer identifier **MUST** be deterministic and authoritative, ensuring that all implementations resolve the same CAIP-2 identifier to the same Canton network.

### Global synchronizers

The `chain_id` for the well known global synchronizers are:

```
canton:mainnet  # Global Synchronizer MainNet
canton:testnet  # Global Synchronizer TestNet
canton:devnet   # Global Synchronizer DevNet
```

See reference below for exact `domainId` values.

### Other synchronizers

Aliases for dedicated synchronizers **MAY** be proposed and **SHOULD** be prefixed with the corresponding network:

```
canton:{mainnet|testnet|devnet}/dedicated-name
```

This approach provides human-readable, interoperable identifiers while decoupling the CAIP representation from Canton's internal identifier format and remaining compatible with future network evolution.

## References

- [The Global Synchronizer](https://docs.canton.network/overview/understand/global-synchronizer#network-environments): DevNet, TestNet, and MainNet environments
- [Scan Global Synchronizer Connectivity API](https://docs.canton.network/sdks-tools/api-reference/splice-scan-gs-connectivity-api): Current synchronizer IDs (`domainId`) for each network

## Rights

Copyright and related rights waived via CC0.
