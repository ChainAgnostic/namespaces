---
namespace-identifier: quantus-caip2
title: Quantus Namespace - Chains
author: ["Nikolaus Heger (@n13)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/228
status: Draft
type: Standard
created: 2026-09-17
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

Quantus Network runs a small, fixed set of networks operated by one team: a production mainnet and a public testnet.
Chains in the `quantus` namespace are therefore referenced by name, following the approach of the `hedera` and `sui` namespaces, rather than by a genesis hash prefix.

A name is stable even if a testnet is reset with a new genesis block, while the genesis hash behind it changes.
Clients that need cryptographic assurance that an RPC node belongs to the named network resolve the name to a genesis hash as described below.

## Syntax

The reference is one of the following enumerated, case-sensitive strings:

- `mainnet` - Quantus mainnet
- `planck` - Planck, the public testnet

New networks are added by amending this profile.
A regular expression that matches the identifiers currently defined is:

```
^quantus:(mainnet|planck)$
```

A regular expression that matches any identifier this namespace could define in the future, within the CAIP-2 limit of 32 characters, is:

```
^quantus:[a-z0-9]{3,32}$
```

### Resolution Method

Each name resolves to the hash of block 0 of that network:

| Reference | Chain name (`system_chain`) | Genesis hash |
|-----------|------------------------------|--------------|
| `mainnet` | `Quantus` | `0xfb5487c0be6ae4ade2d41d16e50465129861636c2b8d61fa94d7a19631626fba` |
| `planck`  | `Planck`  | `0x4901bf5c57fd3f9e726af399c763de6670dbdb115a91c0237e173f16eef65e72` |

To verify that an RPC node belongs to a given network, make a JSON-RPC request with the method `chain_getBlockHash` and block number `0`, and compare the result with the table:

```jsonc
// Request
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "chain_getBlockHash",
  "params": [0]
}

// Response from a Quantus mainnet node
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": "0xfb5487c0be6ae4ade2d41d16e50465129861636c2b8d61fa94d7a19631626fba"
}
```

The `system_chain` method returns the human-readable chain name and can be used as a first, non-cryptographic check.

Note that Quantus block hashes are computed with the Poseidon hash function, so the genesis hash cannot be recomputed from the chain specification with Blake2 tooling from other Substrate-based chains.

### Backwards Compatibility

Not applicable.

## Test Cases

This is a list of manually composed examples:

```
# Quantus mainnet
quantus:mainnet

# Planck testnet
quantus:planck
```

## Additional Considerations

### Rejected Idea: Using the `polkadot` namespace

Quantus is built with the Polkadot SDK, and the `polkadot` namespace would have given mainnet the identifier `polkadot:fb5487c0be6ae4ade2d41d16e5046512`.
That identifier was rejected because it would misrepresent the compatibility between Quantus and Polkadot chains.
Quantus signs with ML-DSA-87 or ML-DSA-65, derives accounts by hashing the public key with Poseidon, hashes blocks with Poseidon, uses proof-of-work consensus and does not support XCM.
No wallet or signer built for the `polkadot` namespace can produce a valid Quantus transaction.

## References

- [Quantus documentation][] - developer documentation for Quantus Network
- [Quantus chain repository][] - node and runtime source code, including the chain specifications
- [Quantus explorer][] - block explorer for mainnet

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[Quantus documentation]: https://docs.quantus.com/
[Quantus chain repository]: https://github.com/Quantus-Network/chain
[Quantus explorer]: https://explorer.quantus.com/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
