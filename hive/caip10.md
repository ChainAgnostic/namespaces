---
namespace-identifier: hive-caip10
title: Hive Namespace - CAIP-10 Account Identifiers
author: ["@feruzm"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/174
status: Draft
type: Standard
created: 2026-02-25
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

For context, see the CAIP-10 specification:
https://chainagnostic.org/CAIPs/caip-10

## Rationale

Hive uses account-based identity with human-readable account names rather than hexadecimal address formats.

Each Hive account name:

- Is globally unique within a Hive network
- Is used directly in transaction operations
- Is validated at the protocol level
- Is constrained by naming rules enforced by consensus

Because Hive accounts are stable identifiers and tied to a specific chain via `chain_id`, they are suitable for CAIP-10 account identifiers.

## Specification

A Hive CAIP-10 account identifier MUST follow:

`hive:<reference>:<account>`

Where:

- `hive` is the namespace
- `<reference>` is defined by the Hive CAIP-2 profile
- `<account>` is a valid Hive account name

### Account Format

Hive account names MUST:

- Be between 3 and 16 characters in total length
- Start with a lowercase letter (`a-z`)
- Contain only lowercase letters (`a-z`), digits (`0-9`), hyphens (`-`), and dots (`.`)
- Not start or end with a hyphen or dot
- Not contain consecutive hyphens or dots
- If dot-separated, each segment must be at least 3 characters and start with a letter

Regex:

```
^(?=.{3,16}$)[a-z]([0-9a-z]|[0-9a-z\-](?=[0-9a-z])){2,}([\.](?=[a-z][0-9a-z\-][0-9a-z\-])[a-z]([0-9a-z]|[0-9a-z\-](?=[0-9a-z])){1,}){0,}$
```

### Resolution

To validate a Hive CAIP-10 identifier:

1. Parse the namespace (`hive`).
2. Validate the CAIP-2 reference according to the Hive CAIP-2 profile.
3. Validate the account name against Hive naming rules.
4. Query a Hive RPC endpoint to confirm account existence.

Account existence may be verified via:

- `condenser_api.get_accounts`
- `database_api.find_accounts`

#### Example Request

```json
{
  "jsonrpc": "2.0",
  "method": "condenser_api.get_accounts",
  "params": [["ecency"]],
  "id": 1
}
```

## Examples

### Hive Mainnet

```
hive:beeab0de000000000000000000000000:ecency
hive:beeab0de000000000000000000000000:good-karma
hive:beeab0de000000000000000000000000:hive.fund
hive:beeab0de000000000000000000000000:v4vapp.dhf
```

### Hive Mirrornet

```
hive:42000000000000000000000000000000:testuser
```

## Security Considerations

Hive account names are human-readable and may be subject to phishing using visually similar names (e.g., `ecency` vs `ecency-fake`).

Applications SHOULD:

- Validate account existence before processing transactions
- Display full CAIP-10 identifiers when clarity is required
- Not assume account ownership without authority verification

Because Hive supports multiple authorities (owner, active, posting), CAIP-10 identifiers represent accounts, not individual keys.

## Test Cases

Valid:

```
hive:beeab0de000000000000000000000000:ecency
hive:beeab0de000000000000000000000000:good-karma
hive:beeab0de000000000000000000000000:hive.fund
hive:beeab0de000000000000000000000000:gtg
hive:42000000000000000000000000000000:test-account
```

Invalid:

```
hive:beeab0de000000000000000000000000:UpperCase
hive:beeab0de000000000000000000000000:ab
hive:beeab0de000000000000000000000000:-invalid
hive:beeab0de000000000000000000000000:3digits
hive:beeab0de000000000000000000000000:has..double
```

## References

- Hive configuration and account rules:
  https://developers.hive.io/tutorials-recipes/understanding-configuration-values.html
- CAIP-10 specification:
  https://chainagnostic.org/CAIPs/caip-10

## Copyright

Copyright and related rights waived via CC0 1.0.
