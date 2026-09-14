---
namespace-identifier: cardano-caip2
title: Cardano Namespace - Blockchain ID Specification
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

Every Cardano network is configured with two identifiers in its genesis files.
The **network magic** is an unsigned 32-bit number exchanged during the node-to-node handshake; nodes configured with different magics will not peer with each other.
The **network id** is a 4-bit value that appears in the header byte of every non-Byron address and distinguishes mainnet from any test network.

The `cardano` CAIP-2 profile identifies a blockchain by both values, joined by a hyphen, in the order and encoding already defined by Cardano's [CIP-34][].
Mainnet is therefore `cardano:1-764824073`.

The network magic is the component that carries uniqueness: the network id has only 16 possible values and cannot, for example, tell the preprod and preview test networks apart, since both use `0`.
The network id is retained because it is canonical, cheap, and lets an implementation check an address against a chain id without a second lookup — an address whose network tag is `0` cannot belong to a chain whose reference begins `1-`.

## Specification

### Semantics

A Cardano chain ID consists of the literal namespace `cardano`, a colon, and a reference composed of the network's network id and network magic separated by a hyphen.
Both values are taken from the network's own genesis configuration, not chosen by the implementer.
Two blockchains configured with the same network id and network magic have the same CAIP-2 chain ID by definition.

### Syntax

```text
chain_id:      "cardano:" + reference
namespace:     cardano
reference:     network_id + "-" + network_magic
network_id:    0 | [1-9] | 1[0-5]
network_magic: 0 | [1-9][0-9]{0,9}
```

The reference must match the following regular expression:

```regex
^(0|[1-9]|1[0-5])-(0|[1-9][0-9]{0,9})$
```

The parsed `network_magic` must additionally be in the unsigned 32-bit integer range `0` through `4294967295`, inclusive.
The regular expression alone is not sufficient to enforce that upper bound.

Both components use ASCII decimal digits without a sign, base prefix, separators, surrounding whitespace, or leading zeroes.
The value zero is encoded as `0` in either position.

The reference is at most 13 characters long, for the widest possible values `15-4294967295`, and so always fits CAIP-2's 32-character limit.
The alternative native identifier, the genesis hash, is 32 bytes and would need truncation; it is not used here.

### Resolution Mechanics

Both components are read from the network's Shelley genesis configuration, which every node loads at startup.

For a self-hosted node, read `networkMagic` and `networkId` from the Shelley genesis file named by `ShelleyGenesisFile` in the node's configuration.
The [mainnet Shelley genesis][] contains:

```json
{
  "networkMagic": 764824073,
  "networkId": "Mainnet",
  "systemStart": "2017-09-23T21:44:51Z"
}
```

For a remote endpoint, the same values are served by the [Koios `/genesis`][] endpoint:

```console
$ curl -s https://api.koios.rest/api/v1/genesis
```

```json
[
  {
    "networkmagic": "764824073",
    "networkid": "Mainnet",
    "systemstart": 1506203091
  }
]
```

The genesis files spell `networkId` as a name rather than a number.
Map it to the numeric network tag defined by [CIP-19][]: `Testnet` is `0` and `Mainnet` is `1`.
Then serialize both values in canonical unsigned decimal form, join them with `-`, and prefix with `cardano:`.
The response above therefore resolves to `cardano:1-764824073`.

A wallet connected over [CIP-30][] exposes only `api.getNetworkId()`, which returns the network id alone.
That is not sufficient to construct a chain ID, because it cannot distinguish two test networks; pair it with the magic reported by the wallet's backend or by an endpoint as above.

## Rationale

The `NetworkId-NetworkMagic` reference is adopted unchanged from [CIP-34][], which is the only standardized chain identifier Cardano has defined for itself and which was written with CAIP-2 integration as a stated goal.
Reusing it means every value already published in the [CIP-34 registry][] and emitted by its reference implementation transfers without recomputation.

CIP-34 rejected the two obvious single-value alternatives for reasons that still hold: the network id alone offers only 16 possibilities, and the genesis hash is 64 hex characters, which is both unfriendly and over CAIP-2's reference limit.
The network magic alone would in practice be unique, and an implementation that only ever compares whole chain IDs would behave identically under either scheme.
Retaining the pair keeps continuity with CIP-34, preserves the address cross-check described above, and avoids test network identifiers as opaque as `cardano:1` and `cardano:2`.

Because both components come from the same genesis configuration, there is exactly one correct reference for any given network, and an implementation cannot produce two chain IDs for one chain by choosing a different network id.

Decimal encoding matches the genesis and API representations and avoids multiple textual forms for the same value, such as hexadecimal, signed, or zero-padded representations.

## Legacy

CIP-34 specifies its own human-readable form as `cip34:NetworkId-NetworkMagic`, and that prefix is in circulation: the reference implementation [cip34-js][] documents `cip34:1-764824073` and `cip34:0-1`, and third-party code accepts those strings where a CAIP-2 identifier is expected.
No `cip34` namespace has ever been registered with CASA, so these are unregistered identifiers rather than a superseded registration.

