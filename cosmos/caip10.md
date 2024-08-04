---
namespace-identifier: cosmos-caip10
title: Cosmos Namespace - Addresses
author: Simon Warta (@webmaster128), Juan Caballero (@bumblefudge)
discussions-to: https://github.com/ChainAgnostic/CAIPs/issues/5, https://github.com/ChainAgnostic/CAIPs/issues/6, https://github.com/ChainAgnostic/CAIPs/pull/1
status: Draft
type: Standard
created: 2022-03-01
updated: 2022-03-01
requires: ["CAIP-2", "CAIP-10"]
supersedes: CAIP-5
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

Cosmos manages accounts on the "account" model rather than the UXTO model, but
uses the format for "segwit" addresses proposed in the Bitcoin codebase by
[BIP_0173][]. 

## Syntax

Valid CAIP-10 `account_id`s in this namespace are 20-byte "bech32"
(i.e. checksummed base32 expressions, as defined in [BIP_0173][])
transformations of 32-byte secp256k1 public keys, prefixed by `cosmos` for an
account address and `cosmosvaloper` for a validator address. For further
information, see the [accounts][] section of the Cosmos documentation.

These addresses can be validated with the following regular expressions, as the
hexadecimals are normalized to lowercase: `cosmos[0-9a-f]{32}` for wallet
addresses, `cosmosvaloper[0-9a-f]{32}` for validators.

## Test Cases

TODO - PR's welcome!

## References

- [ChainID tips][]: A useful thread on chainIDs on the Cosmos SDK github repo
- [IOV Core TS][]: A reference implementation of the CAIP-2 section of this specification in the IOV Core SDK
- [configuration objects][]: Tendermint core requires each chain have a unit
      genesis block and genesis block timestamp, and derives a chain ID
      (`chain_id` in their semantics) deterministically from those values; these
- [IBC]: The Inter Blockchain Communication Protocol is used to enable bridges and multi-chain compatibility between Tendermint chains
- [channels][]: The Inter-Blockchain Communication protocol establishes
      persistent "channels" between the clients of independent Cosmos-based
      blockchains; these can maintain state for assets across two chains like a
      bridged asset or smart contract.
- [ICS]: The InterChain Standards are canonically maintained in this repo, and
      cover all aspects of interop and addressing between/across Cosmos chains
      and networks; these are equivalent to BIPs, EIPs, and CAIPs.
- [IBC#517]: A GitHub thread containing a concise explanation of `chain_id` validation/constraints across Cosmos contexts 

[addresses][]: https://docs.cosmos.network/v0.42/basics/accounts.html
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