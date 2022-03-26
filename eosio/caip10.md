---
namespace-identifier: eosio
title: EOSIO Namespace - Addresses
author: Sebastian Montero (@sebastianmontero)
discussions-to: https://github.com/ChainAgnostic/CAIPs/issues/32
status: Draft
type: Standard
created: 2022-03-02
updated: 2022-03-02
requires: ["CAIP-2", "CAIP-10"]
supersedes: CAIP-7
--- 

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

EOSIO aligns squarely with the "account" model rather than the "UXTO" model.
Each account instantiated in a given chain exists thereafter in the state of
that chain; independent of any other additional state maintained by deployed
smart contracts, the [eosio.token][] smart contract maintains a native-token
balance for each account, and can be queried in various modes from any active
node. 

For any valid account on a given chain, not just current native-token balance
but also the "CPU" compute availability abstraction and the details of
authorization/proof-of-control can be requested from the chain's nodes using the
[get_account][] API call. It is worth noting that unlike other account-based
systems, the `[permissions][]` object (and the sui generis multi-signature system it
references) may be required to prove control of an account or authorize a
transaction. This is, of course, out of scope of this document. 

## Syntax

See the more recent [Standard Account Name][] definition from the Glossary and
the [Naming Best Practices][] from the CDT section of the EOSIO developer
documentation for up-to-date guidance. At time of press, the following regex
accurately validated standard account names on EOSIO:
```
[a-z][.a-z1-5]{10}[a-z1-5]
```

### Backwards Compatibility

Not applicable or unknown.

## Test Cases

This is a list of manually composed examples:

```
eosio:aca376f206b8fc25a6ed44dbdc66547c:bumblefudge1
eosio:e70aaab8997e1dfce58fbfac80cbbb8f:a..........a
eosio:4667b205c6838ef70ff7988f6e8257e8:a1234567890z
eosio:1eaa0824707c8c16bd25145493bf062a:casa2022.biz

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
