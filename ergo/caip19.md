---
namespace-identifier: ergo-caip19
title: Ergo Namespace - Assets
author: Yuriy Gagarin (@gagarin55)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/98
status: Draft
type: Standard
created: 2023-11-04
updated: 2023-12-12
requires: ["CAIP-2", "CAIP-19"]
---

## Rationale

Ergo supports custom tokens as first-class citizens as outlined in [EIP-0004].

A transaction can create tokens from thin air in its outputs if the Asset ID matches the ID of the transaction's first input ([box]). 
Since the box identifier is cryptographically unique, it's impossible to have a second asset with the same identifier. 
This rule also implies that only one new asset can be created per transaction.

The ID format for fungible (ERC20-equivalent) and non-fungible (ERC-721 equivalent) tokens is the same.
The process for issuance of either is also the same.
The only difference is that NFTs must have specific values (see [EIP-0004]) for certain properties.

## Specification of Asset ID

Asset ID is a 32 byte array encoded as a hex string. 
When issued, it is equal to the ID of the transaction's first input that issued this asset.

## Syntax

The syntax of Ergo Asset ID:

```
address:    namespace + ":" chainId + ":" + reference
namespace:  ergo
chain ID:   32-character prefix from the hash of the genesis block
reference:  Ergo Asset ID represented as hex string
```

## Examples

```
# Ergo Mainnet
ergo:b0244dfc267baca974a4caee06120321:56d89fdb0c92605d6c80f06a4c6a217f62bdc5695776f916daeabd708683f60d

# Ergo Testnet
ergo:e7553c9a716bb3983ac8b0c21689a1f3:0160b869f30a5424e59cb3453e8a726b81fe83761d02ab41829cb7b2e4b624bc

```

## Links

- [Token][token] overview
- [Ergo Box][box] overview
- [About addresses in Ergo Documentation][address format]
- [Ergo Assets standard][EIP-0004]
[box]: https://docs.ergoplatform.com/dev/data-model/box/
[token]: https://docs.ergoplatform.com/dev/data-model/box/tokens/
[address format]: https://docs.ergoplatform.com/dev/wallet/address/address_types
[EIP-0004]: https://github.com/ergoplatform/eips/blob/master/eip-0004.md

## Copyright

Copyright and related rights waived via [CC0](../LICENSE).
