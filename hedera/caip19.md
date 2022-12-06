---
namespace-identifier: hedera-caip19
title: Hedera Namespace - Assets
author: Danno Ferrin (@shemnon), Juan Caballero (@bumblefudge)
discussions-to: https://github.com/hashgraph/hedera-improvement-proposal/discussions/169
status: Draft
type: Standard
created: 2021-11-01
updated: 2022-03-27
requires: ["CAIP-2", "CAIP-19"]
replaces: CAIP-75
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

This specification defines a [CAIP-19][] scheme for both fungible and
non-fungible tokenized assets in the Hedera ecosystem.  The [Hedera Token
Service][] is used in slightly different ways for both. When interacting with
these two types of Hedera token, Solidity contracts can interact with most (but
not all!) functions defined by the ERC20 and ERC721; for a list, see the current
[ERC20 & ERC721 Compatibility][] page in the developer documentation.

Standard NFT Fees, Metadata and other uses of the "memo" field in HTS tokens,
and custom fees are all out of scope and are not encoded in a CAIP-conformant
address; see [HIP-17][], [HIP-10][], and [HIP-18][] respectively.

# Fungible Tokens

In CAIP-19 a general asset identification scheme is defined. This is the
implementation of [CAIP-19][] for `token` in representing fungible tokens, which
are addressed in the same way as accounts are addressed in the [Hedera CAIP-10
specification](caip10.md), i.e., `{shard}.{realm}.{address}`.

## Semantics

### Token Asset Namespace

The asset namespace for fungible tokens in the Hedera Token Service (HTS) is
`token` (case-sensitive).

### Asset Reference Definition

The Asset Reference format is the tokenID in the specific hashgraph (see the
[Hedera CAIP-10 specification](caip10.md) for semantics).

## Syntax

The following regular expression can be used to validate fungible tokens:

```
hedera:[-a-zA-Z0-9]{5,32}\/token:[0-9]{1,19}\.[0-9]{1,19}\.[0-9]{1,19}(\-[a-z]{5}){0,1}
```

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```
# Dried Nutm (Dri)
hedera:mainnet/token:0.0.278981
```

# Non-Fungible Tokens

In CAIP-19 a general asset identification scheme is defined. CAIP-153 extended this sane scheme to include a broader characterset, enabling the `.`-concatenated shard/realm prefixes before addresses which are standard in Hedera. This describes the
implementation of [CAIP-19][] for `token` in representing non-fungible tokens, which are
addressed in the same way as accounts are addressed in the [Hedera CAIP-10
specification](caip10.md), i.e., `{shard}.{realm}.{address}`. 

## Semantics

### Token Asset Namespace

The asset namespace is called `nft` hosted in the Hedera Token Service (HTS). It
references HTS non-fungible tokens in the `hedera` namespace (see CAIP-75).

#### Asset Reference Definition

The Asset reference format is the tokenID in the specific hashgraph (see the
[Hedera CAIP-10 specification](caip10.md) for semantics).

#### Token ID Definition

The Token ID reference format is the serial number of the specific token.

## Syntax

The following regular expression can be used to validate fungible tokens:

```
hedera:[-a-zA-Z0-9]{5,32}\/nft:[0-9]{1,19}\.[0-9]{1,19}\.[0-9]{1,19}(\-[a-z]{5}){0,1}\/[0-9]{1,19}
```

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```
# Edition 12 of 50: First-Generation Hedera Robot VENOM EDITION
hedera:mainnet/nft:0.0.55492/12
```

## Links

- [Hedera Token Service SDK Docs][]
- [ERC20 & ERC721 Compatibility][]: Note the "Not Supported" section for each contract!
- [HIP-10][]: Token Metadata JSON Schema (for referencing from deployed NFT memo fields)
- [HIP-17][]: NFT specification
- [HIP-18][]: Custom Token Fees
- [HIP-30]: CAIP Identifiers for the Hedera Network

[CAIP-2]: https://chainAgnostic.org/CAIPS/caip-2
[CAIP-10]: https://chainAgnostic.org/CAIPS/caip-10
[CAIP-19]: https://chainAgnostic.org/CAIPS/caip-19
[HIP-10]: https://github.com/hashgraph/hedera-improvement-proposal/blob/master/HIP/hip-10.md
[HIP-15]: https://github.com/hashgraph/hedera-improvement-proposal/blob/master/HIP/hip-15.md
[HIP-17]: https://github.com/hashgraph/hedera-improvement-proposal/blob/master/HIP/hip-17.md
[HIP-18]: https://github.com/hashgraph/hedera-improvement-proposal/blob/master/HIP/hip-18.md
[HIP-30]: https://github.com/hashgraph/hedera-improvement-proposal/blob/master/HIP/hip-30.md
[Hedera Developer Documentation]: https://docs.hedera.com/guides/
[Native Account Syntax]: https://docs.hedera.com/guides/core-concepts/accounts#account-id
[Hedera Token Service SDK Docs]: https://docs.hedera.com/guides/docs/sdks/tokens
[ERC20 & ERC721 Compatibility]: https://docs.hedera.com/guides/core-concepts/smart-contracts/supported-erc-token-standards

## Copyright

Copyright and related rights waived
via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).