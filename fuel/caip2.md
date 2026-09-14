---
namespace-identifier: fuel-caip2
title: Fuel Namespace - Chains
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

Every Fuel network carries a `CHAIN_ID`, an unsigned 64-bit consensus parameter
that the [Fuel specifications][] describe as "a unique per-chain identifier".
The `fuel` CAIP-2 profile identifies a network by encoding that value as a
canonical unsigned decimal string.
Fuel Ignition, the mainnet, has `CHAIN_ID` `9889`, so its chain ID is
`fuel:9889`.

`CHAIN_ID` is not only a label.
A Fuel transaction id is computed as `sha256(CHAIN_ID ++ serialized_tx)`, so the
value is mixed into the preimage that every signature commits to, and a
transaction signed for one `CHAIN_ID` cannot be replayed on a network with
another.
That is the property CAIP-2 is meant to name.

## Specification

### Semantics

A Fuel chain ID consists of the literal namespace `fuel`, a colon, and a
reference containing the network's `CHAIN_ID`.
Two networks configured with the same `CHAIN_ID` have the same CAIP-2 chain ID
by definition; see [Collisions and non-unique values][] for why this matters in
practice on Fuel.

### Syntax

```text
chain_id:  "fuel:" + reference
namespace: fuel
reference: 0 | [1-9][0-9]{0,19}
```

The reference must match the following regular expression:

```regex
^(0|[1-9][0-9]{0,19})$
```

The parsed value must additionally be in the unsigned 64-bit integer range `0`
through `18446744073709551615`, inclusive.
The regular expression alone is not sufficient to enforce the upper bound.
The maximum `uint64` is 20 digits, so every reference in this namespace fits the
CAIP-2 limit of 32 characters and no truncation rule is required.

The reference uses ASCII decimal digits without a sign, base prefix, separators,
surrounding whitespace, or leading zeroes.
The single value zero is encoded as `0`.
Hexadecimal is not used even though the GraphQL API returns most other Fuel
identifiers as `0x`-prefixed hex; `chainId` is returned as a decimal string.

### Resolution Mechanics

To resolve the chain ID reported by a `fuel-core` node, POST the following query
to its GraphQL endpoint:

```graphql
{
  chain {
    name
    consensusParameters {
      chainId
      version
    }
  }
}
```

```shell
curl -X POST https://mainnet.fuel.network/v1/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ chain { name consensusParameters { chainId version } } }"}'
```

The following is a response from the Fuel Ignition mainnet endpoint, captured on
2026-09-14:

```json
{
  "data": {
    "chain": {
      "name": "Ignition",
      "consensusParameters": {
        "chainId": "9889",
        "version": "V1"
      }
    }
  }
}
```

`chainId` is returned as a JSON string holding a decimal `uint64`.
Parse it as an unsigned 64-bit integer, reject any value that does not parse or
that falls outside the range, re-serialize it in canonical decimal form, and
prefix it with `fuel:`.
The example response therefore resolves to `fuel:9889`.

Do not use `chain.name` as the reference.
It is a display label — `"Ignition"`, `"Fuel Sepolia Testnet"`, `"Local
testnet"` — and the testnet's value contains a space, which the CAIP-2 reference
grammar does not permit.

Because consensus parameters are upgradeable on-chain, a resolved value should
be treated as the network's current identity rather than a permanent one; the
`version` field in the query above tells a client which parameter set it read.

## Rationale

`CHAIN_ID` is the only network-wide value in Fuel that is both consensus-bearing
and stable across nodes.
It is defined in the consensus parameters, it is enforced by every node through
the transaction-id preimage, it is required by every SDK when building a
transaction, and it is exposed by the standard GraphQL interface without any
derivation step.

Decimal encoding matches the node's own JSON representation and avoids a second
textual form for the same value.
A hexadecimal encoding would collide visually with Fuel's 32-byte hex
identifiers, which are a different kind of thing entirely.

The genesis block id was considered as an alternative reference.
It is globally unique where `CHAIN_ID` is not, but it is 32 bytes and would need
truncating in the manner of `polkadot` or `hive`, it is used by no Fuel tooling,
and it is not the value that gives a signature its network scope.
It is listed in the table below so that consumers can still disambiguate the
non-unique references by hand.

The namespace string `fuel` names the ecosystem, matches the protocol's own
name, and is four characters, within the CAIP-2 namespace range of three to
eight.

## Well-Known Networks

The following table lets clients label well-known networks without a round trip.
It is informative; the resolution method above remains authoritative.
Every value was read from the listed endpoint on 2026-09-14.

| Network | `chain.name` | `CHAIN_ID` | CAIP-2 chain ID | Genesis block id |
| --- | --- | ---: | --- | --- |
| Fuel Ignition mainnet | `Ignition` | `9889` | `fuel:9889` | `0x309d796214728e26d0902252db0bbde3e61d4496000b653ddc11b504bcdaea33` |
| Fuel Sepolia Testnet | `Fuel Sepolia Testnet` | `0` | `fuel:0` | `0xdd87728ce9c2539af61d6c5326c234c5cb0722b14a8c059f5126ca2a8ca3b4e2` |
| `fuel-core` local default | `Local testnet` | `0` | `fuel:0` | varies per deployment |

Both public networks report the same base asset id,
`0xf8f8b6283d7fa5b672b530cbb84fcccb4ff8dc40f8176ef4544ddb1f1952ad07`, so the
base asset id is not a network discriminator either.

