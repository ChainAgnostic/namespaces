---
namespace-identifier: eip155-caip19
title: EIP155 Namespace, aka EVM Chains - Assets
author: Simon Warta (@webmaster128), ligi <ligi@ligi.de>, Pedro Gomes (@pedrouid), Antoine Herzog (@antoineherzog), Joel Thorstensson (@oed)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/2
status: Draft
type: Standard
created: 2019-12-05
updated: 2022-03-27
requires: ["CAIP-2", "CAIP-10", "CAIP-19"]
replaces: ["CAIP-21", "CAIP-22"]
---

# CAIP-19

_For context, see the [CAIP-19][] specification._

## Rationale

In the Ethereum space, most assets are either a unique on-chain token referenced
by its address, often called a "native token" ([erc20][] tokens being the most
common), or a uniquely-identifiable token within a registry governed by a
contract at a given address ([erc721][] being the most common), often called an
"NFT". An unambiguous and unique representation is easily achieved by using on-
chain address prefixed by CAIP-2 information.

## Syntax

After the CAIP-2 namespace+chainID, a slash defines an `asset_namespace` and an
`asset_reference`. `asset_namespace` MUST refer to an asset type defined by an
[Ethereum Improvement Proposal][EIP] of category ERC and status Final; the
syntax is simply `erc` prepended to the final EIP number of the published
document defining it, without a hyphen.

- In the case of ERC20 tokens, the namespace is `erc20` and the address of the
  smart contract is the reference.
- In the case of ERC721 tokens, the namespace is `erc721` and the address of the
  smart contract is the reference, with an optional additional identifier for
  the specific token separated from the reference by a "/"

## RegEx

The RegEx validation strings are as follows:

```
asset_id: asset_type + "/" token_id
asset_type: chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id: namespace + Blockchain ID as defined in [CAIP-2](./caip2.md)

asset_namespace: erc[a-z0-9]{2,5}
asset_reference: 0x[a-fA-F0-9]{40}
token_id: [\d]{1,78}
```

## Examples

```
# DAI Token
eip155:1/erc20:0x6b175474e89094c44da98b954eedeac495271d0f

# REQ Token
eip155:1/erc20:0x8f8221afbb33998d8584a2b05749ba73c37a938a

# CryptoKitties Collectible
eip155:1/erc721:0x06012c8cf97BEaD5deAe237070F9587f8E7A266d

# CryptoKitties Collectible ID
eip155:1/erc721:0x06012c8cf97BEaD5deAe237070F9587f8E7A266d/771769

# CryptoCoven.xyz Collectible ID
eip155:1/erc721:0x5180db8f5c931aae63c74266b211f580155ecac8/4663
```

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
