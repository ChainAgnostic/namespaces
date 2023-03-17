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

Polkadot addresses are typically encoded in a Base58 format based on the [Bitcoin Base58-check format][], with few modifications to address the multi-chain context Polkadot operates in.
Specifically, each network defines its own network identifier, which is then included in the Base58 encoding process so that, for most networks, all addresses have the same prefix.
An [SS58 registry] is maintained by the Polkadot blockchain teams, and each prefix is uniquely assigned to a chain on a first-come-first-served basis.
A more in-depth description of address encoding can be found in the [Polkadot address documentation].

As a consequence, a given private-public keypair will yield a different account on each chain where it is used, so de-duplicating Polkadot accounts in a multi-chain context requires decoding addresses to raw public keys and make decisions based on that.

As the default multi-address was used to express individual addresses in CAIP-10, other possible expressions are out of scope of this specification.
Similarly, recovery of chain ID from account type or validation of addresses using the included checksum are out of scope, although both are specified in the [Polkadot address documentation][].

## Syntax

Because address length is dependent on the network, and other components must be checked such as the address' checksum, there is no simple way to verify an address with a regex.
Instead, there are libraries for address validation, encoding, and decoding support, such as the [polkadot-js library].

Nevertheless, if a regex were to be used, it would allow to match on addresses that are either 47 or 48 character long, and only containing Base58 alphabet:

```
[1-9A-HJ-NP-Za-km-z]{47,48}
```

## Test Cases

This is a list of example addresses generated from the same public key, composed using the [Subscan address converter][]:

```
# Public key (in HEX format)
0xd6a3105d6768e956e9e5d41050ac29843f98561410d3a47f9dd5b3b227ab8746

# Polkadot (SS58 prefix = 0)
15rRgsWxz4H5LTnNGcCFsszfXD8oeAFd8QRsR6MbQE2f6XFF

# Kusama (SS58 prefix = 2)
HRkCrbmke2XeabJ5fxJdgXWpBRPkXWfWHY8eTeCKwDdf4k6

# KILT Spiritnet (SS58 prefix = 38)
4smVWa6Hb7WhGh9zgqdAE86p5eZyj8BQJ9Uro4o2zidBnmfX

# Karura (SS58 prefix = 8)
t9hkorC4PGtaw25WsESu684h6HA5dHndvrvLZW174nZM5MR

# Crust Network (SS58 prefix = 66)
cTMC4XwPfBn3bz8kFaVTjaWdkQi6agzMxS11e8hpPHhqLrhGs
```

## References

- [Polkadot documentation][]: Homepage for ecosystem-wide developer documentation
- [Polkadot address documentation][]: Explanation on the Polkadot address system
- [Subscan address converter][]: A tool for transforming addresses according to SS58 across polkadot networks

[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[Bitcoin Base58-check format]: [https://en.bitcoin.it/wiki/Base58Check_encoding
[SS58 registry]: https://github.com/paritytech/ss58-registry
[Polkadot address documentation]: https://docs.substrate.io/reference/address-formats/
[polkadot-js library]: https://polkadot.js.org/docs/util-crypto/examples/validate-address/
[Polkadot documentation]: https://wiki.polkadot.network/
[Polkadot identity system]: https://wiki.polkadot.network/docs/learn-identity
[Subscan address converter]: https://polkadot.subscan.io/tools/ss58_transform?

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
