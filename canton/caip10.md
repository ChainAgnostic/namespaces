---
namespace-identifier: canton-caip10
title: Canton Namespace - Addresses
author: Marc Juchli (@mjuchli-da) <marc.juchli@digitalasset.com>
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/201
status: Draft
type: Standard
created: 2026-08-21
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

For context, see the [CAIP-10](https://chainagnostic.org/CAIPs/caip-10) specification.

## Syntax

CAIP‑10 defines `account_id` as `{chain_id}:{account_address}`
- `chain_id` the [CAIP2 Canton ID](./caip2.md)
- `account_address` the user or entity address on that chain (`[-.%a-zA-Z0-9]{1,128}`).

The `account_address` is derived from the canonical textual representation of a Canton Party ID.  A given Party ID (e.g. `account_address`) is shared across multiple synchronizers (e.g. `chain_id`).

A Canton Party ID has the following canonical form:
```
{partyHint}::{partyNamespace}
```

As the `:` character is not permitted in the CAIP-10 account_address, the canonical Party ID is percent-encoded before being embedded in the CAIP-10 identifier. The resulting format is:
```
canton:{networkIdentifier}:{partyHint}%3A%3A{partyNamespace}
```

Examples:
```
canton:mainnet-global:alice%3A%3A1220...
canton:testnet-global:bob%3A%3A1220...
```

The percent-encoded value preserves the canonical Party ID and can be decoded by implementations using standard percent-decoding. This approach ensures compliance with the CAIP-10 grammar while preserving Canton's existing Party ID semantics and avoiding the introduction of a new account address format.

**Note:** the same PartyId (e.g. account_address) is shared across multiple synchronizers (e.g. chain_id).

## Limitations

The `account_address` length **MUST** be <= 128 characters. The party namespace takes 68 characters, the url encoded colons 6 characters, the `canton:` prefix 7 characters, and thus leaving 49 characters for the `{networkIdentifier}:{partyHint}`.

In the case of `networkIdentifier` being `mainnet-global` (14 characters), and 1 colon separator, the party hint must be <= 32 characters.

## References

- [Canton Core Concepts](https://docs.canton.network/overview/understand/core-concepts#party-identifier-format): Party identifier format

## Rights

Copyright and related rights waived via CC0.
