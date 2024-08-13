---
namespace-identifier: conflux-caip2
title: Conflux Namespace - Chains
author: iosh (@iosh)
discussions-to: <URL of PR, mailing list, etc>
status: Draft
type: Standard
created: 2024-08-09
requires: CAIP-2
---

# CAIP-2

_For context, see the [CAIP-2][] specification._

## Rationale

Conflux network(core space) consists of 2 networks: main network and testing network.
Private networks can also be created.

The main network has a network ID of 1029, represented by `cfx`. The test network has a network ID of 1, represented by `cfxtest`. Private networks are represented by `net[network ID]`.


## Syntax

A network id in the Conflux core space is defined as an unsigned integer ranging from 1 to 4294967295.

### Resolution Mechanics

To resolve the a network reference for a conflux network, POST a JSON-RPC request to the RPC endpoint of the blockchain node with path / for example:

```jsonc
// request
curl -X POST --data \
'{
    "method": "cfx_getStatus",
    "params": [],
    "jsonrpc": "2.0",
    "id": 1
}' \
-H "Content-Type: application/json" \
https://main.confluxrpc.com

// response

{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "bestHash": "0x4e5607b1c23124fad2c7e431f34ca52bc3e28e90df2e3733d0a50d64d4790693",
    "chainId": "0x405",
    "ethereumSpaceChainId": "0x406",
    "networkId": "0x405",
    "epochNumber": "0x6158f8d",
    "blockNumber": "0xeb54f08",
    "pendingTxNumber": "0xc9",
    "latestCheckpoint": "0x614b3a0",
    "latestConfirmed": "0x6158f6a",
    "latestState": "0x6158f89",
    "latestFinalized": "0x6158eb0"
  }
}

```

The response will return a JSON object which will include node status and the `networkId`, encoded in hexadecimal, of the current chain.

## Test Cases

```
# conflux mainnet
conflux:cfx

# conflux testnet
conflux:cfxtest

# private network
conflux:net2024

```

## References

- [CAIP-2][]
- [Conflux core space Docs][] The Conflux Core Space Docs
- [Conflux core space RPC endpoint][] Public available Conflux Core Space network RPC endpoints

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[Conflux core space Docs]: https://doc.confluxnetwork.org/docs/core/Overview
[Conflux core space RPC endpoint]: https://doc.confluxnetwork.org/docs/core/conflux_rpcs

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
