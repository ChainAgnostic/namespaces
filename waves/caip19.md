---
namespace-identifier: waves-caip19
title: Waves Namespace - Assets
author: Maxim Smolyakov (@msmolyakov), Yury Sidorov (@darksyd94)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/49
status: Draft
type: Standard
created: 2023-01-19
requires: ["CAIP-2", "CAIP-19"]
---

## Rationale

Any account can issue its own token. The new token is immediately available.

The ID format for fungible (ERC20-equivalent) and non-fungible (ERC-721
equivalent) tokens is the same.  The process for issuance of either is also the
same. The only difference is that NFTs must have specific values for certain
properties.

## Specification of Asset ID

Asset ID is a 32 byte array encoded as a [Base58btc][]-encoded string. When
issued directly, it is equal to the ID of the transaction that issued this
asset; when the token is issued using via a smart contract call, the asset will
instead be addressed by a Blake2b-256 hash of the transaction and parameters
passed in the call. This is true for both fungible and non-fungible tokens,
which are distinguished instead by their [token][] metadata which can be
retrieved or verified by an RPC call from a node (see [token][] reference).

## Syntax

The syntax of Waves Asset ID:

```
address:    namespace + ":" chainId + ":" + reference
namespace:  waves
chain ID:   [-128..127] value packed to 3 characters with leading zeros
reference:  Waves Asset ID represented as [Base58btc][]-encoded string
```

## Examples

```
# Waves Mainnet (87)
waves:087:DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p

# Waves Testnet (84)
waves:084:2HAJrwa8q4SxBx9cHYaBTQdBjdk5wwqdof7ccpAx2uhZ

# Waves custom network (-7)
waves:-07:2HAJrwa8q4SxBx9cHYaBTQdBjdk5wwqdof7ccpAx2uhZ
```

## Links

- [Token][token] overview
- [Token ID][token id] syntax
- [About addresses in Waves Documentation][address format]
- [Conversion between binary and Base58btc representation][base58btc]

[token]: https://docs.waves.tech/en/blockchain/token
[token id]: https://docs.waves.tech/en/blockchain/token/token-id
[address format]: https://docs.waves.tech/en/blockchain/account/address
[address checksum]: https://docs.waves.tech/en/blockchain/binary-format/address-binary-format
[base58btc]: https://en.bitcoin.it/wiki/Base58Check_encoding#Base58_symbol_chart

## Copyright

Copyright and related rights waived via [CC0](../LICENSE).
