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

The namespace is called "polkadot" to encompass all chains that implement the [Polkadot Host protocol][polkadot-protocol], allowing actors and entities that belong to a relaychain, independent "solo" chain, and L1-like "parachain" to be addressable.

The rationale behind the use of block hash from the genesis block stems from its usage in the Polkadot architecture in network and consensus.

## Syntax

The definition for this namespace will use the `genesis-hash` as an identifier for different Polkadot chains.
The format is a 32 character-long HEX string, without the `0x` prefix, representing the first half of the block 0 (genesis) hash for the given chain.

As CAIP-2 references for this namespace are 32-byte hashes in lowercase HEX, they can be validated with the simple regular expression: `[0-9a-f]{32}`

### Resolution Method

To resolve a blockchain reference for the Polkadot namespace, make a JSON-RPC request to the blockchain node with method `chain_getBlockHash`, for example:

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
The response will return as a value for the result a hash for the block with height 0 that should be sliced to its first 16 bytes (32 characters for base 16) to be CAIP-2/CAIP-10 compatible.

How the address for an RPC node for a given Polkadot-based network is retrieved is out of scope of this document.

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```
# Kusama
polkadot:b0a8d493285c2df73290dfb7e61f870f

# KILT Spiritnet
polkadot:411f057b9107718c9624d6aa4a3f23c1

# Edgeware
polkadot:742a2ca70c2fda6cee4f8df98d64c4c6

# Kulupu
polkadot:37e1f8125397a98630013a4dff89b54c
```

## References

- [Polkadot documentation][]: Homepage for ecosystem-wide developer documentation
- [Polkadot public RPC endpoints][]: for dev/testing purposes
- [Polkadot identity system][]: Introduction to on-chain identity registrars 
- [Polkadot address explainer][]: A quick overview of how network-specific, self-describing addresses can derive from the same private key
- [Polkadot subscan tool][]: A tool for transforming addresses according to [SS58][] across polkadot networks

[polkadot-protocol]: https://wiki.polkadot.network/docs/learn-polkadot-host
[Polkadot address explainer]: https://wiki.polkadot.network/docs/learn-account-advanced
[Polkadot identity system]: https://wiki.polkadot.network/docs/learn-identity
[Polkadot public RPC endpoints]: https://wiki.polkadot.network/docs/maintain-endpoints
[Polkadot documentation]: https://wiki.polkadot.network/
[Polkadot subscan tool]: https://polkadot.subscan.io/tools/ss58_transform?
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
