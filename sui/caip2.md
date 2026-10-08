---
namespace-identifier: sui-caip2
title: Sui Namespace - Chains
author: William Robertson (@williamrobertson13), Omer Sadika (@omersadika)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/146, https://github.com/ChainAgnostic/namespaces/pull/236
status: Draft
type: Informational
created: 2025-06-18
updated: 2026-10-08
---

# CAIP-2

_For context, see the [CAIP-2][] specification._

## Introduction

The Sui namespace identifies networks by name or chain identifier.

- Names (`mainnet`, `testnet`, `devnet`, `localnet`) stay the same across resets.
- Chain identifiers are the first four bytes of the genesis checkpoint digest in lowercase hex, e.g. `35834a8a` for mainnet. They stay fixed for each chain but are not globally unique.

A full node reports its network's genesis checkpoint digest, so either form can be checked against it.

## Specification

### Semantics

A valid CAIP-2 identifier in the Sui namespace takes one of two forms:

`sui:<network>`

Where `<network>` is one of the following reserved names:

- `mainnet`
- `testnet`
- `devnet`
- `localnet`

`sui:<chain identifier>`

Where `<chain identifier>` is the first four bytes of the network's genesis checkpoint digest, as eight lowercase hexadecimal characters.

Sui's RPCs and SDKs use "chain identifier" for the full 32-byte digest, base58btc-encoded, and the Sui CLI calls the four-byte hex value the short form.
The full digest exceeds the 32-character limit on [CAIP-2][] references, so in this profile "chain identifier" always means the four-byte form.

The two forms name networks differently:

- `mainnet` always names the same chain, whose short identifier is `35834a8a`.
- `testnet` has run since May 2023 with short identifier `4c78adac`. A reset is not expected, but is allowed with notice ([Sui Networks]). After a reset, `sui:testnet` would name the new chain; the old chain would keep its short identifier `4c78adac`.
- `devnet` resets regularly, wiping all state and creating a new chain ([Sui Networks]). `sui:devnet` names the current chain.
- `localnet` names the client's local network.
- A private network has no reserved name and is named by its chain identifier.

