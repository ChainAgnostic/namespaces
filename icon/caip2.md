---
namespace-identifier: icon-caip2
title: ICON Namespace - Blockchain ID Specification
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

Every ICON network has a network ID, universally abbreviated NID.
The NID is required in every transaction, and a transaction signed for one NID is rejected on a network with any other, so the NID is the value that binds a signed payload to a network.
The `icon` CAIP-2 profile identifies a network by encoding its NID as a canonical unsigned decimal string.

## Specification

### Semantics

An ICON chain ID consists of the literal namespace `icon`, a colon, and a reference holding the network's NID.
Two networks configured with the same NID have the same CAIP-2 chain ID by definition.

The ICON JSON-RPC renders the NID as a `0x`-prefixed hexadecimal string, because ICON's JSON-RPC v3 encodes every integer that way.
The NID is an integer value, not a string, and the hexadecimal form is a transport encoding rather than the identifier itself.
This profile therefore normalises it to decimal, which removes the case and zero-padding variation that a hexadecimal reference would allow.

### Syntax

```text
chain_id:  "icon:" + reference
namespace: icon
reference: 0 | [1-9][0-9]{0,30}
```

The reference must match the following regular expression:

```regex
^(0|[1-9][0-9]{0,30})$
```

The reference is the canonical unsigned decimal encoding of the NID.
It uses ASCII decimal digits with no `0x` prefix, sign, digit separators, surrounding whitespace, or leading zeroes.

To derive the reference from a JSON-RPC response:

1. Read the `nid` field, for example `"0x1"`.
2. Strip the `0x` prefix and parse the remainder as a hexadecimal integer.
3. Serialise that integer as decimal with no leading zeroes.

ICON has not published an upper bound for NID values, so this profile imposes none beyond the 32-character limit CAIP-2 places on references.
Every NID in public use is far smaller than that limit.

### Resolution Mechanics

To resolve the chain ID reported by an ICON JSON-RPC endpoint, call `icx_getNetworkInfo`:

```json
{
  "jsonrpc": "2.0",
  "method": "icx_getNetworkInfo",
  "params": {},
  "id": 1
}
```

The following is a verbatim response from a MainNet node at `https://ctz.solidwallet.io/api/v3`, with the block height abbreviated:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "platform": "icon",
    "nid": "0x1",
    "channel": "icon_dex",
    "earliest": "0x0",
    "stepPrice": "0x2e90edd00"
  }
}
```

Convert `result.nid` to canonical decimal and prefix it with `icon:`.
The example response therefore resolves to `icon:1`.

The `platform` field should be checked as well.
A node reporting a `platform` other than `icon` is running a different goloop-based network, and this namespace does not claim it.

## Rationale

NID is the only ICON value whose protocol purpose is to say which network a signed payload belongs to, so it is the natural CAIP-2 reference.
It requires no registry lookup, no hashing, and no truncation, and it is already the value every ICON SDK asks a developer to configure.

Decimal was chosen over ICON's native `0x`-prefixed hexadecimal because a hexadecimal reference would admit several spellings of the same network.
`0x1`, `0x01`, `0X1` and `0x001` all denote NID one, and a reference format that accepts more than one string for a network defeats the purpose of a chain ID.
Decimal has exactly one canonical form per value.
The cost is that `icon:1` does not visually match the `"0x1"` an implementer sees in a JSON-RPC response, which the derivation steps above are written to make explicit.
For the three networks in public use the digits happen to be identical either way, since `0x1`, `0x2` and `0x7` are `1`, `2` and `7`; the forms only diverge at NID ten and above.

The genesis block hash was considered and rejected.
ICON's block hashes are 32 bytes, so a hash reference would require the kind of documented truncation `bip122` and `hive` use, and it would discard the NID, which is the identifier ICON's own tooling, transactions and BTP addresses are built around.

## Well-Known Networks

The following table allows clients to label well-known networks without an RPC round trip.
It is informative; the resolution method above remains authoritative.

| Network | NID (as reported) | CAIP-2 chain ID |
| --- | --- | --- |
| ICON MainNet | `0x1` | `icon:1` |
| Lisbon test network | `0x2` | `icon:2` |
| Berlin test network | `0x7` | `icon:7` |

The MainNet value was read from two independent live endpoints, `https://ctz.solidwallet.io/api/v3` and `https://api.icon.community/api/v3`, which agreed.
The Lisbon and Berlin values are taken from the [ICON networks][] documentation; the published endpoints for both test networks did not resolve at the time of writing, so those two rows are documented but not independently confirmed by the authors.

