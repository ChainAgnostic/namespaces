---
namespace-identifier: tenzro-caip25
title: Tenzro Namespace - JSON-RPC Provider Authorization
author: Tenzro Engineering (eng@tenzro.com)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/TBD
status: Draft
type: Standard
created: 2026-05-02
updated: 2026-05-02
requires: ["CAIP-2", "CAIP-25", "CAIP-217"]
---

# CAIP-25

_For context, see the [CAIP-25][] specification._

## Rationale

A Tenzro chain runs three VM façades over a single shared native balance
(EVM, SVM, and Canton/DAML — the Sei-V2-style pointer model). A provider
authorization session against a Tenzro node therefore needs to express
capabilities for **multiple method namespaces routed to the same chain**
rather than for distinct chains. Tenzro reuses [CAIP-25] / [CAIP-217]
for this without inventing new framing: a single Tenzro `chain_id` may
appear under one [CAIP-217] scope object whose `methods` array spans
`eth_*`, `tenzro_*`, and a constrained subset of `solana_*` methods.

This is consistent with how the Tenzro browser extension and SDK
(`network.tenzro.wallet`) authorize sessions today: one scope per chain,
multiple method families within the scope, and the dApp routes calls by
method-name prefix. See "Routing rules" below for the normative routing
that consumers of a Tenzro CAIP-25 session MUST follow.

## Network-Specific versus Namespace-Wide Scopes

Tenzro authorization scopes are **always network-specific** —
`tenzro:<chain_id>` rather than the bare namespace `tenzro`. Each
Tenzro chain has an independent HotStuff-2 BFT validator set and its
own genesis hash; capabilities and account permissions do not transfer
across chains. Implementations MUST NOT use a namespace-wide
`tenzro` scope.

## Multichain Considerations

Tenzro sessions commonly span both a Tenzro chain and external chains
(e.g. a wallet user authorizing a dApp to interact with both
`tenzro:92bd27db9713293097f0e63476e3911e` and `eip155:1`). In that
case implementers SHOULD use distinct [CAIP-217] authorization
objects per chain — the Tenzro scope for Tenzro-routed methods, and a
separate `eip155:N` scope for direct Ethereum interactions.

The Tenzro injected provider (`window.tenzro`, EIP-6963 `rdns =
network.tenzro.wallet`) speaks [EIP-1193] for its EVM façade and
exposes `tenzro_*` and a constrained `solana_*` subset over the same
session. Hosts MAY also expose a parallel `window.solana` Wallet
Standard surface bound to the same underlying account; in that case
the same Tenzro `chain_id` scope authorizes both surfaces.

## Routing rules

Within a Tenzro scope, the provider routes inbound calls by method-name
prefix. Implementations MUST observe the following routing — these
rules match the Tenzro reference extension's `resolveMethodName`
dispatcher and the node's actual RPC surface.

| Method prefix              | Routed to                                        | Notes |
| :------------------------- | :----------------------------------------------- | :---- |
| `eth_*`, `personal_*`, `wallet_*` | EVM façade JSON-RPC on the node           | Standard EIP-1193 surface |
| `tenzro_*`                 | Native Tenzro RPC namespace                      | Multi-VM scope methods, identity, payments, agents, multi-modal AI |
| `solana_signTransaction`, `solana_signAndSendTransaction`, `solana_signMessage`, `solana_signIn` | Wallet-side signers (SVM façade transactions) | Pass-through; signed and submitted via the SVM transaction path |
| `solana_*` reads (`getBalance`, `getTokenAccountsByOwner`, etc.) | **Rejected** — re-route to `tenzro_*` equivalents | Tenzro does NOT implement the Solana JSON-RPC read surface; use `tenzro_listTokens` / `tenzro_getTokenBalance` / `tenzro_crossVmTransfer` |

A request for an unsupported method within the scope MUST return
JSON-RPC error code `-32601` (`Method not found`) with a message
identifying the offending method and the routing rule that rejected it.

## Setting Environmental Variables to pass via scopedProperties

Tenzro scopes SHOULD declare per-scope capabilities in
`scopedProperties`. The following keys are defined by this namespace:

| `scopedProperties` key | Type                              | Meaning |
| :---                   | :---                              | :--- |
| `vmFacades`            | array of `"evm" \| "svm" \| "canton"` | Subset of VM façades the wallet will route for in this session. Default: `["evm", "svm"]`. |
| `dpopBound`            | boolean                           | Whether per-call DPoP-bound auth ([RFC 9449][]) is required. Tenzro extension sessions default to `true`. |
| `nativeAssetCaip19`    | string ([CAIP-19][])              | The CAIP-19 identifier for the native asset (TNZO) on this chain — informational, useful for fee display. |
| `evmChainId`           | integer                           | The EIP-155 integer `chainId` (`eth_chainId`) corresponding to this Tenzro chain — clients use this to fill the `eth_chainId` field of EVM transactions without a separate round-trip. |

Implementers are RECOMMENDED to declare `evmChainId` whenever the EVM
façade is included in `vmFacades`, since EVM tooling needs the
integer chain ID and it cannot be derived from the truncated genesis
hash.

## Examples

Example CAIP-25 Request

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "provider_authorize",
  "params": {
    "sessionScopes": {
      "tenzro:92bd27db9713293097f0e63476e3911e": {
        "methods": [
          "eth_chainId",
          "eth_blockNumber",
          "eth_getBalance",
          "eth_sendTransaction",
          "personal_sign",
          "tenzro_listTokens",
          "tenzro_getTokenBalance",
          "tenzro_crossVmTransfer",
          "solana_signTransaction",
          "solana_signMessage"
        ],
        "notifications": ["accountsChanged", "chainChanged"],
        "accounts": [
          "tenzro:92bd27db9713293097f0e63476e3911e:0x0000000000000000000000000000000000000000000000000000000000000000"
        ]
      }
    }
  }
}
```

Example CAIP-25 Response

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": {
    "sessionScopes": {
      "tenzro:92bd27db9713293097f0e63476e3911e": {
        "methods": [
          "eth_chainId",
          "eth_blockNumber",
          "eth_getBalance",
          "eth_sendTransaction",
          "personal_sign",
          "tenzro_listTokens",
          "tenzro_getTokenBalance",
          "tenzro_crossVmTransfer",
          "solana_signTransaction",
          "solana_signMessage"
        ],
        "notifications": ["accountsChanged", "chainChanged"],
        "accounts": [
          "tenzro:92bd27db9713293097f0e63476e3911e:0x0000000000000000000000000000000000000000000000000000000000000000"
        ]
      }
    },
    "scopedProperties": {
      "tenzro:92bd27db9713293097f0e63476e3911e": {
        "vmFacades": ["evm", "svm"],
        "dpopBound": true,
        "evmChainId": 1337,
        "nativeAssetCaip19": "tenzro:92bd27db9713293097f0e63476e3911e/slip44:tenzro"
      }
    }
  }
}
```

## References

- [CAIP-2][]
- [CAIP-19][]
- [CAIP-25][]
- [CAIP-217][]
- [EIP-1193][]
- [EIP-6963][]
- [RFC 9449][] — DPoP
- [Tenzro Network repository][repo]

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-25]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-25.md
[CAIP-217]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-217.md
[EIP-1193]: https://eips.ethereum.org/EIPS/eip-1193
[EIP-6963]: https://eips.ethereum.org/EIPS/eip-6963
[RFC 9449]: https://www.rfc-editor.org/rfc/rfc9449
[repo]: https://github.com/tenzro/tenzro-network

## Rights

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
