---
namespace-identifier: icon
title: ICON
author: ["Billy Rennekamp (@okwme)"]
discussions-to: https://github.com/0xcounting/FAR/issues/1
status: Draft
type: Informational
created: 2026-09-14
---

# Namespace for ICON blockchains

ICON is a layer-1 blockchain with a delegated proof-of-contribution consensus, in which token holders delegate stake to elected Public Representatives who produce blocks.
Smart contracts on ICON are called SCOREs (Smart Contract on Reliable Environment) and are written in Python or Java rather than compiled to an EVM.
The `icon` namespace covers networks that run the ICON node software and expose its ICON JSON-RPC v3 interface.
Individual networks in the namespace are identified by their network ID, or NID, as specified in the [ICON CAIP-2 profile][].

## Address prefixes

ICON uses two address prefixes, and which one an address carries tells you what kind of account it is before you query anything.
An `hx` address is an externally owned account: a wallet controlled by a key.
A `cx` address is a contract account: a deployed SCORE.
In both cases the prefix is followed by exactly 40 lowercase hexadecimal characters encoding 20 bytes, so a full address is 42 characters.

This is more informative than it looks.
On an EVM chain the same 20-byte address space holds both wallets and contracts, and telling them apart requires a `getCode` call.
On ICON the distinction is carried in the identifier itself, which means an indexer, a wallet, or a CAIP-10 implementation can classify an account with a two-character string comparison.
The governance SCORE at `cx0000000000000000000000000000000000000000` is the conventional example of a contract address.

A later CAIP-10 profile for this namespace will need to preserve both prefixes, because `hx…` and `cx…` with the same 40 hex characters are two different accounts, not two spellings of one.

## ICON 2.0 and BTP

ICON migrated from its original loopchain node software to a new implementation, goloop, in the ICON 2.0 upgrade.
That migration replaced the node software, the consensus engine, and the virtual machine layer, but it did not renumber the networks.
MainNet's NID is `0x1` today, confirmed against two live MainNet endpoints, and the ICON documentation records no renumbering across the ICON 2.0 transition.
Anyone citing a NID for ICON should nonetheless resolve it from a node rather than from an ICON 1.0-era document, because the test networks were replaced during and after that transition.

ICON's cross-chain work, the Blockchain Transmission Protocol, introduced a second identifier format that an implementer will encounter: the BTP Network Address.
It is written `<nid>.<network system>`, so ICON MainNet is `0x1.icon`, and a full BTP address is `btp://0x1.icon/hx…`.
The NID inside a BTP Network Address is the same NID this namespace uses as its CAIP-2 reference, which makes BTP addresses a useful independent corroboration of a NID value.
BTP Network Addresses are not themselves CAIP-2 chain IDs and should not be used as references.

## Rationale

`icon` is the ecosystem's own name, is four characters long, and is all lowercase, so it satisfies the CAIP-2 namespace production `[-a-z0-9]{3,8}` without modification.
The provisional name needed no change: CASA names a namespace after an ecosystem, and ICON is the ecosystem.

NID is the right reference because it is the value the protocol itself uses to bind a signed transaction to a network.
Every ICON transaction carries a `nid` field, and a transaction signed with the wrong `nid` is rejected, so NID is already load-bearing for replay protection rather than being a label bolted on for tooling.

This namespace was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a CAIP-2 for this chain in order to name the assets that exist on it.
The authors do not represent the ICON ecosystem.
It is offered as a starting point for the ICON community to correct, adopt or replace, and the authors would rather it carry a maintainer's name than theirs.

## Governance

Technical standards for ICON are proposed as ICON Improvement Proposals in the [IIPs repository][], following a process modelled on Ethereum's EIPs.
ICON also has on-chain governance: ICX holders delegate stake to Public Representatives, who vote on Network Proposals that can change network parameters, revise the revision number that gates protocol behaviour, and approve or block SCORE deployments.
The [Network Proposals documentation][] describes the proposal types and the voting mechanics.
An implementer should note that ICON's protocol behaviour is versioned on chain by a revision number changed through this process, so behaviour can change without a node release.

## References

- [ICON documentation][] - Concepts, node operation, and client APIs
- [ICON networks][] - The published NID values for MainNet and the test networks
- [ICON JSON-RPC v3][] - The client API, including `icx_getNetworkInfo`
- [ICON accounts][] - The `hx` and `cx` address formats
- [BTP address][] - The BTP Network Address format and its relation to NID
- [IIPs repository][] - ICON Improvement Proposals
- [Network Proposals documentation][] - On-chain governance process
- [ICON CAIP-2 profile][] - The chain ID specification in this namespace

[ICON documentation]: https://docs.icon.community/
[ICON networks]: https://docs.icon.community/develop-on-icon-chain/networks
[ICON JSON-RPC v3]: https://docs.icon.community/develop-on-icon-chain/client-apis/json-rpc-api
[ICON accounts]: https://docs.icon.community/develop-on-icon-chain/blockchain-components/accounts
[BTP address]: https://docs.icon.community/cross-chain-communication/blockchain-transmission-protocol-btp/btp-address
[IIPs repository]: https://github.com/icon-project/IIPs
[Network Proposals documentation]: https://docs.icon.community/operate-icon/governance/network-proposals
[ICON CAIP-2 profile]: ./caip2.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
