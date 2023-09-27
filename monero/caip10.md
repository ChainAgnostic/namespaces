---
namespace-identifier: monero-caip10
title: Monero - Addresses
author: silverpill (@silverpill)
discussions-to: https://github.com/ChainAgnostic/namespaces/issues/41
status: Draft
type: Informational
created: 2023-09-01
requires: ["CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

CAIP-10 defines a pattern for identifying an account in a blockchain. 
Monero chains use UTXO model and [Monero addresses][] are functionally similar to accounts in other namespaces.

## Semantics

Monero has several types of addresses: [standard address](https://monerodocs.org/public-address/standard-address/), [subaddress](https://monerodocs.org/public-address/subaddress/) and [integrated address](https://monerodocs.org/public-address/integrated-address/). 
Any address contains network and address type identifiers, public spend key, public view key, a checksum, and may contain additional data depending on the address type. 
Note that the [Base58-monero][base58-monero] encoding algorithm is used to encode the address from a byte array into a string; it uses the same alphabet as [base58btc][] but should not be decoded using [base58btc][] libraries due to the additional padding step to normalize string length.

CAIP-10 "accounts" should not be confused with [Monero accounts][], which are used in Monero wallets for grouping related addresses and transactions.

## Syntax

Monero CAIP-10 account ID is a case-sensitive string in the form:

```
account_id:        chain_id + ":" + address
chain_id:          See Monero CAIP-2 profile
address:           [a-zA-Z0-9]{95,106}
```

The syntax of `chain_id` is specified in [Monero CAIP-2][].

## Test Cases

This is a list of manually composed examples:

```
# Monero mainnet standard address
monero:418015bb9ae982a1975da7d79277c270:4AdUndXHHZ6cfufTMvppY6JwXNouMBzSkbLYfpAV5Usx3skxNgYeYTRj5UzqtReoS44qo9mtmXCqY45DJ852K5Jv2684Rge

# Monero mainnet integrated address
monero:418015bb9ae982a1975da7d79277c270:4LL9oSLmtpccfufTMvppY6JwXNouMBzSkbLYfpAV5Usx3skxNgYeYTRj5UzqtReoS44qo9mtmXCqY45DJ852K5Jv2bYXZKKQePHES9khPK

# Monero private testnet subaddress
monero:00000000000000000000000000000000:86MD1PNx3vmKUQjLvxNnmUfGQoHXAg8x56Nq97KrziKj5K8ACnpNUYx2KjiNAczP3igo7uUUUoGssDvKuZ7UUEoM1A8cvZs
```

## Additional Considerations

In the future new types of Monero addresses will be introduced. 
They will likely be longer and may exceed the 128 character limit set in [CAIP-10][] specification.

## References

- [Address documentation][Monero Addresses] from Monero documentation
- [Account documentation][Monero Accounts] from Monero documentation

[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[Monero addresses]: https://www.getmonero.org/resources/moneropedia/address.html
[Monero accounts]: https://www.getmonero.org/resources/moneropedia/account.html
[base58-monero]: https://monerodocs.org/cryptography/base58/
[Monero CAIP-2]: https://github.com/ChainAgnostic/namespaces/blob/main/monero/caip2.md
[base58btc]: https://datatracker.ietf.org/doc/html/draft-msporny-base58-02
[base58btc-alphabet]: https://datatracker.ietf.org/doc/html/draft-msporny-base58-02#section-21

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
