---
namespace-identifier: galachain-caip2
title: GalaChain Namespace - Blockchain ID Specification
author: Ben Skaggs (@bnskaggs)
discussions-to: https://github.com/GalaChain/sdk/issues/839
status: Draft
type: Standard
created: 2026-09-29
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

GalaChain currently runs one production network (mainnet) and one persistent public test network (testnet).
Both are operated by Gala Games, and the number of networks is expected to stay very small, so networks are referenced by an enumerated name rather than a numeric identifier.
GalaChain has no in-protocol network identifier: in the default signing mode a transaction is a signed DTO whose signature binds no network id, so the CAIP-2 reference is the only network discriminator available to cross-chain tooling.
(The `ChainId` enum in the GalaChain SDK enumerates *external* chains for bridging — Ethereum, TON, Solana — and does not identify GalaChain networks.)

## Syntax

The namespace is `galachain`.
The reference SHOULD be one of the following enumerated strings:

- `mainnet`
- `testnet`

A regular expression for validating any theoretically possible GalaChain network reference (within the CAIP-2 limit of 32 characters) is:

```
galachain:[-a-z0-9]{1,32}
```

Local development networks started with the GalaChain SDK are not assigned a reference by this profile.

### Resolution Method

There is no in-protocol resolution method.
Each network is reached through its REST gateway, and the mapping is published in the [GalaChain Documentation][]:

| Reference | Gateway |
|---|---|
| `mainnet` | `https://gateway-mainnet.galachain.com/api` |
| `testnet` | `https://gateway-testnet.galachain.com/api` |

A client can confirm it is connected to the intended network by querying a known token class or account balance through the gateway and checking the response against the [GalaChain Explorer][] for mainnet.

## Backwards Compatibility

Not applicable; no prior CAIP-2 identifier exists for GalaChain.

## Test Cases

```
# GalaChain mainnet
galachain:mainnet

# GalaChain testnet
galachain:testnet
```

## Additional Considerations

### Rejected idea: identifying GalaChain within `eip155`

GalaChain accepts secp256k1 signatures and its default addresses are Ethereum-style hashes of the public key, so an `eip155` identifier looks superficially plausible.
It would misrepresent the chain: GalaChain exposes no EVM, no Ethereum JSON-RPC, and no `CHAINID`, and its default DTO signatures bind no chain identifier (the express purpose of EIP-155).

### Rejected idea: a generic `fabric` namespace

Hyperledger Fabric is a framework rather than a network family with shared addressing or a shared actor model.
Two Fabric deployments need share nothing a cross-chain client could rely on, so a framework-level namespace would carry no usable semantics.

## References

- [GalaChain Documentation][] - developer documentation and gateway reference
- [GalaChain SDK][] - open-source SDK
- [GalaChain Explorer][] - mainnet block explorer

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[GalaChain Documentation]: https://docs.galachain.com/latest/
[GalaChain SDK]: https://github.com/GalaChain/sdk
[GalaChain Explorer]: https://explorer.galachain.com

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
