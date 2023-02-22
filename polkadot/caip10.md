---
namespace-identifier: polkadot-caip10
title: Polkadot Namespace - Addresses
author: ["Pedro Gomes (@pedrouid)", "Joshua Mir (@joshua-mir)", "Shawn Tabrizi (@shawntabrizi)", "Juan Caballero (@bumblefudge)", "Antonio Antonino (@ntn-x2)"]
discussions-to: https://github.com/ChainAgnostic/CAIPs/issues/13
status: Draft
type: Standard
created: 2020-04-01
updated: 2023-02-22
requires: ["CAIP-2", "CAIP-10"]
replaces: CAIP-13
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

Polkadot addresses can be expressed in a number of ways, but the canonical expression in Polkadot development is a Base58 [multiaddress][] with a human-readable prefix of one or more characters.
The specification defining these across the entire Polkadot namespace is [SS58][]; this specification summarizes the calculation of an address as `base58encode ( concat ( <address-type>, <address>, <checksum> ) )`, where `<address-type>` is a prefix registered in the [SS58 registry][] and where `<checksum>` options are constrained by targeted output-length.

While the above describes a given keypair as generating many addresses per network, a 47-character multiaddress is the default expression, unique per chain.
Note that a single private key will thus produce different multiaddresses on each chain where it is used, so de-duplicating Polkadot accounts in a multi-chain context may require implementing full support for advanced SS58 functions.

As the default multi-address was used to express individual addresses in CAIP-10, other possible expressions are out of scope of this specification.
Similarly, recovery of chain ID from account type or validation of addresses using the included checksum are out of scope, although both are specified in [SS58][].

## Syntax

As the default/standard expression of an address in Polkadot is a 47-character base58 string, the following regular expression can be used for validating addresses:

```
[1-9A-HJ-NP-Za-km-z]{47}
```

## Test Cases

This is a list of examples composed using the [Polkadot subscan tool][]:

```
# Kusama
//example address from [Polkadot-ENS tutorial][]:
polkadot:b0a8d493285c2df73290dfb7e61f870f:CpjsLDC1JFyrhm3ftC9Gs4QoyrkHKhZKtK7YqGTRFtTafgp

//one address in multiple network-specific expressions, taken from the [Polkadot address explainer][]:

# Underlying Public Key:
0xf52c9c6ef25e069f81a82afad18aefe7e033f069ed1f8d402d5a3f3d243c4e68

# Kusama (relaychain; address-type prefix 2)
polkadot:b0a8d493285c2df73290dfb7e61f870f:J7nW4HZAUVqgJhbW83GGHJFNoKZAmFcMt9Q16rTc2Vn4Hny

# Edgeware (address-type prefix 7)
polkadot:742a2ca70c2fda6cee4f8df98d64c4c6:o45o1za5vsUTbiv2nSP9ndNcE32SgQDJav45X4xvJUDTkw6

# Kulupu (address-type prefix 16)
polkadot:37e1f8125397a98630013a4dff89b54c:2h927wsCYYk1s8N6BaMbYu2CRbKfwL4u13uEcfrg5zpbztW9

# KILT Spiritnet (address-type prefix 38)
polkadot:411f057b9107718c9624d6aa4a3f23c1:4tTXomn4zwz1JRGJ7Hi7risYeGU99MvM9k689i1JGouLBxUX
```

## References

- [Polkadot documentation][]: Homepage for ecosystem-wide developer documentation
- [Polkadot-ENS tutorial][]: A tutorial for native Kusama address support in the ENS front-end
- [Polkadot public RPC endpoints][]: for dev/testing purposes
- [Polkadot identity system][]: Introduction to on-chain identity registrars 
- [Polkadot address explainer][]: A quick overview of how network-specific,
      self-describing addresses can derive from the same private key
- [Polkadot subscan tool][]: A tool for transforming addresses according to SS58 across polkadot networks
- 

[Polkadot address explainer]: https://wiki.polkadot.network/docs/learn-account-advanced
[Polkadot identity system]: https://wiki.polkadot.network/docs/learn-identity
[Polkadot public RPC endpoints]: https://wiki.polkadot.network/docs/maintain-endpoints
[Polkadot documentation]: https://wiki.polkadot.network/
[Polkadot subscan tool]: https://polkadot.subscan.io/tools/ss58_transform?
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
