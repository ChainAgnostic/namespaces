---
namespace-identifier: solana-caip2
title: Solana Namespace - Chains
author: Antoine Herzog (@antoineherzog), Josh Hundley (@oJshua)
discussions-to: https://github.com/ChainAgnostic/CAIPs/pull/60
status: Draft
type: Standard
created: 2021-08-03
updated: 2023-03-27
requires: CAIP-2
replaces: CAIP-28
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for Solana. Blockchains in the "solana" namespace are
validated by their genesis hash; each blockchain is maintained by a
"[Cluster][]" of nodes, with its own gossip entrypoint and other endpoints.
These genesis hashes require no transformations to be used as conformant CAIP-2
references aside from concatenating their first 32 characters.

## Syntax

The namespace "solana" refers to the Solana open-source blockchain platform.

### Reference Definition

The definition for this namespace will use the `genesisHash` as an identifier
for different Solana chains. The method for calculating the chain ID is as
follows with pseudo-code:

```bash
truncate(genesisHash, 32)
```

### Resolution Method

To resolve a blockchain reference for the Solana namespace, make a JSON-RPC
request to the [RPC Endpoints][] of a blockchain node with method
`getGenesisHash`, for example:

```jsonc
// Request
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "getGenesisHash"
}

// Response
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": "5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d"
}
```

The response will return as a value for the result a 44-character
[Base58btc][]-encoded hash for the block with height 0 that should be truncated to
its first 32 characters to be [CAIP-2][] compatible.

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```bash
# Solana Mainnet
solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp

# Solana Devnet
solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1

# Solana Testnet
solana:4uhcVJyU9pJkvQyS88uRDiswHXSCkY3z

```

## References

- [RPC Endpoints][] - RPC reference in Solana official documentation
- [Solana core][] rust crate on crates.io
- [Base58btc][] encoding "alphabet" (i.e. character-set)

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[Cluster]: https://docs.solana.com/clusters
[RPC Endpoints]: https://docs.solana.com/cluster/rpc-endpoints
[Solana core]: https://crates.io/crates/solana-program/
[base58btc]: https://en.bitcoin.it/wiki/Base58Check_encoding#Base58_symbol_chart

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
