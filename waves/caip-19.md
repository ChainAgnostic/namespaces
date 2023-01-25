---
namespace-identifier: waves-caip19
title: Waves Namespace - Assets
author: Maxim Smolyakov (@msmolyakov), Yury Sidorov (@darksyd94)
discussions-to:
status: Draft
type: Standard
created: 2023-01-19
---

## Rationale

Any account can issue its own token. The new token is immediately available.

ID format of fungible and non-fungible tokens is the same.

Process of issuing is also the same. The only difference is that NFTs must have specific values for certain properties.

## Specification of Asset ID

Asset ID is a 32 byte array encoded as Base58 string. It's usually equal to ID of the transaction that issued this asset (except when the token is issued using a dApp contract, but in this case the Asset ID format is always the same). This is true for both fungible and non-fungible tokens.

## Examples

```
# Mainnet
DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p

# Testnet
2HAJrwa8q4SxBx9cHYaBTQdBjdk5wwqdof7ccpAx2uhZ
```

## Links

- [Token](https://docs.waves.tech/en/blockchain/token)
- [Token ID](https://docs.waves.tech/en/blockchain/token/token-id)

## Copyright

Copyright and related rights waived via [CC0](../LICENSE).
