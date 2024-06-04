---
namespace-identifier: eip155-caip25
title: EIP155 Namespace, aka EVM Chains - JSON-RPC Provider Authorization
author: Pedro Gomes (@pedrouid), Hassan Malik (@hmalik88), bumblefudge (@bumblefudge)
discussions-to: 
status: Draft
type: Standard
created: 2024-02-05
updated: 2024-02-05
requires: ["CAIP-25", "CAIP-211", "CAIP-217"]
---

# CAIP-25

_For context, see the [CAIP-211] and [CAIP-25] specifications._

## Rationale

In the Ethereum space, JSON-RPC connections are not constrained by a single interface definition; numerous overlapping implicit and explicit authorities define the valid interactions between a user agent like a wallet and a decentralization application (whether web-based or otherwise).
The core RPC capabilities (concretely, the syntax and semantics of RPC methods and notifications) of any Ethereum or EVM-compatible network are assumed to be defined by the consensus of the Ethereum Improvement Proposal process.
In practice, this consensus is captured almost exhaustively by the [common API documentation][execution API] published by the execution-client community;
this documentation should be considered the implicit authority when no overriding authority has been declared for RPC capabilities.

## Capability Expression

In the context of [CAIP-25][] or other negotiations between decentralized applications and user agents, decentralization applications SHOULD ONLY request, and wallets SHOULD ONLY express support for, RPC methods and notifications specified in the [execution API] documentation.
The [execution API] capabilities are considered the implicit default authority in any `eip155` authorization scope where no authorities have been explicitly declared.

When requesting or expressing support for any other RPC methods and/or notifications, additional authorities SHOULD be requested in a separate [CAIP-217] `authorizationScope` object, with authorities and endpoints explicitly declared as specified in [CAIP-211].

In any scope object with additional authorities declared, methods or notifications specified by multiple authorities should be defined and understood according to the greatest authority in the list as per the [CAIP-211] specification.

## Examples

## References

- [EIP155][]: Ethereum Improvement Proposal specifying generation and validation of ChainIDs

[execution API]: https://github.com/ethereum/execution-apis?tab=readme-ov-file#execution-api-specification
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-25]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-25.md
[CAIP-211]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-211.md
[CAIP-217]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-217.md
[EIP]: https://eips.ethereum.org/EIPS/eip-1
[EIP155]: https://eips.ethereum.org/EIPS/eip-155

## Rights

Copyright and related rights waived via CC0.
