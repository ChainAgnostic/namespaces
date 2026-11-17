---
namespace-identifier: xahau-caip10
title: Xahau Namespace - Account ID Specification
author: Ekiserrepé (@Ekiserrepe)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/231
status: Draft
type: Standard
created: 2026-09-28
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Introduction

Xahau accounts are identified by classic addresses.
A classic address is the Base58Check encoding of a 20-byte AccountID using the
Xahau base58 alphabet and account-address type prefix.

## Specification

### Semantics

The `account_id` identifies one Xahau account on one chain:

```text
account_id:      chain_id + ":" + account_address
chain_id:        See the Xahau CAIP-2 profile
account_address: classic_address
```

The same key can derive the same classic address on multiple Xahau chains.
The CAIP-2 portion therefore MUST be retained to distinguish those accounts.

### Syntax

A classic address:

- is case-sensitive;
- begins with `r`;
- contains 25 to 35 characters;
- uses Xahau's base58 alphabet; and
- encodes a 20-byte AccountID with a four-byte checksum.

The following regular expression is a useful preliminary check:

```regex
^r[1-9A-HJ-NP-Za-km-z]{24,34}$
```

A conforming implementation MUST also decode the address with the Xahau base58
alphabet, verify the account-address type prefix and payload length, and verify
the checksum.
The regular expression alone is not sufficient validation.

### Resolution Mechanics

An application can resolve an account against a trusted `xahaud` server using
the `account_info` method.
For example:

```bash
curl --request POST "https://xahau.network" \
  --header "Content-Type: application/json" \
  --data '{
    "method": "account_info",
    "params": [{
      "account": "r9cZA1mLK5R5Am25ArfXFmqgNwjZgnfk59",
      "ledger_index": "validated"
    }]
  }'
```

Resolution verifies whether the account exists in the selected validated
ledger, but account existence is not required for syntactic validity.
An unfunded classic address can become an account when it receives sufficient
XAH.

## Rationale

Classic addresses are the protocol-native representation accepted in Xahau
transaction fields and API methods.
They map deterministically to AccountIDs and include checksum protection.

Destination tags are unsigned 32-bit routing values used by a receiving
account; they do not identify separate ledger accounts and MUST NOT be appended
to canonical CAIP-10 account IDs.
X-addresses can package a classic address, destination tag, and a main/test
network indicator for user-facing payment routing.
Applications MUST decode an X-address to its classic address and use the actual
CAIP-2 chain ID before constructing a Xahau CAIP-10 account ID.

### Backwards Compatibility

There are no known legacy CAIP-10 identifiers in the `xahau` namespace.

## Test Cases

Valid examples:

```text
# Xahau Mainnet account
xahau:21337:r9cZA1mLK5R5Am25ArfXFmqgNwjZgnfk59

# The same classic address scoped to Xahau Testnet
xahau:21338:r9cZA1mLK5R5Am25ArfXFmqgNwjZgnfk59
```

Invalid canonical account IDs:

```text
# A destination tag is routing metadata, not part of the account address
xahau:21337:r9cZA1mLK5R5Am25ArfXFmqgNwjZgnfk59-123

# An X-address must first be decoded to a classic address
xahau:21338:T7QDemmxnuN7a52A62nx2fxGPWcRahLCf3qaswfrsNW9Lps
```

## References

- [CAIP-2 Profile][] - Xahau chain ID specification.
- [CAIP-10][] - Account ID specification.
- [Xahau Data Types][] - Native account address representation.
- [Xahau Base58 Encodings][] - Alphabet, prefixes, payload sizes, and checksums.
- [Xahau Payment][] - Account destinations and destination tags.
- [xahau-py Address Codec][] - Official classic-address and X-address conversion support.
- [xahaud AccountID Source][] - Protocol implementation of AccountID encoding and parsing.

[CAIP-2 Profile]: ./caip2.md
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[Xahau Data Types]: https://xahau.network/docs/protocol-reference/data-types/
[Xahau Base58 Encodings]: https://xahau.network/docs/protocol-reference/data-types/base-58-encodings/
[Xahau Payment]: https://xahau.network/docs/protocol-reference/transactions/transaction-types/payment/
[xahau-py Address Codec]: https://github.com/Xahau/xahau-py
[xahaud AccountID Source]: https://github.com/Xahau/xahaud/blob/dev/src/libxrpl/protocol/AccountID.cpp

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
