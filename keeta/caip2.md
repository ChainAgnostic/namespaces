---
namespace-identifier: keeta-caip2
title: Keeta - Blockchain ID Specification
author: ["@sc4l3r"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/XXXX
status: Draft
type: Standard
created: 2026-04-27
requires: CAIP-2
---

# CAIP-2

_For context, see the [CAIP-2][] specification._

## Introduction

A Keeta network -- main, test, staging, dev, or any privately-launched network -- is uniquely identified by a single non-negative integer called its `networkId`.
A privately-launched network is a private instance that runs the same Keeta protocol but with isolated transaction visibility and its own validator set; it shares the key-pair format and address encoding with the public networks but is distinguished from them solely by its `networkId`.
The same `networkId` is used by the protocol to deterministically derive the network's [Network Account][accounts] and base token address, so two networks with the same `networkId` are by construction the same network.

This profile maps that `networkId` to a [CAIP-2][] reference.

## Specification

### Semantics

The single input is a Keeta `networkId`: a non-negative integer that the protocol treats as a `bigint`.
Every Keeta network has exactly one, baked into the network's deterministic [Network Account][accounts] and base token address.

The four well-known networks shipped with the SDK ([source][sdk]) are:

| Network alias | `networkId` (decimal) | `networkId` (hex) |
| :------------ | --------------------: | :---------------- |
| `main`        |                 `21378` | `0x5382`            |
| `test`        |            `1413829460` | `0x54455354`        |
| `staging`     |               `5472769` | `0x538201`          |
| `dev`         |               `4474198` | `0x444556`          |

Privately-launched networks have their own arbitrary `networkId` values chosen by the operator.
The four `networkId` values listed above are reserved for the public networks they identify and MUST NOT be reused by private networks.

### Syntax

The CAIP-2 namespace is `keeta`. The CAIP-2 `reference` MUST be the network's `networkId`, rendered as a decimal integer with no leading zeros and no `0x` prefix:

```
keeta:<networkId>
```

The `reference` MUST match:

```
^(0|[1-9][0-9]{0,31})$
```

This is the full 32-digit cap allowed by the [CAIP-2][] reference field.

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

For a Keeta address known to be a [Network Account][accounts], the `networkId` is the value the address was generated from via `Account.generateNetworkAddress(networkId)`.
Implementations that need to validate a [CAIP-2][] string against a live network SHOULD compare the address returned by `userClient.networkAddress` to the address recomputed from the candidate `networkId`.

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
```

The four well-known networks above correspond exactly to the entries in the SDK's `NetworkIDs` table (`main`, `test`, `staging`, `dev`).

Invalid:

```
keeta:0x5382          # hex form is not permitted
keeta:021378          # leading zeros not permitted
keeta:                # empty reference
keeta:main            # symbolic aliases are not permitted
```

## References

- Keeta [accounts] - describes the Network Account and how it is derived from `networkId`.
- Keeta [SDK source][sdk] - `config/index.ts` defines `NetworkIDs` and `getNetworkAlias()`.
- Keeta [whitepaper] - protocol overview.

[accounts]: https://docs.keeta.com/components/accounts
[sdk]: https://github.com/KeetaNetwork/keetanet-client
[whitepaper]: https://keeta.com/whitepaper.pdf
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
