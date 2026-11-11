---
namespace-identifier: near-caip10
title: NEAR Protocol Namespace - Account ID Specification
author: ["Iker Alustiza (@IkerAlus)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/issues/106
status: Draft
type: Standard
created: 2026-11-11
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Introduction

A NEAR account is identified by an account ID, a string such as `alice.near`, rather than by an address derived from a key.
An account holds a balance, access keys and storage, and it may also hold a contract: contracts live at accounts, so there is no separate contract address.
Besides registered names, the protocol defines four kinds of account ID that can be computed offline and used before the account exists on-chain.
All five kinds share one string grammar, so this profile forms every NEAR CAIP-10 identifier the same way: a chain ID from the [NEAR CAIP-2 profile][CAIP-2 Profile], a colon, and the account ID.
The one transformation is that `_`, which NEAR allows and [CAIP-10][] does not, is percent-encoded as `%5F`.

## Specification

### Semantics

A NEAR account ID is a string of 2 to 64 characters made of lowercase alphanumeric parts separated by `.`, with `-` or `_` allowed between alphanumerics inside a part.
No account ID starts or ends with a separator or contains two separators in a row, and uppercase letters are never valid.
The normative rules are in [Nomicon: Accounts][], and [near-account-id][] is the reference validator.

The protocol distinguishes five kinds of account ID by their shape:

| Kind | Shape | Derived from | Example |
| --- | --- | --- | --- |
| Named | Any valid account ID that has none of the shapes below | Registered under its parent account, e.g. `alice.near` under `near` | `wrap.near` |
| NEAR-implicit | 64 lowercase hex characters | An ED25519 public key | `17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1` |
| ETH-implicit | `0x` and 40 lowercase hex characters | An Ethereum address ([NEP-518][]) | `0x1234567890abcdef1234567890abcdef12345678` |
| Deterministic | `0s` and 40 lowercase hex characters | A hash of the contract's initial state ([NEP-616][]) | `0s0123456789abcdef0123456789abcdef01234567` |
| Universal | `0u` and 52 lowercase Crockford base32 characters | A SHA3-256 hash of the account's initial state ([NEP-655][]) | `0u000g40r40m30e209185gr38e1w8124gk2gahc5rr34d1p70x3rfg` |

The kind matters to wallets and indexers, not to this profile: every kind is an account ID under the same grammar and maps to CAIP-10 the same way.

### Syntax

```text
account_id:      chain_id + ":" + account_address
chain_id:        a NEAR CAIP-2 chain ID, e.g. near:mainnet
account_address: the NEAR account ID with every "_" replaced by "%5F"
```

To form an identifier, replace each `_` in the account ID with `%5F` and leave every other character unchanged.
This is a targeted substitution, not general URL encoding: `_` is an unreserved character in [RFC 3986][], so generic URL encoders leave it alone.
`%5F` is the only escape sequence, and it is always written in uppercase, the canonical capitalisation [CAIP-10][] recommends.
Every other character a NEAR account ID can contain is already in CAIP-10's `account_address` set, so each account has exactly one identifier per network: two identifiers name the same account exactly when they are equal strings.
A 64-character account ID contains at most 31 underscores, so an `account_address` is at most 126 characters, within CAIP-10's 128-character limit.

An `account_address` is valid when it matches the regular expression below and, after `%5F` is replaced by `_`, is between 2 and 64 characters long:

```regex
^(([a-z0-9]+(-|%5F))*[a-z0-9]+\.)*([a-z0-9]+(-|%5F))*[a-z0-9]+$
```

This is the NEAR account ID grammar with `_` written as `%5F`.
It rejects a raw `_`, a lowercase `%5f`, any other escape, and uppercase letters.

To read an identifier, split it at its two colons, check the chain ID against the [CAIP-2 profile][CAIP-2 Profile], validate the `account_address` as above, and replace `%5F` with `_` to recover the NEAR account ID.

### Resolution Mechanics

A well-formed identifier does not imply that the account exists.
Implicit, deterministic and universal accounts can be used before they exist on-chain, and a named account can be deleted.
To check whether an account exists, decode the account ID and call the [`view_account`][] query on an RPC endpoint of the network named by the chain ID:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "query",
  "params": {
    "request_type": "view_account",
    "finality": "final",
    "account_id": "wrap.near"
  }
}
```

An existing account returns its state; the following is an abbreviated mainnet response for `wrap.near`, retrieved 2026-11-11:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "amount": "36726877840853981498186491028448",
    "locked": "0",
    "code_hash": "DL2f5xmZ44cQRP6vBMt94rvseH5d5KKnAGis2WkTAsh1",
    "storage_usage": 168836479,
    "block_height": 224042396
  }
}
```

