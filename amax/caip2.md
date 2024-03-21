---
namespace-identifier: amax
title: AMAX Namespace - Chains
author: Narsiss(@Narsiss)
status: Draft
type: Standard
created: 2023-04-14
updated: 2023-04-14
requires: ["CAIP-2", "CAIP-10"]
replaces: CAIP-7
--- 

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

An explanation of and specification for `chain_id` in the AMAX development
environment can be found in the algorithm for signing transactions in the
[Transactions Protocol][] section of the developer documents, because a valid
`chain_id` is required to authorize any transaction on that chain.  Further
information on querying nodes for `chain_id` can be found in the [get_info][] section of the API documentation, and the PR [Chain ID][] that
merged in those capabilities.

## Syntax

The Chain ID, or rather the `chain_id` as defined by AMAX, is always a
64-character hexadecimal string containing the SHA256 hash of the genesis state
of a given chain chain. In order to fit the CAIP-2 reference format, a 32
character prefix of the Chain ID is used; note, however, that the longer
original will be needed to authorize new transactions.

### Resolution Method

See [Chain ID][] and [get_info] for more information about querying
network nodes for [a SHA256 hash of the] genesis state, which is referred to as
`chain ID` and required for authorizing transactions on said chain.

## Test Cases

This is a list of manually composed examples

```
# AMAX Mainnet 
//get_info() --> chain_id=2403d6f602a87977f898aa3c62c79a760f458745904a15b3cd63a106f62adc16
amax:2403d6f602a87977f898aa3c62c79a76

# AMAX Testnet 
//get_info() --> chain_id=208dacab3cd2e181c86841613cf05d9c60786c677e4ce86b266d0a58884968f7
amax:208dacab3cd2e181c86841613cf05d9c

```

## References

- [Official website](https://amax.network)
- [AMAX Documentation](https://docs.amax.network/en/latest/API/AMAX-RPC/)
- [Standard Account Name][]: Canonical definition of account name constraints
- [Chain ID][]: A github PR discussion detailing some key design decisions around `chain_id`
- [Developer Portal](https://developers.eos.io/welcome/v2.1/welcome-to-eosio/index)

[Transactions Protocol]: https://docs.amax.network/en/latest/API/AMAX-RPC/#wallet_sign_trx
[get_info]: https://docs.amax.network/en/latest/API/AMAX-RPC/#get_info
[Chain ID]: https://github.com/EOSIO/eos/pull/3425
[Standard Account Name]: https://developers.eos.io/welcome/v2.1/glossary/index/#standard-account-name
[Account and Permissions]: https://developers.eos.io/welcome/v2.1/introduction-to-eosio/core_concepts
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md



## Rights

Copyright and related rights waived via CC0.