---
namespace-identifier: radix-caip10
title: Radix DLT Namespace - Accounts
author: ["Avaunt (@AVaunt-consulting)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/198
status: Draft
type: Standard
created: 2026-08-01
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Introduction

Radix accounts are on-ledger components with a native address, not raw public
keys. Most accounts begin as **virtual accounts**: an address is derived
offline from an Ed25519 or Secp256k1 public key and can receive deposits
before anything exists on-ledger; the account component is instantiated on
first interaction. Account ownership is mutable — an account that started as
a key-derived virtual account may later be controlled by different keys or by
multi-factor access rules ("smart accounts") — so the address, not any public
key, is the stable identifier.

## Specification

### Semantics

An account address is a bech32m string ([BIP-350][]) composed of:

- **HRP**: the entity specifier `account_` concatenated with the network
  specifier of the target network (`rdx` for mainnet, `tdx_2_` for Stokenet);
- the bech32m separator `1`;
- **data**: 48 base32 characters encoding 30 bytes — 1 entity-type byte
  (e.g. `0x51` for a virtual Ed25519 account, `0xd1` for a virtual Secp256k1
  account, or the type byte of a ledger-allocated account) followed by 29
  address bytes (for virtual accounts, the last 29 bytes of the Blake2b-256
  hash of the controlling public key);
- a 6-character checksum computed over the HRP and data.

Because the checksum covers the HRP, an account address is only valid on the
network named in its HRP, and that network MUST match the [CAIP-2][] segment
of the CAIP-10 identifier (`radix:mainnet` addresses carry `account_rdx`;
`radix:stokenet` addresses carry `account_tdx_2_`).

### Syntax

The `account_id` is formed of the CAIP-2 identifier followed by the native
account address verbatim:

```
account_id:        chain_id + ":" + account_address
chain_id:          radix:[a-z0-9]{1,32} (see the [CAIP-2 Profile][])
account_address:   account_ + hrp_suffix + "1" + [02-9ac-hj-np-z]{54}
hrp_suffix:        rdx | tdx_2_ | (other registered network specifiers)
```

Per-network validation regular expressions:

```
# Mainnet
radix:mainnet:account_rdx1[02-9ac-hj-np-z]{54}

# Stokenet
radix:stokenet:account_tdx_2_1[02-9ac-hj-np-z]{54}
```

The 54 characters after the separator are 48 data characters plus the
6-character checksum, drawn from the bech32 charset (which excludes `1`,
`b`, `i`, `o`).

#### Canonicalization

Addresses MUST be written in lowercase. Bech32m is case-insensitive at decode
time and forbids mixed case entirely; the canonical, and only conformant,
CAIP-10 form for this namespace is the lowercase encoding, so consumers can
compare identifiers by exact string equality.

### Resolution Mechanics

An address can be validated offline (bech32m checksum + HRP inspection),
e.g. with the [Radix Engine Toolkit][], which also derives virtual account
addresses from public keys. On-ledger state, if any, can be queried via the
Gateway API:

```
POST /state/entity/details
{ "addresses": ["account_rdx129a9wuey40lducsne6r8e5q7xmt07068gcede0x0nrwtsnehss5d52"] }
```

A valid virtual-account address that has not yet been instantiated will
report no on-ledger state; it is still a correct CAIP-10 identifier and can
receive deposits.

## Rationale

The native bech32m address is used verbatim (rather than re-encoded) because
it is self-describing (entity and network specifiers), checksummed, and the
only account identifier Radix users, wallets, and APIs exchange. Public keys
are unsuitable identifiers because account ownership is mutable.

### Backwards Compatibility

Olympia-era account addresses (bech32, ending before September 2023) are a
retired format and are not valid in this namespace. The [Radix Engine
Toolkit][] can map an Olympia Secp256k1 account address to its Babylon
equivalent where historical continuity is needed.

## Test Cases

This is a list of manually composed and checksum-validated examples:

```
# Mainnet virtual Ed25519 account
radix:mainnet:account_rdx129a9wuey40lducsne6r8e5q7xmt07068gcede0x0nrwtsnehss5d52

# Stokenet virtual Ed25519 account (same underlying key-hash bytes, different
# network — note the different HRP and checksum)
radix:stokenet:account_tdx_2_129a9wuey40lducsne6r8e5q7xmt07068gcede0x0nrwtsnehrlel8s
```

## Additional Considerations

Radix addresses contain underscore (`_`) characters in their HRP. The
[CAIP-10][] account-address charset (`[-.%a-zA-Z0-9]{1,128}`) predates this
namespace and does not include `_`; this profile nevertheless uses the native
format verbatim for fidelity and usability, following the precedent of other
namespaces whose native identifiers include underscores (e.g. the `stacks`
CAIP-19 profile). Consumers requiring strict CAIP-10 charset conformance MAY
percent-encode underscores as `%5F` per [RFC 3986][]; implementations in this
namespace SHOULD accept both and emit the unencoded form.

## References

- [Radix Accounts][] - account model, virtual accounts, and deposit rules.
- [Address Concepts][] - bech32m address structure: entity specifier, network specifier, 30-byte payload.
- [Radix Engine Toolkit][] - offline address derivation and validation.
- [Gateway API][] - `/state/entity/details` endpoint documentation.

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-2 Profile]: ./caip2.md
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[BIP-350]: https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki
[RFC 3986]: https://www.rfc-editor.org/rfc/rfc3986#section-2.1
[Radix Accounts]: https://docs.radixdlt.com/docs/account
[Address Concepts]: https://docs.radixdlt.com/docs/concepts
[Radix Engine Toolkit]: https://github.com/radixdlt/radix-engine-toolkit
[Gateway API]: https://radix-babylon-gateway-api.redoc.ly/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
