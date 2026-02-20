---
namespace-identifier: eosio
title: EOSIO Namespace - Chains
author: Sebastian Montero (@sebastianmontero)
discussions-to: https://github.com/ChainAgnostic/CAIPs/issues/32
status: Draft
type: Standard
created: 2020-11-30
updated: 2022-03-27
requires: ["CAIP-2", "CAIP-10"]
replaces: CAIP-7
--- 

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

An explanation of and specification for `chain_id` in the EOSIO development
environment can be found in the algorithm for signing transactions in the
[Transactions Protocol][] section of the developer documents, because a valid
`chain_id` is required to authorize any transaction on that chain.  Further
information on querying nodes for `chain_id` can be found in the [Chain API
Plugin][] section of the API documentation, and the PR [EOSIO/eos#3425][] that
merged in those capabilities.

## Syntax

The Chain ID, or rather the `chain_id` as defined by EOSIO, is always a
64-character hexadecimal string containing the SHA256 hash of the genesis state
of a given chain chain. In order to fit the CAIP-2 reference format, a 32
character prefix of the Chain ID is used; note, however, that the longer
original will be needed to authorize new transactions.

### Resolution Method

See [EOSIO/eos#3425][] and [get_info] for more information about querying
network nodes for [a SHA256 hash of the] genesis state, which is referred to as
`chain ID` and required for authorizing transactions on said chain.

## Test Cases

This is a list of manually composed examples

```
# EOS Mainnet 
//get_info() --> chain_id=aca376f206b8fc25a6ed44dbdc66547c36c6c33e3a119ffbeaef943642f0e906
eosio:aca376f206b8fc25a6ed44dbdc66547c

# Jungle Testnet 
//get_info() --> chain_id=e70aaab8997e1dfce58fbfac80cbbb8fecec7b99cf982a9444273cbc64c41473
eosio:e70aaab8997e1dfce58fbfac80cbbb8f

# Telos Mainnet 
//get_info() --> chain_id=e70aaab8997e1dfce58fbfac80cbbb8fecec7b99cf982a9444273cbc64c41473
eosio:4667b205c6838ef70ff7988f6e8257e8

# Telos Testnet 
//get_info() --> chain_id=1eaa0824707c8c16bd25145493bf062aecddfeb56c736f6ba6397f3195f33c9f
eosio:1eaa0824707c8c16bd25145493bf062a
```

## References

- [Standard Account Name][]: Canonical definition of account name constraints
- [EOSIO][]: Overview of developer documentation, starting from core [and unique] concepts
- [EOSIO/eos#3425][]: A github PR discussion detailing some key design decisions around `chain_id`

[Transactions Protocol]: https://developers.eos.io/welcome/v2.1/protocol/transactions_protocol/#32-sign-transaction
[Chain API Plugin]: https://developers.eos.io/manuals/eos/v2.1/nodeos/plugins/chain_api_plugin/api-reference/index
[EOSIO/eos#3425]: https://github.com/EOSIO/eos/pull/3425
[EOSIO]: https://developers.eos.io/welcome/v2.1/introduction-to-eosio/core_concepts
[Standard Account Name]: https://developers.eos.io/welcome/v2.1/glossary/index/#standard-account-name
[Naming Best Practices]: https://developers.eos.io/manuals/eosio.cdt/v1.8/best-practices/naming-conventions/#non-standard-account-names
[get_account]: https://developers.eos.io/manuals/eos/v2.1/nodeos/plugins/chain_api_plugin/api-reference/index#operation/get_account
[get_info]: https://developers.eos.io/manuals/eos/v2.1/nodeos/plugins/chain_api_plugin/api-reference/index#operation/get_info
[eosio.token]: https://developers.eos.io/welcome/v2.2/tutorials/eosio_token
[permissions]: https://developers.eos.io/welcome/v2.1/glossary/index#permission
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
