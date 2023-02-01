---
caip: 2
title: Waves Blockchain ID Specification
author: Maxim Smolyakov (@msmolyakov), Yury Sidorov (@darksyd94)
discussions-to: 
status: Draft
type: Standard
created: 2023-01-19
---

## Abstract

In CAIP-2 a general blockchain identification scheme is defined. This is the implementation of CAIP-2 for Waves network.

## Specification

### Syntax

Blockchains in the "waves" namespace are identified by their chain ID.

Chain ID format is a signed integer in decimal representation. The signed integer is represented as a one-byte signed integer in the range [-128..127].

```
chain_id:    namespace + ":" + reference
namespace:   waves
reference:   integer in the range [-128..127]. If the value is shorter than 3 characters, then must be padded with leading zeros to 3 characters
```

### Resolution method

There is no in-protocol resolution method at present. But there is a solution for some cases where it might be needed.

To resolve a blockchain reference for the Waves namespace, make a GET HTTP request `/addresses` to the blockchain node, for example: https://nodes-testnet.wavesnodes.com/addresses \
Thus, the node will return in response an array of its public blockchain addresses, for example:

```json
[
  "3NA4UdyFVv7v1J6UgGe4moyHm2fambavqvm",
  "3MvbutkV3xapQVUcGBGWCongwfdH8LKTm8w"
]
```

Decode any of them as Base58 string and take the second byte from the resulting array, for example (in pseudocode):

```java
byte getChainId(String address) {
    byte[] decodedAddress = decodeBase58(address);
    return decodedAddress[1];
}
```

This byte is the chain ID of the blockchain where this node is running.

## Rationale

The chain ID is specified as a one-byte signed integer.

For example, chain ID of Mainnet is 87 (ASCII code of "W").

There may also be other custom networks based on Waves, but with a different chain ID.

Chain ID is used in [binary format](https://docs.waves.tech/en/blockchain/binary-format/) of blockchain entities:
- [Block](https://docs.waves.tech/en/blockchain/binary-format/block-binary-format)
- [Transaction](https://docs.waves.tech/en/blockchain/binary-format/transaction-binary-format/)
- [Order](https://docs.waves.tech/en/blockchain/binary-format/order-binary-format)
- [Address](https://docs.waves.tech/en/blockchain/binary-format/address-binary-format)
- [Alias](https://docs.waves.tech/en/blockchain/binary-format/alias-binary-format)

Therefore, these entities cannot be used on another network with different chain ID.

## Test Cases

This is a list of manually composed examples

```
# Waves Mainnet
waves:087

# Waves Testnet
waves:084

# Waves Stagenet
waves:083

# Waves custom network used in the [private node Docker image](https://hub.docker.com/r/wavesplatform/waves-private-node)
waves:082

# Waves custom network with negative Chain ID
waves:-07:3NBNV8hiq8DTVF7UmzFLSUwud3h3pKZkVB3
```

## Links

- [About Chain ID in Waves Documentation](https://docs.waves.tech/en/blockchain/blockchain-network/#chain-id)
- [About binary format of blockchain entities](https://docs.waves.tech/en/blockchain/binary-format/)

## Copyright

Copyright and related rights waived via [CC0](../LICENSE).