---
namespace-identifier: aptos-caip2
title: Aptos Namespace - Chains
author: Jon Tang <@jtang17>
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/169
status: Draft
type: Standard
created: 2025-12-12
updated: 2025-12-12
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for Aptos. Blockchains in the "aptos" namespace are
identified by their numeric `chain_id`, assigned at genesis. Each network is
maintained by a set of validators with its own REST API endpoints. These chain
IDs require no transformations to be used as conformant CAIP-2 references.

## Syntax

The namespace "aptos" refers to the Aptos open-source blockchain platform.

### Reference Definition

The definition for this namespace will use the `chain_id` as an identifier
for different Aptos chains. The chain ID is a positive integer assigned at
genesis:

| Network | Chain ID |
|---------|----------|
| Mainnet | 1        |
| Testnet | 2        |

### Resolution Method

To resolve a blockchain reference for the Aptos namespace, make an HTTP GET
request to the [REST API][] of a fullnode, for example:

```bash
curl https://fullnode.mainnet.aptoslabs.com/v1
```

```jsonc
// Response
{
  "chain_id": 1,
  "epoch": "5000",
  "ledger_version": "500000000",
  "oldest_ledger_version": "0",
  "ledger_timestamp": "1700000000000000",
  "node_role": "full_node",
  "oldest_block_height": "0",
  "block_height": "100000000",
  "git_hash": "abc123..."
}
```

The response will return `chain_id` as an integer that can be used directly
as the CAIP-2 reference.

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```bash
# Aptos Mainnet
aptos:1

# Aptos Testnet
aptos:2

```

## References

- [REST API][] - REST API reference in Aptos official documentation
- [Aptos core][] rust crate on crates.io
- [Networks][] - Aptos network information and endpoints

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[REST API]: https://aptos.dev/en/network/nodes/aptos-api-spec
[Aptos core]: https://crates.io/crates/aptos
[Networks]: https://aptos.dev/en/network/nodes/networks

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
