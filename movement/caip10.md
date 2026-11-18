---
namespace-identifier: movement-caip10
title: Movement Namespace - CAIP-10 Account Identifiers
author: Andy Golay (@andygolay)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/179
status: Draft
type: Standard
created: 2026-03-23
updated: 2026-03-23
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

Movement uses account-based identity with 32-byte hexadecimal addresses.

Each Movement account address:

- Is globally unique within a Movement network
- Is used directly in transaction operations
- Is derived from the account's authentication key at creation
- Is represented as a hex string with a `0x` prefix

Because Movement addresses are stable identifiers and tied to a specific chain via `chain_id`, they are suitable for CAIP-10 account identifiers.

## Specification

A Movement [CAIP-10][] account identifier MUST follow:

`movement:<reference>:<address>`

Where:

- `movement` is the namespace
- `<reference>` is defined by the Movement [CAIP-2 Profile][]
- `<address>` is a valid Movement account address

### Address Format

Movement account addresses MUST:

- Begin with `0x`
- Be followed by 1 to 64 hexadecimal characters (`0-9`, `a-f`, `A-F`)
- Represent a 32-byte (256-bit) value
- Be case-insensitive

The canonical form is the full zero-padded 66-character representation (`0x` + 64 hex characters). Shortened forms that omit leading zeros (e.g., `0x1`) are valid but SHOULD be expanded to the full form for CAIP-10 identifiers.

Regex:

```
^0x[0-9a-fA-F]{1,64}$
```

### Resolution

To validate a Movement CAIP-10 identifier:

1. Parse the namespace (`movement`).
2. Validate the CAIP-2 reference according to the Movement [CAIP-2 Profile][].
3. Validate the address against the address format rules above.
4. Query a Movement REST API endpoint to confirm account existence.

Account existence may be verified via the [REST API][]:

#### Example Request

```bash
curl https://mainnet.movementnetwork.xyz/v1/accounts/0x1
```

#### Example Response

```jsonc
{
  "sequence_number": "0",
  "authentication_key": "0x0000000000000000000000000000000000000000000000000000000000000001"
}
```

The API returns account data for any valid address format. An account with
`sequence_number` of `"0"` and no on-chain resources may not have been
explicitly created yet.

## Examples

### Movement Mainnet

```
movement:126:0x0000000000000000000000000000000000000000000000000000000000000001
movement:126:0x1
movement:126:0xd5fb7899ac1e3b4a51bfbf0dcafaa78453bb8e9a64a93a8e47fedad6b8c48171
```

### Movement Testnet

```
movement:250:0x0000000000000000000000000000000000000000000000000000000000000001
movement:250:0x1
```

## Security Considerations

Movement addresses are hexadecimal strings and may be subject to phishing using visually similar addresses.

Applications SHOULD:

- Validate account existence before processing transactions
- Display full CAIP-10 identifiers when clarity is required
- Expand shortened addresses to their full zero-padded form for comparison

## Test Cases

Valid:

```
movement:126:0x0000000000000000000000000000000000000000000000000000000000000001
movement:126:0x1
movement:126:0xd5fb7899ac1e3b4a51bfbf0dcafaa78453bb8e9a64a93a8e47fedad6b8c48171
movement:250:0x1
```

Invalid:

```
movement:126:0x
movement:126:0xGHIJKL
movement:126:1
movement:126:0x0000000000000000000000000000000000000000000000000000000000000000000001
```

## References

- [REST API][] - Movement REST API for account lookups
- [CAIP-2 Profile][] - Movement chain identification

[CAIP-2 Profile]: ./caip2.md
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[REST API]: https://mainnet.movementnetwork.xyz/v1

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
