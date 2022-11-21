---
namespace-identifier: starknet-caip2
title: StarkNet Namespace - Chains
author: Argent Labs
discussions-to: 
status: Draft
type: Standard
created: 2022-11-18
updated: 2022-11-18
requires: CAIP-2
supersedes: CAIP-5
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

### Rationale / Syntax

The namespace `starknet` refers to the StarkNet Layer 2 on Ethereum.

StarkNet currently represents its chains with string identifiers such as 
`SN_MAIN` and `SN_GOERLI`. They also have field element representations which
are not worth discussing in this specification.

### Resolution Method

To resolve a reference for the StarkNet namespace, make a JSON-RPC
request to a StarkNet Pathfinder node with method `starknet_chainId`, for example:

```python
import requests

response = requests.post(
  url=f"https://starknet-goerli.infura.io/v3/{API_KEY}",
  json={"jsonrpc": "2.0", "method": "starknet_chainId", "params": [], "id": 1},
)

hex_chain_id = response.json()["result"]              # "0x534e5f474f45524c49"
chain_id = bytes.fromhex(hex_chain_id[2:]).decode()   # "SN_GOERLI"
```

The response will return a base-16-encoded field element that should be converted to
a string to format a StarkNet-compatible reference.

## Test Cases

This is a list of manually composed examples:

```
# StarkNet mainnet alpha
starknet:SN_MAIN

# StarkNet goerli alpha
starknet:SN_GOERLI
```

## References

- [Transaction structure][]: StarkNet's documentation on chainIDs used in transaction.
- [Making requests][]: Infura's documentation on how to call their Ethereum-like RPC endpoints.

[Transaction structure]: https://docs.starknet.io/documentation/develop/Blocks/transactions/#chain-id
[Making requests]: https://docs.infura.io/infura/networks/starknet/make-requests
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-21]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-21.md
[CAIP-22]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-22.md

## Rights

Copyright and related rights waived via CC0.