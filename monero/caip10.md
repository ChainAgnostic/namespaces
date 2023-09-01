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

CAIP-10 defines a common URI scheme for identifying actors in a pseudonymous cryptographic system.
Monero chains use the UTXO accounting model and [Monero addresses][] are functionally similar to accounts in other UTXO-based namespaces, where CAIP-10 identifiers represent **payee identifiers** (of which a given actor has many and can self-generate arbitrarily more) rather than **actor identifiers**.

## Semantics

Monero wallets can generate and pay out to several different types of payee addresses: 
1. [standard address](https://monerodocs.org/public-address/standard-address/) for fully-public contexts, 
1. [subaddress](https://monerodocs.org/public-address/subaddress/) for limiting linkability to a specific interactive context, and 
1. [integrated address](https://monerodocs.org/public-address/integrated-address/) which encrypt transaction-specific metadata to a shared secret to enable automation and programmable metadata per context. 

Each of these above addresses contains:
- network identifiers, which map to [CAIP-2][] `chainId`s,
- address type identifiers encoding which of the above it is,  
- a public spend key, 
- a public view key,
- optionally, additional type-specific data (such as a transaction-bound metadata for an integrated address), and
- a checksum derived from the above. 
 
Note that the [base58-monero][] encoding is used to encode address into a string.
The alphabet is identical to that used by [base58btc-alphabet][], but padding is used to normalize encoded length to multiples of 11 characters.
Note that decoding base58-monero with a standard base58 library can create breaking inconsistencies between the binary produced and the originally-encoded byte array if such padding was used when encoding.
Decoding the base58 properly and parsing the address type identifier are required for processing the checksum and thus validating the address.

Monero CAIP-10 URIs should not be referred to as "accounts" to avoid confusion  with "[Monero accounts][]", which is a term of art used in Monero wallet user interfaces for grouping related addresses and transactions into logical units.
Referring to Monero CAIP-10 URIs as encoding "addresses" or "payees" avoids this confusion, as well as potential false equivalences with namespaces built around atomic-account transaction models, as there is a one-to-many relation of wallets to addresses assumed in the Monero actor model.

## Syntax

Monero CAIP-10 account ID is a case-sensitive string in the form:

```
account_id:        chain_id + ":" + address
chain_id:          See Monero CAIP-2
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

In the future, new types of Monero addresses will be introduced. 
They will likely be longer and may exceed the 128 character limit set in the [CAIP-10][] specification.

## References

- [Address documentation][Monero Addresses] from Monero core developer documentation
- [Account documentation][Monero Accounts] from Monero core developer documentation

[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[Monero addresses]: https://www.getmonero.org/resources/moneropedia/address.html
[Monero accounts]: https://www.getmonero.org/resources/moneropedia/account.html
[base58-monero]: https://monerodocs.org/cryptography/base58/
[Monero CAIP-2]: https://github.com/ChainAgnostic/namespaces/blob/main/monero/caip2.md
[base58btc]: https://datatracker.ietf.org/doc/html/draft-msporny-base58-02
[base58btc-alphabet]: https://datatracker.ietf.org/doc/html/draft-msporny-base58-02#section-21

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
