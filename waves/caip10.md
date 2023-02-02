---
namespace-identifier: waves-caip10
title: Waves Namespace - Addresses
author: Maxim Smolyakov (@msmolyakov), Yury Sidorov (@darksyd94)
discussions-to: 
status: Draft
type: Standard
created: 2023-01-19
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

Each Waves "account" has one public key that is the same across any Waves
blockchain. But on each Waves blockchain, this public key is expressed as a
distinct "address" expressed as a 26 byte array derived from public key (and
chain identifier) and represented as a [Base58btc][] encoded string.

Waves "address" can change depending on chain ID. This prevents unintentional
transfers across Waves blockchains. Addresses also contain an [address
checksum][] mechanism, which protects against typos and copying errors of the
address.

## Syntax

The syntax of Waves addresses:

```
caip10-like address:    namespace + ":" chainId + ":" + address
namespace:              waves
chain Id:               [-128..127] value packed with leading zeros at least 3 characters in length
address:                Waves address represented as a [Base58btc][]-encoded string
```

The underlying form of each Waves address is byte array of `Entity type + Chain
ID + Account public key hash + Checksum`, where:
1. `Entity type` — always 1-byte integer with value `1`
2. `Chain ID` — 1-byte integer of current blockchain ID
3. `Account public key hash` — first 20 bytes of the result of
   `keccak256(publicKey)` hashing function
4. `Checksum` — first 4 bytes of the result of `keccak256(Entity type + Chain ID
   + Account public key hash)` hashing function.

### Resolution method

To derive an address from public key, make a GET HTTP request
`/addresses/publicKey/{publicKey}` to the blockchain node, for example:
https://nodes-testnet.wavesnodes.com/addresses/publicKey/7Y5rWP1aB1iGkDer8cS9TasAv1HpvCMZiZ2C9KLema6

Thus, the node will return in response an address of the account with the public
key for the current blockchain, for example:

```json
{
    "address": "3NBNV8hiq8DTVF7UmzFLSUwud3h3pKZkVB3"
}
```

## Test Cases

```
# Namespace-wide Public Key:
# 7Y5rWP1aB1iGkDer8cS9TasAv1HpvCMZiZ2C9KLema6

# Address on Waves Mainnet (87)
waves:087:3PPPJ62chFkr7hQu34WLPwKiywCpeSbfap7

# Address on Waves Testnet (84)
waves:084:3NBNV8hiq8DTVF7UmzFLSUwud3h3pKZkVB3

# Waves custom network (-7)
waves:-07:3NBNV8hiq8DTVF7UmzFLSUwud3h3pKZkVB3
```

## Links

- [About addresses in Waves Documentation][address format]
- [Conversion between binary and Base58btc representation][base58btc]

[address format]: https://docs.waves.tech/en/blockchain/account/address
[address checksum]: https://docs.waves.tech/en/blockchain/binary-format/address-binary-format
[base58btc]: https://en.bitcoin.it/wiki/Base58Check_encoding#Base58_symbol_chart

## Copyright

Copyright and related rights waived via
[CC0](https://creativecommons.org/publicdomain/zero/1.0/).
