---
namespace-identifier: quantus
title: Quantus Namespace
author: ["Nikolaus Heger (@n13)"]
status: Draft
type: Informational
created: 2026-09-17
---

# Namespace for Quantus Network

Quantus Network is a post-quantum secure Layer-1 blockchain.
Transactions are signed with ML-DSA ([FIPS 204][], the standardized form of CRYSTALS-Dilithium) at the ML-DSA-87 or ML-DSA-65 security level instead of the elliptic-curve schemes used by most other chains, accounts are derived from ML-DSA public keys with the [Poseidon][] hash, and blocks are produced by a proof-of-work consensus called QPoW.

The node and runtime are built with the [Polkadot SDK][] (Substrate), so the JSON-RPC surface, SCALE encoding and [SS58][] address encoding will look familiar to developers who know that ecosystem.
Wallets, signers and dapps written for Polkadot chains cannot, however, sign Quantus transactions or verify Quantus signatures, and Quantus does not participate in XCM.
The `quantus` namespace exists so that this difference is visible at the addressing layer.

## Rationale

Quantus differs from the `polkadot` namespace in the parts that matter to cross-chain tooling:

- **Signatures**: every extrinsic is signed with ML-DSA-87 or ML-DSA-65. There is no sr25519, ed25519 or ECDSA support.
- **Account derivation**: an account ID is the 32-byte Poseidon hash of the ML-DSA public key, not the public key itself.
- **Block hashing**: block headers are hashed with Poseidon, not Blake2.
- **Consensus**: blocks are mined with QPoW. There are no validators, nominators or relay chain.

Describing Quantus under `polkadot:` would advertise a level of compatibility that does not exist, in the same way that the `hedera` namespace declined to reuse `eip155` for its EVM-compatible networks.

Because the set of Quantus networks is small and controlled by one team, chains are referenced by name rather than by genesis hash.
Each name resolves to a genesis hash that clients can verify over RPC; see the [CAIP-2 profile](caip2.md).

## Networks

| Network | CAIP-2 | Token | Genesis hash |
|---------|--------|-------|--------------|
| Mainnet | `quantus:mainnet` | QTC (12 decimals) | `0xfb5487c0be6ae4ade2d41d16e50465129861636c2b8d61fa94d7a19631626fba` |
| Planck testnet | `quantus:planck` | PLK (12 decimals) | `0x4901bf5c57fd3f9e726af399c763de6670dbdb115a91c0237e173f16eef65e72` |

All networks use SS58 address prefix `189`, so an address string is the same on every Quantus network and the CAIP-2 identifier is what distinguishes them.

### Mainnet

- **JSON-RPC endpoint**: `https://rpc1-mainnet.quantus.com`
- **Explorer**: `https://explorer.quantus.com`
- **Native currency**: QTC, 12 decimals

### Planck testnet

- **JSON-RPC endpoint**: `https://a1-planck.quantus.cat`
- **Native currency**: PLK, 12 decimals, no monetary value

## Governance

The node, runtime and tooling are developed in the open in the [Quantus Network GitHub organization][].
Runtime upgrades are enacted on-chain.
Changes to this namespace should be proposed as pull requests against this repository and discussed with the Quantus team.

## References

- [Quantus documentation][] - developer documentation for Quantus Network
- [Post-quantum cryptography in Quantus][] - how ML-DSA and Poseidon are used
- [Quantus chain repository][] - node and runtime source code
- [Quantus Network GitHub organization][] - all Quantus repositories
- [FIPS 204][] - the ML-DSA signature standard
- [Poseidon][] - the hash function used for account IDs and block hashes
- [SS58][] - the address encoding used by Quantus
- [Polkadot SDK][] - the framework the Quantus node is built with

[Quantus documentation]: https://docs.quantus.com/
[Post-quantum cryptography in Quantus]: https://docs.quantus.com/deep-dives/pqc/
[Quantus chain repository]: https://github.com/Quantus-Network/chain
[Quantus Network GitHub organization]: https://github.com/Quantus-Network
[FIPS 204]: https://csrc.nist.gov/pubs/fips/204/final
[Poseidon]: https://eprint.iacr.org/2019/458
[SS58]: https://docs.polkadot.com/polkadot-protocol/parachain-basics/accounts/#address-formats
[Polkadot SDK]: https://github.com/paritytech/polkadot-sdk
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
