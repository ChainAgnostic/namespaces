---
namespace-identifier: TVM
title: TVM Ecosystem
author: Lev Antropov(@levantropov), Vitaly Gritsay(@vvismaster)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/52/
status: Draft
type: Informational
created: 2023-03-22
updated: 2023-03-22
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

Networks using TVM do not have a single, commonly accepted standard for
identifying chains with human-readable strings, but the core node runtime
identifies chains by an integer between -2147483648 and 2147483648 (2^31). This
integer is present in each block of each chain, in the property `global_id`.
These work well as `chain_id` values for composing [CAIP-2][] and other
chain-id-qualified CASA schemes.

At time of writing there is not a central registry for avoiding `global_id`
conflicts or for mapping `global_id`s to public endpoints; instead, implementers
should seek chain and node information each chain's documentation (see links
section below for examples). 

```
The name of the chain is built according to the following rule:
tvm:<global_id>
```

## Syntax

Since `global_id`s can only be integers between -2147483648 and 2147483648, they
are easy to validate numerically. A simple regular expression for validating as
a string so would be:
`[-]?[0-9]{1-10}`

### Resolution Mechanics

You can confirm which chain a given node is running by sending a GraphQL request
to a node on that network, requesting only the "global_id" property of any
block.  See, for example:

```
// Using the GraphQL endpoint of Everscale mainnet:
// https://dapp01.itgold.io/graphql 

// Request
query{
  blocks(
    limit: 1
  ){
    global_id
  }
}

// Response
{
  "data": {
    "blocks": [
      {
        "global_id": 42
      }
    ]
  }
}

// Using the GraphQL endpoint of TON mainnet:
// https://dton.io/graphql

// Request
{
  blocks(page: 0, page_size: 1) {
    global_id
  }
}

// Responce
{
  "data": {
    "blocks": [
      {
        "global_id": -239
      }
    ]
  }
}
```

## Test Cases

This is a list of manually composed examples:

```
# Everscale mainnet (global id = 42)
tvm:42

# TON mainnet (global id = -239)
tvm:-239
```

## References
* [Everscale Blockchain](https://docs.everscale.network)
* [Everscale GraphQL](https://dapp01.itgold.io/graphql)
* [TON Blockchain](https://ton.org)
* [TON GraphQL](https://dton.io/graphql)

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
