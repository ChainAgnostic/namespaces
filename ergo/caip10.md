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

Address types are (semantics described below):

* 0x01 - Pay-to-PublicKey(P2PK) address
* 0x02 - Pay-to-Script-Hash(P2SH)
* 0x03 - Pay-to-Script(P2S)

Constructing an address:

- **Prefix byte** = `chain ID + address type`
(for example, P2S script on the testnet starts with 0x13 before Base58)
- **checksum** = `leftmost_4_bytes (blake2b256 (prefix byte || content bytes))`
- **address** = `prefix byte || content bytes || checksum`

For an address type, we form `content bytes` as follows:

- **P2PK** - serialized (compressed) public key
- **P2SH** - first 192 bits of the Blake2b256 hash of serialized script bytes
- **P2S** - serialized script

## Syntax

The syntax of Ergo addresses:

```
caip10-like address:    namespace + ":" chainId + ":" + address
namespace:              ergo
chain Id:               8-bit unsigned integer in which lower 4 bits are zeros 
address:                Ergo address represented as a [Base58btc][]-encoded string
```



## Test Cases

```
# Namespace-wide Public Key:
# [TODO]

# P2PK Address on Ergo Mainnet (0)
ergo:0:[TODO]

# P2PK Address on Ergo Testnet (16)
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
