---
namespace-identifier: tenzro-caip2
title: Tenzro Namespace - Chains
author: Tenzro Engineering (eng@tenzro.com)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/184
status: Draft
type: Standard
created: 2026-05-02
updated: 2026-05-02
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for Tenzro. Blockchains in the "tenzro" namespace are
validated by their genesis block hash; each chain runs an independent
HotStuff-2 BFT consensus instance with its own genesis block and validator
set. Genesis hashes are 32-byte SHA-256 digests of the canonical genesis
block; their first 32 hex characters are used as the CAIP-2 reference.

## Syntax

The namespace "tenzro" refers to the Tenzro Network protocol.

### Reference Definition

The CAIP-2 reference for a Tenzro chain is the lowercase hexadecimal
encoding of the first 16 bytes (32 hex characters) of the genesis block
hash:

```
chain_id := "tenzro:" + lowercase(hex(genesis_hash[0..16]))
```

This conforms to CAIP-2's reference grammar `[-a-zA-Z0-9]{1,32}`.

### Resolution Method

To resolve a Tenzro chain reference, make a JSON-RPC request to the chain's
RPC endpoint with method `tenzro_getBlock` and the genesis block height
(`block_number: 0`):

```jsonc
// Request
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "tenzro_getBlock",
  "params": [{ "block_number": 0 }]
}

// Response (truncated to relevant fields)
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": {
    "hash": "92bd27db9713293097f0e63476e3911e77b706c1b20f4a5e97d44fe7a8d51648",
    "header": {
      "height": 0,
      "chain_id": 1337
    }
  }
}
```

The `hash` field is a 64-character lowercase hex string (32 bytes).
Truncate it to the first 32 characters to obtain the CAIP-2 reference.

EVM-compatible callers may also use `eth_chainId` to retrieve the
integer chain ID, but that integer is **not** the CAIP-2 reference —
the canonical reference always uses the truncated genesis hash.

### Backwards Compatibility

Not applicable. Tenzro is a fresh L1 with no prior CAIP-2 registration.

## Test Cases

```
# Tenzro Testnet
#   genesis hash: 92bd27db9713293097f0e63476e3911e77b706c1b20f4a5e97d44fe7a8d51648
#   integer chain_id (EVM-compat): 1337
tenzro:92bd27db9713293097f0e63476e3911e

# Tenzro Mainnet (TBD — populated at mainnet launch)
tenzro:<genesis_hash[0..16] in lowercase hex>
```

Until mainnet is launched, only the testnet reference above is canonical.

## References

- [CAIP-2][]
- [Tenzro Network repository][repo]
- [HotStuff-2 BFT][hs2]

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[repo]: https://github.com/tenzro/tenzro-network
[hs2]: https://eprint.iacr.org/2023/397.pdf

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
