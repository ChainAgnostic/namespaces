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

Waves "account" has a public key that is the same for any Waves blockchain.

But Waves "address" is 26 byte array derived from public key and represented as Base58 encoded string.

Waves "address" can change depending on chain ID. It prevents unintentional transfers on other Waves blockchains. Address also contains checksum, which protects against typos and copying errors of the address.

## Syntax

The syntax of Waves addresses:

```
caip10-like address:    namespace + ":" + address
namespace:              waves
address:                Waves address represented as Base58 encoded string
```

Waves address is byte array of `Entity type + Chain ID + Account public key hash + Checksum`, where:
1. `Entity type` — always 1-byte integer with value `1`
2. `Chain ID` — 1-byte integer of current blockchain ID
3. `Account public key hash` — first 20 bytes of the result of `keccak256(publicKey)` hashing function
4. `Checksum` — first 4 bytes of the result of `keccak256(Entity type + Chain ID + Account public key hash)` hashing function

### Resolution method

To derive an address from public key, make a GET HTTP request `/addresses/publicKey/{publicKey}` to the blockchain node, for example: https://nodes-testnet.wavesnodes.com/addresses/publicKey/7Y5rWP1aB1iGkDer8cS9TasAv1HpvCMZiZ2C9KLema6 \
Thus, the node will return in response an address of the account with the public key for the current blockchain, for example:

```json
{
    "address": "3NBNV8hiq8DTVF7UmzFLSUwud3h3pKZkVB3"
}
```

## Test Cases

```
# Public Key:
# 7Y5rWP1aB1iGkDer8cS9TasAv1HpvCMZiZ2C9KLema6

# Waves Mainnet
waves:3PPPJ62chFkr7hQu34WLPwKiywCpeSbfap7

# Waves Testnet
waves:3NBNV8hiq8DTVF7UmzFLSUwud3h3pKZkVB3
```

## Links

- [About addresses in Waves Documentation](https://docs.waves.tech/en/blockchain/account/address)

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
