---
namespace-identifier: xahau-caip19
title: Xahau Namespace - Asset ID Specification
author: Ekiserrepé (@Ekiserrepe)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/231
status: Draft
type: Standard
created: 2026-09-28
requires: ["CAIP-2", "CAIP-10", "CAIP-19", "CAIP-20"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Introduction

Xahau supports three asset-identification models:

1. native XAH;
2. fungible tokens identified by a currency code and issuer account; and
3. URI Tokens identified by a protocol-derived 256-bit object ID.

This profile defines canonical CAIP-19 asset types for each model.

## Specification

### Syntax

```text
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           See the Xahau CAIP-2 profile
asset_namespace:    "slip44" | "token" | "uritoken"
asset_reference:    slip44_ref | token_ref | uritoken_ref

slip44_ref:         "21337"
token_ref:          currency_ref + "." + issuer_address
currency_ref:       standard_code | nonstandard_code
standard_code:      Three-character Xahau currency code, RFC 3986 percent-encoded
nonstandard_code:   [0-9A-F]{40}
issuer_address:     Valid Xahau classic address
uritoken_ref:       [0-9A-F]{64}
```

Alphabetic hexadecimal digits MUST be uppercase.
Percent-encoded bytes MUST use uppercase hexadecimal digits.

### Native XAH (`slip44`)

Native XAH uses SLIP-44 coin type `21337` as defined by [CAIP-20][].
It has no issuer.

```text
xahau:21337/slip44:21337
```

The SLIP-44 reference identifies native XAH on any Xahau chain when combined
with that chain's CAIP-2 identifier.

### Issued Fungible Tokens (`token`)

An issued fungible token is uniquely identified by both its currency code and
issuer classic address.
Balances are tracked in trust lines.

Xahau supports two currency-code formats:

- a case-sensitive, three-character ASCII code; or
- a nonstandard 160-bit value rendered as 40 uppercase hexadecimal characters.

The uppercase code `XAH` is reserved and MUST NOT be used for an issued token.

A nonstandard code MUST NOT begin with the byte `00`, because that prefix
identifies the protocol's internal encoding of a three-character code.
Such a currency MUST be represented by its three-character `standard_code`.

CAIP-19 does not permit most punctuation accepted by Xahau currency codes
directly in an asset reference.
Each byte outside the unreserved alphanumeric subset MUST therefore be encoded
as `%HH` according to RFC 3986.
For example, the protocol currency code `A?B` is represented as `A%3FB`.

The currency reference and issuer are joined with a period:

```text
{currency_ref}.{issuer_address}
```

### URI Tokens (`uritoken`)

URI Tokens are Xahau's native non-fungible tokens.
Each URI Token is identified by a 32-byte object ID rendered as 64 uppercase
hexadecimal characters.

The protocol derives this ID using SHA-512Half over the URI Token ledger-space
key, issuer AccountID, and URI.
Consequently, an issuer can create no more than one URI Token for the same URI.

## Resolution Mechanics

Native XAH requires no object lookup.

Issued tokens can be resolved through ledger methods that return trust lines,
such as `account_lines`, using the issuer and currency code from the asset
reference.

A URI Token can be resolved with `ledger_entry` using its object ID:

```bash
curl --request POST "https://xahau.network" \
  --header "Content-Type: application/json" \
  --data '{
    "method": "ledger_entry",
    "params": [{
      "index": "540CFA50B8F713F5CDF361E3D74490E14592E6E95E520926A2E4B2F667CBC1BE",
      "ledger_index": "validated"
    }]
  }'
```

Resolution MUST be performed against a server whose network ID matches the
CAIP-2 chain ID.

## Rationale

The native and issued-token forms mirror Xahau's protocol-native asset
representations.
The URI Token object ID is stable across ownership transfers, so it identifies
the asset without embedding the current owner or sale state.

### Backwards Compatibility

There are no known legacy CAIP-19 identifiers in the `xahau` namespace.

## Test Cases

```text
# Native XAH on Mainnet
xahau:21337/slip44:21337

# Native XAH on Testnet
xahau:21338/slip44:21337

# Three-character issued token
xahau:21337/token:USD.r9cZA1mLK5R5Am25ArfXFmqgNwjZgnfk59

# Issued token whose protocol currency code contains punctuation
xahau:21337/token:A%3FB.r9cZA1mLK5R5Am25ArfXFmqgNwjZgnfk59

# Issued token with a nonstandard 160-bit currency code ("MAGIC")
xahau:21337/token:4D41474943000000000000000000000000000000.r9cZA1mLK5R5Am25ArfXFmqgNwjZgnfk59

# EVR, the Evernode token issued on Xahau Mainnet
xahau:21337/token:EVR.rEvernodee8dJLaFsujS6q1EiXvZYmHXr8

# URI Token
xahau:21337/uritoken:540CFA50B8F713F5CDF361E3D74490E14592E6E95E520926A2E4B2F667CBC1BE
```

The following asset types are invalid:

```text
# The native asset is not an issued token
xahau:21337/token:XAH.r9cZA1mLK5R5Am25ArfXFmqgNwjZgnfk59

# Nonstandard codes must not use the reserved 0x00 prefix
xahau:21337/token:0000000000000000000000005553440000000000.r9cZA1mLK5R5Am25ArfXFmqgNwjZgnfk59

# Hexadecimal references must be uppercase
xahau:21337/uritoken:540cfa50b8f713f5cdf361e3d74490e14592e6e95e520926a2e4b2f667cbc1be
```

The URI Token test vector is derived from issuer
`rfkE1aSy9G8Upk4JssnwBxhEv5p4mn2KTy` and URI bytes `DEADBEEF`:

```text
SHA-512Half(0x0055 || issuer AccountID || 0xDEADBEEF)
= 540CFA50B8F713F5CDF361E3D74490E14592E6E95E520926A2E4B2F667CBC1BE
```

## References

- [CAIP-2 Profile][] - Xahau chain ID specification.
- [CAIP-10 Profile][] - Xahau account ID specification.
- [CAIP-19][] - Asset Type and Asset ID specification.
- [CAIP-20][] - SLIP-44 asset namespace specification.
- [SLIP-44][] - Registry assigning coin type 21337 to XAH.
- [Xahau Currency Formats][] - Native XAH and issued-token formats.
- [Xahau URI Tokens][] - URI Token behavior and transaction types.
- [Xahau URI Token Object][] - URI Token fields and object ID derivation.
- [xahaud URI Token Index Source][] - Protocol implementation of URI Token ID derivation.

[CAIP-2 Profile]: ./caip2.md
[CAIP-10 Profile]: ./caip10.md
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[CAIP-20]: https://chainagnostic.org/CAIPs/caip-20
[SLIP-44]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[Xahau Currency Formats]: https://xahau.network/docs/protocol-reference/data-types/currency-formats/
[Xahau URI Tokens]: https://xahau.network/docs/features/network-features/uritoken/
[Xahau URI Token Object]: https://xahau.network/docs/protocol-reference/ledger-data/ledger-objects-types/uritoken/
[xahaud URI Token Index Source]: https://github.com/Xahau/xahaud/blob/dev/src/libxrpl/protocol/Indexes.cpp#L489-L496

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