A missing account returns an error whose `cause.name` is `UNKNOWN_ACCOUNT`.
Confirm the endpoint's network first, by resolving its chain ID as described in the CAIP-2 profile.

## Rationale

### Why the account ID itself

NEAR has one account ID type for every kind of account, and it is the identifier wallets, RPC methods and explorers already use.
Using it unchanged apart from `_` keeps identifiers readable and lets them round-trip without a lookup.
A key-derived form is not an option, because a NEAR account is not tied to a key: a named account can hold many access keys and change them over time.

### Why `%5F`

`_` is valid in NEAR account IDs and in live use: `v3.oin_finance.near` is a NEP-141 token contract on mainnet.
[CAIP-10][] excludes `_` from `account_address` and recommends percent-encoding for characters outside its set.
Percent-encoding is lossless and reversible.
Replacing `_` with an allowed character instead would merge distinct accounts: `a_b.near` and `a-b.near` are different accounts.
Because `_` is the only character that needs escaping and its escape is fixed as `%5F`, string equality is account equality.
No case normalisation is needed either: NEAR account IDs are lowercase by rule, unlike [EIP-55][] addresses, whose mixed case is a checksum.

### Relationship to `eip155`

ETH-implicit accounts are controlled by an Ethereum key through the [NEP-518][] wallet contract, and Web3 wallets reach them through EIP-155 chain IDs 397 (mainnet) and 398 (testnet).
The account `0x…` on `near:mainnet` is therefore the same account as `eip155:397:0x…`, seen from two namespaces.
The NEAR form is always lowercase, so an EIP-55 checksummed address must be lowercased before it is used as a NEAR account ID.

### Backwards Compatibility

There is no earlier NEAR CAIP-10 profile, but `near:<network>:<account_id>` identifiers are already in use, for example in WalletConnect sessions read by NEAR's [wallet-selector][].
For account IDs without `_`, those identifiers are already in this profile's canonical form.

Producers that write a raw `_` emit strings outside CAIP-10's grammar.
Producers MUST emit `%5F`.
Consumers MAY accept a raw `_` or a lowercase `%5f` from such producers, and MUST convert it to `%5F` before comparing or re-emitting the identifier.
Code that extracts the account ID from an identifier, as wallet-selector does with `split(":")[2]`, MUST also replace `%5F` with `_` before using it as a NEAR account ID.

## Test Cases

### Valid identifiers

| Identifier | Account ID | Notes |
| --- | --- | --- |
| `near:mainnet:wrap.near` | `wrap.near` | Named account, the wrapped NEAR contract |
| `near:mainnet:near` | `near` | Top-level named account |
| `near:mainnet:usdt.tether-token.near` | `usdt.tether-token.near` | `-` needs no escape |
| `near:testnet:wrap.testnet` | `wrap.testnet` | Named account on testnet |
| `near:mainnet:v3.oin%5Ffinance.near` | `v3.oin_finance.near` | `_` encoded as `%5F` |
| `near:mainnet:17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1` | Same as the address | NEAR-implicit shape; this account holds the native USDC contract |
| `near:mainnet:0x1234567890abcdef1234567890abcdef12345678` | Same as the address | ETH-implicit |
| `near:mainnet:0s0123456789abcdef0123456789abcdef01234567` | Same as the address | Deterministic |
| `near:mainnet:0u000g40r40m30e209185gr38e1w8124gk2gahc5rr34d1p70x3rfg` | Same as the address | Universal |
| `near:mainnet:aa` | `aa` | Shortest valid account ID |