Implementations that need to accept them should treat `cip34:` as an input alias for `cardano:` and normalize to `cardano:` on output.
The reference is byte-identical across the two prefixes, so the mapping is a prefix substitution in both directions and no registry data changes.
The Cardano community may of course prefer to register `cip34` instead; this profile can be renamed without any change to the reference format or to the test cases below.

## Backwards Compatibility

There was no previously registered CAIP-2 profile for Cardano.
This profile does not change Cardano's native network id or network magic values, and it does not change CIP-34's reference format.

## Test Cases

### Valid identifiers

| Identifier | Reason |
| --- | --- |
| `cardano:1-764824073` | Cardano mainnet |
| `cardano:0-1` | Preprod test network, which mirrors mainnet's five-day epochs |
| `cardano:0-2` | Preview test network, which runs shorter one-day epochs for faster testing |
| `cardano:0-1097911063` | The legacy public testnet, retired but listed by CIP-34 for historical records |
| `cardano:15-4294967295` | Upper boundary of both components |

### Invalid identifiers

| Identifier | Reason |
| --- | --- |
| `cardano:764824073` | Network magic without the network id |
| `cardano:1` | Network id without the network magic |
| `cardano:` | Empty reference |
| `cardano:1-0764824073` | Leading zero in the network magic |
| `cardano:01-764824073` | Leading zero in the network id |
| `cardano:16-764824073` | Network id above the 4-bit maximum |
| `cardano:1-4294967296` | Network magic above the `uint32` maximum |
| `cardano:-1-764824073` | Signed network id |
| `cardano:1_764824073` | Wrong separator |
| `cardano:1-0x2d964a09` | Hexadecimal network magic |
| `cardano: 1-764824073` | Leading whitespace |
| `Cardano:1-764824073` | Incorrect namespace casing |
| `cardano:5f20df933584822601f9e3f8c024eb5e` | Truncated genesis hash rather than the specified reference |

## Well-Known Networks

The following table allows clients to label well-known networks without a round trip.
It is informative; the resolution method above remains authoritative.

| Network | Network id | Network magic | CAIP-2 chain ID |
| --- | ---: | ---: | --- |
| Mainnet | `1` | `764824073` | `cardano:1-764824073` |
| Preprod | `0` | `1` | `cardano:0-1` |
| Preview | `0` | `2` | `cardano:0-2` |
| Legacy testnet (retired) | `0` | `1097911063` | `cardano:0-1097911063` |

These values are those of the [CIP-34 registry][], and the mainnet pair was confirmed against the [mainnet Shelley genesis][] in the `cardano-node` repository.
The mainnet, preprod, and preview pairs were each confirmed against a live [Koios `/genesis`][] response on 2026-09-14.
The legacy testnet is no longer served by a public endpoint, so its pair is cited from the registry only.

## Security Considerations

Resolving a chain ID from an endpoint only establishes what that endpoint reports.
It does not authenticate the endpoint, and a network magic is chosen by whoever launches a network rather than allocated by a registry, so a private or forked network may deliberately or accidentally reuse a well-known pair.
Applications that rely on a trusted chain identity should use authenticated endpoints, or corroborate the result against the network's genesis hash — `5f20df933584822601f9e3f8c024eb5eb252fe8cefb24d1317dc3d432e940ebb` for mainnet — which is recorded in the [CIP-34 registry][] and is collision-resistant where the magic is not.

Operators of private networks that must remain distinguishable should keep their magic stable, avoid the well-known values above, and coordinate with every other network in the same interoperability domain.

## References

- [CAIP-2][] - Blockchain ID specification
- [CIP-34][] - Chain ID Registry, defining the `NetworkId-NetworkMagic` format
- [CIP-34 registry][] - Machine-readable network id, network magic, and genesis hash for each network
- [CIP-19][] - Cardano addresses, defining the network tag values `0` for testnets and `1` for mainnet
- [CIP-30][] - dApp-wallet bridge, whose `getNetworkId()` returns the network id alone
- [mainnet Shelley genesis][] - Official `networkMagic` and `networkId` for mainnet
- [mainnet node configuration][] - Names the genesis files and records their hashes
- [Koios `/genesis`][] - Public endpoint returning network magic and network id per network
- [cip34-js][] - Reference implementation of CIP-34 chain IDs

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CIP-34]: https://cips.cardano.org/cip/CIP-34
[CIP-34 registry]: https://github.com/cardano-foundation/CIPs/blob/master/CIP-0034/registry.json
[CIP-19]: https://cips.cardano.org/cip/CIP-19
[CIP-30]: https://cips.cardano.org/cip/CIP-30
[mainnet Shelley genesis]: https://github.com/IntersectMBO/cardano-node/blob/master/configuration/cardano/mainnet-shelley-genesis.json
[mainnet node configuration]: https://github.com/IntersectMBO/cardano-node/blob/master/configuration/cardano/mainnet-config.json
[Koios `/genesis`]: https://api.koios.rest/api/v1/genesis
[cip34-js]: https://github.com/dcSpark/cip34-js

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
