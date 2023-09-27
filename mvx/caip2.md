---
namespace-identifier: mvx-caip2
title: MultiversX Namespace - Chains
author: MultiversX Team <contact@multiversx.com>
discussions-to: https://github.com/ChainAgnostic/namespaces/issues/89
status: Draft
type: Standard
created: 2023-09-11
requires: ["CAIP-2"]
---

# CAIP-2

_For context, see the [CAIP-2][] specification._

## Abstract

In CAIP-2 a general blockchain identification scheme is defined. This is the
profile of CAIP-2 specific to the MultiversX network.

### MultiversX Namespace

The namespace `mvx` refers to the wider MultiversX ecosystem.

## Rationale

MultiversX consists of multiple networks: a production network (Mainnet), a development testing network (Devnet)
and a testing network (Testnet).

## Syntax

An identifier for an MultiversX chain consists of the namespace prefix "mvx:"
followed by the appropriate `chainId` corresponding to that chain.

### Reference Definition

The reference for each MultiversX chain is identical to its native representation in the MultiversX ecosystem:
`1` for `Mainnet`, `D` for `Devnet`, `T` for `Testnet`

### Resolution Method

To resolve a blockchain reference for the MultiversX namespace, you can query the `network/config` endpoint on either the [lower level layer](https://gateway.multiversx.com) or the public [higher level layer](https://api.multiversx.com) that uses the gateway level underneath.

```jsonc
// Request
curl -X GET "https://api.multiversx.com/network/config" -H "accept: application/json"

// Response (formatted)
{
  "data": {
    "config": {
      "erd_chain_id": "1",
     // ... other fields
    }
  },
  "code": "successful"
}
```

The response will return a JSON object which will include the network configuration information and
the `erd_chain_id` defined above can be retrieved from the `config` property of the
response object.
This can be used directly as the `reference` section of a CAIP-2 or CAIP-10.

## Backwards Compatibility

Not applicable.

## Test Cases

```
This is a list of manually composed examples

# MultiversX Mainnet
mvx:1

# MultiversX Devnet
mvx:D

# MultiversX Testnet
mvx:T
```

## References

- [MultiversX Constants](https://docs.multiversx.com/developers/constants)
- [MultiversX REST API](https://docs.multiversx.com/sdk-and-tools/rest-api)
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md)

## Rights

Copyright and related rights waived via CC0.
