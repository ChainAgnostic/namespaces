---
namespace-identifier: casper-caip350
title: Casper Namespace - Interoperable Address
binary-key: 0004
author: Michael Steuer (@mssteuer)
discussions-to: https://ethereum-magicians.org/t/erc-7930-interoperable-addresses/23365
status: Draft
type: Standard
created: 2026-09-25
requires: ["CAIP-2", "CAIP-10", "CAIP-350"]
---

## Namespace Reference

ChainType binary key: `0x0004`

[CAIP-104] namespace: `casper`

## Chain reference

See this namespace's [CAIP-2](caip2.md) profile. Casper networks are identified by their chainspec name (e.g. `casper` for mainnet, `casper-test` for testnet), as returned in the `chainspec_name` field of the `info_get_status` RPC method.

### Text representation

```
<chainspec_name>
```

Where `<chainspec_name>` is the case-sensitive chainspec name of the network.

> **Note:** Per [CAIP-350], the full chain identifier is `casper:<chainspec_name>` (e.g., `casper:casper`, `casper:casper-test`).

A ChainType without a reference (an [ERC-7930] _Interoperable Address_ with a zero-length _ChainReference_) is represented in text as the bare namespace, `casper`, and denotes "any Casper network".

#### Text -> customary (CAIP-2) conversion

The text representation is identical to the chain reference of the [CAIP-2](caip2.md) chain identifier; no conversion is needed.

#### Customary (CAIP-2) -> text conversion

The chain reference of the [CAIP-2](caip2.md) chain identifier is identical to the text representation; no conversion is needed.

### Binary representation

The chain reference is the ASCII (equivalently UTF-8) encoding of the chainspec name, with no terminator and no padding. Length is variable (6 bytes for `casper`, 11 bytes for `casper-test`).

#### Text -> binary conversion

Encode the chainspec name as ASCII bytes.

#### Binary -> text conversion

Decode the bytes as ASCII. Implementations MUST reject bytes outside the CAIP-2 reference character set `[-_a-zA-Z0-9]`.

### Examples

| Chain | Text | Binary (ChainReference) |
|-------|------|-------------------------|
| Casper mainnet | `casper:casper` | `0x636173706572` |
| Casper testnet | `casper:casper-test` | `0x6361737065722d74657374` |

## Addresses

Casper identifies accounts and contracts with a `Key`, as defined in the [casper-types] crate. See this namespace's [CAIP-10](caip10.md) profile for how account hashes are derived from Ed25519 and Secp256k1 public keys.

This profile supports the following `Key` variants, which together cover every account and contract that can send or receive a cross-chain message:

| Variant | Key tag | Identifies | Native text form |
|---------|---------|------------|------------------|
| `Key::Account` | `0x00` | Account, by its account hash | `account-hash-<64 hex>` |
| `Key::Hash` | `0x01` | Contract package (Casper 1.x contracts) | `hash-<64 hex>` |
| `Key::AddressableEntity` | `0x11` | Account, contract or system entity (Casper 2.x) | `entity-account-<64 hex>`, `entity-contract-<64 hex>`, `entity-system-<64 hex>` |

Public keys are not addresses on Casper: they MUST be converted to their account hash (per the [CAIP-10](caip10.md) profile) before being represented in this profile.

### Text representation

```
<formatted_key>
```

Where `<formatted_key>` is the lowercase formatted string of the `Key`, exactly as produced by `Key::to_formatted_string()` in [casper-types], e.g. `account-hash-79c9563deeb7bbd05e91c7dddddec9328717fea1ae846dd54ab9dfeaae015bc0`.

#### Text -> native conversion

No transformation; the text representation is the native formatted string.

#### Native -> text conversion

No transformation. Implementations SHOULD lowercase the hexadecimal portion, since [CEP-57] checksum casing applies to public keys, not to formatted keys.

### Binary representation

The address is the [casper-types] `bytesrepr` serialization of the `Key`: a 1-byte key tag, followed for `Key::AddressableEntity` by a 1-byte entity kind tag (`0x00` system, `0x01` account, `0x02` smart contract), followed by the 32-byte hash.

| Variant | Address length | Layout |
|---------|----------------|--------|
| `Key::Account` | 33 bytes | `0x00` ‖ account hash |
| `Key::Hash` | 33 bytes | `0x01` ‖ package hash |
| `Key::AddressableEntity` | 34 bytes | `0x11` ‖ entity kind ‖ entity hash |

Including the key tag keeps the representation lossless: an account hash and a contract package hash with the same 32 bytes are distinct addresses.

#### Text -> binary conversion

