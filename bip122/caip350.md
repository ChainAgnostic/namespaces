---
namespace-identifier: bip122-caip350
title: BIP122 Namespace - Interoperable Address
binary-key: 0001
author: Orca (@0xrcinus), Mono (@0xMonoAx)
discussions-to: https://ethereum-magicians.org/t/erc-7930-interoperable-addresses/23365
status: Draft
type: Standard
created: 2026-01-29
requires: CAIP-2
---

## Namespace Reference

ChainType binary key: `0x0001`
[CAIP-104] namespace: `bip122`

## Chain reference

See this namespace's [CAIP-2](caip2.md) profile. The chain reference is the first 32 characters (16 bytes) of the genesis block hash in lowercase hex.

### Text representation

```
<genesis_hash_prefix>
```

Where `<genesis_hash_prefix>` is the first 32 lowercase hex characters (16 bytes) of the genesis block hash as defined in [BIP122][].

> **Note:** Per [CAIP-350], the full chain identifier is `bip122:<genesis_hash_prefix>` (e.g., `bip122:000000000019d6689c085ae165831e93`, `bip122:000000000933ea01ad0ee984209779ba`).

##### Text representation -> customary (CAIP-2) conversion

The text representation (chain reference) is the same as the chain reference in the [CAIP-2](caip2.md) chain identifier; no conversion is needed.

##### Customary (CAIP-2) conversion - text representation conversion

The chain reference in the [CAIP-2](caip2.md) chain identifier is the same as the text representation; no conversion is needed.

#### Binary representation

The chain reference is the 16 bytes corresponding to the first 32 hex characters of the genesis block hash. Bytes are in the same order as the hex string (first two hex characters encode the first byte, etc.).

#### Text -> binary conversion

Decode the 32-character lowercase hex string to 16 bytes (RFC-4616 base16, no 0x-prefix).

#### Binary -> text conversion

Encode the 16 bytes as 32 lowercase hex characters (RFC-4616 base16, no 0x-prefix).

#### Examples

| Chain | Text (chain reference) | Binary |
|-------|------------------------|--------------------------------|
| Bitcoin mainnet | `000000000019d6689c085ae165831e93` | `0x000000000019d6689c085ae165831e93` |
| Bitcoin testnet | `000000000933ea01ad0ee984209779ba` | `0x000000000933ea01ad0ee984209779ba` |
| Litecoin mainnet | `12a765e31ffd4059bada1e25190f6e98` | `0x12a765e31ffd4059bada1e25190f6e98` |

## Addresses

See this namespace's [CAIP-10](caip10.md) profile. BIP122 supports multiple address types (P2SH, SegWit, Taproot) with different native encodings (base58btc, bech32, bech32m).

### Text representation

```
<address>
```

Where `<address>` is the full native ASCII form (base58btc, bech32, or bech32m) as in [CAIP-10](caip10.md)—e.g. P2SH `35PBEaofpUeH8VnnNSorM1QZsadrZoQp4N`, SegWit `bc1qwz2lhc40s8ty3l5jg3plpve3y3l82x9l42q7fk`, or Taproot `bc1pmzfrwwndsqmk5yh69yjr5lfgfg4ev8c0tsc06e`.

#### Text representation -> native representation conversion

No transformation; the text representation is the native representation.

#### Native representation -> text representation conversion

No transformation; the native representation is the text representation.

### Binary representation

The binary representation uses a one-byte type prefix followed by the decoded payload (without checksum):

- **0x01 — P2SH**: 1 byte version (network-dependent) + 20 bytes script hash (21 bytes total after type).
- **0x02 — Witness (SegWit / Taproot)**: 1 byte witness version (0 for P2WPKH, 1 for P2TR, etc.) + 20 or 32 bytes program (22 or 34 bytes total after type).

Checksums are omitted in binary; they can be recomputed when converting back to text.

#### Text -> binary conversion

1. Detect address type from prefix (e.g. `3` for P2SH, `bc1q`/`tb1q` etc. for witness).
2. Decode using the appropriate scheme ([base58btc][] for P2SH, [bech32][]/[bech32m][] for witness) and strip checksum.
3. Prepend type byte 0x01 (P2SH) or 0x02 (witness), then append version byte and hash/program bytes as above.

#### Binary -> text conversion

1. Read the type byte (0x01 or 0x02).
2. For 0x01: read 21 bytes (1 version + 20 hash), encode with base58btc including checksum for the target network.
3. For 0x02: read 1 byte witness version, then 20 or 32 bytes program; encode with [bech32][] or [bech32m][] (and correct HRP for network).

### Examples

| Text (Bitcoin mainnet) | Binary (hex, after type byte) |
|------------------------|-------------------------------|
| P2SH `35PBEaofpUeH8VnnNSorM1QZsadrZoQp4N` | `0x01` + base58btc-decoded payload (version + 20-byte hash) |
| SegWit `bc1qwz2lhc40s8ty3l5jg3plpve3y3l82x9l42q7fk` | `0x02` + `0x00` + 20-byte witness program |
| Taproot `bc1pmzfrwwndsqmk5yh69yjr5lfgfg4ev8c0tsc06e` | `0x02` + `0x01` + 32-byte witness program |

## Error handling

When converting from this profile's [CAIP-2] encoding to this profile's [CAIP-350] encoding, the chain reference is already fully specified (32 hex chars), so no loss of information or difference of expression occurs. For addresses, invalid or unsupported native encodings (e.g. legacy P2PKH excluded from [CAIP-10](caip10.md)) should be rejected with an appropriate error.

## Implementation considerations

Legacy P2PKH addresses are excluded from [CAIP-10](caip10.md) and therefore from this profile. Only P2SH, SegWit, and Taproot address types are supported. Implementations must use the correct HRP and version bytes per network (e.g. mainnet vs testnet, or other BIP122 chains).

## Extra considerations

Wallets and other software are expected to be able to fetch the extra information needed to convert from [CAIP-2](caip2.md) to produce the corresponding identifier defined by this standard.

## References

[BIP122]: https://github.com/bitcoin/bips/blob/master/bip-0122.mediawiki
[BIP13]: https://github.com/bitcoin/bips/blob/master/bip-0013.mediawiki
[BIP173]: https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki
[BIP350]: https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki
[base58btc]: https://datatracker.ietf.org/doc/html/draft-msporny-base58-02
[bech32]: https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki
[bech32m]: https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[CAIP-104]: https://chainagnostic.org/CAIPs/caip-104
[CAIP-350]: https://chainagnostic.org/CAIPs/caip-350
