---
namespace-identifier: movement-caip2
title: Movement Namespace - Chains
author: Andy Golay (@andygolay)
discussions-to:
status: Draft
type: Standard
created: 2026-03-23
updated: 2026-03-23
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for Movement. Blockchains in the "movement" namespace are
identified by their numeric `chain_id`, assigned at genesis. Each network is
maintained by a set of validators with its own REST API endpoints. These chain
IDs require no transformations to be used as conformant CAIP-2 references.

## Syntax

The namespace "movement" refers to the Movement Network blockchain platform.

### Reference Definition

The definition for this namespace will use the `chain_id` as an identifier
for different Movement chains. The chain ID is a positive integer assigned at
genesis:

| Network | Chain ID |
|---------|----------|
| Mainnet | 126      |
| Testnet | 250      |

### Resolution Method

To resolve a blockchain reference for the Movement namespace, make an HTTP GET
request to the [REST API][] of a fullnode, for example:

```bash
# Mainnet
curl https://mainnet.movementnetwork.xyz/v1

# Testnet
curl https://testnet.movementnetwork.xyz/v1
```

```jsonc
// Mainnet Response
{
  "chain_id": 126,
  "epoch": "10777734",
  "ledger_version": "101649253",
  "oldest_ledger_version": "0",
  "ledger_timestamp": "1774318053802368",
  "node_role": "full_node",
  "oldest_block_height": "0",
  "block_height": "40497312",
  "git_hash": "f24a5bc"
}
```

```jsonc
// Testnet Response
{
  "chain_id": 250,
  "epoch": "...",
  "ledger_version": "...",
  "oldest_ledger_version": "0",
  "ledger_timestamp": "...",
  "node_role": "full_node",
  "oldest_block_height": "0",
  "block_height": "...",
  "git_hash": "..."
}
```

The response will return `chain_id` as an integer that can be used directly
as the CAIP-2 reference.

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```bash
# Movement Mainnet
movement:126

# Movement Testnet
movement:250

```

## References

- [REST API][] - REST API reference for Movement Network
- [Networks][] - Movement network information and endpoints
- [Explorer][] - Movement block explorer

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[REST API]: https://mainnet.movementnetwork.xyz/v1
[Networks]: https://docs.movementnetwork.xyz/
[Explorer]: https://explorer.movementnetwork.xyz/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
