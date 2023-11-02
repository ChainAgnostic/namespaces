---
namespace-identifier: ergo-caip10
title: Ergo Namespace - Addresses
author: Yuriy Gagarin (@gagarin55)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/...
status: Draft
type: Standard
created: 2023-11-02
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale


Ergo "address" can change depending on chain ID. This prevents unintentional
transfers across Ergo blockchains.

## Syntax

The syntax of Ergo addresses:

```
caip10-like address:    namespace + ":" chainId + ":" + address
namespace:              ergo
chain Id:               8-bit unsigned integer in which lower 4 bits are zeros characters in length
address:                Ergo address represented as a [Base58btc][]-encoded string
```

The underlying form of each Ergo address is ...

### Resolution method

...

## Test Cases

```
# Namespace-wide Public Key:
# [TODO]

# Address on Ergo Mainnet (0)
ergo:0:[TODO]

# Address on Ergo Testnet (16)
ergo:16:[TODO]
```

## Links

- [About addresses in Ergo Documentation][address format]
- [Conversion between binary and Base58btc representation][base58btc]

[address format]: https://docs.ergoplatform.com/dev/wallet/address/address_types
[base58btc]: https://en.bitcoin.it/wiki/Base58Check_encoding#Base58_symbol_chart

## Copyright

Copyright and related rights waived via
[CC0](https://creativecommons.org/publicdomain/zero/1.0/).
