---
namespace-identifier: near-caip2
title: NEAR Protocol Namespace - Blockchain ID Specification
author: ["Billy Rennekamp (@okwme)"]
discussions-to: https://github.com/0xcounting/FAR/issues/1
status: Draft
type: Standard
created: 2026-09-14
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

Every NEAR Protocol node is configured with a `chain_id`: a human-readable string that names the network it belongs to.
The reference implementation, [nearcore][], describes this field in its own genesis schema as "ID of the blockchain. This must be unique for every blockchain."
The `near` CAIP-2 profile identifies a network by that string, used verbatim.

The `chain_id` string is NEAR's native network identifier.
[NEP-518][] also assigns [EIP-155][] chain IDs — 397 for mainnet, 398 for testnet, and 399 for any other NEAR network — so that Web3-compatible wallets can address NEAR; those integers name the same networks from the EVM side and belong to the `eip155` namespace, not to this profile.
NEAR does not derive an everyday network identifier from a genesis hash in the manner of [BIP-122][].
A genesis hash does exist and is served by the same RPC call used here, but it is 44 base58 characters and cannot be carried in a CAIP-2 reference without truncation.
The Rationale below sets out that trade-off explicitly, because a human-readable identifier is a social convention while a genesis hash is self-certifying, and readers deserve to know which property they are getting.

## Specification

### Semantics

A NEAR chain ID consists of the literal namespace `near`, a colon, and a reference equal to the network's nearcore `chain_id` string.
Two nodes reporting the same `chain_id` have the same CAIP-2 chain ID by definition.

The `chain_id` is fixed for the life of a network: it is set in the genesis configuration and is not renegotiated by consensus, upgraded by protocol version, or altered by resharding.

### Syntax

```text
chain_id:  "near:" + reference
namespace: near
reference: the nearcore chain_id string, unmodified
```

The reference must match the following regular expression, which is the [CAIP-2][] reference grammar unchanged:

```regex
^[-_a-zA-Z0-9]{1,32}$
```

The reference is the `chain_id` byte-for-byte.
No case folding, trimming, normalisation, or transliteration is applied, and the comparison is case-sensitive.

nearcore types `chain_id` as an unconstrained string, so it is possible in principle to configure a network whose `chain_id` exceeds 32 characters or contains characters outside the CAIP-2 set.
Such a network has no identifier under this profile, and an implementation MUST reject it rather than truncate or escape it.
No public NEAR network is in that position: every `chain_id` constant shipped in nearcore is at most 23 characters and draws only on lowercase letters, digits, `-`, and `_`.

### Resolution Mechanics

