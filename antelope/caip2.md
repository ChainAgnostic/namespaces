---
namespace-identifier: antelope-caip2
title: Antelope Namespace - Chains
author: Aaron Caswell (@porkchop)
status: Draft
type: Standard
created: 2023-09-19
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Abstract

In [CAIP-2][], a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for networks that are based on the Antelope Blockchain Platform.

### Antelope Namespace

The namespace "antelope" refers to the wider Antelope Blockchain Platform ecosystem.

## Rationale

Antelope consists of multiple networks: EOS production network (EOS Mainnet), EOS
testing network (EOS Testnet), WAX production network (WAX Mainnet), WAX
testing network (WAX Testnet), and more. Each network has a unique chain id that
can be used to identify it.

An identifier for an Antelope chain consists of the namespace prefix "antelope:"
followed by a truncated form of the chain id.

## Syntax

The Chain ID, or rather the `chain_id` as defined by Antelope, is always a
64-character hexadecimal string containing the SHA256 hash of the genesis state
of a given chain. In order to fit the CAIP-2 reference format, a 32
character prefix of the Chain ID is used; note, however, that the longer
original will be needed to authorize new transactions.

### Resolution Method

To resolve the chain id for an Antelope chain, a GET or POST request can be
made to an Antelope node using the JSON-RPC method [/v1/chain/get_info][]. This will
return a JSON object with the key `chain_id`, whose value is the SHA256 of the
genesis state of the current chain. The full chain id is required for authorizing
transactions on said chain.


For example:

```jsonc
// Request
curl https://wax.greymass.com/v1/chain/get_info | jq

// Response (formatted)
{
  "server_version": "e46acfd8",
  "chain_id": "1064487b3cd1a897ce03ae5b6a865651747e2e152090f99c1d19d44e01aea5a4",
  "head_block_num": 267371511,
  "last_irreversible_block_num": 267371184,
  "last_irreversible_block_id": "0fefc2b09338c1d7b33d8f7c9dfe3880106b2862abe3ec3fcd4a093f16db74cf",
  "head_block_id": "0fefc3f7b918ac83c6b9bd83052557ba7ec2d1d4113158e3834aa38869863edf",
  "head_block_time": "2023-09-19T20:55:37.000",
  "head_block_producer": "alohaeosprod",
  "virtual_block_cpu_limit": 10833331,
  "virtual_block_net_limit": 1048576000,
  "block_cpu_limit": 200000,
  "block_net_limit": 1048576,
  "server_version_string": "v3.2.3wax01-hotfix",
  "fork_db_head_block_num": 267371511,
  "fork_db_head_block_id": "0fefc3f7b918ac83c6b9bd83052557ba7ec2d1d4113158e3834aa38869863edf",
  "server_full_version_string": "v3.2.3wax01-hotfix-e46acfd8c35935371f908e8f3ca3d33e32220a83-dirty",
  "total_cpu_weight": "38295019677381184",
  "total_net_weight": "149904335281667264",
  "earliest_available_block_num": 267198264,
  "last_irreversible_block_time": "2023-09-19T20:52:53.500"
}
```

Note that the `chain_id` value returned must be substringed to the first 32 characters.

For example, this JavaScript code transforms the above response into a CAIP-2 identifier:

```javascript
// For the WAX mainnet
const chainId = "1064487b3cd1a897ce03ae5b6a865651747e2e152090f99c1d19d44e01aea5a4";
const prefix = chainId.substring(0, 32);
const identifier = "antelope:" + prefix;

console.log(identifier); // prints "antelope:1064487b3cd1a897ce03ae5b6a865651"

```

## Backwards Compatibility

Not applicable.

## Test Cases

```
# EOS Mainnet
// /v1/chain/get_info --> chain_id=aca376f206b8fc25a6ed44dbdc66547c36c6c33e3a119ffbeaef943642f0e906
antelope:aca376f206b8fc25a6ed44dbdc66547c

# Jungle Testnet
// /v1/chain/get_info --> chain_id=e70aaab8997e1dfce58fbfac80cbbb8fecec7b99cf982a9444273cbc64c41473
antelope:e70aaab8997e1dfce58fbfac80cbbb8f

# WAX Mainnet
// /v1/chain/get_info --> chain_id=1064487b3cd1a897ce03ae5b6a865651747e2e152090f99c1d19d44e01aea5a4
antelope:1064487b3cd1a897ce03ae5b6a865651

# WAX Testnet
// /v1/chain/get_info --> chain_id=f16b1833c747c43682f4386fca9cbb327929334a762755ebec17f6f23c9b8a12
antelope:f16b1833c747c43682f4386fca9cbb32
```

## References

- [Antelope documentation](https://docs.eosnetwork.com/)
- [Antelope JSON-RPC](https://docs.eosnetwork.com/apis/leap/latest/)
- [CAIP-2][]

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[/v1/chain/get_info]: https://docs.eosnetwork.com/apis/leap/latest/chain.api#operation/get_block_info

## Rights

Copyright and related rights waived via CC0.
