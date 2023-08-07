---
namespace-identifier: eip155-caip2
title: EIP155 Namespace, aka EVM Chains - Chains
author: Simon Warta (@webmaster128), ligi <ligi@ligi.de>, Pedro Gomes (@pedrouid), Antoine Herzog (@antoineherzog), Joel Thorstensson (@oed)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/2
status: Draft
type: Standard
created: 2019-12-05
updated: 2022-03-27
requires: CAIP-2
replaces: CAIP-3
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

The chain ID defined in EIP155 is the most widely used chain identifier in the
Ethereum ecosystem known to the authors. It optimizes for uniqueness and its
usage for replay protection has helped it achieve wide adoption. Unique network
IDs can be self-registered in the [ethereum-lists/chains][] registry.

## Syntax

For reference, The format of reference currently specified in EIP155 is an
unsigned integer in decimal representation. Due to length restrictions of the
reference field (32 characters), the largest supported `CHAIN_ID` at time of
writing is `99999999999999999999999999999999`.


### Resolution Method

To resolve a blockchain reference for the EIP155 namespace, make a JSON-RPC
request to a blockchain node with method `eth_chainId`, for example:

```
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
  "result": "0x1"
}
```

The response will return a base-16-encoded integer that should be converted to
base 10 to format an EIP155-compatible blockchain reference.

## Test Cases

This is a list of manually composed examples

```
# Ethereum mainnet
eip155:1

# Görli
eip155:5

# Auxilium Network Mainnet
eip155:28945486
```

## References

- [EIP155][]: Ethereum Improvement Proposal specifying generation and validation of ChainIDs
- [ethereum-lists/chains][]: An open registry for eip155 network operators to claim a
      unique chainID and self-publish RPC/node information for them.
- [ERC20][]: Basic [aka Fungible] Token Standard
- [ERC721][]: Non-Fungible Token Standard

[ethereum-lists/chains]: https://github.com/ethereum-lists/chains
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-21]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-21.md
[CAIP-22]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-22.md
[EIP155]: https://eips.ethereum.org/EIPS/eip-155
[ERC20]: https://eips.ethereum.org/EIPS/eip-20
[ERC721]: https://eips.ethereum.org/EIPS/eip-721


## Rights

Copyright and related rights waived via CC0.
