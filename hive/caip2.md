---
namespace-identifier: hive-caip2
title: Hive Namespace - CAIP-2 Chain Identifiers
author: ["@feruzm"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/174
status: Draft
type: Standard
created: 2026-02-25
requires: CAIP-2
---

# CAIP-2

For context, see the CAIP-2 specification:
https://chainagnostic.org/CAIPs/caip-2

## Rationale

Hive defines a 32-byte (`64` hex characters) `chain_id` value used for transaction signing and network identification.

Because CAIP-2 restricts the `reference` field to a maximum of 32 characters, this specification defines the `reference` as:

> The first 32 lowercase hexadecimal characters of Hive's `chain_id`.

This approach ensures:

- Deterministic chain identification
- Compatibility with CAIP-2 length constraints
- Collision resistance appropriate for blockchain network identifiers
- Alignment with other CAIP-2 namespace implementations

## Specification

### Namespace

`hive`

### Reference

The `reference` MUST:

- Be lowercase hexadecimal
- Match the pattern: `[0-9a-f]{32}`

### Resolution

To derive a valid CAIP-2 identifier:

1. Query a Hive node using `database_api.get_config`.
2. Retrieve the `HIVE_CHAIN_ID` value from the response.
3. Convert to lowercase.
4. Truncate to the first 32 hexadecimal characters.

#### Example Request

```json
{
  "jsonrpc": "2.0",
  "method": "database_api.get_config",
  "id": 1
}
```

#### Example Response (partial)

```json
{
  "HIVE_CHAIN_ID": "beeab0de00000000000000000000000000000000000000000000000000000000"
}
```

## Known Networks (Non-Normative Examples)

### Hive Mainnet

Full chain_id: `beeab0de00000000000000000000000000000000000000000000000000000000`
CAIP-2: `hive:beeab0de000000000000000000000000`

---

### Hive Mirrornet

Full chain_id: `42`
CAIP-2: `hive:42000000000000000000000000000000` (zero-padded to 32 hex characters)

> **Note:** The mirrornet is a periodic snapshot of mainnet used for testing. There is no permanent public testnet at this time; mirrornet instances are ephemeral.

## Security Considerations

Applications MUST validate network configuration before accepting CAIP-2 identifiers.

Hive uses account-based identity rather than address-based identity. Applications implementing CAIP-10 should validate account existence via RPC.

## Test Cases

```
hive:beeab0de000000000000000000000000
hive:42000000000000000000000000000000
```

## References

- Hive configuration documentation:
  https://developers.hive.io/tutorials-recipes/understanding-configuration-values.html
- CAIP-2 specification:
  https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via CC0 1.0.
