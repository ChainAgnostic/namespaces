---
namespace-identifier: eip155-caip10
title: EIP155 Namespace, aka EVM Chains - Addresses
author: Simon Warta (@webmaster128), ligi <ligi@ligi.de>, Pedro Gomes (@pedrouid), Antoine Herzog (@antoineherzog), Joel Thorstensson (@oed)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/2
status: Draft
type: Standard
created: 2019-12-05
updated: 2022-03-27
requires: ["CAIP-2", "CAIP-10"]
replaces: CAIP-3
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

While Ethereum "accounts" were the unstated norm in the definition of
[CAIP-10][], there are still some particularities of the syntax that should be
specified for the unfamiliar.  

### Special case of EOA

In order to enable decentralized applications to specify EOAs as an address, we propose using chainID 0. This would signify that it can live on multiple networks. In absence of this, addresses will be assigned to only one chain using CAIP-10 chainID syntax, an EOA would be required to be assigned multiple times for each chain. Specifying 0 as chainID for EOA, further enables EOAs to be designated as an EOA once, and be treated as an EOA on every applicable chain

## Syntax

Ethereum addresses were, historically, case-insensitive and normalized to use
all-lowercase letters (`abcdef`) like most hexadecimal numeric types.  With the
ratification of [EIP-55][], however, a particular normalization of lowercase- and
uppercase- `abcdefABCDEF` characters was invented as an efficient form of
checksum. See [EIP-55][] for specification.

The chain ID will be used to represent blockchain except special case of 0 as chainID to represent EOA.

The `chain_id` string will be ammended as follows:

```
chain_id:    namespace + ":" + network_id + ":" + reference
network_id:    [0-9]{1,1}
namespace:   [-a-z0-9]{3,8}
reference:   [-_a-zA-Z0-9]{1,32}
```

### Backwards Compatibility

An earlier version of the CAIP-10 schema was defined by appending as suffix the
CAIP-2 chainId delimited by the at sign (@), i.e.
`0x22227A31dd842196A246d8f3b775998560eAa61d@eip155:1` in the above example. This
was changed [Aug 11,
2021](https://github.com/ChainAgnostic/CAIPs/commit/0697e26601d30d8e99df17954ed3
e5a1fd59e049) and some systems built against the earlier drafts may present
accounts in this manner.

## Test Cases

```
# EOA
eip155:0:0x839395e20bbB182fa440d08F850E6c7A8f6F0780

# Ethereum mainnet (valid/checksummed)
eip155:1:0x22227A31dd842196A246d8f3b775998560eAa61d

# Ethereum mainnet (will not validate in EIP155-conformant systems)
eip155:1:0x22227a31dd842196a246d8f3b775998560eaa61d

# Polygon mainnet (valid/checksummed)
eip155:137:0x0495766cD136138Fc492Dd499B8DC87A92D6685b

# Polygon mainnet (will not validate in EIP155-conformant systems)
eip155:137:0x0495766CD136138FC492DD499B8DC87A92D6685B

```

## Security Concerns

We should have users sign a message to prove they have an EOA (Greg to fill out more completely)

## References

- [EIP-155][]: Ethereum Improvement Proposal specifying generation and validation of ChainIDs
- [ethereum-lists/chains][]: An open registry for eip155 network operators to claim a
      unique chainID and self-publish RPC/node information for them.
- [ERC-20][]: Basic [aka Fungible] Token Standard
- [ERC-721][]: Non-Fungible Token Standard

[Chainid.network]: https://github.com/ethereum-lists/chains
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-21]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-21.md
[CAIP-22]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-22.md
[EIP-155]: https://eips.ethereum.org/EIPS/eip-155
[EIP-55]: https://eips.ethereum.org/EIPS/eip-55
[ERC-20]: https://eips.ethereum.org/EIPS/eip-20
[ERC-721]: https://eips.ethereum.org/EIPS/eip-721


## Rights

Copyright and related rights waived via CC0.
