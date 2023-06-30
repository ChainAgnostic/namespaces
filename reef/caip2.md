---
namespace-identifier: reef-caip2
title: Reef Namespace - Chains
author: Boo 0x (@boo-0x)
status: Draft
type: Standard
created: 2023-06-30
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2](https://chainagnostic.org/CAIPs/caip-2) specification.*

## Rationale

The namespace is called "reef" to encompass all chains of the Reef ecosystem. This includes a production network and one or more test networks.

The rationale behind the use of block hash from the genesis block stems from its usage in the Reef architecture in network and consensus.

## Syntax

The definition for this namespace will use the `genesis-hash` as an identifier for different Reef chains.
The format is a 32 character-long HEX string, without the `0x` prefix, representing the first half of the block 0 (genesis) hash for the given chain.

As CAIP-2 references for this namespace are 32-byte hashes in lowercase HEX, they can be validated with the simple regular expression: `[0-9a-f]{32}`

### Resolution Method

There is no index or registry that maps genesis hashes to networks, and defining such a mechanism for doing so is out of the scope for this specification.
This specification assumes that consumers of this class of CAIP-2 identifiers are able to properly resolve them to the appropriate network.
This specification then defines how to verify that a given RPC node, reachable via a regular URL, belongs to a given Reef network.

Given the URL of a Reef network RPC node, make a JSON-RPC request to the node with method `chain_getBlockHash`, for example:

```jsonc
// Request
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "chain_getBlockHash",
  "params": [0]
}

// Response
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": "0x7834781d38e4798d548e34ec947d19deea29df148a7bf32484b7b24dacf8d4b7"
}
```
The response will return as a value for the result a hash for the block with height 0 (i.e., genesis block).
The leading `0x` and the last 32 characters will need to be trimmed, such that the resulting string is a 32-character HEX string (i.e., 16 bytes) that represents the CAIP-2 identifier for the Reef network the RPC node is part of.

## Test Cases

This is a list of manually composed examples

```
# Reef Mainnet
reef:7834781d38e4798d548e34ec947d19de

# Reef Scuba testnet
reef:b414a8602b2251fa538d38a932239150
     
## References[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
- [Reef Chain](https://reef.io/)
- [Docs](https://docs.reef.io/)
- [GitHub](https://github.com/reef-chain)

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