Lisbon is the long-term-support test network and is the one to target for pre-production testing.
Berlin is the first-stage test network and is reset more aggressively.

## Private Networks and Collisions

NID is chosen by the operator of a network, not allocated by a global registry.
Local development networks conventionally run with a small NID, and every deployment started from the same local-network image shares whatever default that image ships with, so a low-valued reference may name many unrelated private chains and must not be treated as identifying one globally unique network.
If two distinct networks use the same NID, this profile cannot distinguish them and their CAIP-2 chain IDs collide.

Operators who need a distinguishable private network should pick a NID well away from the well-known values above and keep it stable.

## Backwards Compatibility

There was no previously registered CAIP-2 profile for ICON.
This profile does not change any native ICON identifier.

ICON migrated from its original loopchain node software to goloop in the ICON 2.0 upgrade.
MainNet's NID is `0x1` after that migration, as confirmed against live nodes, and the ICON documentation records no renumbering.
The test networks were replaced across and after the transition, however, so NIDs quoted for retired test networks such as Euljiro or Yeouido should not be assumed to be live.

## Test Cases

### Valid identifiers

| Identifier | Reason |
| --- | --- |
| `icon:1` | ICON MainNet |
| `icon:2` | Lisbon test network |
| `icon:7` | Berlin test network |
| `icon:0` | Valid zero reference |
| `icon:255` | Decimal form of a hypothetical NID `0xff` |

### Invalid identifiers

| Identifier | Reason |
| --- | --- |
| `icon:` | Empty reference |
| `icon:0x1` | Native hexadecimal transport form rather than canonical decimal |
| `icon:0X1` | Hexadecimal form with uppercase prefix |
| `icon:01` | Leading zero |
| `icon:00` | Non-canonical zero |
| `icon:-1` | Signed value |
| `icon:0xff` | Hexadecimal representation of 255 |
| `icon:1.icon` | BTP Network Address rather than a CAIP-2 reference |
| `icon:0x1.icon` | BTP Network Address, also containing an illegal `.` |
| `icon: 1` | Leading whitespace |
| `ICON:1` | Incorrect namespace casing |

## Additional Considerations

Some goloop-based deployments distinguish a chain's internal chain ID, CID, from its network ID, NID, and the two need not be equal.
This profile normatively uses the `nid` reported by `icx_getNetworkInfo`, because that is the value transactions are signed against.
The authors were unable to review the goloop reference implementation to describe the CID/NID relationship precisely, because the `icon-project/goloop` repository was not publicly reachable at the time of writing.
The ICON community should correct this section if the distinction matters for any network that expects to be named in this namespace.

A later CAIP-10 profile must preserve ICON's `hx` and `cx` address prefixes; see the [namespace README][].
A later CAIP-19 profile will need to cover the native coin ICX alongside ICON's IRC token standards, whose tokens are SCOREs identified by `cx` addresses.

## Security Considerations

Resolving a chain ID through `icx_getNetworkInfo` establishes only what the queried endpoint reports.
It does not authenticate the endpoint, and it does not make an operator-chosen NID globally unique.
Applications that depend on a trusted chain identity should use authenticated endpoints, or corroborate the reported NID against a known block hash on the network they expect.

## References

- [CAIP-2][] - Blockchain ID specification
- [ICON networks][] - Published NID values for MainNet, Lisbon and Berlin
- [ICON JSON-RPC v3][] - The client API, including `icx_getNetworkInfo` and the `0x`-prefixed integer encoding
- [ICON accounts][] - The `hx` and `cx` address formats referenced in the test cases
- [BTP address][] - BTP Network Addresses such as `btp://0x1.icon/hx…`, which embed the same NID
- [namespace README][] - ICON namespace overview, address prefixes, and the ICON 2.0 transition

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[ICON networks]: https://docs.icon.community/develop-on-icon-chain/networks
[ICON JSON-RPC v3]: https://docs.icon.community/develop-on-icon-chain/client-apis/json-rpc-api
[ICON accounts]: https://docs.icon.community/develop-on-icon-chain/blockchain-components/accounts
[BTP address]: https://docs.icon.community/cross-chain-communication/blockchain-transmission-protocol-btp/btp-address
[namespace README]: ./README.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
