---
namespace-identifier: solana-caip25
title: Solana Namespace - JSON-RPC Provider Authorization
author: Jon Wong (@jnwng), Glitch (@glitch-txs), bumblefudge (@bumblefudge)
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

## Network-Specific versus Namespace-Wide Scopes

Few use-cases incorporating multiple Solana-compatible networks require granular permissions or capability declarations per-chain, so a Solana-wide [CAIP-217] authorization scope (keyed to the entire `solana` namespace rather than to a specific chain), with permissions and capabilities set and with only one member at a time in the `chains` array, is recommended in most cases.

## Multichain Considerations

Developers addressing multichain use-cases incorporating non-Solana networks are RECOMMENDED to use distinct [CAIP-217] authorization objects per chain type, in cases where those [CAIP-25] capabilities and configurations can be deterministically mapped to [Wallet Standard Multichain Extensions] variables by a [CAIP-25] provider.

Also, consumers of the [Wallet Standard][] interface assume the `WalletAdapterNetwork` enum variable to be set to exactly one network at a time, so implementers are recommended to map only one `chains` member at a time to this standard interface, whether by ordering it by preference or by never allowing it to have more than one member at a time.

## Setting Environmental Variables to pass via Wallet Standard

Wallet capabilities in the [Wallet Standard] model are declared upfront at time of connection and persisted as read-only constants.
For maximum interoperability and stability, wallets are recommended to declare these variables explicitly in the `scopedProperties` object corresponding to each Solana scope they authorize when accepting a [CAIP-25] connection.
Note that the `scopedProperties` object is partitioned to parallel the `sessionScopes`, so duplicate entries need to be made for each Solana scope.

|`scopedProperties` key in [CAIP-25] expression|[Wallet Adapter] mapping|values|documentation|interface reference|
|---|---|---|---|---|
|`supportedTransactionVersions`|`supportedTransactionVersions`|array containing `0` and/or `legacy` (both by default)|[solana.com][Transaction Version Declaration]|[github.com][Transaction Version Interface Reference]|

## Examples

Example CAIP-25 Request

```json

{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "provider_authorize",
  "params": {
    "sessionScopes": {
      "bip122": { ... },
      "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp": { ... }
      "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1": { ... }
    },
  }
}

```

Example CAIP-25 Response

```json

{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "provider_authorize",
  "params": {
    "sessionScopes": {
      "bip122": { ... },
      "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp": { ... }
      "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1": { ... }
    },
    "scopedProperties": {
      "bip122": { ... }
      "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp": {
        "supportedTransactionVersions": ["legacy", "0"]
      }
      "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1": {
        "supportedTransactionVersions": ["0"]
      }
    }         
  }
}

```

## References

- [EIP155][]: Ethereum Improvement Proposal specifying generation and validation of ChainIDs
- [Wallet Standard][] Interface specification
- [Wallet Adapter][] Tooling
- [Wallet Standard Multichain Extensions][]
- [Transaction Version Declaration][]

[Wallet Adapter]: https://github.com/anza-xyz/wallet-adapter/tree/master?tab=readme-ov-file#wallet-adapter
[Wallet Standard]: https://wallet-standard.github.io/wallet-standard/
[Wallet Standard Multichain Extensions]: https://github.com/wallet-standard/wallet-standard/blob/master/EXTENSIONS.md
[Transaction Version Declaration]: https://solana.com/docs/core/transactions/versions#current-transaction-versions
[Transaction Version Interface Reference]: https://github.com/wallet-standard/wallet-standard/blob/master/packages/example/wallets/src/solanaWallet.ts#L79-L88
[CAIP-25]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-25.md
[CAIP-217]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-217.md
[EIP155]: https://eips.ethereum.org/EIPS/eip-155

## Rights

Copyright and related rights waived via CC0.
