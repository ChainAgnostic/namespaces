---
namespace-identifier: supra-caip2
title: Supra Namespace - Chains
author: Bharat Jain <supra-bharatjain>
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/192
status: Draft
type: Standard
created: 2026-07-21
updated: 2026-07-21
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for Supra. Blockchains in the "supra" namespace are
identified by their numeric `chain_id`, assigned at genesis. Each network is
maintained by a set of validators with its own REST RPC endpoints. These chain
IDs require no transformations to be used as conformant CAIP-2 references.

## Syntax

The namespace "supra" refers to the Supra open-source blockchain platform.

### Reference Definition

The definition for this namespace will use the `chain_id` as an identifier
for different Supra chains. The chain ID is a positive integer assigned at
genesis:

| Network | Chain ID |
|---------|----------|
| Mainnet | 8        |
| Testnet | 6        |

### Resolution Method

To resolve a blockchain reference for the Supra namespace, make an HTTP GET
request to the REST RPC of a fullnode, for example:

```bash
curl https://rpc-mainnet.supra.com/rpc/v3/transactions/chain_id
```

```jsonc
// Response
8
```

The response is the `chain_id` as an integer that can be used directly as the
CAIP-2 reference.

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```bash
# Supra Mainnet
supra:8

# Supra Testnet
supra:6

```

## References

- [REST RPC][] - REST RPC reference in Supra official documentation
- [Networks][] - Supra network information and endpoints

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[REST RPC]: https://docs.supra.com/network/move/rest-api
[Networks]: https://docs.supra.com/network/network-information

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
