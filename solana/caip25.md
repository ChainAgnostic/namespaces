---
namespace-identifier: solana-caip25
title: Solana Namespace - JSON-RPC Provider Authorization
author: Jon Wong (@jnwng), Glitch (@glitch) bumblefudge (@bumblefudge)
discussions-to: https://github.com/anza-xyz/wallet-adapter/issues/807
status: Draft
type: Standard
created: 2024-02-05
updated: 2024-02-05
requires: ["CAIP-25", "CAIP-217"]
---

# CAIP-25

_For context, see the [CAIP-25][] specification._

## Rationale

In the Solana ecosystem, standardization of the RPC provider interface has centered on the [Wallet Standard] and [Wallet Adapter] open-source tooling.
For the most part, progressive [CAIP-25] negotiation and iteration is possible over a [Wallet Standard] connection, with the former inheriting the declaration of initial capabilities and permissions made in the latter as initial state for further negotation.

## Network-specific versus Namespace-wide Scopes

Few use-cases incorporating multiple Solana-compatible networks require granular permissions or capability declarations per-chain, so a Solana-wide [CAIP-217] authorization scope (keyed to the entire `solana` namespace rather than to a specific chain), with identical permissions and capabilities across one or more chains, is recommended in most cases.

Multi-chain use-cases incorporating non-Solana chains should use distinct [CAIP-217] authorization objects per chain type, in cases where those [CAIP-25] capabilities and configurations can be deterministically mapped to [Wallet Standard Multichain Extensions] variables by a [CAIP-25] provider.

## Session Properties

Wallet capabilities in the [Wallet Standard] model are declared upfront at time of connection and persisted as read-only constants, so wallets are recommended to declare them explicitly in the `sessionProperties` object in a [CAIP-25] interaction for maximum interoperability and stability.
Note that the `sessionProperties` object is shared across any and all namespaces in a given wallet<>application session, which may span multiple types of networks all declaring `sessionProperties`, so to avoid collisions the following properties names are recommended for easy mapping to the **case-sensitive** properties names in the [Wallet Standard]:

|`sessionProperties` key in [CAIP-25] expression|[Wallet Adapter] mapping|values|documentation|reference implementation|
|---|---|---|---|---|
|`SolanaTransactionVersion`|`SolanaTransactionVersion`|`0` or `legacy` (default)|[solana.com][Transaction Version Declaration]|[github.com][Transaction Version Refimpl]|
|`SolanaTransactionCommitment`|`SolanaTransactionCommitment`|`finalized` (default), `confirmed`, `processed`|[solana.com][State Commitment Declaration]|[github.com][State Commitment Refimpl]|

As these properties are mandatory and required for stability in [Wallet Standard] connections, [CAIP-25] providers MAY inject defaults if any of the above are not set explicitly by a wallet.
For this reason, wallets are RECOMMENDED to set them explicitly even if not requested by their counterparty to avoid inaccurate values being injected.

## Examples

TBD

## References

- [EIP155][]: Ethereum Improvement Proposal specifying generation and validation of ChainIDs
- [Wallet Standard][] Interface specification
- [Wallet Adapter][] Tooling
- [Wallet Standard Multichain Extensions][]
- [Transaction Version Declaration][]
- [State Commitment Declaration][]

[Wallet Adapter]: https://github.com/anza-xyz/wallet-adapter/tree/master?tab=readme-ov-file#wallet-adapter
[Wallet Standard]: https://wallet-standard.github.io/wallet-standard/
[Wallet Standard Multichain Extensions]: https://github.com/wallet-standard/wallet-standard/blob/master/EXTENSIONS.md
[Transaction Version Declaration]: https://solana.com/docs/core/transactions/versions#current-transaction-versions
[Transaction Version Refimpl]: https://github.com/anza-xyz/wallet-standard/blob/2c354cf07daa1d440ba9631fcefc5c00b07aa9dd/packages/core/features/src/signTransaction.ts#L31
[State Commitment Declaration]: https://solana.com/docs/rpc#configuring-state-commitment
[State Commitment Refimpl]: https://github.com/anza-xyz/wallet-standard/blob/2c354cf07daa1d440ba9631fcefc5c00b07aa9dd/packages/core/features/src/signTransaction.ts#L660
[CAIP-25]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-25.md
[CAIP-217]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-217.md
[EIP155]: https://eips.ethereum.org/EIPS/eip-155

## Rights

Copyright and related rights waived via CC0.