Parse the formatted string into a `Key` (e.g. with `Key::from_formatted_str`) and serialize it with `bytesrepr` (`ToBytes::to_bytes`).

#### Binary -> text conversion

Deserialize the bytes into a `Key` with `bytesrepr` (`FromBytes::from_bytes`) and format it with `Key::to_formatted_string()`. Implementations MUST reject trailing bytes and any key tag or entity kind not listed above.

### Examples

| Text | Binary (Address) |
|------|------------------|
| `account-hash-79c9563deeb7bbd05e91c7dddddec9328717fea1ae846dd54ab9dfeaae015bc0` | `0x0079c9563deeb7bbd05e91c7dddddec9328717fea1ae846dd54ab9dfeaae015bc0` |
| `hash-abababababababababababababababababababababababababababababababab` | `0x01abababababababababababababababababababababababababababababababab` |
| `entity-contract-abababababababababababababababababababababababababababababababab` | `0x1102abababababababababababababababababababababababababababababababab` |

The first example is the account hash of the Ed25519 public key `01cd4f2ed572ea555ca46c17c83c43e609d2e916871236f40faa9ba747478e8dee` from this namespace's [CAIP-10](caip10.md) test cases.

Complete [ERC-7930] _Interoperable Addresses_:

Account on Casper mainnet
: `casper:casper` + `account-hash-79c9563deeb7bbd05e91c7dddddec9328717fea1ae846dd54ab9dfeaae015bc0`
: `0x0001000406636173706572210079c9563deeb7bbd05e91c7dddddec9328717fea1ae846dd54ab9dfeaae015bc0`

Account on Casper testnet (Secp256k1 key `02022ade9bd8e06033e99b1bfbf789db4e2db0349045818469bbcaf756996900e838`)
: `casper:casper-test` + `account-hash-5b7e450d8b1e58de5f012db6c6e934431a6b6b063e5d4955914675e791797712`
: `0x000100040b6361737065722d7465737421005b7e450d8b1e58de5f012db6c6e934431a6b6b063e5d4955914675e791797712`

Contract package on Casper mainnet
: `casper:casper` + `hash-abababababababababababababababababababababababababababababababab`
: `0x00010004066361737065722101abababababababababababababababababababababababababababababababab`

Smart contract entity on Casper testnet
: `casper:casper-test` + `entity-contract-abababababababababababababababababababababababababababababababab`
: `0x000100040b6361737065722d74657374221102abababababababababababababababababababababababababababababababab`

Chain identifier for Casper mainnet (no address)
: `casper:casper`
: `0x000100040663617370657200`

## Error handling

Conversions between this profile and [CAIP-2] are lossless, since both use the chainspec name. Conversion from [CAIP-10] is lossless for account hashes. A public key can be converted into this profile (via its account hash), but not recovered from it.

Implementations SHOULD signal an error when:

- the chain reference contains characters outside `[-_a-zA-Z0-9]`;
- the address does not deserialize to exactly one supported `Key` variant, or has trailing bytes;
- the address length does not match its key tag (33 bytes for `0x00` and `0x01`, 34 bytes for `0x11`).

## Implementation considerations

- Contracts deployed before Casper 2.0 are addressed by their contract package hash (`Key::Hash`), which stays stable across contract upgrades. Implementations SHOULD use the package hash, not a contract (version) hash, to identify a contract.
- On Casper 2.x networks that enable addressable entities (a chainspec setting), an account can be referenced as `Key::Account` or as `Key::AddressableEntity` with entity kind `account`, and a contract as `Key::Hash` or as an entity. These produce different binary addresses. Applications comparing addresses for equality SHOULD normalize to the form native to the target network.
- The chainspec name, not the genesis hash, identifies the network. This matches the [CAIP-2](caip2.md) profile and the replay protection Casper itself applies to transactions.

## Extra considerations

Canonicity holds per `Key` variant, but not across variants: as noted above, one Casper 2.x account has two valid binary forms. Systems relying on byte equality of _Interoperable Addresses_ should account for this.

## References

- [casper-types]: Rust types for the Casper network, including `Key` and its `bytesrepr` serialization
- [CEP-57]: Checksummed hex encoding for Casper public keys and hashes
- [Casper Docs site][]

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[CAIP-104]: https://chainagnostic.org/CAIPs/caip-104
[CAIP-350]: https://chainagnostic.org/CAIPs/caip-350
[ERC-7930]: https://eips.ethereum.org/EIPS/eip-7930
[casper-types]: https://docs.rs/casper-types/latest/casper_types/enum.Key.html
[CEP-57]: https://github.com/casper-network/ceps/blob/master/text/0057-checksummed-addresses.md
[Casper Docs site]: https://docs.casper.network/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
