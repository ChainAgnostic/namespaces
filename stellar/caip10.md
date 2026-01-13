---
namespace-identifier: stellar-caip10
title: Stellar Namespace - Addresses
author: Pelle Braendgaard (@pelle)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/157
status: Draft
type: Standard
created: 2025-11-6
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

In [CAIP-10][], a string-based general account address scheme is defined.
Stellar supports multiple address formats to accommodate different use cases:

### Classic Addresses (G-addresses)

Classic Stellar addresses are Ed25519 public keys encoded using Stellar's `strkey` format (base32 encoding as defined in [RFC 4648]).
A classic Stellar address has the following characteristics:

* It is exactly 56 characters long
* It starts with the character `G`
* It uses base32 encoding with character set `[A-Z][2-7]`
* It is case-insensitive (though conventionally uppercase)
* It includes a CRC16 checksum for error detection
* It may optionally include a memo appended with a hyphen (`-`) separator

### Muxed Accounts (M-addresses)

Muxed accounts (introduced in Protocol 13, [CAP-0027]) encode both a classic address and a 64-bit unsigned integer ID into a single string.
A muxed account address has the following characteristics:

* It is exactly 69 characters long
* It starts with the character `M`
* It uses base32 encoding (same character set as G-addresses)
* It is case-insensitive (though conventionally uppercase)
* It encodes both the underlying G-address and a 64-bit memo ID
* It includes a checksum for validation
* Muxed accounts are a client-side abstraction; only the underlying G-address
  exists on the ledger

### Federated Addresses

Federated addresses (defined in SEP-0002) provide human-readable addressing in the format `username*domain.com`.
These addresses must be resolved to a G-address or M-address via the federation protocol before use in transactions.
For CAIP-10 purposes, federated addresses should be resolved to their canonical G or M format.

### Syntax

The `account_id` is a case-insensitive string in the form:

```sh
account_id:        chain_id + ":" + account_address
chain_id:          See [CAIP-2][]
account_address:   classic_address | muxed_address
classic_address:   G[A-Z2-7]{55} + optional_memo
optional_memo:     ("-" + memo_value)?
memo_value:        memo_text | memo_id | memo_hash
memo_text:         [^\-]{1,28}
memo_id:           [0-9]{1,20}
memo_hash:         [0-9a-fA-F]{64}
muxed_address:     M[A-Z2-7]{68}
```

### Semantics

The `chain_id` is specified by the [CAIP-2][] which describes the blockchain id
(typically `stellar:pubnet` or `stellar:testnet`).

The `account_address` represents an account on the Stellar network and can be
expressed in multiple formats:

1. **Classic Address (G-address)**: A base32-encoded Ed25519 public key,
   optionally followed by a memo. Memos are used to identify specific recipients
   or purposes at the destination address and come in several types:

   * **MEMO_TEXT**: A string up to 28 bytes, encoded in ASCII or UTF-8
   * **MEMO_ID**: A 64-bit unsigned integer (0 to 18446744073709551615)
   * **MEMO_HASH**: A 32-byte hash (64 hex characters)
   * **MEMO_RETURN**: A 32-byte hash intended as the hash of a transaction being refunded

   When included, the memo is separated from the address by a hyphen (`-`).

2. **Muxed Address (M-address)**: A compact format that encodes both the classic
   G-address and a 64-bit memo ID into a single base32-encoded string starting
   with `M`. Muxed addresses eliminate the need for separate memo handling and
   reduce user error. They are particularly useful for custodial services and
   exchanges that use pooled accounts.

**Important Notes**:

* Memos (especially `MEMO_ID`) are critical for exchange deposits and withdrawals
* Forgetting a memo when sending to an exchange typically results in lost funds
  or delayed crediting
* Muxed addresses provide a safer alternative by embedding the memo ID directly
  in the address
* Only `MEMO_ID` can be encoded in muxed addresses; `MEMO_TEXT` and `MEMO_HASH` require
  classic addresses with appended memos

## Test Cases

This is a list of manually composed examples

```sh
# Pubnet classic address (without memo)
stellar:pubnet:GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ

# Testnet classic address (without memo)
stellar:testnet:GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ

# Classic address with MEMO_ID
stellar:pubnet:GDQP2KPQGKIHYJGXNUIYOMHARUARCA7DJT5FO2FFOOKY3B2WSQHG4W37-123456789

# Classic address with MEMO_TEXT
stellar:pubnet:GDQP2KPQGKIHYJGXNUIYOMHARUARCA7DJT5FO2FFOOKY3B2WSQHG4W37-payment-reference

# Classic address with MEMO_HASH (hex-encoded)
stellar:pubnet:GDQP2KPQGKIHYJGXNUIYOMHARUARCA7DJT5FO2FFOOKY3B2WSQHG4W37-b64aa7c0f6d5f5f6e8f1d1c7f5e5d5c5f5e5d5c5f5e5d5c5f5e5d5c5f5e5d5c5

# Muxed address (Pubnet) with embedded ID 0
stellar:pubnet:MA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAAAAAAAACJUQ

# Muxed address (Pubnet) with embedded ID 420
stellar:pubnet:MA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAAAAAABUTGI4

# Muxed address (Testnet)
stellar:testnet:MCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMAAAAAAAAAAAJLKA
```

## Backwards Compatibility

Classic G-addresses without memos maintain full backward compatibility with
existing Stellar implementations. Muxed M-addresses (Protocol 13+) may not be
supported by older clients and should be verified before use.

## References

* [Stellar Account Addressing][] - Overview of Stellar account addressing
* [SEP-0023: Strkey][SEP-0023] - Specification for strkey encoding used in Stellar addresses
* [CAP-0027: Muxed Accounts][CAP-0027] - Proposal for muxed account support
* [Stellar Memos][] - Detailed explanation of memo types and usage
* [SEP-0002: Federation Protocol][SEP-0002] - Human-readable federated addresses
* [Pooled Accounts Guide][] - Guide to muxed accounts and memos for pooled accounts


[CAIP-2]: ./caip2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[Stellar Account Addressing]: https://developers.stellar.org/docs/learn/fundamentals/stellar-data-structures/accounts
[SEP-0023]: https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md
[CAP-0027]: https://stellar.org/protocol/cap-27
[RFC 4648]: https://datatracker.ietf.org/doc/html/rfc4648
[Stellar Memos]: https://developers.stellar.org/docs/learn/encyclopedia/transactions-specialized/memos
[SEP-0002]: https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0002.md
[Pooled Accounts Guide]: https://developers.stellar.org/docs/learn/encyclopedia/transactions-specialized/pooled-accounts-muxed-accounts-memos

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
