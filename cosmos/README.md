---
namespace-identifier: cosmos
title: Cosmos Namespace
---

# Namespace for Cosmos chains

This document describes the syntax and structure of the [Cosmos][] namespace,
which formalized a URI scheme for references on the broader Cosmos ecosystem.
This ecosystem includes many different kinds of blockchains, variously
interoperable and interconnected, but share the consensus rules and
[configuration objects][] of the Tendermint consensus engine.  The namespace
thus defined includes blockchains generated using the [Cosmos
SDK](https://github.com/cosmos/cosmos-sdk) such as Cosmoshub, Binance, and the
Cosmos Testnets, but also [Weave](https://github.com/iov-one/weave)-based
blockchains, like IOV.  These blockchains can have drastically different
properties and capabilities, but have certain interoperability commitments
imposed by the shared SDK and use the message-based Inter-Blockchain
Communication Protocoal (IBC) to communicate and move assets between them along
"[channels][]".

## References

- [ChainID tips][] : A useful thread on chainIDs on the Cosmos SDK github repo
- [IOV Core TS][] : A reference implementation of the CAIP-2 section of this specification in the IOV Core SDK
- [configuration objects][] : Tendermint core requires each chain have a unit
      genesis block and genesis block timestamp, and derives a chain ID
      (`chain_id` in their semantics) deterministically from those values; these
- [IBC][] : The Inter Blockchain Communication Protocol is used to enable bridges and multi-chain compatibility between Tendermint chains
- [channels][] : The Inter-Blockchain Communication protocol establishes
      persistent "channels" between the clients of independent Cosmos-based
      blockchains; these can maintain state for assets across two chains like a
      bridged asset or smart contract.
- [ICS][] : The InterChain Standards are canonically maintained in this repo, and
      cover all aspects of interop and addressing between/across Cosmos chains
      and networks; these are equivalent to BIPs, EIPs, and CAIPs.
- [IBC#517][] : A GitHub thread containing a concise explanation of `chain_id` validation/constraints across Cosmos contexts 

[addresses]: https://docs.cosmos.network/v0.42/basics/accounts.html
[IBC#517]: https://github.com/cosmos/ibc/issues/517
[IBC]: https://github.com/cosmos/ibc-go/blob/main/docs/ibc/overview.md
[ICS]: https://github.com/cosmos/ibc
[ChainID tips]: https://github.com/cosmos/cosmos-sdk/issues/5363
[channels]: https://github.com/cosmos/ibc-go/blob/main/docs/ibc/overview.md#channels
[clients]: https://github.com/cosmos/ibc-go/blob/main/docs/ibc/overview.md#clients
[configuration objects]: https://docs.tendermint.com/v0.35/tendermint-core/using-tendermint.html#fields
[IOV Core TS]: https://github.com/iov-one/iov-core/blob/1cd39e708b/packages/iov-cosmos/src/caip5.ts
[BIP_0173]: https://en.bitcoin.it/wiki/BIP_0173
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-21]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-21.md
[CAIP-22]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-22.md

## Rights

Copyright and related rights waived via CC0.