## Collisions and Non-Unique Values

Fuel's `CHAIN_ID` is not allocated by a registry, and the public testnet does not
use a distinct value: as of 2026-09-14 `https://testnet.fuel.network/v1/graphql`
reports `chainId` `0`, and `chain_config.json` for `fuel-core`'s bundled
`local-testnet` chainspec also sets `"chain_id": 0`.
`fuel:0` therefore names the public testnet, every developer's local node, and
every CI fixture at once.
This profile does not paper over that: `fuel:0` is a valid identifier and it is
ambiguous.

Consumers that must distinguish these should corroborate with an out-of-band
signal — the endpoint they connected to, `chain.name`, or the genesis block id
from the table above — and must not infer "this is the public testnet" from
`fuel:0` alone.
Operators of long-lived networks should choose a `CHAIN_ID` that is not `0` and
keep it stable.

The authors would prefer that Fuel assign the public testnet a distinct
`CHAIN_ID`, which would resolve the ambiguity at the source, and flag this as
the main point on which this draft invites correction from Fuel maintainers.

## Backwards Compatibility

There was no previously registered CAIP-2 profile for Fuel.
This profile does not change Fuel's native `CHAIN_ID` values.

Fuel is not an EVM chain and must not be addressed under the `eip155` namespace,
despite using `0x`-prefixed hex identifiers.
Its ledger is UTXO-based, its assets are native 32-byte `AssetId`s rather than
contract balances, its addresses are 32 bytes rather than 20, and its
transaction-id derivation differs from Ethereum's, so an `eip155` identifier for
a Fuel network would be wrong at every layer above the chain ID.

## Test Cases

### Valid identifiers

| Identifier | Reason |
| --- | --- |
| `fuel:9889` | Fuel Ignition mainnet |
| `fuel:0` | Fuel Sepolia Testnet, and any default local node; ambiguous by design |
| `fuel:1` | Valid one-digit reference |
| `fuel:18446744073709551615` | Upper `uint64` boundary |

### Invalid identifiers

| Identifier | Reason |
| --- | --- |
| `fuel:` | Empty reference |
| `fuel:00` | Non-canonical zero |
| `fuel:09889` | Leading zero |
| `fuel:-1` | Signed value |
| `fuel:0x26a1` | Hexadecimal representation |
| `fuel:18446744073709551616` | Above the `uint64` maximum |
| `fuel:9_889` | Digit separator |
| `fuel: 9889` | Leading whitespace |
| `fuel:Ignition` | Network display name rather than `CHAIN_ID` |
| `FUEL:9889` | Incorrect namespace casing |

## Additional Considerations

A CAIP-19 profile for Fuel is a natural follow-up and is not attempted here.
The pieces are already well defined: an `AssetId` is
`sha256(CONTRACT_ID ++ SUB_IDENTIFIER)` and is rendered as 64 lowercase hex
characters, which fits the CAIP-19 `asset_reference` class
`[-.%a-zA-Z0-9]{1,128}` once the `0x` prefix is dropped or retained by
convention.
The open questions are whether to keep the `0x` prefix and how to name the base
asset, which is a consensus parameter rather than the output of a contract
deployment.

## Security Considerations

Resolving a chain ID through the GraphQL API establishes only what the queried
endpoint reports.
It does not authenticate the endpoint, and because `CHAIN_ID` is operator-chosen
and not registry-allocated, a node can report any value it likes — including
`9889`.
Applications relying on a trusted chain identity should use endpoints they trust
and, where the distinction matters, corroborate against the genesis block id.

Because consensus parameters are upgradeable by the `PRIVILEGED_ADDRESS`, a
cached chain ID can in principle go stale; clients that pin one should re-resolve
after a consensus-parameters version change.

## References

- [CAIP-2][] - Blockchain ID specification
- [Fuel specifications][] - Protocol specification set
- [Consensus parameters][] - Defines `CHAIN_ID` as `uint64`, "a unique per-chain identifier", alongside `BASE_ASSET_ID` and `PRIVILEGED_ADDRESS`
- [Transaction ID][] - `sha256(CHAIN_ID ++ serialized_tx(tx))`, the replay-protection derivation
- [Asset ID][] - `sha256(CONTRACT_ID ++ SUB_IDENTIFIER)`, for the follow-up CAIP-19 profile
- [fuel-core][] - Reference node implementation
- [Local testnet chainspec][] - `bin/fuel-core/chainspec/local-testnet/chain_config.json`, the source of the default `chain_id` of `0`
- [Fuel GraphQL API][] - The `chain` and `nodeInfo` queries used above

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[Fuel specifications]: https://github.com/FuelLabs/fuel-specs
[Consensus parameters]: https://github.com/FuelLabs/fuel-specs/blob/master/src/tx-format/consensus_parameters.md
[Transaction ID]: https://github.com/FuelLabs/fuel-specs/blob/master/src/identifiers/transaction-id.md
[Asset ID]: https://github.com/FuelLabs/fuel-specs/blob/master/src/identifiers/asset.md
[fuel-core]: https://github.com/FuelLabs/fuel-core
[Local testnet chainspec]: https://github.com/FuelLabs/fuel-core/blob/master/bin/fuel-core/chainspec/local-testnet/chain_config.json
[Fuel GraphQL API]: https://docs.fuel.network/docs/graphql/
[Collisions and non-unique values]: #collisions-and-non-unique-values

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
