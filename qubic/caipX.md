---
namespace-identifier: qubic-caip2
title: Qubic Namespace - Blockchain ID Specification
author: ["Aleix (@aleishio)"]
discussions-to: <URL of PR>
status: Draft
type: Standard
created: 2025-02-20
requires: ["CAIP-2"]
---

# CAIP-2: 

This document is about the details of the Qubic network namespace and reference for CAIP-2.

## Abstract
In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for Qubic network.


## Specification

### Namespace

The namespace "qubic" refers to the wider Qubic ecosystem.

### Reference Definition

The reference for the Qubic mainnet is defined as follows:

- `qubic:mainnet`

This designation ensures a clear and unambiguous reference to the Qubic mainnet.

### Testnet Consideration

As of the creation date of this document, the Qubic blockchain operates solely on its mainnet. Should a testnet be introduced in the future, it will be assigned a distinct reference, such as:

qubic:testnet

This approach ensures clarity and separation between different network environments.

## Semantics

- **Namespace (`qubic`)**: Identifies the Qubic blockchain.
- **Reference (`mainnet`)**: Specifies the primary live network of the Qubic blockchain.

## Syntax

The blockchain identifier for Qubic adheres to the following syntax:

qubic:mainnet

This identifier is case-sensitive and must be used exactly as specified.

## Resolution Mechanics

To resolve and interact with the Qubic blockchain using this identifier, clients should direct their requests to the official Qubic RPC endpoint:

https://rpc.qubic.org

This endpoint provides access to network statistics, smart contract interactions, and other blockchain-related data. Detailed API documentation is available at [Qubic RPC Documentation][1].

## Backwards Compatibility

This is the initial definition of the Qubic namespace under the CAIP-2 standard. There are no previous versions or legacy identifiers associated with this specification.

## Test Cases

To validate the correct implementation of the Qubic blockchain identifier, consider the following examples:

- Valid Identifier: `qubic:mainnet`
- Invalid Identifier: `Qubic:mainnet` (namespace must be lowercase)
- Invalid Identifier: `qubic:MAINNET` (reference must be lowercase)
- Invalid Identifier: `qubic:` (reference is required)

## Additional Considerations

Future updates to the Qubic network, such as the introduction of additional networks (e.g., testnets), will necessitate corresponding updates to this specification to include new references.

## References

- [CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
- [Qubic RPC Documentation][1]: https://qubic.github.io/integration/Partners/qubic-rpc-doc.html?urls.primaryName=Qubic%20RPC%20Archive%20Tree

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

