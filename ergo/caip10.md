---
namespace-identifier: ergo-caip10
title: Ergo Namespace - Addresses
author: Yuriy Gagarin (@gagarin55)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/98
status: Draft
type: Standard
created: 2023-11-02
updated: 2023-11-09
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

A given Ergo "address" changes completely depending on the network identifier segment.
Different address types in the Ergo-specific UTXO model, like the network identifier used to encode the network on which the address can be dereferenced, can only be determined by decoding the string and inspecting the initial prefix byte.
This prevents unintentional transfers across Ergo blockchains.

Constructing an address:

- **Prefix byte** = `network identifier + address type discriminant`
- **checksum** = `leftmost_4_bytes (blake2b256 (prefix byte || content bytes))`
- **address** = `prefix byte || content bytes || checksum`

Network type is 8-bit unsigned integer in which lower 4 bits are zeros.

Possible values:
* Mainnet - 0 (in hex `0x00`)
* Testnet - 16 (in hex `0x10`)


Address types are (semantics described below):

* 0x01 - Pay-to-PublicKey(P2PK) address
* 0x02 - Pay-to-Script-Hash(P2SH)
* 0x03 - Pay-to-Script(P2S)

For an address type, we form `content bytes` as follows:

- **P2PK** - serialized (compressed) public key
- **P2SH** - first 192 bits of the Blake2b256 hash of serialized script bytes
- **P2S** - serialized script

The checksum is calculated after concatenating prefix byte to content bytes, and then postpended to form a full Ergo standard address notation.

## Syntax

The syntax of Ergo addresses:

```
caip10-like address:    namespace + ":" chainId + ":" + address
namespace:              ergo
chain Id:               32-character prefix from the hash of the genesis block 
address:                Ergo address represented as a [Base58btc][]-encoded string
```



## Test Cases

```
# Namespace-wide Public Key:
# 0x0202f2b96aa59e6f37fc978883f78e54fd319fa37dcf971d8e69f9e9225376bcf1

# P2PK Address on Ergo Mainnet
ergo:b0244dfc267baca974a4caee06120321:9eYMpbGgBf42bCcnB2nG3wQdqPzpCCw5eB1YaWUUen9uCaW3wwm

# P2PK Address on Ergo Testnet
ergo:e7553c9a716bb3983ac8b0c21689a1f3:3WvdWQMfUeKFcsQudPM4zqTCcncSAtYZgi96Vr3zLJqYQVn2qmaw
```

## Links

- [About addresses in Ergo Documentation][address format]
- [Conversion between binary and Base58btc representation][base58btc]

[address format]: https://docs.ergoplatform.com/dev/wallet/address/address_types
[base58btc]: https://en.bitcoin.it/wiki/Base58Check_encoding#Base58_symbol_chart

## Copyright

Copyright and related rights waived via
[CC0](https://creativecommons.org/publicdomain/zero/1.0/).
