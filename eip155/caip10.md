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

To express Ethereum account without reference to any specific [EIP-155][] chain ID, CAIP-10 identifiers can use the special `chainId` segment `0`.

In the Ethereum account system, "externally owned accounts" (i.e. "offchain" wallets) are controlled by user agents and not by on-chain entities (i.e. deployed or deployable smart contract code). 
The special chainId `0` SHOULD only be used for accounts that can be used in off-chain contexts, i.e. without the use of an Ethereum node.

Note that a given address cannot be assumed to work on all current and future networks with an [EIP-155][] `chainId`, which may express or derive addresses differently for a given private key; a user account expressed with `chainId` segment of 0 is assumed to control the same account on `chainId` 1 and most ethereum chains, but MAY control a different account or additional accounts on networks that extend the account or addressing model of Ethereum, assume different key or hash derivations, etc.

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
namespace:   [-a-z0-9]{3,8}
network_id:    [0-9]{1,64}
reference:   0x[a-fA-F0-9]{1,40}
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

## Security Considerations

As the Ethereum namespace evolved, user-agents that connect to dapps through an [EIP-1193][] interface started to accrue "off-chain" use-cases such as authenticating control of an onchain account with an "off-chain" signature (i.e. a transaction signed by the wallet and verified by a dapp or website without either party submitting it to a node or running any on-chain functions). It is RECOMMENDED that wallets using the chainId of `0` be authenticated in a standardized and secure manner which produces verifiable receipts of the authenticaiton event, such as that documented in [ERC-4361][] and extended by [CAIP-122][].

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
[CAIP-122]: https://chainagnostic.org/CAIPs/caip-122
[ERC-4361]: https://eips.ethereum.org/EIPS/eip-4361
[EIP-1193]: https://eips.ethereum.org/EIPS/eip-1193
[EIP-155]: https://eips.ethereum.org/EIPS/eip-155
[EIP-55]: https://eips.ethereum.org/EIPS/eip-55
[ERC-20]: https://eips.ethereum.org/EIPS/eip-20
[ERC-721]: https://eips.ethereum.org/EIPS/eip-721


## Rights

Copyright and related rights waived via CC0.
