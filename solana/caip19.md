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

On solana, all contracts are stateless and state is instead represented using "accounts". More specifically, all fungible and non-fungible tokens are using the same instance of token contracts and for each token:

- 1 single global "mint" account instance is used for the global data like "total supply".
- each token account represent an account balance belong to a certain address.

And the difference between fungible token and non-fungible token is that non-fungible token mint has a total supply of 1 and zero decimal place.
But both asset type can be identified by their "mint" account. 


## Syntax

After the CAIP-2 namespace+chainID, a slash defines an `asset_namespace` and an `asset_reference`. 
- 

## Examples

```
# One Solana Mainnet NFT
solana:4sGjMW1sUnHzSxGspuhpqLDx6wiyjNtZ/spl-token-mint:{the-token-mint-account-address}
```

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```
# Solana Mainnet
solana:4sGjMW1sUnHzSxGspuhpqLDx6wiyjNtZ

# Solana Devnet
solana:8E9rvCKLFQia2Y35HXjjpWzj8weVo44K
```

## References

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