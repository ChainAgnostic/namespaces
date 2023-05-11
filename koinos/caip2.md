---
namespace-identifier: koinos-caip2
title: Koinos Namespace - Chains
author: Roamin (@roaminro)
status: Draft
type: Standard
created: 2023-04-10
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Abstract

In [CAIP-2][], a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for networks that are based on the Koinos Blockchain Framework.

### Koinos Namespace

The namespace "koinos" refers to the wider Koinos Blockchain Framework ecosystem.

## Rationale

Koinos consists of multiple networks: a production network (Mainnet) and a
testing network (TestNet). Each network has a unique chain id that can be used to identify it.

An identifier for a Koinos chain consists of the namespace prefix "koinos:"
followed by a truncated form of the chain id.

## Syntax

Due to length and character limitations of CAIP-2 reference identifiers
(references must adhere to `[-_a-zA-Z0-9]{1,32}`), the chain id of a Koinos chain cannot be used
directly as a reference.

Instead, only the first 32 characters of the URL-safe base64-encoding chain id will be used.

### Resolution Method

To resolve the chain id for a Koinos chain, a GET request can be
made to a Koinos node using the JSON-RPC method `chain.get_chain_id`. This will return
a JSON object with the key `chain_id`, whose value is the base64-url chain id of the current chain.

For example:

```jsonc
// Request
curl -d '{"jsonrpc":"2.0", "method":"chain.get_chain_id", "params":{}, "id":0}' https://api.koinos.io

// Response (formatted)
{
  "jsonrpc": "2.0",
  "result": {
    "chain_id": "EiBZK_GGVP0H_fXVAM3j6EAuz3-B-l3ejxRSewi7qIBfSA=="
  },
  "id": 0
}
```

Note that the `chain_id` value returned must be substringed to the first 32 characters.

For example, this JavaScript code transforms the above response into a CAIP-2 identifier:

```javascript
// For the Koinos mainnet
const chainId = "EiBZK_GGVP0H_fXVAM3j6EAuz3-B-l3ejxRSewi7qIBfSA==";
const prefix = chainId.substring(0, 32);
const identifier = "koinos:" + prefix;

console.log(identifier); // prints "koinos:EiBZK_GGVP0H_fXVAM3j6EAuz3-B-l3e"

```

## Backwards Compatibility

Not applicable.

## Test Cases

```
# Koinos Mainnet (chain id= EiBZK_GGVP0H_fXVAM3j6EAuz3-B-l3ejxRSewi7qIBfSA== )
koinos:EiBZK_GGVP0H_fXVAM3j6EAuz3-B-l3e

# Koinos Harbinger (Testnet; chain id= EiAAKqFi-puoXnuJTdn7qBGGJa8yd-dcS2P0ciODe4wupQ== )
koinos:EiAAKqFi-puoXnuJTdn7qBGGJa8yd-dc
```

## References

- [Koinos documentation](https://docs.koinos.io/)
- [Koinos JSON-RPC](https://docs.koinos.io/rpc/json-rpc.html)
- [CAIP-2][]

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Rights

Copyright and related rights waived via CC0.
