---
namespace-identifier: animica
title: Animica
author: Animica (@animicaorg)
discussions-to: https://github.com/ChainAgnostic/namespaces/pulls
status: Draft
type: Informational
created: 2026-08-22
requires: ["CAIP-2", "CAIP-10", "CAIP-19"]
---

# Namespace for Animica chains

Animica is an open-source proof-of-work Layer 1 whose accounts sign with post-quantum ML-DSA-65 ([FIPS 204][]) signatures and whose smart contracts run in a Python virtual machine.
Its mainnet has been live since 2026-04-06 and its native token is ANM, denominated in nano-ANM (1 ANM = 10^9 nANM).
The `animica` namespace covers networks that implement the Animica protocol and expose its native JSON-RPC interface.
Individual networks are identified by their integer chain id, as specified in the [Animica CAIP-2 profile][CAIP-2 Profile].

The mainnet identifier `animica:1` is already in production use.
Animica's [x402][] payment lane settles in ANM against the network id `animica:1`, and its published MCP tooling and [chain parameters][Chain Parameters] use the same identifier.
This namespace documents that identifier and the account and asset forms that build on it, so that chain-agnostic wallets, payment protocols, and SDKs can refer to Animica without inventing their own conventions.

## Rationale

Animica is not an EVM chain and cannot be placed in the `eip155` namespace.
Its node exposes a handful of `eth_*`-style convenience methods (for example `eth_gasPrice`), but its addresses are bech32m strings carrying a signature-scheme id and a SHA3-256 key digest, its transactions are canonical CBOR signed with ML-DSA-65, and its chain id `1` would collide with Ethereum mainnet under `eip155:1`.
A dedicated namespace with the native integer chain id as the reference gives applications an identifier that matches what the node itself reports and what is already exchanged on the wire.

The same bech32m human-readable part `anim` is used on every Animica network.
The CAIP-2 portion of an identifier is therefore the only thing that distinguishes an account or asset on mainnet from the same account or asset on a test network.

## Governance

Animica's protocol and reference node are developed in the open in the [Animica source repository][].
Protocol changes ship as versioned releases of the node software and activate at pre-announced block heights; there is no on-chain governance mechanism.
Changes to this namespace profile should be proposed on the pull request linked in the `discussions-to` header or as an issue in the source repository.

## References

- [Animica website][] - Project overview and downloads
- [Animica CAIP-2 profile][CAIP-2 Profile] - Chain identifiers in this namespace
- [Animica CAIP-10 profile][CAIP-10 Profile] - Account identifiers in this namespace
- [Animica CAIP-19 profile][CAIP-19 Profile] - Asset identifiers in this namespace
- [Animica source repository][] - Node, wallets, and specifications
- [Chain Parameters][] - Chain ids, units, and network parameters
- [HD Derivation][] - Normative BIP-39/SLIP-0010 to ML-DSA-65 derivation and address test vectors
- [Public RPC][] - Public JSON-RPC 2.0 endpoint for mainnet (`POST https://rpc.animica.org/rpc`)
- [Explorer][] - Mainnet block explorer
- [PyPI package][] - `animica` Python package (node, CLI, and libraries)
- [NonKYC market][] - Exchange where ANM trades (ANM/USDT)
- [x402][] - Payment protocol whose Animica lane uses `animica:1` as its network id
- [FIPS 204][] - Module-Lattice-Based Digital Signature Standard (ML-DSA)

[Animica website]: https://animica.org
[CAIP-2 Profile]: ./caip2.md
[CAIP-10 Profile]: ./caip10.md
[CAIP-19 Profile]: ./caip19.md
[Animica source repository]: https://github.com/animicaorg/all
[Chain Parameters]: https://github.com/animicaorg/all/blob/36f995f241cd3e54f66c7a5a6f373d4587bbc60d/docs/spec/CHAIN_PARAMS.md
[HD Derivation]: https://github.com/animicaorg/all/blob/36f995f241cd3e54f66c7a5a6f373d4587bbc60d/docs/wallet/HD_DERIVATION.md
[Public RPC]: https://rpc.animica.org/rpc
[Explorer]: https://explorer.animica.org
[PyPI package]: https://pypi.org/project/animica/
[NonKYC market]: https://nonkyc.io/market/ANM_USDT
[x402]: https://github.com/x402-foundation/x402
[FIPS 204]: https://csrc.nist.gov/pubs/fips/204/final

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
