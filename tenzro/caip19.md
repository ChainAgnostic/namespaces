---
namespace-identifier: tenzro-caip19
title: Tenzro Namespace - Asset
author: Tenzro Engineering (eng@tenzro.com)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/184
status: Draft
type: Standard
created: 2026-05-02
updated: 2026-05-02
requires: ["CAIP-2", "CAIP-10", "CAIP-19"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Rationale

Tenzro hosts assets across three VM façades (EVM, SVM, Canton/DAML) that all
share a single underlying native balance — the Sei-V2-style pointer model.
For CAIP-19 purposes, an asset is identified by its canonical Tenzro token
ID (a 32-byte SHA-256 of `creator || nonce`) regardless of which VM façade a
client uses to interact with it. The same TNZO holding is reachable as wTNZO
(ERC-20) on the EVM façade, as a wTNZO SPL token on the SVM façade, and as a
CIP-56 holding on the Canton façade — but the CAIP-19 reference is one and
the same.

Two asset namespaces are defined:

| `asset_namespace` | Meaning                                            |
| :---------------- | :------------------------------------------------- |
| `slip44`          | TNZO native coin — uses the [SLIP-44][] coin index |
| `token`           | Fungible token registered in Tenzro's unified token registry, identified by 32-byte token ID |
| `nft`             | Non-fungible token, identified by `<collection_id>/<token_id>` where `collection_id` is the 32-byte collection ID |

The native TNZO coin SHOULD use the `slip44` namespace once a SLIP-44 index
is registered upstream. Until then, implementations MAY use the literal
reference `tenzro` under `slip44` (vendor-prefixed pre-registration); see
the SLIP-44 PR tracker for the registered index.

## Syntax

After the [CAIP-2][] chain prefix, a slash defines an `asset_namespace` and
an `asset_reference`:

```
asset_id := chain_id "/" asset_namespace ":" asset_reference [ "/" token_id ]
```

- `chain_id`: CAIP-2 identifier (see `caip2.md`)
- `asset_namespace`: `slip44` | `token` | `nft`
- `asset_reference`:
  - For `slip44`: registered SLIP-44 coin index (decimal integer) or the
    pre-registration string `tenzro`
  - For `token`: 64-character lowercase hex of the 32-byte token ID
  - For `nft`: 64-character lowercase hex of the 32-byte collection ID
- `token_id` (NFT only): 64-character lowercase hex of the 32-byte
  `mintRandom`-derived token ID, or a decimal integer for sequentially
  minted tokens

## Examples

```
# Tenzro Testnet — native TNZO coin (pre-registration form)
tenzro:92bd27db9713293097f0e63476e3911e/slip44:tenzro

# Tenzro Testnet — fungible token (e.g. an ERC-20 deployed via TOKEN_FACTORY)
tenzro:92bd27db9713293097f0e63476e3911e/token:7a4bcb13a6b2b384c284b5caa6e5ef3126527f93000000000000000000000000

# Tenzro Testnet — NFT (collection_id / token_id)
tenzro:92bd27db9713293097f0e63476e3911e/nft:a1b2c3d4e5f6...64hex.../42
```

## Cross-VM identity

The same asset identifier MUST resolve to the same underlying balance
regardless of which VM façade a client queries. For example, given a TNZO
balance for an account `A`:

- `eth_getBalance(A)` on the EVM façade
- `tenzro_getTokenBalance({owner: A, token: <wtnzo_evm_addr>})` on the
  Tenzro-native API
- An SPL token-account query against the SVM `tenzro_cross_vm` program for
  wTNZO

…all return the same numeric value (in 18-decimal precision; SPL truncates
to 9 decimals at the boundary). The CAIP-19 identifier is the cross-VM
canonical name; the per-VM contract addresses are aliases.

## References

- [CAIP-2][]
- [CAIP-10][]
- [CAIP-19][]
- [SLIP-44][]
- [Tenzro Network repository][repo]

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[SLIP-44]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[repo]: https://github.com/tenzro/tenzro-network

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
