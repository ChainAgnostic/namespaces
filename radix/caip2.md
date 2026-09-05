---
namespace-identifier: radix-caip2
title: Radix DLT Namespace - Chains
author: ["Avaunt (@AVaunt-consulting)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/198
status: Draft
type: Standard
created: 2026-08-01
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

Radix Babylon networks are few and centrally registered: one production
mainnet and a small set of persistent test networks. Each network is defined
in the node software by three coupled identifiers: a numeric **network ID**
(`1` for mainnet, `2` for Stokenet), a **logical name** (`mainnet`,
`stokenet`), and an **HRP network specifier** used inside every address on
that network (`rdx`, `tdx_2_`).

This profile uses the **logical name** as the CAIP-2 reference. The logical
name is the identifier integrators already pass in the `network` field of
every Core API request, it is human-readable, and the set of networks is
small and governed, so collisions are not a practical concern (the same
reasoning used by the `hedera` and `stellar` namespaces).

## Syntax

The reference SHOULD be populated with one of the following enumerated
logical network names:

- `mainnet` — Radix mainnet (network ID `1`)
- `stokenet` — the primary public testnet (network ID `2`)

Other logical names defined by the node software (e.g. transient test
networks with HRP specifier `tdx_<hex_id>_`, or `simulator` for the local
`resim` simulator, network ID `242`) follow the same pattern.

A regular expression for validating any theoretically possible Radix
network reference is:

```
radix:[a-z0-9]{1,32}
```

### Resolution Method

To resolve the network of a node or gateway, query its network configuration
endpoint and compare the returned logical name and network ID:

- Gateway API: `POST /status/network-configuration`
- Core API (own node): `POST /core/status/network-configuration`

Example response (mainnet gateway, abbreviated):

```json
{
  "network_id": 1,
  "network_name": "mainnet",
  "well_known_addresses": {
    "xrd": "resource_rdx1tknxxxxxxxxxradxrdxxxxxxxxx009923554798xxxxxxxxxradxrd"
  }
}
```

Addresses themselves are also network-bound: every bech32m address embeds the
network's HRP specifier (`rdx`, `tdx_2_`), and its 6-character checksum is
computed over the HRP, so an address valid on one network is invalid on every
other network.

## Backwards Compatibility

The retired Olympia network generation (2021–2023) used different address
formats and APIs; its end state was migrated into Babylon's genesis. Olympia
is not addressable in this namespace.

## Test Cases

This is a list of manually composed examples:

```
# Radix mainnet
radix:mainnet

# Radix Stokenet (primary public testnet)
radix:stokenet
```

## Additional Considerations

### Rejected idea: numeric network-ID references

Using the numeric network ID as the reference (`radix:1`, `radix:2`) was
considered and rejected: the logical name is what Radix APIs accept in
request bodies, what node configuration files use, and what integrators see
in documentation, whereas the numeric ID appears mainly inside transaction
headers. Both identifiers are listed in the table in the
[namespace README](README.md) so either can be derived from the other.

## References

- [Radix Networks][] - network IDs, logical names, gateway URLs and native addresses per network.
- [Well-Known Addresses][] - canonical per-network address registry including `network_id` and `network_hrp_suffix`.
- [Gateway API][] - `/status/network-configuration` endpoint documentation.
- [Core API][] - node-local equivalent for integrators running their own node.

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[Radix Networks]: https://docs.radixdlt.com/docs/network-setup
[Well-Known Addresses]: https://docs.radixdlt.com/docs/well-known-addresses
[Gateway API]: https://radix-babylon-gateway-api.redoc.ly/
[Core API]: https://radix-babylon-core-api.redoc.ly/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
