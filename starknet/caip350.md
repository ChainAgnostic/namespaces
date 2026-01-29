---
namespace-identifier: starknet-caip350
title: StarkNet Namespace - Interoperable Address
binary-key: 0003
author: Orca (@0xrcinus), Mono (@0xMonoAx)
discussions-to: https://ethereum-magicians.org/t/erc-7930-interoperable-addresses/23365
status: Draft
type: Standard
created: 2026-01-29
requires: CAIP-2
---

## Namespace Reference

ChainType binary key: `0x0003`
[CAIP-104] namespace: `starknet`

## Chain reference

See this namespace's [CAIP-2](caip2.md) profile. Chains are identified by string identifiers (e.g. `SN_MAIN`, `SN_GOERLI`) that are encoded as field elements on the chain but expressed as ASCII strings in CAIP-2.

### Text representation

```
<chain_id_string>
```

Where `<chain_id_string>` is the case-sensitive chain identifier (e.g. `SN_MAIN`, `SN_GOERLI`) as returned by `starknet_chainId` after converting the hex-encoded field element to a string.

> **Note:** Per [CAIP-350], the full chain identifier is `starknet:<chain_id_string>` (e.g., `starknet:SN_MAIN`, `starknet:SN_GOERLI`).

##### Text representation -> customary (CAIP-2) conversion

The text representation is identical to the [CAIP-2](caip2.md) chain identifier; no conversion is needed.

##### Customary (CAIP-2) conversion - text representation conversion

The [CAIP-2](caip2.md) chain identifier is identical to the text representation; no conversion is needed.

#### Binary representation

The chain reference is the binary form of the chain ID as used by the chain: the bytes obtained by decoding the hex-encoded value returned by `starknet_chainId` (RFC-4616 base16, strip any `0x` prefix). This is the field element in byte form. Length is variable (e.g. 7 bytes for `SN_MAIN`, 9 bytes for `SN_GOERLI`). The ChainReference field in binary Interoperable Addresses must carry this byte sequence; higher-level framing (e.g. length prefix) is defined by [ERC-7930][] / CAIP-350.

#### Text -> binary conversion

Obtain the chain ID string (the segment after `starknet:`). To get the binary form: decode the hex returned by `starknet_chainId` for that chain to bytes. Equivalently, for current chain IDs the byte form coincides with the UTF-8 encoding of the string.

#### Binary -> text conversion

Decode the bytes to the chain ID string (for current identifiers, the bytes are UTF-8/ASCII) and format as `starknet:<string>`.

#### Examples

| Chain | Text | Binary (hex of ChainReference) |
|-------|------|--------------------------------|
| StarkNet mainnet | `starknet:SN_MAIN` | `0x534e5f4d41494e` (binary form from `starknet_chainId`) |
| StarkNet Goerli | `starknet:SN_GOERLI` | `0x534e5f474f45524c49` (binary form from `starknet_chainId`) |

## Addresses

See this namespace's [CAIP-10](caip10.md) profile. StarkNet addresses are 32-byte field elements, represented as `0x` followed by 64 hexadecimal characters (zero-padded), with optional [EIP-55][] checksum.

### Text representation

```
<address>
```

Where `<address>` is the 32-byte field element as in [CAIP-10](caip10.md): `0x` followed by 64 hex characters (EIP-55 checksum recommended), e.g. `0x02DdfB499765c064eaC5039E3841AA5f382E73B598097a40073BD8B48170Ab57`.

##### Text representation -> native representation conversion

Strip the `0x` prefix and decode the 64 hex characters to 32 bytes. Checksum validation (if present) follows [EIP-55][].

##### Native representation -> text representation conversion

Encode the 32 bytes as 64 hex characters with `0x` prefix. Apply [EIP-55][] checksum for the canonical text form.

#### Binary representation

The address is stored as the raw 32 bytes (big-endian), as in the native field element representation. No length prefix is needed for fixed-size addresses.

#### Text -> binary conversion

Remove the `0x` prefix and decode the 64 hex characters to 32 bytes (RFC-4616 base16).

#### Binary -> text conversion

Encode the 32 bytes as 64 hex characters and prepend `0x`. Apply [EIP-55][] checksum for the canonical form.

#### Examples

| Text | Binary (hex of Address field) |
|------|-------------------------------|
| `0x02DdfB499765c064eaC5039E3841AA5f382E73B598097a40073BD8B48170Ab57` | `0x02ddfb499765c064eac5039e3841aa5f382e73b598097a40073bd8b48170ab57` (32 bytes) |

### Error handling

When converting from CAIP-2 to this profile, the chain reference is fully determined by the chain ID string, so no loss of information occurs. If a chain ID is unknown or the UTF-8 encoding is invalid, implementations should signal an error.

### Implementation considerations

Chain IDs are resolved via `starknet_chainId` (hex-encoded); the interoperable format uses the string form for text representation and the hex-decoded bytes (binary form) for binary representation. Addresses are always 32 bytes; leading zero in hex is normal for field elements below 2^255.

### Extra considerations

Wallets and other software are expected to be able to fetch the extra information needed to convert from [CAIP-2](caip2.md) to produce the corresponding identifier defined by this standard.

## References

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[CAIP-104]: https://chainagnostic.org/CAIPs/caip-104
[CAIP-350]: https://chainagnostic.org/CAIPs/caip-350
[EIP-55]: https://eips.ethereum.org/EIPS/eip-55
[ERC-7930]: https://eips.ethereum.org/EIPS/eip-7930
