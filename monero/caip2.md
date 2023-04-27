---
namespace-identifier: monero-caip2
title: Monero - Chains
author: silverpill (@silverpill)
discussions-to: https://github.com/ChainAgnostic/namespaces/issues/41
status: Draft
type: Informational
created: 2023-04-27
requires: ["CAIP-2"]
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

CAIP-2 defines a way to identify a blockchain. Monero blockchain, its forks and testnets can be uniquely identified by their genesis blocks.

## Syntax

Monero chain ID is a hash of its genesis block, truncated to the first 32 characters.

### Resolution Mechanics

To obtain the genesis block hash, make a JSON-RPC request to the Monero daemon with method [get_block_header_by_height].

Request:

```json
{
  "jsonrpc": "2.0",
  "id": "0",
  "method": "get_block_header_by_height",
  "params": {
    "height": 0
  }
}
```

Response example (Monero mainnet):

```json
{
  "id": "0",
  "jsonrpc": "2.0",
  "result": {
    "block_header": {
      "block_size": 80,
      "block_weight": 80,
      "cumulative_difficulty": 1,
      "cumulative_difficulty_top64": 0,
      "depth": 2873685,
      "difficulty": 1,
      "difficulty_top64": 0,
      "hash": "418015bb9ae982a1975da7d79277c2705727a56894ba0fb246adaabb1f4632e3",
      "height": 0,
      "long_term_weight": 80,
      "major_version": 1,
      "miner_tx_hash": "c88ce9783b4f11190d7b9c17a69c1c52200f9faaee8e98dd07e6811175177139",
      "minor_version": 0,
      "nonce": 10000,
      "num_txes": 0,
      "orphan_status": false,
      "pow_hash": "",
      "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",
      "reward": 17592186044415,
      "timestamp": 0,
      "wide_cumulative_difficulty": "0x1",
      "wide_difficulty": "0x1"
    },
    "credits": 0,
    "status": "OK",
    "top_hash": "",
    "untrusted": false
  }
}
```

## Test Cases

This is a list of manually composed examples:

```
# Monero mainnet
monero:418015bb9ae982a1975da7d79277c270

# Monero stagenet
monero:76ee3cc98646292206cd3e86f74d88b4

# Monero testnet
monero:48ca7cd3c8de5b6a4d53d2861fbdaedc

# Wownero mainnet
monero:a3fd635dd5cb55700317783469ba749b
```

## Additional Considerations

Private testnet (also known as **regtest** or **fakechain**) has the same genesis block hash as Monero mainnet.
To avoid conflicts, implementers should use chain ID `monero:00000000000000000000000000000000` to identify this chain.

## References

- [Monero Networks][]

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[get_block_header_by_height]: https://www.getmonero.org/resources/developer-guides/daemon-rpc.html#get_block_header_by_height
[Monero Networks]: https://monerodocs.org/infrastructure/networks/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
