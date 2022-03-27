---
namespace-identifier: polkadot-caip2
title: Polkadot Namespace - Chains
author: ["Pedro Gomes (@pedrouid)", "Joshua Mir (@joshua-mir)", "Shawn Tabrizi (@shawntabrizi)", "Juan Caballero (@bumblefudge)"]
discussions-to: https://github.com/ChainAgnostic/CAIPs/issues/13
status: Draft
type: Standard
created: 2020-04-01
updated: 2022-03-27
requires: CAIP-2
replaces: CAIP-13
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

The namespace is called "polkadot" to refer to Polkadot-like "parachains,"
parallel and independent Layer 1s coordinated by the Polkadot relay chains.

The rationale behind the use of block hash from the genesis block stems from its
usage in the Polkadot architecture in network and consensus.

## Syntax

The definition for this namespace will use the `genesis-hash` as an indentifier
for different Polkadot chains. The format is a 32 character prefix of the block
hash (lower case SHA256 hex).

As CAIP-2 references for this namespace are 32-byte SHA256 hashes in lowercase
hex, they can be validated with the simple regular expression: `[0-9a-f]{32}`

### Resolution Method

To resolve a blockchain reference for the Polkadot namespace, make a JSON-RPC
request to the blockchain node with method `chain_getBlockHash`, for example:

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
The response will return as a value for the result a hash for the block with
height 0 that should be sliced to its first 16 bytes (32 characters for base 16)
to be CAIP-2/CAIP-10 compatible.

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```
# Kusama
polkadot:b0a8d493285c2df73290dfb7e61f870f

# Edgeware
polkadot:742a2ca70c2fda6cee4f8df98d64c4c6

# Kulupu
polkadot:37e1f8125397a98630013a4dff89b54c
```

## References

- [Polkadot documentation][]: Homepage for ecosystem-wide developer documentation
- [Polkadot-ENS tutorial][]: A tutorial for native Kusama address support in the ENS front-end
- [Polkadot public RPC endpoints][]: for dev/testing purposes
- [Polkadot identity system][]: Introduction to on-chain identity registrars 
- [Polkadot address explainer][]: A quick overview of how network-specific,
      self-describing addresses can derive from the same private key
- [Polkadot subscan tool][]: A tool for transforming addresses according to SS58 across polkadot networks

[Polkadot address explainer]: https://www.quora.com/How-do-different-wallet-addresses-work-on-Polkadot-and-Kusama
[Polkadot identity system]: https://wiki.polkadot.network/docs/learn-identity
[Polkadot public RPC endpoints]: https://wiki.polkadot.network/docs/maintain-endpoints
[Polkadot documentation]: https://wiki.polkadot.network/
[Polkadot subscan tool]: https://polkadot.subscan.io/tools/ss58_transform?
[Polkadot-ENS tutorial]: https://wiki.polkadot.network/docs/ens
[SS58]: https://docs.substrate.io/v3/advanced/ss58/
[SS58 registry]: https://github.com/paritytech/ss58-registry/blob/main/ss58-registry.json
[multiaddress]: https://github.com/multiformats/multiaddr#specification
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-21]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-21.md
[CAIP-22]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-22.md
[EIP155]: https://eips.ethereum.org/EIPS/eip-155
[ERC20]: https://eips.ethereum.org/EIPS/eip-20
[ERC721]: https://eips.ethereum.org/EIPS/eip-721

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).