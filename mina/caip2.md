---
namespace-identifier: mina-caip2
title: Mina Namespace - Chains
author: Mina Foundation
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/91
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

Mina consists of multiple networks: a production network `mainnet`, a testing network matching the production network `devnet`, a testing network for new features `testnet` and networks where new features are trialed.

Networks trialing new features are identified by a codename, for example `berkeley`. 

An identifier for a Mina chain consists of the namespace prefix "mina:" followed by human readable reference identifying each network. 
These identifiers may be extended to include codenames and prefixed to include the type of network. These names are separated by "-". 

The type of network may be:
- mainnet, the production network.
- devnet, indicating a stable copy of the network used for developer testing.
- testnet, indicating a less stable copy of the network where new features can be deployed and tested. 

The names chosen above are taken from the signature schema's for each blockchain and current network identifiers can be found in the documentation [here](https://docs2-git-major-upgrade-minadocs.vercel.app/node-operators)

## Syntax

The blockchain namespace and blockchain identifiers will be in lowercase [a-z] and contain no whitespaces and have a miximum length of 30 characters.

The human readable identifier for a network may be one of the following strings:

- `mainnet` 
- `testnet` 
- `devnet` 
- `berkeley`

Note that new human readable identifiers may be created for new networks by concatenating existing ones using `-` as a separator, i.e. `berkeley-testnet`. 

A regular expression for validating the above or any other theoretically possible Mina network identifier string (that fits under the CAIP-20 limit of 32 characters) can be defined as:

```
^mina:[a-z]{1,12}?(-[a-z]{1,12})?$
```

At time of writing the current recognized identifiers are the ones listed above and no canonical human-readable or machine-readable mapping has yet been published. In future, the Mina official docs will link to such a mapping once one is published.

See [Test Cases](#test-cases).

### Resolution Method

Use a graphQL query to obtain the identifier after connecting to a network:

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

Click here for more information on the [Mina GraphQL API][].

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

- [Mina Protocol Website][]
- [Mina Protocol Developer Documentation][]
- [Mina GraphQL API][] documentation
- [Mina Rosetta Implementation][] 

[CAIP-2]: https://ChainAgnostic.org/CAIPs/caip-2
[Mina GraphQL API]: https://docs.minaprotocol.com/node-developers/graphql-api
[Mina Protocol Website]: https://minaprotocol.com/
[Mina Protocol Developer Documentation]: https://docs.minaprotocol.com/
[Mina Rosetta Implementation]: https://docs.minaprotocol.com/node-operators/rosetta

## Rights

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
