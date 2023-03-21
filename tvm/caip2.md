---
namespace-identifier: TVM

title: TVM Ecosystem

author: Lev Antropov(@levantropov), Vitaly Gritsay(@vvismaster)

discussions-to: https://github.com/ChainAgnostic/namespaces/pull/52/

status: Draft

type: Informational

created: 2023-01-23

updated:

replaces:
---

# CAIP-2

*For context, see the [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-X.md) specification.*

## Rationale
Networks using TVM do not have a single, commonly accepted standard for identifying chains, so chains will be named according to their generally accepted names.

Based on the above, the syntax for constructing a namespace is a conditional arrangement, necessary rather for third-party projects (for example, WalletConnect, etc).

```
The name of the chain is built according to the following rule:
tvm:<network_name>_<chain_name>

network_name: blockchain network name, for example: `everscale` or `ton`
chain_name: common chain name, eg 'mainnet'
```

## Semantics and Syntax
### Everscale
The names of the chains will be as follows
```
tvm:everscale_mainnet
tvm:everscale_devnet
```
#### Resolution Mechanics on Everscale
You can check which network the dApp is running on by sending a request (https://dapp01.itgold.io/graphql):

```
// Request
query{
  blocks(
    limit: 1
  ){
    global_id
  }
}

// Responce
{
  "data": {
    "blocks": [
      {
        "global_id": 42
      }
    ]
  }
}

Where 42 is the Everscale Mainnet Global ID
```

### TON
The names of the chains will be as follows
```
tvm:ton_mainnet
tvm:ton_devnet
```
#### Resolution Mechanics on TON
You can check which network the dApp is running on by sending a request (https://dton.io/graphql):
```
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

Where -239 is the TON Mainnet Global ID
```
## Test Cases
```
This is a list of manually composed examples

# Everscale mainnet (global id = 42)
tvm:everscale_mainnet

# TON mainnet (global id = -239)
tvm:ton_mainnet
```
## References
* [Everscale Blockchain](https://docs.everscale.network)
* [Everscale GraphQL](https://dapp01.itgold.io/graphql)
* [TON Blockchain](https://ton.org)
* [TON GraphQL](https://dton.io/graphql)

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