To resolve the chain ID reported by a NEAR JSON-RPC endpoint, call the [`status`][] method:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "status",
  "params": []
}
```

The `chain_id` field of the result is a required member of `RpcStatusResponse` and is documented there as "Unique chain id."
The following is an abbreviated response from `https://rpc.mainnet.near.org`, retrieved 2026-09-14:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "chain_id": "mainnet",
    "genesis_hash": "EPnLgE7iEq9s7yTkos96M3cWymH5avBAPm3qx3NXqR8H",
    "protocol_version": 86,
    "version": { "version": "2.13.4" }
  }
}
```

Validate `result.chain_id` against the regular expression above and prefix it with `near:`.
The example response therefore resolves to `near:mainnet`.

The same value is available from the `genesis_config` method, which returns the network's genesis configuration including `chain_id`, and from an unauthenticated `GET /status` on the same host.
`status` is preferred because it is the cheapest call, it is the first example in NEAR's own RPC introduction, and it returns `genesis_hash` alongside `chain_id` for clients that wish to corroborate (see Security Considerations).

## Rationale

### Why the `chain_id` string

The `chain_id` is the native network discriminator in NEAR: the value NEAR's own documentation uses to name its networks, the value baked into its RPC hostnames, and the only network identifier a NEAR developer encounters in ordinary work.
Using it requires no registry, no transformation, and no lookup table, and it produces identifiers — `near:mainnet`, `near:testnet` — that a reader can check at a glance.

Human-readable references have ample precedent in CASA.
`sui` uses `mainnet`, `testnet`, and `devnet`; `flow` uses `mainnet` and `testnet`; `stellar` uses `pubnet` and `testnet`; `cosmos` uses self-declared chain-id strings, and [CAIP-2][] itself gives `cosmos:cosmoshub-3` among its worked examples.
`tezos` registers `tezos:mainnet` as an alias for a hash-derived identifier and states plainly that "it is determined by social consensus what chain ID is considered as `tezos:mainnet`."

### Why not the genesis hash

NEAR does have a genesis hash, and it is a genuine alternative: a 32-byte `CryptoHash` returned as base58 in `status.genesis_hash`, stable and distinct across the two public networks.
It has a property the `chain_id` string lacks — it is self-certifying.
A client that already knows the expected genesis hash can detect a lying endpoint, whereas any endpoint can claim `"chain_id": "mainnet"` and nothing about the string contradicts it.

Three facts argue against making it the reference.

First, it does not fit.
Base58 encoding of 32 bytes yields 43 or 44 characters; both live values are 44.
A CAIP-2 reference is at most 32, so the profile would have to define a truncation, as [BIP-122][] and the `hive` namespace do.
Truncating base58 is worse than truncating hex: hex is byte-aligned, so `bip122`'s first 32 characters are exactly the first 16 bytes of the hash, whereas the first 32 characters of a base58 string correspond to no clean byte boundary and cannot be decoded independently of the discarded tail.
The truncated form would be neither the hash nor a hash of anything.

Second, NEAR's genesis is not where a reader would look for it.
Mainnet's `genesis_height` is 9820210 and testnet's is 42376888, not 0, because each network's genesis is a state snapshot rather than a bootstrapped empty chain.
A request for block `0` on either public endpoint returns `UNKNOWN_BLOCK`, verified 2026-09-14.
An implementer following the usual "hash of block 0" recipe gets an error, not an identifier.

Third, nothing is lost by not using it: `status` returns both fields, so this profile names networks by the string and leaves the hash available as corroborating evidence for clients that want it.
The result is the same split `sui` describes — a stable, legible identifier for naming, and a cryptographic digest for verification — and this profile adopts it for the same reasons.

### Why `near`

CASA names a namespace after the ecosystem.
NEAR Protocol calls itself NEAR throughout its documentation, its token ticker, its RPC hostnames, and its root account.
`near` is four characters and conforms to the CAIP-2 namespace grammar `[-a-z0-9]{3,8}`.
It is also the namespace proposed in the closed 2021 draft [CAIPs PR #43][], so adopting it preserves whatever informal use that draft seeded.

## Well-Known Networks

The following table lets clients label well-known networks without an RPC round trip.
It is informative; resolution via `status` remains authoritative.

| Network | `chain_id` | CAIP-2 chain ID | EIP-155 ID ([NEP-518][]) |
| --- | --- | --- | --- |
| NEAR mainnet | `mainnet` | `near:mainnet` | 397 |
| NEAR testnet | `testnet` | `near:testnet` | 398 |

`mainnet` and `testnet` are the two public networks described in NEAR's [networks documentation][], and both constants are defined in nearcore at [`core/primitives-core/src/chains.rs`][chains.rs].
That file also defines `mocknet`, `benchmarknet`, and `congestion_control_test`; these name internal test deployments that nobody outside can reach, so they are not listed as well-known networks, although they are valid references under this profile.
The EIP-155 column is informative and belongs to the `eip155` namespace; NEP-518's catch-all 399 is shared by every other NEAR network and so cannot discriminate between them.

The retired `betanet` appears in older material, including [CAIPs PR #43][].
Its endpoint `https://rpc.betanet.near.org` returned no response when queried on 2026-09-14 and no `betanet` constant remains in nearcore.
`near:betanet` should be treated as historical.

