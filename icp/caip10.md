---
namespace-identifier: icp-caip10
title: Account ID Specification for the Internet Computer Namespace
author: Jeff Jafari (@asjn3e)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/238
status: Draft
type: Standard
created: 2026-10-11
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Introduction

An account in this namespace is a principal.
Principals identify both users and canisters (smart contracts).
A user signs requests with a key, and a canister sends calls from its own principal.
Both kinds can hold tokens, and from the principal alone a client cannot always tell which kind it is.

ICRC-1 token ledgers add subaccounts on top of principals.
This profile covers principals only; see the [Rationale section](#rationale).

## Specification

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [BCP 14][] ([RFC 2119][], [RFC 8174][]) when, and only when, they appear in all capitals, as shown here.

### Semantics

A principal is a byte string of 0 to 29 bytes.
The [IC Interface Specification][Principals] defines several classes:

- Opaque IDs: the network generates these for canisters. They typically end with the byte `0x01`.
- Self-authenticating IDs: `SHA-224(public_key) · 0x02`, 29 bytes. A user who holds the matching private key signs requests as this principal.
- Derived IDs: 29 bytes ending with `0x03`.
- The anonymous ID: the single byte `0x04`.
- Reserved IDs: a blob of 0 to 28 bytes followed by `0x7f`. Because no principal is longer than 29 bytes, every principal whose last byte is `0x7f` is reserved. Reserved IDs address neither a canister nor a user.

The empty principal is the ID of the management canister, a system interface.

On every [ICRC-1][] ledger, a principal owns a default account: the account with no subaccount.
The [ICRC-1 Textual Encoding][] of a default account is the principal's own textual form.
A CAIP-10 ID in this namespace therefore also names the principal's default account on every ICRC-1 ledger of that network.

### Syntax

```
account_id:        chain_id + ":" + account_address
chain_id:          "icp:" + [0-9a-f]{32}   (see the CAIP-2 profile)
account_address:   ([a-z2-7]{5}-){1,10}[a-z2-7]{1,5}
```

The `account_address` is the canonical textual form of the principal, as the [IC Interface Specification][Textual IDs] defines it:

1. Compute the CRC-32 checksum of the principal bytes, big-endian.
2. Put the 4 checksum bytes in front of the principal bytes.
3. Encode the result in Base32 ([RFC 4648][]), lowercase, with no padding.
4. Insert a dash after every 5 characters, except at the end.

The result is 8 to 63 characters long.
CAIP-10 is case-sensitive, and the address MUST be lowercase.

The regular expression is necessary but not sufficient.
It checks only the shape of the address, and it accepts some lengths that no principal produces.
Implementations MUST validate an address with all three of these steps:

1. Decode it with a principal library. This checks the CRC-32 checksum.
2. Encode the decoded principal again.
3. Compare the result with the input. If they differ, the address is not canonical and MUST be rejected.

Step 3 rejects uppercase input and input without dashes.
The IC Interface Specification allows parsers to accept uppercase input, so decoding alone does not prove that an address is canonical.
Suitable libraries include `Principal.fromText` in `@dfinity/principal` and `Principal::from_text` in the `ic-principal` crate.

### Resolution Mechanics

A principal needs no network lookup.
The textual form carries its own checksum, and the same principal is valid on every ICP network.
The CAIP-2 part of the account ID says which network is meant.

## Rationale

A principal is the identity that sends every request to the network.
It plays the role of an address on EVM chains.
CAIP-10 consumers such as [CAIP-25][] sessions need the account that signs, and on ICP that account is a principal.

The profile does not include ICRC-1 accounts with subaccounts, for three reasons:

- Subaccounts are not a protocol concept.
  The [ICRC-1][] ledger standard defines them, and each ledger keeps its own balances under them.
  A subaccount never signs anything.
- The [ICRC-1 Textual Encoding][] of an account does not always fit.
  A 29-byte principal with a 32-byte subaccount encodes to 136 characters, and CAIP-10 allows 128.
  Self-authenticating principals, which most users have, are 29 bytes long.
- The ICP drafts that solve the length problem are not accepted.
  The [ICRC-22][ICRC-22 draft] draft defines a shorter form that removes the dashes from the principal.
  The NNS has not accepted it, and `@dfinity/principal` 3.4.3 rejects the dash-less principal it produces.

The profile also does not include account identifiers of the ICP ledger.
An account identifier is 64 hexadecimal characters: a CRC-32 checksum followed by a SHA-224 hash of a principal and a subaccount.
The hash cannot be reversed to get the principal, and other ledgers do not use account identifiers.

### Backwards Compatibility

The 2023 working group draft in [icvc/icp-namespace][] used the same form: the textual principal after an `icp` chain ID.
This profile adds the lowercase rule and the canonical check.

## Test Cases

```bash
# Canister: the ICP ledger (10-byte opaque ID)
icp:737ba355e855bd4b61279056603e0550:ryjl3-tyaaa-aaaaa-aaaba-cai

# User: a self-authenticating principal (29 bytes), from the ICRC-1 Textual Encoding examples
icp:737ba355e855bd4b61279056603e0550:k2t6j-2nvnp-4zjm3-25dtz-6xhaa-c7boj-5gayf-oj3xs-i43lp-teztq-6ae
```

The following strings are valid account IDs, but they name system or reserved principals, not ordinary accounts.
Wallets SHOULD NOT accept them as destinations for funds; see the [Security](#security) section.

```bash
# Shortest valid address: the empty principal, which is the management canister
icp:737ba355e855bd4b61279056603e0550:aaaaa-aa

# The anonymous principal
icp:737ba355e855bd4b61279056603e0550:2vxsx-fae

# A reserved ID: the single byte 0x7f
icp:737ba355e855bd4b61279056603e0550:ck4ig-id7
```

The following strings are not valid account IDs:

```bash
# Uppercase
icp:737ba355e855bd4b61279056603e0550:RYJL3-TYAAA-AAAAA-AAABA-CAI

# Dashes removed
icp:737ba355e855bd4b61279056603e0550:ryjl3tyaaaaaaaaaaaabacai

# ICRC-1 account with a subaccount
icp:737ba355e855bd4b61279056603e0550:k2t6j-2nvnp-4zjm3-25dtz-6xhaa-c7boj-5gayf-oj3xs-i43lp-teztq-6ae-6cc627i.1

# ICP ledger account identifier of the default account of k2t6j-...-6ae
icp:737ba355e855bd4b61279056603e0550:051b05839339f89053454a4b9865ea0452a4bffe2b1cd41f4982bad10c1e637c
```

## Additional Considerations

### Security

Any client can send calls as the anonymous principal, `2vxsx-fae`, without a signature.
Wallets SHOULD NOT offer it as a destination for funds.

The management canister, `aaaaa-aa`, is a system interface, not an account that anyone controls.
Wallets SHOULD NOT offer it as a destination for funds either.

Reserved IDs carry the highest risk of lost funds.
A reserved ID matches the regular expression, passes the CRC-32 check, and survives the canonical check, so it is a valid account address.
It addresses neither a canister nor a user, so no one can move funds sent to it.
Wallets SHOULD reject reserved IDs, whose last byte is `0x7f`, as transfer destinations.

### Subaccounts

Many applications use ICRC-1 subaccounts, for example exchanges that give each customer a deposit subaccount.
A later revision of this profile, or a separate profile, can add them once ICP standards settle a textual form that fits in 128 characters.
The [ICRC-22][ICRC-22 draft] draft is the current work on that question.

## References

- [CAIP-10][]: the Account ID Specification.
- [BCP 14][]: the meaning of the requirement key words, defined by [RFC 2119][] and [RFC 8174][].
- [CAIP-2 profile][]: how this namespace forms the chain ID.
- [Principals][]: the principal classes in the IC Interface Specification.
- [Textual IDs][]: the textual form of principals in the IC Interface Specification.
- [ICRC-1][]: the fungible token standard, which defines accounts and subaccounts.
- [ICRC-1 Textual Encoding][]: the textual form of ICRC-1 accounts, and the source of the example principal.
- [icvc/icp-namespace][]: the 2023 working group draft of a CAIP-10 profile for ICP, by Quint Daenen.
- [ICRC-22 draft][]: payment request URIs, with a draft short form for ICRC-1 accounts.

[CAIP-2 profile]: ./caip2.md
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[CAIP-25]: https://chainagnostic.org/CAIPs/caip-25
[BCP 14]: https://www.rfc-editor.org/info/bcp14
[RFC 2119]: https://www.rfc-editor.org/rfc/rfc2119
[RFC 8174]: https://www.rfc-editor.org/rfc/rfc8174
[Principals]: https://docs.internetcomputer.org/references/ic-interface-spec/#id-classes
[Textual IDs]: https://docs.internetcomputer.org/references/ic-interface-spec/#textual-ids
[RFC 4648]: https://datatracker.ietf.org/doc/html/rfc4648#section-6
[ICRC-1]: https://github.com/dfinity/ICRC-1/blob/main/standards/ICRC-1/README.md
[ICRC-1 Textual Encoding]: https://github.com/dfinity/ICRC-1/blob/main/standards/ICRC-1/TextualEncoding.md
[icvc/icp-namespace]: https://github.com/icvc/icp-namespace/pull/2
[ICRC-22 draft]: https://github.com/dfinity/ICRC/pull/101

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
