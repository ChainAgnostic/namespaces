---
namespace-identifier: tron-caip2
title: TRON Namespace – Chains
author:
  - "Daniel Rocha (@danroc)"
status: Draft
type: Standard
created: 2025-07-15
requires:
  - "CAIP-2"
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

In the TRON ecosystem, chain IDs uniquely identify each network. They are
derived from the genesis block hash, as specified in [TIP-474][].

## Syntax

A [CAIP-2][] chain ID for a TRON network uses the `tron` namespace, and the
reference portion is the decimal representation of the value returned by the
[`eth_chainId`] RPC method.

In TRON, the RPC’s `eth_chainId` response is defined as the last four bytes of
the genesis block hash. As a 32-bit value, it ranges from `0x00000000` through
`0xFFFFFFFF`.

A full TRON chain ID has the form:

```text
tron:<decimal-chain-id>
```

## Resolution Mechanics

To obtain the chain ID, send an `eth_chainId` JSON-RPC request to any TRON
node:

```json5
// Request
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "eth_chainId",
  "params": []
}

// Response
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": "0x2b6653dc"
}
```

The `result` field is a hexadecimal string. Convert it to a base-10 integer to
construct the CAIP-2 reference:

```text
0x2b6653dc → 728126428
```

Thus, the Mainnet chain ID becomes:

```text
tron:728126428
```

## Test Cases

Here are some common TRON networks and their CAIP-2 chain IDs:

```text
# TRON Mainnet
tron:728126428

# TRON Testnet – Shasta
tron:2494104990

# TRON Testnet – Nile
tron:3448148188
```

## References

- [CAIP-2][]: CAIP-2 Specification
- [TIP-474]: TRON Improvement Proposal for chain-ID generation
- [`eth_chainId`]: TRON JSON-RPC method documentation

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[TIP-474]: https://github.com/tronprotocol/tips/blob/master/tip-474.md
[`eth_chainId`]: https://developers.tron.network/reference/eth_chainid

## Copyright

All rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
