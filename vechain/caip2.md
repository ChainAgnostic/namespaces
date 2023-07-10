---
namespace-identifier: vechain-caip2
title: Vechain Namespace
author: Darren Kelly (@darrenvechain))
status: Draft
type: Standard
created: 2023-07-10
updated: 2023-07-10
requires: CAIP-2
---

# CAIP-2
*For context, see the [CAIP-2][] specification.*


## Abstract

In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for VechainThor network.

### Vechain Namespace

The namespace "vechain" refers to the wider Vechain ecosystem.

## Rationale

Vechain consists of 2 networks: a production network and a testing network. Private networks can also be created to aid in local development. Each network has a unique genesis ID that can be used to identify it.

An identifier for a VechainThor chain consists of the namespace prefix "vechain:"
followed by a truncated form of the chain's genesis ID.

## Syntax

Due to length and character limitations of CAIP-2 reference identifiers
(references must adhere to `[-_a-zA-Z0-9]{1,32}`), the commonly referenced
standard genesis ID of a vechain cannot be used
directly as a reference.

Instead, one change must be made:
1. Only the last 32 characters of the genesis ID will be used

### Resolution Method

To resolve the blockchain reference for VechainThor chain, a GET request can be
made to an VechainThor node on the path `blocks/0`. This will return
a JSON object with the the key `id`, whose value is the hex encoded ID of the current chain.

For example:

```jsonc
// Request
curl -H "https://mainnet.vechain.org/blocks/0"

// Response (formatted)
{
  "number": 0,
  "id": "0x00000000851caf3cfdb6e899cf5958bfb1ac3413d346d43539627e6be7ec1b4a",
  "size": 170,
  "parentID": "0xffffffff53616c757465202620526573706563742c20457468657265756d2100"
}
```

```javascript
const genesisId = "0x00000000851caf3cfdb6e899cf5958bfb1ac3413d346d43539627e6be7ec1b4a";
//get the last 32 characters of the genesis ID
const truncatedId = genesisId.slice(-32);
const identifier = "vechain:" + truncatedId;

console.log(identifier); // prints "vechain:b1ac3413d346d43539627e6be7ec1b4a"
```

## Test Cases

```
# VechainThor MainNet has the genesis ID 0x00000000851caf3cfdb6e899cf5958bfb1ac3413d346d43539627e6be7ec1b4a
vechain:b1ac3413d346d43539627e6be7ec1b4a

# VechainThor TestNet has the genesis ID 0x000000000b2bce3c70bc649a02749e8687721b09ed2e15997f466536b20bb127
vechain:87721b09ed2e15997f466536b20bb127
```

## References

- [VechainThor REST API](https://docs.vechain.org/thor/thorest-api)
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md)

## Rights

Copyright and related rights waived via CC0.