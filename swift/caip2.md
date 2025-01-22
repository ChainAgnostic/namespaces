---
namespace-identifier: swift-caip2
title: SWIFT Network - Network Identifiers
author: Bumblefudge (@bumblefudge), Daniel Rocha (@danroc)
status: Draft
type: Informational
created: 2025-01-22
updated: 2025-01-22
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

The topology of SWIFT's current and next-generation messaging networks is not sufficiently known by the authors to specify the current system of gateways.
This profile is a stub awaiting prototyping efforts.

## Syntax

TBD

### Special Case: Off-network Modeling

To borrow SWIFT data models and accounting conventions without sending or receiving SWIFT messages, simply use network identifier `0`.
As in other namespaces, it is used here to refer to "out of band"/"off-network" usage.

## References

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md

## Rights

Copyright and related rights waived via CC0.
