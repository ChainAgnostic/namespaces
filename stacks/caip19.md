---
namespace-identifier: stacks-caip19
title: Stacks Namespace - Asset
author: Friedger (@friedger)
discussions-to: 
status: Draft
type: Standard
created: 2023-05-21
updated: 2023-05-21
requires: ["CAIP-2", "CAIP-10", "CAIP-19"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Rationale

On Stacks, there are three types of native assets: STX, fungible tokens and non-fungible tokens. STX tokens are exposed to the users,
the two others are only internal to smart contracts defined by the programming language Clarity. A Stacks smart contract can define 
more than one native fungible or non-fungible token to allow detailed control over assets.

Smart contracts that contain only one fungible token, resp. one non-fungible token defines a Stacks fungible token (FT), 
resp. a Stacks non-fungible token (NFT). There are corresponding standards (SIP) exposing token functions to the user.


## Syntax

After the [CAIP-2][] (namespace+chainID), a slash defines an `asset_namespace` and an `asset_reference`. 
The `asset_namespace` is defined via the SIP  or  

| Reference   | Equivalent to | See also            |
| :---        | :----         | :---                |
| sip9        | ERC20 Token   |  |
| sip10       | ERC721        |  |
| sip13       | ERC1155       |  |
| nft         |               | SC defining one native non-fungible token but not following sip9 standard |
| ft         |               | SC defining one native fungible token but not following sip10 standard |


## Examples

```
# Stacks Mainnet NFT：
stacks:1/sip9:SP3D6PV2ACBPEKYJTCMH7HEN02KP87QSP8KTEH335.megapont-space-agency/4

# Stacks Mainnet xBTC
stacks:1/sip10:SP3DX3H4FEYZJZ586MFBS25ZW3HZDMEW92260R2PR.Wrapped-Bitcoin
```

## Links

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md


## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
