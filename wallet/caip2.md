---
namespace-identifier: wallet-caip2
title: Wallet Namespace - RPC namespaces
author: ["Vandan Parikh (@vandan)", "Bumblefudge (@bumblefudge)"]
discussions-to: <URL of PR, mailing list, etc>
status: Draft
type: <Standard | Meta | Informational>
created: <date created on, in ISO 8601 (yyyy-mm-dd) format>
requires (*optional): <["CAIP-X", "CAIP-Y"]>
replaces (*optional): <CAIP-Z>
---

*For context, see the [CAIP-2][] specification.*

Each `chainId` reference in the `wallet:` namespace is defined as the namespace identifier for another namespace.

This combination (i.e. `wallet:eip155`) refers not to an `eip155` network but specifically to an application<>wallet connection defined according to the wallet and RPC conventions of the `eip155` namespace.

## Rationale

Implementers of [CAIP-25][] and other multichain application<>wallet connections have long struggled with how to map offchain or direct-to-wallet methods, notifications, and metadata to one another across namespaces, and how to safely and ergonomically segregate them from node-dependent/network-dependent functions.
For this reason, an abstraction (in the form of a "meta-namespace" routing to the other namespaces) is here proposed.

## Semantics

`wallet:{namespace}` is functionally an alias for `{namespace}:wallet`, where `:wallet` refers to a special-case of a wallet connection, not a proper network (as required by the CAIP-2 profile for `eip155`).

## Syntax

The only valid values for a `chainId` reference in the `wallet` namespace are the namespace identifiers of other namespaces.
For a current list of these, see [namespaces][].

### Resolution Mechanics

All resolution is defined in the namespace referred to, and ideally specified in its `/README.md` file here.
As resolution depends entirely on transport and connection mechanism, no uniform resolution mechanics should be assumed.

## Test Cases

< TODO  >

## Additional Considerations

< TODO >

## References

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-25]: https://chainagnostic.org/CAIPs/caip-25
[namespaces]: https://namespaces.chainagnostic.org/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/)
