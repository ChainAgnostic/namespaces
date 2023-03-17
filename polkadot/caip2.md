---
namespace-identifier: polkadot-caip2
title: Polkadot Namespace - Chains
author: [ "Pedro Gomes (@pedrouid)", "Joshua Mir (@joshua-mir)", "Shawn Tabrizi (@shawntabrizi)", "Juan Caballero (@bumblefudge)", "Antonio Antonino (@ntn-x2)" ]
discussions-to: https://github.com/ChainAgnostic/CAIPs/issues/13
status: Draft
type: Standard
created: 2020-04-01
updated: 2023-02-22
requires: CAIP-2
replaces: CAIP-13
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

The namespace is called "polkadot" to encompass all chains that implement the [Polkadot Host protocol][polkadot-protocol], allowing actors and entities that belong to a relay chain, independent "solo" chain, and L1-like "parachain" to be addressable.

The rationale behind the use of block hash from the genesis block stems from its usage in the Polkadot architecture in network and consensus.

## Syntax

The definition for this namespace will use the `genesis-hash` as an identifier for different Polkadot chains.
The format is a 32 character-long HEX string, without the `0x` prefix, representing the first half of the block 0 (genesis) hash for the given chain.

As CAIP-2 references for this namespace are 32-byte hashes in lowercase HEX, they can be validated with the simple regular expression: `[0-9a-f]{32}`

### Resolution Method

There is no index or registry that maps genesis hashes to networks, and defining such a mechanism for doing so is out of the scope for this specification.
This specification assumes that consumers of this class of CAIP-2 identifiers are able to properly resolve them to the appropriate network.
This specification then defines how to verify that a given RPC node, reachable via a regular URL, belongs to a given Polkadot network.

Given the URL of a Polkadot network RPC node, make a JSON-RPC request to the node with method `chain_getBlockHash`, for example:

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
  "result": "0x91b171bb158e2d3848fa23a9f1c25182fb8e20313b2c1eb49219da7a70ce90c3"
}
```
The response will return as a value for the result a hash for the block with height 0 (i.e., genesis block).
The leading `0x` and the last 32 characters will need to be trimmed, such that the resulting string is a 32-character HEX string (i.e., 16 bytes) that represents the CAIP-2 identifier for the Polkadot network the RPC node is part of.

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```
# Polkadot relay chain
polkadot:91b171bb158e2d3848fa23a9f1c25182

# Kusama relay chain
polkadot:b0a8d493285c2df73290dfb7e61f870f

# KILT Spiritnet parachain on Polkadot
polkadot:a0453819cbf8b4df9423a5cd601f546c

# Karura parachain on Kusama
polkadot:baf5aabe40646d11f0ee8abbdc64f4a4

# Crust Network solo chain
polkadot:8b404e7ed8789d813982b9cb4c8b664c
```

## References

- [Polkadot documentation][]: Homepage for ecosystem-wide developer documentation
- [Polkadot public RPC endpoints][]: for dev/testing purposes
- [Polkadot subscan tool][]: A tool for transforming addresses according to [SS58][] across polkadot networks

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[polkadot-protocol]: https://wiki.polkadot.network/docs/learn-polkadot-host
[Polkadot documentation]: https://wiki.polkadot.network/
[Polkadot public RPC endpoints]: https://wiki.polkadot.network/docs/maintain-endpoints
[Polkadot subscan tool]: https://polkadot.subscan.io/tools/ss58_transform?

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