The longest possible `account_address` is 126 characters: a 64-character account ID, `aa_a_a…_a`, with 31 underscores.

```text
near:mainnet:aa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa%5Fa
```

### Invalid identifiers

| Identifier | Reason |
| --- | --- |
| `near:mainnet:` | Empty account address |
| `near:mainnet:v3.oin_finance.near` | Raw `_` is outside CAIP-10's grammar; see [Backwards Compatibility](#backwards-compatibility) |
| `near:mainnet:v3.oin%5ffinance.near` | Lowercase escape; the canonical form is `%5F` |
| `near:mainnet:wrap%2Enear` | `%5F` is the only escape; `.` needs none |
| `near:mainnet:Wrap.near` | Uppercase letters are never valid in NEAR account IDs |
| `near:mainnet:0x1234567890ABCDEF1234567890abcdef12345678` | Uppercase hex; ETH-implicit IDs are lowercase |
| `near:mainnet:a` | Shorter than 2 characters |
| `near:mainnet:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | Longer than 64 characters |
| `near:mainnet:alice..near` | Two separators in a row |
| `near:mainnet:.alice.near` | Starts with a separator |
| `near:mainnet:alice.near.` | Ends with a separator |
| `near:mainnet:alice%5F.near` | Decodes to `alice_.near`, which has two separators in a row |

## Security Considerations

A NEAR CAIP-10 identifier names an account, not a key.
A named account can hold several access keys and change them at any time, and a NEAR-implicit account can add keys beyond the one its ID is derived from.
Systems that bind an identity to an identifier, for example through `did:pkh`, should check control against the account's current access keys rather than infer a key from the identifier.

A named account can be deleted and its ID created again, possibly by someone else, so an identifier can come to name a different owner.
Named accounts are human-readable and open to look-alikes such as `alice.near` and `alice-near.near`; applications should display the full identifier.
The account hierarchy governs creation only: `alice.near` decides who creates `app.alice.near`, but has no control over it afterwards.

A raw `_` and `%5F` spell the same account.
Implementations that accept the legacy form must normalise it before comparing identifiers, or they may treat one account as two.

## Additional Considerations

The kind of an account can be read from the shape of its ID, as in the table above, but nothing in this profile depends on it.
New account derivations added by future protocol versions, as [NEP-655][] added universal accounts at protocol version 88, produce valid account IDs and need no change to this profile.

## References

- [CAIP-2 Profile][] - NEAR chain IDs, the first part of every identifier
- [CAIP-10][] - Account ID specification
- [RFC 3986][] - Percent-encoding, Section 2.1
- [Nomicon: Accounts][] - Normative NEAR account ID rules
- [near-account-id][] - Reference account ID validator, including the predicates for each kind
- [NEP-518][] - ETH-implicit accounts and EIP-155 chain IDs 397 and 398
- [NEP-616][] - Deterministic account IDs (`0s`)
- [NEP-655][] - Universal account IDs (`0u`), stabilised at protocol version 88
- [`view_account`][] - RPC query for an account's state
- [EIP-55][] - Mixed-case checksum encoding of Ethereum addresses
- [wallet-selector][] - NEAR wallet library that reads `near` CAIP-10 accounts from WalletConnect sessions

[CAIP-2 Profile]: ./caip2.md
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[RFC 3986]: https://www.rfc-editor.org/rfc/rfc3986#section-2.1
[Nomicon: Accounts]: https://nomicon.io/DataStructures/Account
[near-account-id]: https://github.com/near/near-account-id-rs
[NEP-518]: https://github.com/near/NEPs/blob/master/neps/nep-0518.md
[NEP-616]: https://github.com/near/NEPs/blob/master/neps/nep-0616.md
[NEP-655]: https://github.com/near/NEPs/blob/master/neps/nep-0655.md
[`view_account`]: https://docs.near.org/api/rpc/contracts#view-account
[EIP-55]: https://eips.ethereum.org/EIPS/eip-55
[wallet-selector]: https://github.com/near/wallet-selector

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
