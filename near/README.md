---
namespace-identifier: near
title: NEAR Protocol
author: ["Billy Rennekamp (@okwme)"]
discussions-to: https://github.com/0xcounting/FAR/issues/1
status: Draft
type: Informational
created: 2026-09-14
---

# Namespace for NEAR Protocol chains

NEAR Protocol is a sharded, proof-of-stake smart contract platform whose reference implementation is [nearcore][].
The `near` namespace covers networks running the NEAR Protocol and exposing its standard JSON-RPC interface.
Individual networks in the namespace are identified by their nearcore `chain_id` as specified in the [NEAR CAIP-2 profile](./caip2.md).

## What is different from EVM chains

Three things surprise developers arriving from an EVM chain, and all three matter for CAIP implementers.

**Networks are named, not numbered.**
There is no EIP-155-style integer and no chain identifier derived from a genesis hash in everyday NEAR tooling.
A node is configured with a `chain_id` string — `mainnet`, `testnet` — and that string is what wallets, SDKs, and RPC endpoints switch on.
A genesis hash exists and is served by the same RPC call, but it is 44 base58 characters, which does not fit a CAIP-2 reference; the [CAIP-2 profile](./caip2.md) discusses that trade-off in detail.

**Accounts are named, and contracts live at accounts.**
A NEAR account ID is a human-readable name such as `alice.near`, between 2 and 64 characters, built from lowercase alphanumeric parts separated by `.`, `_`, or `-`.
Names are hierarchical like domain names: only `near` can create `alice.near`, and only `alice.near` can create `app.alice.near`.
There are also implicit accounts, whose ID is derived from a key rather than registered: a NEAR-implicit account ID is the 64-character lowercase hex encoding of an ED25519 public key, and an ETH-implicit account ID is `0x` followed by 40 lowercase hex characters.
Crucially, an account and a contract are the same object.
Deploying a contract does not mint a new address — it attaches code to an existing account, which continues to hold a balance, keys, and storage.
There is no separate "contract address" concept to map onto, so a CAIP-10 profile for `near` describes accounts and contracts with one syntax.

**Tokens are addressed by account ID.**
A [NEP-141][] fungible token is identified by the account ID of the contract that implements it, not by a `0x` address.
`wrap.near` is wrapped NEAR, `token.v2.ref-finance.near` is REF, `usdt.tether-token.near` is USDt, and `token.sweat` is SWEAT — note that the last one is not under the `near` top-level account at all.

A future CAIP-19 profile for this namespace must confront one concrete obstacle.
[CAIP-19][] restricts `asset_reference` to `[-.%a-zA-Z0-9]{1,128}`, and [CAIP-10][] restricts `account_address` to the same character set.
Neither permits `_`, which is legal inside a NEAR account ID and is in live use: `v3.oin_finance.near` is a deployed NEP-141 contract whose `ft_metadata` call returns symbol `nUSDO`.
Percent-encoding `_` as `%5F` is permitted by both CAIPs and is the obvious candidate, but it is a decision for whoever writes those profiles and is deliberately left open here.
This document scopes itself to CAIP-2 and flags the constraint rather than pre-empting it.

## Rationale

The namespace is named after the ecosystem, `near`, which is the name NEAR Protocol uses for itself throughout its documentation, its RPC hostnames, its token, and its root account.
It is four characters and satisfies the CAIP-2 namespace grammar `[-a-z0-9]{3,8}`.
The `near` string was also the namespace proposed in a 2021 draft, [CAIPs PR #43][], by authors from the NEAR and Ceramic communities.
That PR was closed in 2023 with a request to resubmit against the namespaces repository, and [namespaces issue #106][] has tracked the absence since 2024.
This draft picks up that thread; it does not claim continuity of authorship with it, and it differs from it in scope and in resolution method.

This namespace was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a CAIP-2 for this chain in order to name 72 assets that exist on it.
The authors do not represent the NEAR ecosystem.
It is offered as a starting point for the NEAR community to correct, adopt or replace, and the authors would rather it carry a maintainer's name than theirs.

## Governance

Protocol and contract standards for NEAR are proposed as NEAR Enhancement Proposals.
[NEP-0001][] defines the process, the roles of the Protocol and Contract Standards Working Groups, and the requirement that a proposal reach working-group approval before it is marked Final.
Fungible tokens are standardised this way as [NEP-141][], with metadata in NEP-148 and storage in NEP-145.

The `chain_id` values themselves are not governed by a NEP.
They are constants in [nearcore][], the reference implementation, and are shipped in the genesis configuration each network's operators run.
Changing the `chain_id` of an existing public network would be a hard fork of its identity and has not happened for `mainnet` or `testnet`.

## References

- [NEAR documentation][] - Developer documentation, RPC reference, and protocol concepts
- [NEAR networks][] - Official description of `mainnet`, `testnet`, and `localnet`
- [nearcore][] - Reference implementation; `core/primitives-core/src/chains.rs` holds the `chain_id` constants
- [Nomicon: Accounts][] - Normative account ID rules, the validity regex, and implicit account derivation
- [NEP-0001][] - NEAR Enhancement Proposal process and working groups
- [NEP-141][] - Fungible token standard; tokens are addressed by contract account ID
- [CAIP-2][] - Blockchain ID specification
- [CAIP-10][] - Account ID specification, whose `account_address` grammar excludes `_`
- [CAIP-19][] - Asset type and ID specification, whose `asset_reference` grammar excludes `_`
- [CAIPs PR #43][] - Closed 2021 draft of a NEAR CAIP-2, the prior art for the `near` namespace
- [namespaces issue #106][] - Open issue tracking the missing NEAR namespace

[NEAR documentation]: https://docs.near.org
[NEAR networks]: https://docs.near.org/protocol/network/networks
[nearcore]: https://github.com/near/nearcore
[Nomicon: Accounts]: https://nomicon.io/DataStructures/Account
[NEP-0001]: https://github.com/near/NEPs/blob/master/neps/nep-0001.md
[NEP-141]: https://github.com/near/NEPs/blob/master/neps/nep-0141.md
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[CAIPs PR #43]: https://github.com/ChainAgnostic/CAIPs/pull/43
[namespaces issue #106]: https://github.com/ChainAgnostic/namespaces/issues/106

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
