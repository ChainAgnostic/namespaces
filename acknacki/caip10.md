---
namespace-identifier: acknacki-caip10
title: Acki Nacki Blockchain - Account ID Specification
author: Mitja Goroshevsky (@Futurizt)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/XXX
status: Draft
type: Standard
created: 2026-04-07
requires: CAIP-2, CAIP-10
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Introduction

Acki Nacki uses a two-part account addressing scheme. Each account is
identified by a **DApp ID** (256 bits) and an **Account ID** (256 bits),
forming a 512-bit composite address called `AccountRouting`.

The DApp ID groups contracts into a logical application. All contracts
within the same DApp ID share a gas pool (DappConfig) and can transact
internally without gas costs. The Account ID uniquely identifies the
contract within its DApp.

When a contract is deployed by an external message, its DApp ID equals
its own Account ID (self-originating). When deployed by an internal
message from another contract, it inherits the sender's DApp ID.

## Specification

### Semantics

An Acki Nacki account address consists of:
- **DApp ID**: 256-bit identifier (32 bytes, 64 hex chars)
- **Account ID**: 256-bit identifier (32 bytes, 64 hex chars)

Together they form an `AccountRouting` — the full address used for
message routing and thread assignment in the Acki Nacki network.

### Syntax

The CAIP-10 account address is the concatenation of the lowercase
hex-encoded DApp ID and Account ID, separated by a period:

```
acknacki:<chain_id>:<dapp_id>.<account_id>
```

Where:
- `<chain_id>` is the CAIP-2 reference (e.g. `0` for mainnet)
- `<dapp_id>` is the 64-character lowercase hex DApp ID
- `<account_id>` is the 64-character lowercase hex Account ID

For self-originating contracts (deployed via external message),
`dapp_id == account_id`.

Validation regex for the account address portion:

```
[0-9a-f]{64}\.[0-9a-f]{64}
```

Total CAIP-10 validation:

```
acknacki:[-]?[0-9]{1,10}:[0-9a-f]{64}\.[0-9a-f]{64}
```

### Resolution Mechanics

An account can be queried via the GraphQL API using only the Account ID
portion (prefixed with `0:` for legacy compatibility):

```graphql
query {
  blockchain {
    account(address: "0:<account_id_hex>") {
      info {
        balance
      }
    }
  }
}
```

The DApp ID of a deployed contract can be determined from the deployment
transaction: if deployed externally, `dapp_id = account_id`; if deployed
internally, `dapp_id` is inherited from the sender.

## Rationale

The two-part address reflects Acki Nacki's unique DApp ID architecture.
Unlike workchain-based addressing used in other chains, the DApp ID
is a logical grouping mechanism that determines gas routing and thread
assignment. Including both parts in the CAIP-10 address preserves the full
routing information needed for cross-DApp operations.

The period separator (`.`) is used instead of colon (`:`) to avoid
ambiguity with the CAIP-10 namespace:chain_id:address format.

### Backwards Compatibility

This is the initial specification. No legacy identifiers exist.

## Test Cases

```
# Self-originating contract on mainnet (dapp_id == account_id)
acknacki:0:03079cdd1f5c3044fb3f7993becb2f581ffc1e3d128db4afc411e7870af883c3.03079cdd1f5c3044fb3f7993becb2f581ffc1e3d128db4afc411e7870af883c3

# Child contract deployed within a DApp on mainnet
# (dapp_id = SwarmRoot address, account_id = child wallet address)
acknacki:0:afdfe5f15a73a966f38de23bd38436a6a0a0f02a4b81f53d30d6eab94b374610.5fcf27147706876b13be473280ca6fa3ce9e5babf3d288926d929ca37998a505

# Contract on shellnet
acknacki:1:03079cdd1f5c3044fb3f7993becb2f581ffc1e3d128db4afc411e7870af883c3.03079cdd1f5c3044fb3f7993becb2f581ffc1e3d128db4afc411e7870af883c3
```

## Additional Considerations

The DApp ID system is fundamental to Acki Nacki's gasless transaction
model. Contracts within the same DApp ID share a gas pool via DappConfig,
enabling internal transactions without explicit gas payment. Cross-DApp
transfers of the native VMSHELL token are zeroed at the protocol level,
while ECC tokens (SHELL) can cross DApp boundaries.

Future protocol upgrades may introduce additional addressing components
(e.g., thread identifiers) that could extend this specification.

## References

- [Acki Nacki Documentation][docs] - Official documentation
- [Acki Nacki Accounts][accounts] - Account and DApp ID documentation
- [DApp ID Guide][dappid] - Full guide on DApp ID creation and fees
- [CAIP-2 Profile][] - Acki Nacki chain identification

[docs]: https://docs.ackinacki.com
[accounts]: https://docs.ackinacki.com/for-developers/accounts
[dappid]: https://dev.ackinacki.com/dapp-id-full-guide-creation-fees-centralized-replenishment
[CAIP-2 Profile]: ./caip2.md
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
