---
namespace-identifier: neo-caip2
title: Neo Namespace - Chains
author: Erik Zhang (@erikzhang)
discussions-to: https://github.com/neo-project/proposals/issues/238
status: Draft
type: Standard
created: 2026-07-19
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

Every Neo N3 node is configured with an unsigned 32-bit Network Magic value.
The `neo` CAIP-2 profile identifies a blockchain by encoding that value as a
canonical unsigned decimal string.

## Specification

### Semantics

A Neo chain ID consists of the literal namespace `neo`, a colon, and a
reference containing the blockchain's Network Magic.
Two blockchains configured with the same Network Magic have the same CAIP-2
chain ID by definition.

### Syntax

```text
chain_id:  "neo:" + reference
namespace: neo
reference: 0 | [1-9][0-9]{0,9}
```

The reference must match the following regular expression:

```regex
^(0|[1-9][0-9]{0,9})$
```

The parsed value must additionally be in the unsigned 32-bit integer range
`0` through `4294967295`, inclusive.
The regular expression alone is not sufficient to enforce the upper bound.

The reference uses ASCII decimal digits without a sign, base prefix,
separators, surrounding whitespace, or leading zeroes.
The single value zero is encoded as `0`.
It is a valid reference and has no special meaning.

### Resolution Mechanics

To resolve the chain ID reported by a Neo N3 JSON-RPC endpoint, call the
[`getversion`][] method:

```json
{
  "jsonrpc": "2.0",
  "method": "getversion",
  "params": [],
  "id": 1
}
```

The response contains the Network Magic in `result.protocol.network`.
The following is an abbreviated response from a MainNet node:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocol": {
      "network": 860833102
    }
  }
}
```

Validate the returned value as a `uint32`, serialize it in canonical unsigned
decimal form, and prefix it with `neo:`.
The example response therefore resolves to `neo:860833102`.

## Rationale

Network Magic is the native network discriminator in Neo N3 protocol settings
and is exposed directly by the standard JSON-RPC interface.
Using it requires no additional registry or transformation and works for both
public and independently operated Neo N3 networks.

Decimal encoding matches the JSON-RPC representation and avoids multiple
textual forms for the same value, such as hexadecimal, signed, or zero-padded
representations.
The `neo` namespace identifier and decimal Network Magic reference were
supported by the Neo community in the [namespace discussion][].

## Well-Known Networks

The following table allows clients to label well-known networks without an RPC
round trip.
It is informative; the resolution method remains authoritative.

| Network | Network Magic | CAIP-2 chain ID |
| --- | ---: | --- |
| Neo N3 MainNet | `860833102` | `neo:860833102` |
| Neo N3 TestNet T5 | `894710606` | `neo:894710606` |
| NeoFS MainNet | `91414437` | `neo:91414437` |
| NeoFS TestNet | `735783775` | `neo:735783775` |

The Neo N3 values are defined by the official [MainNet configuration][] and
[TestNet configuration][].
The NeoFS values are defined by the [NeoGo network magic constants][].

## Private Networks and Collisions

Network Magic is selected by the operator of a private Neo N3 network and is
not allocated by a global registry.
If two distinct blockchains use the same Network Magic, this profile cannot
distinguish them and their CAIP-2 chain IDs collide.

Operators that require a distinguishable private-network identifier must keep
their Network Magic stable, avoid the well-known values above, and coordinate
with every other network in the interoperability domain.
Selecting a random `uint32` value and checking known deployments reduces the
risk of accidental collision but does not guarantee global uniqueness.

Development tools can reuse conventional values across isolated deployments.
For example, NeoGo defines `56753` as a default private-network magic; such a
default must not be treated as identifying one globally unique blockchain.

## Backwards Compatibility

There was no previously registered CAIP-2 profile for Neo N3.
This profile does not change Neo's native Network Magic values.

## Test Cases

### Valid identifiers

| Identifier | Reason |
| --- | --- |
| `neo:0` | Valid zero reference |
| `neo:91414437` | NeoFS MainNet |
| `neo:860833102` | Neo N3 MainNet |
| `neo:894710606` | Neo N3 TestNet T5 |
| `neo:4294967295` | Upper `uint32` boundary |

### Invalid identifiers

| Identifier | Reason |
| --- | --- |
| `neo:` | Empty reference |
| `neo:00` | Non-canonical zero |
| `neo:0860833102` | Leading zero |
| `neo:-1` | Signed value |
| `neo:+1` | Explicit sign |
| `neo:4294967296` | Above the `uint32` maximum |
| `neo:0x334f454e` | Hexadecimal representation |
| `neo:1_000` | Digit separator |
| `neo: 860833102` | Leading whitespace |
| `NEO:860833102` | Incorrect namespace casing |

## Security Considerations

Resolving a chain ID through `getversion` only establishes what the queried
endpoint reports.
It does not authenticate that endpoint or make an operator-selected Network
Magic globally unique.
Applications that rely on a trusted chain identity should use authenticated
endpoints or corroborate the result with trusted chain metadata.

## References

- [CAIP-2][] - Blockchain ID specification
- [Neo ProtocolSettings][] - Reference implementation and `uint32` Network Magic type
- [`getversion`][] - JSON-RPC method exposing `result.protocol.network`
- [MainNet configuration][] - Official Neo N3 MainNet Network Magic
- [TestNet configuration][] - Official Neo N3 TestNet T5 Network Magic
- [NeoGo network magic constants][] - NeoFS and development-network values
- [Namespace discussion][] - Neo community review of this profile

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[Neo ProtocolSettings]: https://github.com/neo-project/neo/blob/master-n3/src/Neo/ProtocolSettings.cs
[`getversion`]: https://docs.neo.org/docs/n3/reference/rpc/getversion.html
[MainNet configuration]: https://github.com/neo-project/neo-node/blob/master-n3/src/Neo.CLI/config.json
[TestNet configuration]: https://github.com/neo-project/neo-node/blob/master-n3/src/Neo.CLI/config.testnet.json
[NeoGo network magic constants]: https://github.com/nspcc-dev/neo-go/blob/master/pkg/config/netmode/netmode.go
[Namespace discussion]: https://github.com/neo-project/proposals/issues/238

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
