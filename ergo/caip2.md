---
namespace-identifier: ergo-caip2
title: Ergo Blockchain ID Specification
author: Yuriy Gagarin (@gagarin55)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/98
status: Draft
type: Standard
created: 2023-11-02
updated: 2023-11-09
---


## Abstract

In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for Ergo network.


## Specification

Blockchains in the "ergo" namespace are identified by their chain ID.

Chain ID is 32-character prefix from the hash of the genesis block of a given chain, in lowercase hex representation.


### Syntax

The `chain_id` is a case-sensitive string in the form

```
chain_id:    namespace + ":" + reference
namespace:   ergo
reference:   32-character prefix from the hash of the genesis block
```

### Resolution method

One can resolve chain ID by request `info` method on Ergo node API (see [RPC Endpoints][]):
```
curl https://node.ergo.watch/info
```

JSON Response contains `genesisBlockId` field:
```
{
...
  "genesisBlockId" : "b0244dfc267baca974a4caee06120321562784303a8a688976ae56170e4d175b",
...
}
```
So chain ID for Mainnet is `b0244dfc267baca974a4caee06120321`.


## Test Cases

This is a list of manually composed examples

```
# Ergo mainnet
ergo:b0244dfc267baca974a4caee06120321

# Ergo testnet
ergo:e7553c9a716bb3983ac8b0c21689a1f3

```

## References
- [Address][] - Address Encoding scheme on Ergo blockchain
- [RPC Endpoints][] - Ergo full node RPC API

[Address]:https://docs.ergoplatform.com/assets/py/Ergo_Address_Encoding/
[RPC Endpoints]:https://docs.ergoplatform.com/node/swagger/


## Copyright

Copyright and related rights waived via [CC0](../LICENSE).