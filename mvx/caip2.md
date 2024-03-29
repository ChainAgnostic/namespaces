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

In [CAIP-2][] a general blockchain identification scheme is defined. 
This is the implementation of CAIP-2 for the MultiversX network.

### MultiversX Namespace

The namespace `mvx` refers to the wider MultiversX ecosystem.

## Rationale

MultiversX consists of multiple networks: a production network (Mainnet), a development testing network (Devnet)
and a testing network (Testnet). More may be canonically addressed in the future.

## Syntax

An identifier for an MultiversX chain consists of the namespace prefix "mvx:"
followed by the chain's `chainId`.

### Reference Definition

The reference to the MultiversX chain is identical the MultiversX community's native one-character representation for each chain:
`1` for `Mainnet`, 
`D` for `Devnet`, or
`T` for `Testnet`

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

- [MultiversX Constants][] is where chainIds in their native, one-character representation are canonically published to date by the community
- [MultiversX REST API][] 
- [MultiversX Specifications][]
- [Integrators Guide][] 

[MultiversX Docs]: https://docs.multiversx.com/
[MultiversX Specifications]: https://github.com/multiversx/mx-specs
[MultiversX Constants]: https://docs.multiversx.com/developers/constants
[MultiversX governance]: https://agora.multiversx.com/c/governance/9
[MultiversX REST API]: https://docs.multiversx.com/sdk-and-tools/rest-api
[Integrators Guide]: https://docs.multiversx.com/integrators/overview
[BIP_0173]: https://en.bitcoin.it/wiki/BIP_0173
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md

## Rights

Copyright and related rights waived via CC0.
