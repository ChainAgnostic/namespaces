---
namespace-identifier: klv
title: Klever Namespace
author: Nicollas Gabriel da Silva (@nickgs1337)
discussions-to: https://forum.klever.org/, https://github.com/klever-io/klever-go/discussions
status: Draft
type: Informational
created: 2026-05-13
---

# Namespace for Klever Blockchains

This document defines the applicability of CAIP schemes to the networks of the
Klever blockchain ecosystem. Klever is a layer-1 proof-of-stake blockchain
with ed25519 keys, Bech32 addresses prefixed `klv1...`, Wasmer-based smart
contracts, and a native multi-asset model (KDA — Klever Digital Asset) that
supports fungible tokens, NFTs, and SFTs as first-class on-chain primitives.

## Syntax

The namespace `klv` refers to the open-source Klever blockchain protocol and
its production, testing, and development networks.

## References

- [Klever][] — Klever's main website and ecosystem hub.
- [KleverChain explorer][kleverscan] — Public block explorer for Klever
  mainnet, testnet, and devnet.
- [Klever node REST API][klever-api] — Public REST endpoint to fetch chain
  identity, account state, and asset metadata.
- [Klever Connect SDK][klever-connect] — Official TypeScript SDK that
  implements the Klever transaction format, signing flow, and Bech32 address
  encoding.
- [klever-go node source][klever-go] — Reference Go implementation of the
  Klever node, including the address converter, transaction processing, and
  KDA built-in functions.
- [SLIP-44][] — The registry of canonical coin types for derivation paths.
  Klever is registered as coin type `690` (`KLV`, `KleverChain`).
- [BIP_0173][] — The Bech32 specification used for Klever addresses.

[Klever]: https://klever.org
[kleverscan]: https://kleverscan.org
[klever-api]: https://api.mainnet.klever.org/v1.0
[klever-connect]: https://github.com/klever-io/klever-connect
[klever-go]: https://github.com/klever-io/klever-go
[SLIP-44]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[BIP_0173]: https://en.bitcoin.it/wiki/BIP_0173
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md

## Rights

Copyright and related rights waived via CC0.
