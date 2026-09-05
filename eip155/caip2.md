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

The chain ID defined in [EIP-155] is the most widely used chain identifier in the Ethereum ecosystem known to the authors. It optimizes for uniqueness and its usage for replay protection has helped it achieve wide adoption. 
Unique network IDs can be self-registered in the [ethereum-lists/chains][] registry.

## Syntax

For reference, The format of reference currently specified in [EIP-155] is an unsigned integer of type UINT256, which is 64 characters long in hexadecimal notation.
That said, the longest `chainId` registered in the registry is 15 characters long, and compatibility with major wallets and common tooling in the Ethereum ecosystem is endangered when `chainId`s exceed 55 bits, so implementers are encouraged to observe the much shorter profile defined in [EIP-2294] in contexts where longer chainIds need to be supported.

### Null Network Reference

The `chainId` value `0` is valid per the original [specification for the chainId system][EIP-155] but unused in (and prescribed by the tooling for) the canonical registry mentioned in that same specification.
As proposed in [EIP-3788], this otherwise un-used `chainId` could be re-defined for signaling _independence_ from the `chainId`/replay-protection system in some contexts.

As `chainId`s represent locators for dynamic networks, the absence of a locator can be interpreted as refering either to no network, or to capabilities and resources replayable/applicable in the context of any network.
In the context of authorizations per [CAIP-25], methods for communicating directly to the wallet can thus be requested in the scope of `eip155:0`, as these are not affected by the adding or subtracting of specific network scopes.
Where such methods are inferred or signaled out of band, it is recommended to encode them as `methods` properties of the `eip155:0` scope (even if not requested) in [CAIP-25] responses for clarity and canonicity.

See also the Special Case of EOA section of [the CAIP-10 profile](caip10.md#special-case-of-eoa) for a third special case for chain-unspecified  addresses in the CAIP-10 system and in native ethereum-only code.

### Resolution Method

To resolve a blockchain reference for the [EIP-155] namespace, make a JSON-RPC request to a blockchain node with method `eth_chainId`, for example:

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

The response will return a base-16-encoded integer that should be converted to base 10 to format an [EIP-155]-compatible blockchain reference.

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

- [EIP-155][]: Ethereum Improvement Proposal specifying generation and validation of ChainIDs
- [ethereum-lists/chains][]: An open registry for eip155 network operators to claim a
      unique chainID and self-publish RPC/node information for them.
- [ERC-20][]: Basic [aka Fungible] Token Standard
- [ERC-721][]: Non-Fungible Token Standard

[ethereum-lists/chains]: https://github.com/ethereum-lists/chains
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-21]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-21.md
[CAIP-22]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-22.md
[ERC-20]: https://eips.ethereum.org/EIPS/eip-20
[EIP-155]: https://eips.ethereum.org/EIPS/eip-155
[ERC-721]: https://eips.ethereum.org/EIPS/eip-721
[ERC-2294]: https://eips.ethereum.org/EIPS/eip-2294
[ERC-3788]: https://eips.ethereum.org/EIPS/eip-3788

## Rights

Copyright and related rights waived via CC0.
