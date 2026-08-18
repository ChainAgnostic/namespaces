---
namespace-identifier: pinet-caip2
title: Pi Network - Blockchain ID Specification
author: Hakkyung Lee (@hklee93)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/199
status: Draft
type: Informational
created: 2026-08-19
requires: CAIP-2
---

# CAIP-2

_For context, see the [CAIP-2][] specification._

## Introduction

This document specifies the `pinet` namespace for Pi Network chain identifiers that conform to [CAIP-2][].

Pi Network operates Mainnet and Testnet as separate networks with distinct network passphrases.

## Specification

### Semantics

The `chain_id` is a human-readable identifier for a Pi Network environment.

The following references and network passphrases are defined:

| CAIP-2 chain ID | Pi Network environment | Exact network passphrase |
| --------------- | ---------------------- | ------------------------ |
| `pinet:mainnet` | Pi Network Mainnet     | `Pi Network`             |
| `pinet:testnet` | Pi Network Testnet     | `Pi Testnet`             |

Network passphrases are case-sensitive.

### Syntax

The namespace is `pinet`.

The reference is either `mainnet` or `testnet`.

The complete chain ID MUST match the following regular expression:

```regex
^pinet:(mainnet|testnet)$
```

### Resolution Mechanics

An implementation resolves a candidate Pi Network Horizon endpoint by sending an HTTP `GET` request to its root path and reading the `network_passphrase` field from the JSON response.

For example (mainnet):

```console
$ curl https://api.mainnet.minepi.com/
```

An abridged Mainnet response contains:

```json
{
  "network_passphrase": "Pi Network"
}
```

For example (testnet):

```console
$ curl https://api.testnet.minepi.com/
```

An abridged Testnet response contains:

```json
{
  "network_passphrase": "Pi Testnet"
}
```

The implementation MUST compare the returned value exactly and case-sensitively.

The implementation MUST resolve `Pi Network` to `pinet:mainnet`.

The implementation MUST resolve `Pi Testnet` to `pinet:testnet`.

The implementation MUST reject an unrecognized network passphrase instead of inferring a chain ID.

Implementations MAY use another trusted endpoint that exposes the same Horizon root response.

## Rationale

Pi Network constitutes a separate ecosystem with its own networks, governance, validators, native asset, public infrastructure, and network passphrases.

Human-readable references were selected because Pi Network's exact, case-sensitive network passphrases provide deterministic resolution.

### Backwards Compatibility

There are no previously standardized CAIP-2 identifiers for Pi Network chains.

Applications using non-standard identifiers will need to map them to `pinet:mainnet` or `pinet:testnet`.

## Test Cases

The following chain IDs are valid:

```text
pinet:mainnet
pinet:testnet
```

The following values are invalid:

```text
pi:mainnet
pinet:pubnet
pinet:Mainnet
pinet:Pi Testnet
```

`pi:mainnet` is invalid because `pi` does not satisfy the minimum namespace length required by [CAIP-2][].

The other invalid values do not match a reference defined by this specification.

## Additional Considerations

Future Pi Network environments require an update to this document and deterministic resolution mechanics before receiving a `pinet` chain reference.

## References

- [CAIP-2][] - Defines the chain-agnostic blockchain identifier format.
- [CAIP-104][] - Defines the purpose and authoring guidelines for namespace
  references.
- [Pi Whitepaper][] - Introduces the Pi Network protocol and ecosystem.
- [Pi Developer Documentation][] - Documents Pi Network application and
  blockchain integration.
- [Pi Mainnet Horizon][] - Exposes the Mainnet Horizon root response used for
  resolution.
- [Pi Testnet Horizon][] - Exposes the Testnet Horizon root response used for
  resolution.

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-104]: https://chainagnostic.org/CAIPs/caip-104
[Pi Whitepaper]: https://minepi.com/white-paper/
[Pi Developer Documentation]: https://developers.minepi.com/
[Pi Mainnet Horizon]: https://api.mainnet.minepi.com/
[Pi Testnet Horizon]: https://api.testnet.minepi.com/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
