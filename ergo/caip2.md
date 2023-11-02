---
caip: 2
title: Ergo Blockchain ID Specification
author: Yuriy Gagarin (@gagarin55)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/..
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
Chain ID is 8-bit unsigned integer in decimal representation.

### Syntax

The `chain_id` is a case-sensitive string in the form

```
chain_id:    namespace + ":" + reference
namespace:   ergo
reference:   8-bit unsigned integer
```

### Resolution method

## Rationale

The chain ID is specified as a one-byte unsigned integer.

For example, the chain ID of Mainnet is 0, for Testnet is 16.

There may also be other custom networks based on Ergo, but with a different
chain ID.

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