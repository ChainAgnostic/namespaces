---
namespace-identifier: fuel
title: Fuel
author: ["Billy Rennekamp (@okwme)"]
discussions-to: https://github.com/0xcounting/FAR/issues/1
status: Draft
type: Informational
created: 2026-09-14
---

# Namespace for Fuel chains

Fuel is an execution layer built around the FuelVM, with contracts written in
Sway and an Ethereum L1 for data availability and settlement.
The `fuel` namespace covers networks that run `fuel-core` and expose its
GraphQL node API.
A network in the namespace is identified by its `CHAIN_ID` consensus parameter,
as specified in the [Fuel CAIP-2 profile][caip2].

Fuel is **not** an EVM chain, and the resemblance is a trap worth naming up
front.
Addresses, asset ids, contract ids and block ids are all `0x`-prefixed 32-byte
hex, which looks like Ethereum and reads like Ethereum, but almost nothing
underneath matches.
Fuel has a UTXO ledger rather than an account-balance ledger, so a wallet holds
coins that are spent and recreated.
It is natively multi-asset: every asset is a first-class 32-byte `AssetId`
carried on UTXOs, not an ERC-20 balance inside a contract's storage, and an
`AssetId` is derived as `sha256(CONTRACT_ID ++ SUB_IDENTIFIER)`.
It has *predicates*, pure stateless functions that unlock a UTXO by returning
true, which have no EVM equivalent.
An Ethereum address is 20 bytes; a Fuel `Address` is 32.
A tool that treats a Fuel identifier as an EVM one will silently truncate.

## Rationale

The reference is the network's `CHAIN_ID`, a `uint64` consensus parameter,
written in canonical decimal — `fuel:9889` for Fuel Ignition mainnet.
That value is not decorative: a Fuel transaction id is
`sha256(CHAIN_ID ++ serialized_tx)`, so `CHAIN_ID` is the domain separator that
makes a signature valid on one network and worthless on another, which is
exactly what CAIP-2 exists to name.
The alternative was the human network name (`Ignition`, `Fuel Sepolia
Testnet`), rejected because those are display labels that can be changed without
a consensus event and, in the testnet's case, contain spaces that the CAIP-2
reference grammar does not allow.

Implementers should read the collision note in the [CAIP-2 profile][caip2]
before shipping.
Fuel's testnet reports `CHAIN_ID` `0`, and so does the default `fuel-core` local
chain config, so `fuel:0` does not identify one network.
This was verified live rather than assumed, and it is the main open issue in
this draft.

This namespace was drafted by the maintainers of FAR, an open cross-reference
between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a CAIP-2 for
Fuel in order to name ETH, FUEL and the other assets issued on it.
The authors do not represent the Fuel ecosystem.
It is offered as a starting point for the Fuel community to correct, adopt or
replace, and the authors would rather it carry a maintainer's name than theirs.

## Governance

Fuel's protocol rules are maintained as the [Fuel specifications][], a versioned
document set covering the transaction format, the FuelVM, the identifier
derivations and the consensus parameters; `fuel-core` is the reference
implementation.
There is no numbered improvement-proposal series comparable to EIPs or NEPs, so
the specification repository and its pull requests are the process.

Consensus parameters, `CHAIN_ID` included, are upgradeable on-chain: an
`Upgrade` transaction signed by the `PRIVILEGED_ADDRESS` can install a new
parameter set, and a node reports the active set's version alongside its values.
A cross-chain implementer should therefore treat a network's `CHAIN_ID` as
stable in practice but not immutable by construction, and should re-resolve it
rather than hard-coding it forever.

## References

- [Fuel specifications][] - Protocol specification; `tx-format/consensus_parameters.md` defines `CHAIN_ID` as a `uint64`
- [Transaction ID][] - Shows `CHAIN_ID` acting as the signing-domain separator
- [Asset ID][] - The `sha256(CONTRACT_ID ++ SUB_IDENTIFIER)` derivation behind Fuel's native multi-asset model
- [fuel-core][] - Reference node implementation and the source of the default local chain config
- [Fuel documentation][] - Developer documentation, including the GraphQL API reference
- [Sway][] - The contract language and its predicate model

[Fuel specifications]: https://github.com/FuelLabs/fuel-specs
[Transaction ID]: https://github.com/FuelLabs/fuel-specs/blob/master/src/identifiers/transaction-id.md
[Asset ID]: https://github.com/FuelLabs/fuel-specs/blob/master/src/identifiers/asset.md
[fuel-core]: https://github.com/FuelLabs/fuel-core
[Fuel documentation]: https://docs.fuel.network/
[Sway]: https://github.com/FuelLabs/sway
[caip2]: ./caip2.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
