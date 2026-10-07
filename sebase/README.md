---
namespace-identifier: sebase
title: JUNCA SOCIAL ECOSYSTEM CHAIN (SE BASE)
author: JAIOS Institutional Governance (@juncaGlobal)
status: Draft
type: Informational
created: 2026-10-07
discussions-to: https://github.com/ChainAgnostic/namespaces/issues/234
requires: ["CAIP-2"]
---

# Namespace for JUNCA SOCIAL ECOSYSTEM CHAIN (SE BASE)

This draft proposes `sebase` as the namespace for the native protocol of JUNCA SOCIAL ECOSYSTEM CHAIN, abbreviated SE BASE.
JSEC is the native token name and symbol; it is distinct from the network name.

## Rationale

SE BASE uses a deterministic native state-transition protocol and validator-certified finality.
The namespace describes that protocol family and the resolution of its native network identifiers.
A JSON-RPC method name or an address encoding alone does not establish the execution or transaction semantics of another namespace.
The proposed CAIP-2 mapping preserves existing native Chain IDs.

## Governance

The protocol's applicable institutional controls are administered by JAIOS Institutional Governance.
The [institutional website][Governance] describes its public institutional context.
Network definitions and public connection profiles remain distinct from observed deployment, admission and finality.
Each network retains its own identity, genesis, state and validator context.
Registration of this namespace would document identifiers for interoperability; it would not certify live operation, wallet support, legal authorisation or asset movement.

## Profiles

- [CAIP-2](caip2.md) — proposed native network identifiers and resolution.
- Account and asset profiles are outside this initial proposal.

## References

- [SE BASE][Network] — public network information.
- [Technical documentation][Documentation] — protocol and interfaces.
- [Canonical interfaces][Interfaces] — documented network identity queries.
- [Protocol architecture][Protocol] — execution and finality context.
- [JAIOS Institutional Governance][Governance] — institutional context.
- [CAIP-2][] — chain identification syntax.

[Network]: https://chain.jaios-governance.org/
[Documentation]: https://docs.jaios-governance.org/
[Interfaces]: https://docs.jaios-governance.org/implementation
[Protocol]: https://docs.jaios-governance.org/protocol
[Governance]: https://jaios-governance.org/
[CAIP-2]: https://standards.chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

