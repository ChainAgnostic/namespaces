---
namespace-identifier: amax
title: AMAX Namespace - Addresses
author: Narsiss (@Narsiss)
status: Draft
type: Standard
created: 2023-04-14
updated: 2023-04-14
requires: ["CAIP-2", "CAIP-10"]
--- 

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

AMAX aligns squarely with the "account" model rather than the "UXTO" model.
Each account instantiated in a given chain exists thereafter in the state of
that chain; independent of any other additional state maintained by deployed
smart contracts, the [token][] smart contract maintains a native-token
balance for each account, and can be queried in various modes from any active
node. 

For any valid account on a given chain, not just current native-token balance
but also the "CPU" compute availability abstraction and the details of
authorization/proof-of-control can be requested from the chain's nodes using the
[get_account][] API call. It is worth noting that unlike other account-based
systems, the [permissions][] object (and the sui generis multi-signature system it
references) may be required to prove control of an account or authorize a
transaction. This is, of course, out of scope of this document. 

## Syntax

See the more recent [Standard Account Name][] definition from the Glossary and
the [Naming Best Practices][] from the CDT section of the AMAX developer
documentation for up-to-date guidance. At time of press, the following regex
accurately validated standard account names on AMAX:
```
[a-z][.a-z1-5]{10}[a-z1-5]
```

### Backwards Compatibility

Not applicable or unknown.

## Test Cases

This is a list of manually composed examples:

```
amax:aca376f206b8fc25a6ed44dbdc66547c:bumblefudge1
amax:e70aaab8997e1dfce58fbfac80cbbb8f:a..........a
amax:4667b205c6838ef70ff7988f6e8257e8:a1234567890z
amax:1eaa0824707c8c16bd25145493bf062a:casa2022.biz

```

## References

- [Standard Account Name][]: Canonical definition of account name constraints
- [EOSIO][]: Overview of developer documentation, starting from core [and unique] concepts
- [EOSIO/eos#3425][]: A github PR discussion detailing some key design decisions around `chain_id`

[Transactions Protocol]: https://docs.amax.network/en/latest/API/AMAX-RPC/#wallet_sign_trx
[get_info]: https://docs.amax.network/en/latest/API/AMAX-RPC/#get_info
[get_account]: https://docs.amax.network/en/latest/API/AMAX-RPC/#get_account
[token]: https://developers.eos.io/welcome/v2.2/tutorials/eosio_token
[Chain ID]: https://github.com/EOSIO/eos/pull/3425
[Standard Account Name]: https://developers.eos.io/welcome/v2.1/glossary/index/#standard-account-name
[Account and Permissions]: https://developers.eos.io/welcome/v2.1/introduction-to-eosio/core_concepts
[permissions]: https://developers.eos.io/welcome/latest/protocol-guides/accounts_and_permissions
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md


## Rights

Copyright and related rights waived via CC0.