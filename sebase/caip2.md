---
namespace-identifier: sebase-caip2
title: SE BASE - Blockchain ID Specification
author: JAIOS Institutional Governance (@juncaGlobal)
status: Draft
type: Informational
created: 2026-10-07
discussions-to: https://github.com/ChainAgnostic/namespaces/issues/234
requires: ["CAIP-2"]
---

# CAIP-2

For context, see [CAIP-2][].

## Introduction

This draft maps a SE BASE native Chain ID to a CAIP-2 identifier under the proposed `sebase` namespace.
It preserves the native numeric identifiers and distinguishes Mainnet from Testnet2.
The proposed namespace is subject to review and is not an accepted registry entry.

## Specification

### Semantics

The reference is the canonical positive decimal representation of the native Chain ID assigned to a network of this protocol.
These identifiers name separate network definitions:

| Network definition | Native Chain ID | Proposed CAIP-2 identifier |
| --- | --- | --- |
| Mainnet | 326797836 | `sebase:326797836` |
| Testnet2 | 326797837 | `sebase:326797837` |

The Mainnet row describes an assigned network identity, not a claim of public activation.
A Chain ID from another namespace has no implied relationship to a SE BASE network with the same numeric reference.
Assigned identifiers must not be reused for a different genesis lineage.

### Syntax

The namespace is the lowercase string `sebase`.
The reference consists of ASCII decimal digits, with no sign, whitespace or leading zeros.
The complete identifier matches:

```text
^sebase:[1-9][0-9]{0,31}$
```

Syntactic validity does not imply that a numeric reference has been assigned to a network.
Hexadecimal RPC quantities are decoded to an integer and rendered as canonical decimal digits before forming the CAIP-2 identifier.
Hexadecimal strings are not CAIP-2 references in this profile.

### Resolution Mechanics

An integration obtains the selected network's connection profile from an authoritative network definition.
The [public interface documentation][Interfaces] documents the Testnet2 identity query at `https://rpc.testnet2.jaios-governance.org`.

Request body:

```json
{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}
```

The documented Testnet2 result value is `0x137a8a0d`, which maps to `sebase:326797837`.
This is a documentation-based test vector, not a fresh live response.
The method name is an identity-query compatibility surface and does not classify the native runtime.

The returned Chain ID must match the selected network definition.
Network health and finalised evidence are separate observations.
For authenticated network binding, an implementation also verifies the selected genesis context and native finality evidence using the protocol's verification rules.
A numeric RPC response alone is not cryptographic proof of network identity.
A query failure or identity mismatch must not switch the integration to another network.

Mainnet endpoint details must be obtained from an authoritative Mainnet-specific connection profile.
The Testnet2 and initial Public Testnet endpoints are not Mainnet resolvers.

## Rationale

The decimal Chain ID already serves as the native network boundary.
A namespace qualified representation preserves that value while providing cross-protocol disambiguation.
A genesis check supplements the numeric identifier during authenticated resolution; this draft does not fabricate a genesis hash.

### Backwards Compatibility

The public interface documentation also describes an initial Public Testnet using a separate network definition.
That profile must not be substituted for Mainnet or Testnet2.
This initial proposal defines the two network identities in the table above.

## Test Cases

| Input | Result |
| --- | --- |
| `sebase:326797836` | Valid syntax; assigned Mainnet identity |
| `sebase:326797837` | Valid syntax; assigned Testnet2 identity |
| Testnet2 RPC quantity `0x137a8a0d` | Reference `326797837` |
| `sebase:0326797836` | Invalid leading zero |
| `SEBASE:326797836` | Invalid namespace casing |
| `sebase:0x137a8a0c` | Invalid decimal reference |
| `sebase:0` | Invalid zero reference |
| `sebase:-326797836` | Invalid signed reference |
| Mainnet selected; RPC reports `0x137a8a0d` | Network identity mismatch |
| Any correctly formatted unassigned reference | Syntactically valid; assignment unresolved |

## References

- [CAIP-2][] — cross-protocol chain identifiers.
- [Canonical interfaces][Interfaces] — documented RPC identity methods.
- [Protocol architecture][Protocol] — native execution and finality.
- [SE BASE network information][Network] — public protocol context.

[CAIP-2]: https://standards.chainagnostic.org/CAIPs/caip-2
[Interfaces]: https://docs.jaios-governance.org/implementation
[Protocol]: https://docs.jaios-governance.org/protocol
[Network]: https://chain.jaios-governance.org/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

