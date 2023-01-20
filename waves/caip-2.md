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
reference:   integer in the range [-128..127]
```

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
waves:87

# Waves Testnet
waves:84

# Waves Stagenet
waves:83

# Waves custom net launched with the private node Docker image https://hub.docker.com/r/wavesplatform/waves-private-node
waves:82
```

## Links

- [About Chain ID in Waves Documentation](https://docs.waves.tech/en/blockchain/blockchain-network/#chain-id)
- [About binary format of blockchain entities](https://docs.waves.tech/en/blockchain/binary-format/)

## Copyright

Copyright and related rights waived via [CC0](../LICENSE).