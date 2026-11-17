---
namespace-identifier: xahau-caip2
title: Xahau Namespace - Blockchain ID Specification
author: Ekiserrepé (@Ekiserrepe)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/231
status: Draft
type: Standard
created: 2026-09-28
requires: ["CAIP-2"]
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

Xahau chains use an unsigned integer network ID to distinguish independent
networks and protect signed transactions from cross-network replay.
The CAIP-2 reference is the canonical decimal representation of this network
ID.

## Specification

### Semantics

A Xahau chain ID has the form `xahau:{network_id}`, where `network_id` is the
numeric network identifier configured by the chain and returned by the
`server_info` API method.

The currently documented public networks are:

| Network | Network ID | CAIP-2 chain ID |
| --- | ---: | --- |
| Mainnet | `21337` | `xahau:21337` |
| Testnet | `21338` | `xahau:21338` |

### Syntax

The chain reference MUST be the base-10 representation of an unsigned 32-bit
integer in the range `0` through `4294967295`, without leading zeroes.

The following regular expression validates the canonical decimal form but does
not by itself enforce the upper bound:

```regex
^(0|[1-9][0-9]{0,9})$
```

### Resolution Mechanics

To resolve the network ID, send a `server_info` request to a trusted `xahaud`
server for the target network.
For example, the following request uses the public Xahau Mainnet HTTPS endpoint:

```bash
curl --request POST "https://xahau.network" \
  --header "Content-Type: application/json" \
  --data '{"method":"server_info","params":[{}]}'
```

The response contains the network ID at `result.info.network_id`:

```json
{
  "result": {
    "info": {
      "network_id": 21337
    },
    "status": "success"
  }
}
```

The integer is rendered directly in base 10 and appended to the `xahau`
namespace prefix.

Xahau transactions include the same value in their `NetworkID` field.
This field is required on Xahau Mainnet and Testnet and prevents a signed
transaction from being replayed on another compatible network.

## Rationale

Using the protocol-native network ID makes the CAIP-2 identifier directly
resolvable through the standard server API and aligns chain selection with the
value committed to signed transactions.
Decimal encoding is canonical, compact, and requires no transformation beyond
rendering the returned unsigned integer.

### Backwards Compatibility

There are no known legacy CAIP-2 identifiers for Xahau chains.

## Test Cases

```text
# Xahau Mainnet
xahau:21337

# Xahau Testnet
xahau:21338
```

The following values are invalid:

```text
xahau:021337
xahau:-1
xahau:0x5359
xahau:4294967296
```

## References

- [CAIP-2][] - Blockchain ID specification.
- [Xahau Network Configuration][] - Official endpoints and network IDs.
- [Xahau Request Formatting][] - HTTP and WebSocket API request formats.
- [Xahau Transaction Common Fields][] - `NetworkID` requirements and replay protection.
- [xahaud][] - Open-source Xahau server implementation.

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[Xahau Network Configuration]: https://xahau.network/docs/infrastructure/installing-xahaud/
[Xahau Request Formatting]: https://xahau.network/docs/features/http-websocket-apis/request-formatting-guide/
[Xahau Transaction Common Fields]: https://xahau.network/docs/protocol-reference/transactions/transaction-common-fields/
[xahaud]: https://github.com/Xahau/xahaud

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
