---
namespace-identifier: sui-caip350
title: Sui Namespace - Interoperable Address
binary-key: 0005
author: William Robertson (@williamrobertson13), Omer Sadika (@omersadika)
discussions-to: https://ethereum-magicians.org/t/erc-7930-interoperable-addresses/23365, https://github.com/ChainAgnostic/namespaces/pull/237
status: Draft
type: Standard
created: 2026-10-08
requires: ["CAIP-2", "CAIP-10"]
---

## Namespace Reference

ChainType binary key: `0x0005`

[CAIP-104] namespace: `sui`

## Chain reference

This profile identifies Sui networks by their full 32-byte genesis checkpoint digest.
The [CAIP-2 Profile][] uses a network name or the digest's first four bytes; names can move between chains, and four-byte identifiers can collide.

### Text representation

```
<genesis_checkpoint_digest>
```

Where `<genesis_checkpoint_digest>` is the digest as 64 lowercase hexadecimal characters, without a `0x` prefix.

> **Note:** Per [CAIP-350], the full chain identifier is `sui:<genesis_checkpoint_digest>` (e.g., `sui:35834a8ac17ca48fb14ac8f99c17c98747e95dd07294ae41a46b382246a4499b`).

Without a chain reference, `sui:` means any Sui network and has `ChainReferenceLength` zero.

Sui's RPCs return this digest in base58btc.
This profile uses hex to keep the [CAIP-2] identifier as a text prefix, as in the [`solana` profile][Solana CAIP-350 Profile].

#### Text -> customary (CAIP-2) conversion

Take the first 8 characters, e.g. `sui:35834a8a` for mainnet.
This loses information: retain the full digest to distinguish colliding prefixes and restore the original chain on import.
Show a reserved name only if the full digest matches its current trusted mapping.
For `devnet` and `localnet`, use the client's configured node; nodes report both as `unknown`.

#### Customary (CAIP-2) -> text conversion

- `sui:mainnet` converts to the mainnet digest below; `sui:testnet` converts to the testnet digest while the current testnet runs. After a reset, use the new testnet's digest.
- `sui:devnet` and `sui:localnet` use the digest from the client's trusted node for that network (`chain_id` from gRPC `GetServiceInfo`, or the GraphQL `chainIdentifier` field).
- For a four-byte identifier, determine the intended network from a retained full digest, trusted node or mapping of known networks. Fail if ambiguous; a matching prefix alone is insufficient, even for `35834a8a` or `4c78adac`.

Base58btc-decode RPC digests to 32 bytes, check any supplied four-byte identifier against the first four bytes, and fail on a mismatch.
Hex-encode the full digest for the text form.

### Binary representation

The full 32-byte digest, in order; `ChainReferenceLength` is `0x20` when present.
An absent reference has empty text and bytes, with length zero.

#### Text -> binary conversion

Base16-decode nonempty references to 32 bytes ([RFC-4648]).
Reject anything other than 64 lowercase hexadecimal characters or an empty reference.

#### Binary -> text conversion

Base16-encode nonempty references as 64 lowercase hexadecimal characters, without `0x`.

### Examples

| Network | Text (chain reference) | Binary |
|---|---|---|
| Sui mainnet | `35834a8ac17ca48fb14ac8f99c17c98747e95dd07294ae41a46b382246a4499b` | `0x35834a8ac17ca48fb14ac8f99c17c98747e95dd07294ae41a46b382246a4499b` |
| Sui testnet | `4c78adacf2a2f5ad80f27ed7d54aa69d3a78f1ca67fdef9ecf5754f5b8bb77b0` | `0x4c78adacf2a2f5ad80f27ed7d54aa69d3a78f1ca67fdef9ecf5754f5b8bb77b0` |

