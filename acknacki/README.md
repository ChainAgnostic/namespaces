---
namespace-identifier: acknacki
title: Acki Nacki Blockchain
author: Mitja Goroshevsky (@Futurizt)
status: Draft
type: Informational
created: 2026-04-07
---

# Namespace for Acki Nacki Blockchain

Acki Nacki is a Rust implementation of a probabilistic proof-of-stake
consensus protocol optimized for fast finality, while allowing for high
throughputs via execution parallelization. It achieves higher Byzantine
fault tolerance than Nakamoto, BFT (including Hotstuff and AptosBFT),
Solana, and other modern consensus protocols. The protocol reaches
consensus in two communication steps and exchanges a total number of
messages per consensus round that is subquadratic in the number of nodes.

Acki Nacki runs AVM (Advanced Virtual Machine) supporting both Ton Virtual
Machine (TVM) and WASM execution environments. It features a DApp ID system for gasless
internal transactions, ECC (Extra Currency Collection) token transfers,
and native support for AI agent operations.

## Rationale

The `acknacki` namespace (8 characters, the CAIP-2 maximum) identifies
the Acki Nacki blockchain family. The reference field uses the
`global_id` integer from the block header, which uniquely identifies
each network (mainnet, shellnet/testnet).

A separate namespace from `tvm` is necessary because:
- Acki Nacki runs AVM supporting TVM and WASM, evolving beyond TVM
- The DApp ID threading model is unique to Acki Nacki
- The consensus mechanism is specific to Acki Nacki
- Address format uses DApp ID routing, not workchain IDs

## Governance

Acki Nacki core protocol developer is [GOSH](https://gosh.sh). Protocol
specifications and node software are open source at
[github.com/ackinacki/ackinacki][github]. Network updates are performed
bitcoin-style — node owners update their nodes to a newest version at
will. There is no DAO, foundation or governance body.

The consensus protocol is formally described in a peer-reviewed
publication at [ACNS 2024 (Springer)][springer].

## References

- [Acki Nacki Documentation][docs] - Official documentation
- [Acki Nacki Developer Portal][dev] - Developer guides and API reference
- [Acki Nacki GitHub][github] - Node software and smart contracts
- [Consensus Paper (Springer)][springer] - "Acki Nacki: A Probabilistic
  Proof-of-Stake Consensus Protocol with Fast Finality and
  Parallelisation" (ACNS 2024)
- [Block Explorer][explorer] - Mainnet block explorer

[docs]: https://docs.ackinacki.com
[dev]: https://dev.ackinacki.com
[github]: https://github.com/ackinacki/ackinacki
[springer]: https://doi.org/10.1007/978-3-031-61486-6_4
[explorer]: https://mainnet.ackinacki.org

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
