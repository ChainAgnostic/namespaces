---
namespace-identifier: eip155
title: EIP155 Namespace, aka EVM Chains
author: Simon Warta (@webmaster128), ligi <ligi@ligi.de>, Pedro Gomes (@pedrouid), Antoine Herzog (@antoineherzog), Pedro Gomes (@pedrouid), Joel Thorstensson (@oed)
discussions-to: https://github.com/ChainAgnostic/namespaces/pulls/2
status: Draft
type: Standard
created: 2022-01-19
updated: 2022-01-19
requires: CAIP-2, CAIP-10, CAIP-19
supersedes: CAIP-3, CAIP-21, CAIP-22
---

# Namespace for EIP155 chains

This document describes the syntax and structure of the [EIP155][] namespace,
commonly referred to as the "EVM" namespace for chains using the Ethereum
Virtual Machine. 

## Introduction

[EIP155][] is an Ethereum Improvement Process specifying addressing across
Ethereum-based chains, generalized by [CAIP-2][]. Definition of valid
`references` within that namespace and constraints are deferred to the
[EIP155][] specification, which may be superseded by future EIPs.

## References

- [EIP155][]: Ethereum Improvement Proposal specifying generation and validation of ChainIDs
- [ethereum-lists/chains][]: An open registry for eip155 network operators to claim a
      unique chainID and self-publish RPC/node information for them.
- [ERC20][]: Basic [aka Fungible] Token Standard
- [ERC721][]: Non-Fungible Token Standard

[Chainid.network]: https://github.com/ethereum-lists/chains
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
