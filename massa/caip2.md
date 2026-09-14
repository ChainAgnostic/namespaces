---
namespace-identifier: massa-caip2
title: Massa Namespace - Blockchain ID Specification
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

Every Massa node is configured with an unsigned 64-bit `chain_id`.
The value is mixed into the signed form of every operation, so an operation signed for one Massa network is invalid on any other, which is the same replay-protection role [EIP-155][] plays for EVM chains.
The `massa` CAIP-2 profile identifies a network by encoding that `chain_id` as a canonical unsigned decimal string.

## Specification

### Semantics

A Massa chain ID consists of the literal namespace `massa`, a colon, and a reference holding the network's `chain_id`.
Two networks configured with the same `chain_id` have the same CAIP-2 chain ID by definition.
The `chain_id` is a protocol constant of the node build, not a runtime-negotiated value, so it is stable for the lifetime of a network.

### Syntax

```text
chain_id:  "massa:" + reference
namespace: massa
reference: 0 | [1-9][0-9]{0,19}
```

The reference must match the following regular expression:

```regex
^(0|[1-9][0-9]{0,19})$
```

The parsed value must additionally be in the unsigned 64-bit integer range `0` through `18446744073709551615`, inclusive.
The regular expression alone is not sufficient to enforce the upper bound.
The longest possible reference is 20 digits, which is within the 32-character limit CAIP-2 places on references, so no truncation is ever needed.

The reference uses ASCII decimal digits with no sign, base prefix, digit separators, surrounding whitespace, or leading zeroes.

### Resolution Mechanics

To resolve the chain ID reported by a Massa JSON-RPC endpoint, call the [`get_status`][] method:

```json
{
  "jsonrpc": "2.0",
  "method": "get_status",
  "params": [],
  "id": 1
}
```

The `chain_id` is returned as a JSON number at `result.chain_id`.
The following is an abbreviated response from a MainNet node at `https://mainnet.massa.net/api/v2`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "version": "MAIN.5.0",
    "chain_id": 77658377,
    "current_mip_version": 1,
    "config": {
      "genesis_timestamp": 1705312800000,
      "thread_count": 32
    }
  }
}
```

Validate the returned value as a `u64`, serialize it in canonical unsigned decimal form, and prefix it with `massa:`.
The example response therefore resolves to `massa:77658377`.

The same value is also readable from on-chain code through the AssemblyScript smart-contract SDK, so a contract can assert which network it is executing on.

## Rationale

`chain_id` is the only value in the Massa protocol whose purpose is to say which network a signed payload belongs to.
Using it requires no registry, no transformation, and no trusted third party, and it works identically for the public networks and for privately operated ones.

Decimal encoding matches the JSON-RPC representation, which returns `chain_id` as a JSON number rather than a string.
It also avoids having two textual forms for one network, which is what a hexadecimal or zero-padded encoding would introduce.

The genesis block hash was considered and rejected as the reference.
Massa produces blocks in 32 parallel threads, so "the genesis block" is 32 blocks rather than one, and no single hash is canonical for a network.

The published values are derived from four-letter network codes written out as ASCII code points, which is a useful sanity check when reviewing a value by eye.
`MASM` (MainNet) is `77 65 83 77`, giving `77658377`.
`MASB` (BuildNet) is `77 65 83 66`, giving `77658366`.
`MASS` (SecureNet) is `77 65 83 83`, giving `77658383`.
`MASL` (LabNet) is `77 65 83 76`, giving `77658376`.

## Well-Known Networks

The following table allows clients to label well-known networks without an RPC round trip.
It is informative; the resolution method above remains authoritative.

| Network | `chain_id` | CAIP-2 chain ID |
| --- | ---: | --- |
| Massa MainNet | `77658377` | `massa:77658377` |
| Massa BuildNet (public test network) | `77658366` | `massa:77658366` |
| Massa SecureNet | `77658383` | `massa:77658383` |
| Massa LabNet | `77658376` | `massa:77658376` |
| Sandbox (local development) | `77` | `massa:77` |

The MainNet and BuildNet values were read from live nodes and also appear in the [Massa network constants][] documentation.
All five values are defined in the `CHAINID` constant of the [Massa reference implementation][], which selects them from the node's version string.

## Private Networks and Collisions

The sandbox value `77` is a fixed constant shared by every node built with a `SAND*` version string.
Every local sandbox in the world therefore resolves to `massa:77`, and that identifier must not be treated as naming one globally unique network.

An operator running a private Massa network with a modified `CHAINID` is choosing a value that no registry allocates.
If two distinct networks pick the same `chain_id`, this profile cannot distinguish them and their CAIP-2 chain IDs collide.
Such operators should pick a value well away from the five above and keep it stable for the life of the network.

## Backwards Compatibility

There was no previously registered CAIP-2 profile for Massa.
This profile does not change any native Massa identifier.

`chain_id` was introduced during the Massa testnet phase, before MainNet launch, and MainNet has carried `77658377` since genesis, so no legacy form needs to be accepted.

## Test Cases

### Valid identifiers

| Identifier | Reason |
| --- | --- |
| `massa:77658377` | Massa MainNet |
| `massa:77658366` | Massa BuildNet, the public test network |
| `massa:77658383` | Massa SecureNet |
| `massa:77` | Local sandbox, not a globally unique network |
| `massa:0` | Valid zero reference |
| `massa:18446744073709551615` | Upper `u64` boundary, 20 digits |

### Invalid identifiers

| Identifier | Reason |
| --- | --- |
| `massa:` | Empty reference |
| `massa:00` | Non-canonical zero |
| `massa:077658377` | Leading zero |
| `massa:-1` | Signed value |
| `massa:0x4a0f909` | Hexadecimal representation |
| `massa:77_658_377` | Digit separator |
| `massa: 77658377` | Leading whitespace |
| `massa:18446744073709551616` | Above the `u64` maximum |
| `massa:MASM` | Four-letter network code rather than the numeric `chain_id` |
| `MASSA:77658377` | Incorrect namespace casing |

## Additional Considerations

Massa addresses carry a category character and a version byte that a later CAIP-10 profile will need to specify; see the [namespace README][] for the `AU1…` / `AS1…` scheme.
A later CAIP-19 profile will need to distinguish the native coin MAS from MRC-20 tokens, which are ordinary smart contracts identified by an `AS…` address.

## Security Considerations

Resolving a chain ID through `get_status` establishes only what the queried endpoint reports.
It does not authenticate the endpoint, and it does not make an operator-chosen `chain_id` globally unique.
Applications that depend on a trusted chain identity should use authenticated endpoints, or corroborate the reported `chain_id` against the `genesis_timestamp` and other configuration values in the same response.

## References

- [CAIP-2][] - Blockchain ID specification
- [Massa reference implementation][] - The `CHAINID` constant and its per-network values
- [`get_status`][] - JSON-RPC method that reports `chain_id`
- [Massa network constants][] - Published `CHAINID` values for MainNet and BuildNet
- [Massa public networks][] - Public endpoints used to verify the values in this document
- [EIP-155][] - The replay-protection design Massa's `chain_id` cites as precedent
- [namespace README][] - Massa namespace overview and address prefix scheme

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[Massa reference implementation]: https://github.com/massalabs/massa/blob/main/massa-models/src/config/constants.rs
[`get_status`]: https://docs.massa.net/docs/build/api/jsonrpc
[Massa network constants]: https://docs.massa.net/docs/node/constants
[Massa public networks]: https://docs.massa.net/docs/build/networks-faucets/public-networks
[EIP-155]: https://eips.ethereum.org/EIPS/eip-155
[namespace README]: ./README.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
