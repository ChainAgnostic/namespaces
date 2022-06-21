---
namespace-identifier: stacks-caip2
title: Stacks Namespace - Chains
author: Léo Pradel @pradel, Greg Ogunyanwo @gregogun
discussions-to: https://forum.stacks.org/t/caip-2-and-caip-10-stacks-specification/13290
status: Draft
type: Standard
created: 2022-06-07
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for Stacks. The chain ID is used as a way to mitigate
replay attacks on different Stacks chains, as it is included in the transaction encoding.
Stacks mainnet runs on bitcoin mainnet and testnet runs on bitcoin testnet3 .

## Syntax

For reference, the format of reference currently specified in SIP-005 is an
unsigned integer in decimal representation. The unsigned integer is represented
as a 32-bit unsigned integer with a maximum value of 2^32-1. 

### Resolution Method

To resolve a blockchain reference for the stacks namespace, make an API call
request to a blockchain node on the route `/v2/info`, the response will contain the
`network_id` field. For example:

```
{
  "id": 1,
  "network_id": 1,
  "server_version": "stacks-node 2.05.0.2.0 (develop:4641001+, release build, linux [x86_64])",
  // ... other fields
}
```

## Test Cases

This is a list of manually composed examples

```
# Stacks mainnet
stacks:1

# Stacks testnet
stacks:2147483648
```

## References

- [SIP-005][]
- [API documentation][]

[SIP-005][https://github.com/stacksgov/sips/blob/main/sips/sip-005/sip-005-blocks-and-transactions.md]
[API documentation][https://hirosystems.github.io/stacks-blockchain-api/#operation/get_core_api_info]
[CAIP-2][https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md]

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
