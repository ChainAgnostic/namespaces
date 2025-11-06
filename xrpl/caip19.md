---
namespace-identifier: xrpl-caip19
title: XRP Ledger Namespace - Assets
author: Pelle Braendgaard (@pelle)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/158/
status: Draft
type: Standard
created: 2023-02-23
updated: 2025-11-06
requires: ["CAIP-2", "CAIP-10", "CAIP-19", "CAIP-20"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Rationale

The XRP Ledger supports multiple types of digital assets beyond its native XRP token. These include fungible tokens (issued currencies via trust lines), non-fungible tokens (NFTokens via XLS-20), AMM liquidity pool tokens, and the newer Multi-Purpose Tokens (MPTs). This specification defines how to identify each asset type using the CAIP-19 standard.

## Asset Types

The XRP Ledger has the following asset types:

1. **Native XRP** - The native digital asset of the XRP Ledger, used for transaction fees and as a bridge currency
2. **Trust Line Tokens (Issued Currencies)** - Fungible tokens issued by accounts, representing any asset (fiat currencies, commodities, other tokens)
3. **NFTokens** - Non-fungible tokens following the XLS-20 standard, representing unique digital or physical assets
4. **AMM LP Tokens** - Liquidity provider tokens from Automated Market Makers (XLS-30), representing shares in liquidity pools
5. **Multi-Purpose Tokens (MPTs)** - Next-generation fungible tokens with improved efficiency (currently in development)

## Syntax

The asset identification follows the CAIP-19 standard with the chain ID from [CAIP-2][] followed by a slash, an asset namespace, a colon, and an asset reference.

```
asset_id:           chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           See [CAIP-2][]
asset_namespace:    "slip44" | "token" | "xls20" | "xls30" | "xls33"
asset_reference:    slip44_ref | token_ref | xls20_ref | xls30_ref | xls33_ref

slip44_ref:         "144"
token_ref:          currency_code + "." + issuer_address
currency_code:      standard_code | nonstandard_code
standard_code:      [A-Za-z0-9?!@#$%^&*<>(){}[\]|]{3}
nonstandard_code:   [0-9A-F]{40}
issuer_address:     r[1-9a-hj-zA-HJ-NP-Z]{24,34}
xls20_ref:          [0-9A-F]{64}
xls30_ref:          [0-9A-F]{40} + "." + amm_address
amm_address:        r[1-9a-hj-zA-HJ-NP-Z]{24,34}
xls33_ref:          [0-9A-F]{64}
```

## Semantics

### Native Asset (`slip44`)

The native XRP token uses the SLIP-44 coin type as defined in [CAIP-20][]. XRP has coin type 144 in the SLIP-44 registry.

**Reference format:** `144`

### Trust Line Tokens (`token`)

Issued currencies on the XRP Ledger are fungible tokens that exist in trust lines between accounts. Each token is identified by a currency code and an issuer address.

**Currency codes** can be:
- **Standard format:** 3-character ASCII string (typically ISO 4217 codes like USD, EUR, but can include symbols)
- **Nonstandard format:** 40-character (160-bit) hexadecimal string for custom identifiers

**Reference format:** `{currency_code}.{issuer_address}`

The currency code and issuer address are separated by a period (`.`).

### NFTokens (`xls20`)

NFTokens follow the XLS-20 standard and are identified by their unique 64-character hexadecimal NFTokenID. The NFTokenID encodes multiple pieces of information including flags, transfer fee, issuer address, taxon, and sequence number.

**Reference format:** `{nftoken_id}`

### AMM LP Tokens (`xls30`)

Automated Market Maker liquidity provider tokens (XLS-30) represent ownership shares in AMM pools. LP token currency codes always start with `03` followed by 38 hex characters (a truncated SHA-512 hash of the asset pair). The issuer is the AMM account address.

**Reference format:** `{lp_currency_code}.{amm_address}`

### Multi-Purpose Tokens (`xls33`)

Multi-Purpose Tokens (XLS-33) are next-generation fungible tokens designed for improved efficiency. Each MPT is identified by a unique 64-character hexadecimal identifier.

**Reference format:** `{mpt_id}`

Note: MPTs are currently in development and not yet available on mainnet.

## Test Cases

```
# Native XRP on Livenet
xrpl:0/slip44:144

# RLUSD issued currency on Livenet (Ripple USD stablecoin)
xrpl:0/token:RLUSD.rMxCKbEDwqr76QuheSUMdEGf4B9xJ8m5De

# USD issued by Bitstamp on Livenet
xrpl:0/token:USD.rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B

# SOLO token with nonstandard currency code on Livenet (Sologenic)
xrpl:0/token:534F4C4F00000000000000000000000000000000.rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz

# NFToken on Livenet
xrpl:0/xls20:000B013A95F14B0044F78A264E41713C64B5F89242540EE208C3098E00000D65

# AMM LP token on Livenet (XRP/TST pool)
xrpl:0/xls30:039C99CD9AB0B70B32ECDA51EAAE471625608EA2.rE54zDvgnghAoPopCgvtiqWNq3dU5y836S

# NFToken on Testnet
xrpl:1/xls20:00081388C47ABB000CAFAF6F89F18D4E5F6A3377E340DA2C09999E250000001F

# Multi-Purpose Token on Devnet (hypothetical - MPTs not yet on mainnet)
xrpl:2/xls33:000000000A1B2C3D4E5F6789ABCDEF0123456789ABCDEF0123456789ABCDEF01
```

## References

- [XRPL Tokens Documentation][] - Overview of token types on XRP Ledger
- [XRPL Fungible Tokens][] - Trust line tokens and issued currencies
- [XRPL NFTokens (XLS-20)][] - Non-fungible token standard
- [XRPL AMM (XLS-30)][] - Automated market maker specification
- [XRPL Currency Formats][] - Standard and nonstandard currency code formats
- [NFToken Object][] - NFTokenID structure and encoding
- [SLIP-44][] - Registered coin types for BIP-0044

[CAIP-2]: ./caip2.md
[CAIP-10]: ./caip10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-20]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-20.md
[XRPL Tokens Documentation]: https://xrpl.org/docs/concepts/tokens
[XRPL Fungible Tokens]: https://xrpl.org/docs/concepts/tokens/fungible-tokens
[XRPL NFTokens (XLS-20)]: https://xrpl.org/docs/concepts/tokens/nfts
[XRPL AMM (XLS-30)]: https://xrpl.org/docs/concepts/tokens/decentralized-exchange/automated-market-makers
[XRPL Currency Formats]: https://xrpl.org/docs/references/protocol/data-types/currency-formats
[NFToken Object]: https://xrpl.org/docs/references/protocol/data-types/nftoken
[SLIP-44]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
