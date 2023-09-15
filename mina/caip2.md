---
namespace-identifier: mina-caip2
title: Mina Namespace - Chains
author: Mina Foundation
discussions-to: 
status: Draft
type: Standard
created: 2023-09-15
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Abstract

In CAIP-2 a general blockchain identification scheme is defined. This is the implementation of CAIP-2 for Mina network.

### Mina Namespace

The namespace "mina" refers to the wider Mina ecosystem.

## Rationale

Mina consists of multiple networks: a production network `mainnet`, a testing network `testnet` and networks where new features are trialed. Networks trialing new features are identified by a codename, for example `berkeley`. 

An identifier for a Mina chain consists of the namespace prefix "mina:" followed by human readable reference identifying each network. These identifiers may be extended to include codenames and prefixed to include the type of network. These names are separated by "-". 

The type of network will be:
- devnet, indicating a stable copy of the network used for developer testing.
- testnet, indicating a less stable copy of the network where new features can be deployed and tested. 

The names chosen above are taken from the signature schema's for each blockchain.

## Syntax

The blockchain namespace and blockchain identifiers will be in lowercase.

The human readable identifier for a network may be one of the following strings:

- `mainnet` 
- `testnet` 
- `devnet` 
- `berkeley`

The human readable identifiers above may be composed to add description using `-` as a separator.

See [Test Cases](#test-cases).

### Resolution Method

Use a graphQL query to obtain the identifier:

```
query MyQuery {
  networkID
}
```

The response will be:

```
{
  "data": {
    "networkID": "mina:mainnet"
  }
}
```

Use the value provided in the `networkID` field.

Click here for more information on the [Mina GraphQL API](https://docs.minaprotocol.com/node-developers/graphql-api)


## Backwards Compatibility

Not applicable.

## Test Cases

This is a list of manually composed examples

```
# Mina Mainnet
mina:mainnet

# Mina Devnet
mina:devnet

# Mina Testnet
mina:testnet

# Mina Berkeley 
mina:berkeley

# Mina Devnet Berkeley 
mina:devnet-berkeley

# Mina Testnet Berkeley 
mina:testnet-berkeley

```

## References

- [CAIP-2] https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
- [Mina Protocol Website] https://minaprotocol.com/
- [Mina Protocol Developer Documentation] https://docs.minaprotocol.com/
- [Mina Rosetta Implementation] https://docs.minaprotocol.com/node-operators/rosetta


## Rights

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