These are the base58btc constants `4btiuiMPvEENsttpZC7CZ53DruC3MAgfznDbASZ7DR6S` (mainnet) and `69WiPg3DAQiwdxfncX6wYQ2siKwAe6L9BZthQea3JNMD` (testnet) in [Sui's source][Sui digests], decoded to bytes.

## Addresses

Sui addresses are 32 bytes, with the same text form as the [CAIP-10 Profile][].
Account addresses and object IDs, including packages and shared objects, share this space; both are valid.

### Text representation

```
0x<address>
```

Where `<address>` is the 32 bytes as exactly 64 lowercase hexadecimal characters.

#### Text -> native conversion

No transformation.

#### Native -> text conversion

Left-pad short forms such as `0x2` with zeros to 64 digits, and lowercase.
Reject a native address with more than 64 hexadecimal digits.

### Binary representation

The 32 address bytes; `AddressLength` is `0x20` when present.
An absent address has empty text and bytes, with length zero, distinct from the zero address or `0x`.

#### Text -> binary conversion

For a nonempty address, remove the `0x` and base16-decode ([RFC-4648]).

#### Binary -> text conversion

For a nonempty address, base16-encode in lowercase and add the `0x` prefix.

### Examples

| Native | Text | Binary |
|---|---|---|
| `0x90eb19346f76a7d5e0a8e2630d3b3728039d41fd8f1062dd3776f95e0b8ce5f0` (an account) | `0x90eb19346f76a7d5e0a8e2630d3b3728039d41fd8f1062dd3776f95e0b8ce5f0` | `0x90eb19346f76a7d5e0a8e2630d3b3728039d41fd8f1062dd3776f95e0b8ce5f0` |
| `0x90EB19346F76A7D5E0A8E2630D3B3728039D41FD8F1062DD3776F95E0B8CE5F0` (the same account, upper case) | `0x90eb19346f76a7d5e0a8e2630d3b3728039d41fd8f1062dd3776f95e0b8ce5f0` | `0x90eb19346f76a7d5e0a8e2630d3b3728039d41fd8f1062dd3776f95e0b8ce5f0` |
| `0x2` (the Sui framework package) | `0x0000000000000000000000000000000000000000000000000000000000000002` | `0x0000000000000000000000000000000000000000000000000000000000000002` |

An account on Sui mainnet as a complete [ERC-7930] Interoperable Address:

```
0x0001 0005 20 35834a8ac17ca48fb14ac8f99c17c98747e95dd07294ae41a46b382246a4499b 20 90eb19346f76a7d5e0a8e2630d3b3728039d41fd8f1062dd3776f95e0b8ce5f0
  ^^^^ ^^^^ ^^ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ^^ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  |    |    |  ChainReference: mainnet genesis checkpoint digest                 |  Address
  |    |    ChainReferenceLength (32)                                            AddressLength (32)
  |    ChainType (sui)
  Version (1)
```

Sui mainnet alone, as a Chain Identifier with no address:

```
0x000100052035834a8ac17ca48fb14ac8f99c17c98747e95dd07294ae41a46b382246a4499b00
```

The same account on any Sui network, with no chain reference:

```
0x00010005002090eb19346f76a7d5e0a8e2630d3b3728039d41fd8f1062dd3776f95e0b8ce5f0
```

## Error handling

Either component may be absent, but reject an Interoperable Address with both absent ([ERC-7930]).
Reject a nonempty chain reference that is not exactly 32 bytes (64 lowercase hexadecimal characters in text).
Reject a nonempty address that is not exactly 32 bytes (`0x` followed by 64 lowercase hexadecimal digits in standard text).

Parsing an Interoperable Address never needs outside information.
Imports requiring a node or trusted mapping are problematic conversions under [CAIP-350]; libraries should distinguish failed or ambiguous lookups from malformed input.
An absent chain reference has no [CAIP-2] equivalent.
Conversion to CAIP-10 requires supplying any missing chain or address.

## Implementation considerations

One key derives the same address on every Sui network, but authorization depends on each network's address aliases ([CAIP-10 Profile]).
A receiver must check the chain reference, not just the address.
Without a chain reference, an account address means that address on any Sui network; most objects exist on only one network, so object IDs should carry one.

An address does not say whether it is an account or an object.
Assets sent to an object can only be retrieved through that object's own Move module, and never from a package or other immutable object such as `0x2` ([Sui Transfer to Object]).

## Extra considerations

Chain references and addresses each have exactly one text form and one binary form.
A devnet reset changes its chain reference, allowing receivers to reject messages from the previous devnet.
Store chain references rather than names.
Updates follow the Governance section of the [CAIP-2 Profile][].

## References

- [CAIP-2 Profile] - This namespace's chain IDs.
- [CAIP-10 Profile] - This namespace's account IDs.
- [Sui digests] - The genesis checkpoint digests of mainnet and testnet in Sui's source.
- [Sui gRPC API] - `LedgerService`, including `GetServiceInfo`.
- [Sui GraphQL API] - Reference for Sui's GraphQL RPC, including `chainIdentifier`.
- [Sui Transfer to Object] - How objects receive objects sent to their address.
- [Solana CAIP-350 Profile] - The `solana` namespace's Interoperable Address profile.
- [CAIP-2] - Chain ID Specification.
- [CAIP-104] - Namespaces.
- [CAIP-350] - Interoperable Address profiles.
- [ERC-7930] - Interoperable Addresses.
- [RFC-4648] - Base16, base32 and base64 encodings.

[CAIP-2 Profile]: ./caip2.md
[CAIP-10 Profile]: ./caip10.md
[Sui digests]: https://github.com/MystenLabs/sui/blob/main/crates/sui-types/src/digests.rs
[Sui gRPC API]: https://github.com/MystenLabs/sui-apis/blob/main/proto/sui/rpc/v2/ledger_service.proto
[Sui GraphQL API]: https://docs.sui.io/references/sui-graphql
[Sui Transfer to Object]: https://docs.sui.io/develop/objects/transfers/transfer-to-object
[Solana CAIP-350 Profile]: https://namespaces.chainagnostic.org/solana/caip350
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-104]: https://chainagnostic.org/CAIPs/caip-104
[CAIP-350]: https://chainagnostic.org/CAIPs/caip-350
[ERC-7930]: https://eips.ethereum.org/EIPS/eip-7930
[RFC-4648]: https://datatracker.ietf.org/doc/html/rfc4648

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