## Private Networks and Collisions

A NEAR `chain_id` is chosen by whoever writes the genesis configuration, and no global registry allocates it.
Two unrelated networks can therefore share a `chain_id` and collide under this profile, exactly as private networks collide in the `neo` and `cosmos` namespaces.

The failure is not hypothetical.
nearcore's helper for unconfigured local networks generates `test-chain-` followed by five random characters, so every local deployment gets a distinct identifier by default; but a developer who pins `chain_id` to `localnet` across several machines has created several distinct blockchains sharing one identifier.
nearcore's genesis schema warns about precisely this: "If your testnet blockchains do not have unique chain IDs, you will have a bad time."

Operators of private networks that must be externally distinguishable should choose a `chain_id` that is stable, is not one of the well-known values above, and is unique within their interoperability domain — which reduces the risk of collision without conferring global uniqueness.

## Backwards Compatibility

There is no previously registered CAIP-2 profile for NEAR.
[CAIPs PR #43][] proposed `near:mainnet`, `near:testnet`, `near:betanet`, and `near:guildnet` in 2021 and was closed in 2023 without merging, with a request to resubmit against the namespaces repository.
Identifiers minted against that draft for `mainnet` and `testnet` remain valid under this profile, since the reference is unchanged.

That draft resolved the `chain_id` through `EXPERIMENTAL_genesis_config` and additionally enumerated the Aurora EVM chain IDs under `eip155`.
This profile prefers the stable `status` method, and it does not claim EVM chain IDs: Aurora is a contract deployed on NEAR whose EVM-facing identifiers belong to the `eip155` namespace and are out of scope here.
The same holds for NEAR's own [NEP-518][] EIP-155 IDs: `eip155:397` and `near:mainnet` name the same network from two namespaces, and this profile defines only the second.

This profile does not change any native NEAR `chain_id` value.

## Test Cases

### Valid identifiers

| Identifier | Reason |
| --- | --- |
| `near:mainnet` | NEAR mainnet, the production network; `status.chain_id` is `"mainnet"` |
| `near:testnet` | NEAR testnet, the public pre-production network; `status.chain_id` is `"testnet"` |
| `near:mocknet` | Pre-release testing network constant defined in nearcore |
| `near:test-chain-abcde` | Shape of a nearcore-generated local network identifier |
| `near:congestion_control_test` | Longest nearcore constant, 23 characters, exercising `_` in a reference |

### Invalid identifiers

`near:Mainnet` and `near:1` are syntactically well-formed CAIP-2 strings that this profile still rejects, because no NEAR network reports those values; the rest fail the grammar outright.

| Identifier | Reason |
| --- | --- |
| `near:` | Empty reference |
| `NEAR:mainnet` | Incorrect namespace casing |
| `near:Mainnet` | Reference is case-sensitive and does not match the reported `chain_id` |
| `near: mainnet` | Leading whitespace |
| `near:mainnet.near` | `.` is not permitted in a CAIP-2 reference |
| `near:EPnLgE7iEq9s7yTkos96M3cWymH5avBAPm3qx3NXqR8H` | Genesis hash, 44 characters, exceeds the 32-character limit |
| `near:1` | No NEAR `chain_id` is numeric; NEAR's EIP-155 IDs (397, 398, 399) belong to `eip155`, not here |

## Security Considerations

Resolving a chain ID through `status` establishes only what the queried endpoint reports.
Because the reference is a self-declared string rather than a digest, a hostile or misconfigured endpoint can claim `mainnet` at no cost, and nothing in the identifier detects it.

Clients that need assurance should pin `genesis_hash` alongside the chain ID.
`status` returns both in one response, so a client can require that a chain ID be accompanied by its expected genesis hash and reject the endpoint otherwise:

| CAIP-2 chain ID | `genesis_hash` |
| --- | --- |
| `near:mainnet` | `EPnLgE7iEq9s7yTkos96M3cWymH5avBAPm3qx3NXqR8H` |
| `near:testnet` | `FWJ9kR6KFWoyMoNjpLXXGHeuiy7tEY6GmoFeCA5yuc6b` |

Both pairs were confirmed on 2026-09-14 from two independently operated providers, `rpc.*.near.org` and FastNEAR, which agreed exactly, and re-confirmed on 2026-11-11; NEAR reviewers independently confirmed them against dRPC and Intear.

Transport authentication remains the responsibility of the client.
A pinned genesis hash proves which chain an honest response describes; it does not prove the response was honest, is current, or was not replayed.

## Additional Considerations

A CAIP-10 profile for `near` will need to address one constraint this profile does not reach.
NEAR account IDs may contain `_`, which is legal in a CAIP-2 reference but is excluded from [CAIP-10][]'s `account_address` grammar `[-.%a-zA-Z0-9]{1,128}` and from [CAIP-19][]'s identical `asset_reference` grammar.
Live NEP-141 token contracts are affected: `v3.oin_finance.near` is deployed on mainnet and answers `ft_metadata` with symbol `nUSDO`.
Percent-encoding `_` as `%5F` is permitted by both CAIPs and has been confirmed by NEAR reviewers as the intended remedy (`v3.oin_finance.near` → `v3.oin%5Ffinance.near`); since account IDs are lowercase, nothing else needs normalising.
The CAIP-10 and CAIP-19 profiles that codify it are left to a follow-up, along with NEAR's three implicit and deterministic account formats.

## References

- [CAIP-2][] - Blockchain ID specification
- [CAIP-10][] - Account ID specification, whose grammar excludes `_`
- [CAIP-19][] - Asset type and ID specification, whose grammar excludes `_`
- [nearcore][] - Reference implementation of NEAR Protocol
- [chains.rs][] - nearcore constants defining `mainnet`, `testnet`, and internal test networks
- [`status`][] - JSON-RPC method returning `chain_id` and `genesis_hash`; first example in NEAR's RPC introduction
- [NEAR JSON-RPC OpenAPI][] - Machine-readable schema; `RpcStatusResponse.chain_id` is required and documented as "Unique chain id."
- [genesis_config][] - JSON-RPC method returning the genesis configuration, including `chain_id` and `genesis_height`
- [networks documentation][] - Official description of `mainnet`, `testnet`, and `localnet`, with their status endpoints
- [Nomicon: Accounts][] - Normative NEAR account ID rules
- [BIP-122][] - Precedent for a truncated genesis-hash reference
- [EIP-155][] - Precedent for a numeric chain identifier
- [NEP-518][] - Web3-compatible wallet support; assigns EIP-155 chain IDs 397 (mainnet), 398 (testnet) and 399 (other)
- [CAIPs PR #43][] - Closed 2021 NEAR CAIP-2 draft
- [namespaces issue #106][] - Open issue tracking the missing NEAR namespace

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[nearcore]: https://github.com/near/nearcore
[chains.rs]: https://github.com/near/nearcore/blob/master/core/primitives-core/src/chains.rs
[`status`]: https://docs.near.org/api/rpc/introduction
[NEAR JSON-RPC OpenAPI]: https://github.com/near/nearcore/blob/master/chain/jsonrpc/openapi/openapi.json
[genesis_config]: https://docs.near.org/api/rpc/protocol
[networks documentation]: https://docs.near.org/protocol/network/networks
[Nomicon: Accounts]: https://nomicon.io/DataStructures/Account
[BIP-122]: https://github.com/bitcoin/bips/blob/master/bip-0122.mediawiki
[EIP-155]: https://eips.ethereum.org/EIPS/eip-155
[NEP-518]: https://github.com/near/NEPs/blob/master/neps/nep-0518.md
[CAIPs PR #43]: https://github.com/ChainAgnostic/CAIPs/pull/43
[namespaces issue #106]: https://github.com/ChainAgnostic/namespaces/issues/106

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
