---
namespace-identifier: klv-caip19
title: Klever Namespace - Assets
author: Nicollas Gabriel da Silva (@nickgs1337)
discussions-to: https://forum.klever.org/, https://github.com/klever-io/klever-go/discussions
status: Draft
type: Standard
created: 2026-05-13
requires: ["CAIP-2", "CAIP-19"]
---

# CAIP-19

_For context, see the [CAIP-19][] specification._

## Rationale

Klever ships a native multi-asset model called **KDA** (Klever Digital Asset)
that supports fungible tokens, non-fungible tokens (NFTs), and semi-fungible
tokens (SFTs) as first-class on-chain primitives — assets are not encoded as
smart-contract balances. The asset type enum is defined in
[`data/transaction/contracts.pb.go`][klever-contracts] (`Fungible = 0`,
`NonFungible = 1`, `SemiFungible = 2`).

The single asset namespace `kda` covers fungible, NFT, and SFT tokens. The
asset type (fungible / NFT / SFT) is metadata returned by the public asset
API and is not encoded in the CAIP-19 identifier itself.

## Syntax

```
caip19 asset id:    chainId + "/" + assetNamespace + ":" + assetReference [ + "/" + tokenId ]
namespace:          klv
chainId:            108 (Mainnet), 109 (Testnet), or 100001 (Devnet) — see CAIP-2
assetNamespace:     kda  (covers fungible, NFT, and SFT)
assetReference:     the on-chain asset id, e.g. KLV, KFI, DVK-34ZH, DVKNFT-1SW5
tokenId:            (optional) 1-indexed integer instance within an NFT/SFT collection
```

Klever asset IDs come in two shapes:

- **Protocol assets** — short uppercase tickers minted at genesis (`KLV`,
  `KFI`).
- **User-minted assets** — `TICKER-NONCE` form, where `NONCE` is a 4-char
  base36 (`[0-9A-Z]{4}`) suffix the chain assigns at creation to ensure
  uniqueness across issuers using the same ticker (`DVK-34ZH`, `WBTC-3FB5`,
  `DVKNFT-1SW5`). The suffix is generated deterministically by
  `CreateNewAssetIdentifier` in [`core/process/kda/assetHelper.go`][klever-assethelper]
  by hashing the caller address, nonce, and ticker, then base36-encoding the
  first 4 chars (see also `TickerSeparator = "-"` and
  `TickerRandomSequenceLength = 4` in
  [`core/process/kda/kdautils/utils.go`][klever-kdautils]).

Both shapes share the `kda` asset namespace.

## Test Cases

Live mainnet asset ids from `https://api.mainnet.klever.org/v1.0/assets/list`:

```
# Native Klever token (KLV) on Mainnet
klv:108/kda:KLV

# Native governance token (KFI) on Mainnet
klv:108/kda:KFI

# User-minted fungible asset on Mainnet
klv:108/kda:DVK-34ZH
klv:108/kda:WBTC-3FB5

# NFT collection on Mainnet
klv:108/kda:DVKNFT-1SW5

# Specific NFT instance #1 within the DVKNFT-1SW5 collection
klv:108/kda:DVKNFT-1SW5/1

# Testnet KLV
klv:109/kda:KLV
```

## References

- [Klever asset metadata endpoint][klever-asset-api] — REST endpoint that
  returns full KDA metadata (type, precision, max supply, issuer, etc.).
- [Klever Connect SDK][klever-connect] — TypeScript helpers for resolving
  asset metadata.
- [klever-go node source][klever-go] — Reference implementation of the KDA
  asset creation and identifier-generation logic.
- [CAIP-19][] — The chain-agnostic asset ID specification.

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[klever-asset-api]: https://api.mainnet.klever.org/v1.0/assets
[klever-connect]: https://github.com/klever-io/klever-connect
[klever-go]: https://github.com/klever-io/klever-go
[klever-contracts]: https://github.com/klever-io/klever-go/blob/develop/data/transaction/contracts.pb.go
[klever-assethelper]: https://github.com/klever-io/klever-go/blob/develop/core/process/kda/assetHelper.go
[klever-kdautils]: https://github.com/klever-io/klever-go/blob/develop/core/process/kda/kdautils/utils.go

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
