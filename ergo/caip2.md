---
caip: 2
title: Ergo Blockchain ID Specification
author: Yuriy Gagarin (@gagarin55)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/98
status: Draft
type: Standard
created: 2023-11-02
updated: 2023-11-02
---


## Abstract

In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for Ergo network.


## Specification

Blockchains in the "ergo" namespace are identified by their chain ID.

Chain ID is 8-bit unsigned integer in which lower 4 bits are zeros.

Possible values:
* Mainnet - 0 (in hex `0x00`)
* Testnet - 16 (in hex `0x10`)
* Testnet2 - 32 (in hex `0x20`)
...
* TestnetN - 240 in (hex `0xF0`)


### Syntax

The `chain_id` is a case-sensitive string in the form

```
chain_id:    namespace + ":" + reference
namespace:   ergo
reference:   8-bit unsigned integer in which lower 4 bits are zeros
```

### Resolution method
...TODO...

## Rationale

The chain ID is specified as a 8-bit in which lower 4 bits are zeros.

Because of [Address][] encoding scheme there is only $2^4$ possible blockchains in Ergo ecosystem.

So, the chain ID of Mainnet is 0, for Testnet is 16.

Chain ID is used in [Address][] generation. Therefore, addresses from one chain are invalid on another.

## Test Cases

This is a list of manually composed examples

```
# Ergo mainnet
ergo:0

# Ergo testnet
ergo:16

```

## References
- [Address][] - Address Encoding scheme on Ergo blockchain

[Address]:https://docs.ergoplatform.com/assets/py/Ergo_Address_Encoding/



## Copyright

Copyright and related rights waived via [CC0](../LICENSE).