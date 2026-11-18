---
namespace-identifier: galachain
title: GalaChain Namespace
author: Ben Skaggs (@bnskaggs)
status: Draft
type: Informational
created: 2026-09-29
---

# Namespace for GalaChain

GalaChain is a layer-1 network built on Hyperledger Fabric and operated by Gala Games.
It is not an EVM chain: there is no JSON-RPC interface and no `CHAINID` opcode.
Clients interact with it over REST gateways, and smart contracts ("chaincode") are written in TypeScript.
Transactions are signed data-transfer objects (DTOs): by default the caller signs a deterministic JSON serialisation of the request with a secp256k1 key, and the signature is verified by the chaincode itself, so a third party may submit a transaction on a signer's behalf without being able to alter it.
Accounts are identified by prefixed aliases, most commonly `eth|` followed by an Ethereum-style checksummed address derived from the signer's public key; legacy `client|` and `service|` aliases also exist.

## Rationale

Although GalaChain accepts secp256k1 signatures and derives its default account addresses from Ethereum-style public-key hashes, it shares no execution environment, RPC surface, or chain-id mechanism with the `eip155` family, so it cannot be identified as an EVM chain without misrepresenting what a client can do with it.
Nor is "Hyperledger Fabric" a namespace: Fabric is a framework, and each deployment defines its own identity model, channels, and contracts.
GalaChain's actor model (signed DTOs, `eth|`-prefixed addresses, a single TokenContract for fungible and non-fungible assets) is specific to GalaChain, so a dedicated namespace is the accurate scope.

A GalaChain network hosts several Fabric channels (for example the `asset` channel, which hosts the token contract).
The CAIP-2 identifier denotes the network as a whole; channel and contract selection are application-level concerns expressed in gateway URLs.

## Governance

GalaChain is developed and operated by Gala Games.
The SDK is open source at [GalaChain SDK][] (Apache-2.0); network-level changes are made by the operator rather than through a public improvement-proposal process.
Where this profile conflicts with the [GalaChain Documentation][], treat the documentation as canonical.

## References

- [GalaChain Documentation][] - developer documentation, including the integration guide and REST gateway reference
- [GalaChain SDK][] - open-source SDK (chain-api, chain-client, chaincode framework)
- [Mainnet Gateway][] - Swagger documentation for the mainnet REST gateway
- [Testnet Gateway][] - Swagger documentation for the testnet REST gateway
- [GalaChain Explorer][] - mainnet block explorer
- [Hyperledger Fabric][] - the underlying framework

[GalaChain Documentation]: https://docs.galachain.com/latest/
[GalaChain SDK]: https://github.com/GalaChain/sdk
[Mainnet Gateway]: https://gateway-mainnet.galachain.com/docs
[Testnet Gateway]: https://gateway-testnet.galachain.com/docs
[GalaChain Explorer]: https://explorer.galachain.com
[Hyperledger Fabric]: https://hyperledger-fabric.readthedocs.io/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
