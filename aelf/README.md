---
namespace-identifier: aelf
title: aelf
author: ["Billy Rennekamp (@okwme)"]
discussions-to: https://github.com/0xcounting/FAR/issues/1
status: Draft
type: Informational
created: 2026-09-14
---

# Namespace for aelf blockchains

aelf is a layer-1 blockchain built around a main chain and a set of side chains, each of which is a full blockchain with its own block production, its own state, and its own chain ID.
The main chain indexes the side chains and carries cross-chain verification, so a side chain is a first-class member of the network rather than a rollup or a bridge deployment.
The `aelf` namespace covers chains that run the aelf node software and expose its HTTP chain API.
Individual chains in the namespace are identified by their chain ID, as specified in the [aelf CAIP-2 profile][].

An implementer's first surprise is that "the aelf chain" is not one chain.
Production traffic is split between the main chain `AELF` and the side chain `tDVV`, which have separate balances, separate contracts, and separate transaction histories, connected by cross-chain transfers.
Any integration that treats aelf as a single network will silently lose half of it.

## Token identity is a symbol, not an address

This is the most important thing to know before writing an aelf integration, and it is where the EVM mental model breaks hardest.

On an EVM chain, each fungible token is its own contract, so a token's contract address is its identity, and CAIP-19 can use that address as the asset reference.
aelf does not work this way.
Every fungible token, every NFT collection, and the native ELF coin all live inside a single **MultiToken** system contract that is deployed once per chain.
A token is created by calling `Create` on that contract with a symbol, and from then on the token's identity is the **symbol** — `ELF`, `USDT`, and so on — used as a key inside that one contract's state.
There is no per-token contract and no per-token address to point at.

The practical consequence is blunt.
On aelf MainChain, every token in existence shares the contract address `JRmBduh4nXWi1aXgdUsj5gJrzeZb2LxmrAbf7W99faZSvoAaE`, and on the `tDVV` side chain every token shares `7RzVGiuVWkvL4VfVHdZfQF2Tri3sgLe9U991bohHFfSRZXuGX`.
Both were confirmed against live nodes for this document: each address returns a contract descriptor set containing `token_contract.proto` and the `MultiToken` service.
A cross-reference project that keyed aelf assets by contract address, as it would for an EVM chain, found every aelf token collapsing onto the same key.
That failure is the direct motivation for writing this namespace down.

A CAIP-19 profile for this namespace must therefore key fungible assets on `(chain ID, symbol)`, not on a contract address.
The asset namespace should encode the symbol, and the MultiToken contract address should appear at most as context, never as the discriminator.
Note also that symbols are unique per chain, not across chains: the same symbol may exist on both `AELF` and `tDVV` as separate token entries whose supplies are connected only by explicit cross-chain transfers.

## Addresses

An aelf address is a plain base58 string with no prefix, derived by hashing a public key.
aelf tooling and explorers frequently display addresses in a decorated form, `ELF_<base58 address>_<chain ID>`, for example `ELF_JRmBduh4nXWi1aXgdUsj5gJrzeZb2LxmrAbf7W99faZSvoAaE_AELF`.
That decorated form is a display convention that embeds the chain ID, not a distinct address type; the on-chain value is the bare base58 string in the middle.
An implementer should accept both forms on input, store the bare form, and note that the trailing segment of the decorated form is exactly the CAIP-2 reference this namespace defines.

Unlike ICON or Massa, aelf addresses do not distinguish contracts from wallets by prefix.
Both are the same shape, and telling them apart requires querying the chain.

## Rationale

`aelf` is the ecosystem's own name, is four characters long, and is all lowercase, so it satisfies the CAIP-2 namespace production `[-a-z0-9]{3,8}` without modification.
The project styles its name in lowercase, which happens to match what CAIP-2 requires.

`aelf:AELF` looks like a stutter, and it is worth being explicit about why it is not.
The lowercase `aelf` is the namespace, naming the ecosystem.
The uppercase `AELF` is the reference, naming one specific chain in it — the main chain — and it is spelled that way because a chain ID in aelf is a short base58 string that the main chain's was deliberately chosen to spell.
The side chains read `tDVV` and `tDVW`, so the apparent duplication disappears as soon as a second chain is named.

This namespace was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a CAIP-2 for this chain in order to name the assets that exist on it.
The authors do not represent the aelf ecosystem.
It is offered as a starting point for the aelf community to correct, adopt or replace, and the authors would rather it carry a maintainer's name than theirs.

## Governance

aelf's protocol is developed in the open in the [aelf reference implementation][].
Contract-level standards are published as aelf Contract Standards, numbered ACS0 through ACS12, covering deployment, transaction fees, parallel execution, proposals, consensus, and cross-chain behaviour; the [ACS introduction][] indexes them.

Governance is executed on chain by three system contracts rather than off chain.
The Parliament contract lets the elected block producers approve proposals, the Association contract lets a fixed set of members do so, and the Referendum contract lets token holders vote.
Contract deployments and upgrades themselves run through this machinery via ACS0, which means the set of deployed system contracts on a given chain is a governance outcome.
Block producers are elected by staked voting through the Election contract.

## References

- [aelf documentation][] - Concepts, node operation, and the chain API
- [aelf reference implementation][] - The C# node, and the source of the chain ID encoding
- [aelf chain ID helper][] - `ChainHelper`, the normative chain ID encoding and decoding
- [MultiToken contract][] - The shared token contract and its symbol-keyed model
- [ELF token][] - Published MultiToken contract addresses for `AELF` and `tDVV`
- [aelf addresses][] - Address derivation and encoding
- [aelf cross-chain][] - Main chain and side chain architecture
- [ACS introduction][] - aelf Contract Standards index
- [aelf governance][] - On-chain governance model
- [aelf CAIP-2 profile][] - The chain ID specification in this namespace

[aelf documentation]: https://docs.aelf.com/
[aelf reference implementation]: https://github.com/AElfProject/AElf
[aelf chain ID helper]: https://github.com/AElfProject/AElf/blob/dev/src/AElf.Types/Helper/ChainHelper.cs
[MultiToken contract]: https://docs.aelf.com/tools/smart-contract-api/multi-token-contract/
[ELF token]: https://docs.aelf.com/about-aelf/elf-token/
[aelf addresses]: https://docs.aelf.com/learn/addresses/
[aelf cross-chain]: https://docs.aelf.com/learn/cross-chain/introduction/
[ACS introduction]: https://docs.aelf.com/learn/acs-introduction/
[aelf governance]: https://docs.aelf.com/about-aelf/governance/
[aelf CAIP-2 profile]: ./caip2.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