A network can have two IDs, and different networks can share a four-byte identifier.
To compare chains, resolve each ID using trusted network information and compare the full genesis digests ([Resolution Mechanics](#resolution-mechanics)).

### Syntax

#### Regular Expression

`^sui:(mainnet|testnet|devnet|localnet|[0-9a-f]{8})$`

Every name contains a letter that is not a hexadecimal digit, so names and chain identifiers cannot be confused.
Future names will follow the same rule and use only lowercase letters, digits and hyphens, up to 32 characters.
This regular expression will be updated when one is added.

#### Examples

`sui:mainnet`

`sui:35834a8a`

### Governance

A new name is added only by updating this profile, for example when a new long-running public network launches.
Updates are accepted from this profile's authors, or from Mysten Labs (@MystenLabs) or the Sui Foundation, which coordinate Sui's standards ([README][Sui Namespace]).

### Resolution Mechanics

To resolve a CAIP-2 identifier, ask a trusted full node of the network for its genesis checkpoint digest.
Its first four bytes, in lowercase hex, are the chain identifier; for `sui:<chain identifier>`, check that they match.
A matching prefix alone does not identify the intended network.
Use a retained full digest or trusted endpoint to resolve ambiguity; fail if the network remains ambiguous.

Mainnet and the current testnet can also be resolved from the digests under [Test Cases](#test-cases), taken from [Sui's source][Sui digests].
After a testnet reset, use its new digest for `sui:testnet`.
Comparing a node's digest against them detects a node serving the wrong network.
A node does not report the names `devnet` or `localnet`: for those, the network is whichever one the client's configured node serves.

There is no registry of chain identifiers or endpoints.
The public networks' endpoints are listed in [Sui Networks]; a private network's operators share its endpoints themselves.

Over gRPC, call `GetServiceInfo` on `sui.rpc.v2.LedgerService`.
It returns `chain_id`, the base58btc-encoded genesis checkpoint digest, and `chain`: `mainnet`, `testnet`, or `unknown` for any other network, including devnet and local networks.

**Sample request (for mainnet):**

```
grpcurl fullnode.mainnet.sui.io:443 sui.rpc.v2.LedgerService/GetServiceInfo
```

**Sample response (abridged):**

```json
{
  "chainId": "4btiuiMPvEENsttpZC7CZ53DruC3MAgfznDbASZ7DR6S",
  "chain": "mainnet"
}
```

Decoding `4btiuiMPvEENsttpZC7CZ53DruC3MAgfznDbASZ7DR6S` from base58btc gives `35834a8ac17ca48fb14ac8f99c17c98747e95dd07294ae41a46b382246a4499b`, whose first four bytes are the chain identifier `35834a8a`.

Over GraphQL ([Sui GraphQL API]), the `chainIdentifier` field returns the same base58btc-encoded digest.

## Rationale

Names and chain identifiers serve different needs:

- Names let clients follow devnet resets or switch local networks without changing their chain ID configuration.
- Chain identifiers stay fixed for a chain; a reset's new genesis digest determines its identifier.

`localnet` follows the chain names the [Sui wallet standard][Sui Wallet Standard] already uses, and works like shared local-development chain IDs elsewhere, such as `eip155:31337`, the default for Hardhat and Anvil.

The chain identifier form lets a chain that has no reserved name, such as a private network, be identified without changing this profile.
It is the four-byte value Sui's JSON-RPC API and CLI have long shown.

Four bytes distinguish the current public Sui networks, but private or local networks can collide with each other or with a public network.
Records that must tell any two Sui chains apart should also store the full genesis checkpoint digest.

### Backwards Compatibility

Every identifier valid under the earlier version of this profile (`sui:mainnet`, `sui:testnet`, `sui:devnet`) is still valid and keeps its meaning.

The earlier version resolved names over JSON-RPC, which returned the chain identifier directly (for example `35834a8a`).
JSON-RPC is deprecated on Sui's public full nodes, but a value obtained from it is a chain identifier as this profile defines it.

## Test Cases

#### Sui Mainnet

- **CAIP-2 Chain IDs:** `sui:mainnet`, `sui:35834a8a`
- **Genesis checkpoint digest:** `4btiuiMPvEENsttpZC7CZ53DruC3MAgfznDbASZ7DR6S`

#### Sui Testnet

- **CAIP-2 Chain ID:** `sui:testnet`, or, for the current testnet, `sui:4c78adac`
- **Genesis checkpoint digest:** `69WiPg3DAQiwdxfncX6wYQ2siKwAe6L9BZthQea3JNMD`

#### Sui Devnet

- **CAIP-2 Chain ID:** `sui:devnet`, or the current devnet's chain identifier
- **Resolved chain identifier:** changes with each reset; `945654c4` on 2026-10-08

#### Local network

- **CAIP-2 Chain ID:** `sui:localnet`, or the local network's chain identifier
- **Resolved chain identifier:** depends on the local network

#### Invalid

- `sui:Mainnet` (names are lowercase)
- `sui:35834A8A` (chain identifiers are lowercase)
- `sui:35834a8ac17ca48f` (a chain identifier is exactly four bytes)
- `sui:4btiuiMPvEENsttpZC7CZ53DruC3MAgfznDbASZ7DR6S` (the full base58btc digest; use its first four bytes, in hex)

## References

- [Sui Docs] - Developer documentation and concept overviews for building on Sui.
- [Sui Networks] - Sui's networks and their data-retention policies.
- [Sui gRPC API] - `LedgerService`, including `GetServiceInfo`.
- [Sui GraphQL API] - Reference for Sui's GraphQL RPC, including `chainIdentifier`.
- [Sui digests] - The genesis checkpoint digests of mainnet and testnet in Sui's source.
- [Sui GitHub] - Official GitHub repository for the Sui smart contract platform.
- [Sui Network Info] - Information regarding Sui networks and their release schedules.
- [Sui Namespace] - This namespace's overview, including its governance.
- [Sui Wallet Standard] - The chain names Sui wallets use.
- [CAIP-2] - Chain ID Specification.

[Sui Docs]: https://docs.sui.io/
[Sui Networks]: https://docs.sui.io/develop/sui-architecture/networks
[Sui gRPC API]: https://github.com/MystenLabs/sui-apis/blob/main/proto/sui/rpc/v2/ledger_service.proto
[Sui GraphQL API]: https://docs.sui.io/references/sui-graphql
[Sui digests]: https://github.com/MystenLabs/sui/blob/main/crates/sui-types/src/digests.rs
[Sui GitHub]: https://github.com/MystenLabs/sui
[Sui Network Info]: https://sui.io/networkinfo
[Sui Namespace]: ./README.md
[Sui Wallet Standard]: https://github.com/MystenLabs/ts-sdks/blob/main/packages/wallet-standard/src/chains.ts
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
