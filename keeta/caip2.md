---
namespace-identifier: keeta-caip2
title: Keeta - Blockchain ID Specification
author: ["@sc4l3r", "@xescure"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/183
status: Draft
type: Standard
created: 2026-04-27
requires: ["CAIP-2"]
---

# CAIP-2

_For context, see the [CAIP-2][] specification._

## Introduction

A Keeta network -- main, test, staging, dev, or any privately-launched network -- is uniquely identified by a single non-negative integer called its `networkId`.
Every network has its own set of validators and its own ledger; a privately-launched network runs the same protocol and shares the key-pair format and address encoding with the public networks, and is distinguished from them solely by its `networkId`.
The same `networkId` is used by the protocol to deterministically derive the network's [network account][accounts] and base token address, so a `networkId` identifies exactly one network.

A network may additionally host subnets, which are subordinate to it and identified together with it rather than by a `networkId` of their own; this revision of the profile does not identify subnets (see [Additional Considerations](#additional-considerations)).

This profile maps the `networkId` to a [CAIP-2][] reference.

## Specification

### Semantics

The single input is a Keeta `networkId`: a non-negative integer that the protocol treats as a `bigint`.
Every Keeta network has exactly one, baked into the network's deterministic [network account][accounts] and base token address.

The four well-known networks shipped with the SDK ([source][sdk]) are:

| Network alias | `networkId` (decimal) | `networkId` (hex) |
| :------------ | --------------------: | :---------------- |
| `main`        |                 `21378` | `0x5382`            |
| `test`        |            `1413829460` | `0x54455354`        |
| `staging`     |               `5472769` | `0x538201`          |
| `dev`         |               `4474198` | `0x444556`          |

Privately-launched networks have their own `networkId` values chosen by the operator.
There is no formal registry of `networkId` values; operators are expected to coordinate to avoid collisions, and the four values listed above are reserved for the public networks they identify and MUST NOT be reused.

The value `0` is the default `networkId` used by Keeta's SDKs for local test networks and offline fixtures, comparable to `eip155:31337`; it never identifies a public network and MUST NOT be reused by a privately-launched network.

### Syntax

The CAIP-2 namespace is `keeta`.
The CAIP-2 `reference` MUST be the network's `networkId`, rendered as a decimal integer with no leading zeros and no `0x` prefix:

```
keeta:<networkId>
```

The `reference` MUST match:

```
^(0|[1-9][0-9]{0,31})$
```

This is the full 32-digit cap allowed by the [CAIP-2][] reference field.
A `networkId` is an unbounded integer, so a network whose `networkId` exceeds 32 decimal digits cannot be identified under this profile.

### Resolution Mechanics

The `networkId` of a connected network can be obtained via the `@keetanetwork/keetanet-client` SDK:

```ts
import * as KeetaNet from "@keetanetwork/keetanet-client";

const client = KeetaNet.UserClient.fromNetwork("test", null);
const networkId = client.network; // bigint
const caip2 = `keeta:${networkId.toString(10)}`;
```

To resolve a [CAIP-2][] string back to a network alias, parse the `reference` segment as a `bigint` and pass it through the SDK's `getNetworkAlias`:

```ts
import * as KeetaNet from "@keetanetwork/keetanet-client";

const reference = "1413829460"; // from "keeta:1413829460"
const alias = KeetaNet.Client.Config.getNetworkAlias(BigInt(reference)); // "test"
```

For a Keeta address known to be a [network account][accounts], the `networkId` is the value the address was generated from via `Account.generateNetworkAddress(networkId)`.
Implementations that need to validate a [CAIP-2][] string against a live network SHOULD compare the address returned by `client.networkAddress` (on the `UserClient` above) to the address recomputed from the candidate `networkId`.

## Rationale

Keeta defines its `networkId` as a `bigint`.

Decimal was chosen for the [CAIP-2][] `reference` because:

- It matches the integer nature of the underlying value.
- It is consistent with other numeric-id [CAIP-2][] namespaces such as `eip155`.
- It avoids ambiguity around case and `0x` prefixing.

### Backwards Compatibility

This is the first [CAIP-2][] specification for the `keeta` namespace, so there are no legacy identifiers to support.

## Test Cases

```
# Main network
keeta:21378

# Test network
keeta:1413829460

# Staging network
keeta:5472769

# Dev network
keeta:4474198

# Example private network with an arbitrary numeric id
keeta:9000001

# Local test network (SDK default; see Semantics)
keeta:0
```

The four well-known networks above correspond exactly to the entries in the SDK's `NetworkIDs` table (`main`, `test`, `staging`, `dev`).

Invalid:

```
keeta:0x5382          # hex form is not permitted
keeta:021378          # leading zeros not permitted
keeta:                # empty reference
keeta:main            # symbolic aliases are not permitted
```

## Additional Considerations

### Subnets

A Keeta block carries an optional subnet identifier alongside its `networkId`, and a ledger is scoped to one network and one subnet.
Each subnet belongs to exactly one network, and a network may host many subnets, so a subnet is identified by its network together with its own subnet identifier rather than by a `networkId` of its own.
This revision of the profile identifies networks only.
A future revision will identify subnets as `keeta:<networkId>-<subnetId>` once they are publicly deployed; `-` is a permitted character in a [CAIP-2][] reference.

## References

- Keeta [accounts] - describes the network account and how it is derived from `networkId`.
- Keeta [SDK package][sdk] - `config/index.d.ts` declares `NetworkIDs` and `getNetworkAlias()`.
- Keeta [whitepaper] - protocol overview.

[accounts]: https://docs.keeta.com/components/accounts
[sdk]: https://www.npmjs.com/package/@keetanetwork/keetanet-client
[whitepaper]: https://keeta.com/whitepaper.pdf
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
