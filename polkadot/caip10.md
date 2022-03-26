---
namespace-identifier: polkadot-caip10
title: Polkadot Namespace - Addresses
author: ["Pedro Gomes (@pedrouid)", "Joshua Mir (@joshua-mir)", "Shawn Tabrizi (@shawntabrizi)", "Juan Caballero (@bumblefudge)"]
discussions-to: https://github.com/ChainAgnostic/CAIPs/issues/13
status: Draft
type: Standard
created: 2020-04-01
updated: 2020-04-02
requires: ["CAIP-2", "CAIP-10"]
supersedes: CAIP-13
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

Polkadot addresses can be expressed a number of ways, but the default form is a
base58 [multiaddress][] with a human-readable prefix of one or more characters.
The specification defining these across the entire Polkadot namespace is
[SS58][]; this specification summarizes the calculation of an address as
`base58encode ( concat ( <address-type>, <address>, <checksum> ) )`, where
`<address-type>` is a prefix registered in the [SS58 registry][] and where
`<checksum>` options are constrained by targeted output-length.

While the above describes a given keypair as generating many addresses per
network, a 47-character multiaddress is the default expression, unique per
chain.  Note that a single private key will thus produce different
multiaddresses on each chain where it is used, so de-duplicating accounts in a
multi-Polkadot context requires implementing full support for advanced SS58
functions.

As the default multi-address was used to express individual addresses in
CAIP-10, other possible expressions are out of scope of this specification.
Similarly, recovery of chain ID from account type or validation of addresses
using the included checksum are out of scope, although both are specified in
[SS58][].

## Syntax

As the default/standard expression of an address in Polkadot is a 47-character
base58 string, the following regular expression can be used for validating
addresses:

```
[1-9A-HJ-NP-Za-km-z]{47}
```

## Test Cases

This is a list of examples composed using the [polkadot.subscan tool][]:

```
# Kusama
//example address from [Polkadot-ENS tutorial][]:
polkadot:b0a8d493285c2df73290dfb7e61f870f:CpjsLDC1JFyrhm3ftC9Gs4QoyrkHKhZKtK7YqGTRFtTafgp

//one address in multiple network-specific expressions, taken from the [Polkadot address explainer][]:

# Underlying Public Key:
0x54a0lf789elcflcf69da4010f7001dfaea8e4166656f332ebb5b38ec85704811

# Kusama (coordination chain; address-type prefix 0)
polkadot:b0a8d493285c2df73290dfb7e61f870f:EVH78gP5ATklKjHonVpxM8c1W6rWPKn5cAS14fXn4Ry5NxK

# Edgeware (address-type prefix 7)
polkadot:742a2ca70c2fda6cee4f8df98d64c4c6:jRaQ6PPzcqNnckcLStwqrTjEvpKnJUP2Jw65Ut36LQQUycd

# Kulupu (address-type prefix 16)
polkadot:37e1f8125397a98630013a4dff89b54c:2dWWj2G2TEhvC9PnVEpAExrZ4J6yGx94imvGcdfkG2ko1u6x
```

## References

- [Polkadot documentation][]: Homepage for ecosystem-wide developer documentation
- [Polkadot-ENS tutorial][]: A tutorial for native Kusama address support in the ENS front-end
- [Polkadot public RPC endpoints][]: for dev/testing purposes
- [Polkadot identity system][]: Introduction to on-chain identity registrars 
- [Polkadot address explainer][]: A quick overview of how network-specific,
      self-describing addresses can derive from the same private key
- [Polkadot subscan tool][]: A tool for transforming addresses according to SS58 across polkadot networks

[Polkadot address explainer]: https://www.quora.com/How-do-different-wallet-addresses-work-on-Polkadot-and-Kusama
[Polkadot identity system]: https://wiki.polkadot.network/docs/learn-identity
[Polkadot public RPC endpoints]: https://wiki.polkadot.network/docs/maintain-endpoints
[Polkadot documentation]: https://wiki.polkadot.network/
[Polkadot subscan tool]: https://polkadot.subscan.io/tools/ss58_transform?
[Polkadot-ENS tutorial]: https://wiki.polkadot.network/docs/ens
[SS58]: https://docs.substrate.io/v3/advanced/ss58/
[SS58 registry]: https://github.com/paritytech/ss58-registry/blob/main/ss58-registry.json
[multiaddress]: https://github.com/multiformats/multiaddr#specification
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-21]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-21.md
[CAIP-22]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-22.md
[EIP155]: https://eips.ethereum.org/EIPS/eip-155
[ERC20]: https://eips.ethereum.org/EIPS/eip-20
[ERC721]: https://eips.ethereum.org/EIPS/eip-721

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
