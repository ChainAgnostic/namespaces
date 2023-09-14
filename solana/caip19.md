---
namespace-identifier: solana-caip19
title: Solana Namespace - Asset
author: Qiao Liang (@qbig)
discussions-to: 
status: Draft
type: Standard
created: 2022-06-01
updated: 2022-06-01
requires: ["CAIP-2", "CAIP-10", "CAIP-19", "CAIP-30"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Rationale

On Solana, all contracts are stateless and state is instead represented using "accounts". More specifically, all fungible and non-fungible tokens use the same instance of token contracts and for each token:

- 1 single global "mint" account instance is used for the global data like "total supply".
- each token account represents an account balance belonging to a given address.

The only difference between fungible tokens and non-fungible tokens is that non-fungible token mints have a total supply of 1 and zero decimal place. Both asset type can be identified by their "mint" account. 


## Syntax

After the [CAIP-2][] (namespace+chainID), a slash defines an `asset_namespace` and an `asset_reference`. Since both fungible and non-fungible tokens can be identified using the mint account, we use `token` (fungible) and `nft` (non-fungible) as the asset namespaces and the address of the `mint` account as the reference in both.

| Reference   | Equivalent to | See also            |
| :---        | :----         | :---                |
| token       | ERC20 Token   | [Metaplex](https://docs.metaplex.com/programs/token-metadata/token-standard) Fungible   |
| nft         | ERC721        | [Metaplex](https://docs.metaplex.com/programs/token-metadata/token-standard) NonFungible|


## Examples

```
# One Solana Mainnet NFT：Pesky Penguins #398
solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp/nft:Fz6LxeUg5qjesYX3BdmtTwyyzBtMxk644XiTqU5W3w9w

# Solana Mainnet USDC
solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp/token:EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
```

## Links

[Address Lookup Table Proposal]: https://docs.solana.com/proposals/transactions-v2
[Account Types]: https://docs.solana.com/terminology#account
[Address Expressions]: https://docs.solana.com/cli/transfer-tokens#receive-tokens
[Token Mint]: https://spl.solana.com/token#creating-a-new-token-type
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-30]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-30.md


## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
