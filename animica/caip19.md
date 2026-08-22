---
namespace-identifier: animica-caip19
title: Animica Namespace - Assets
author: Animica (@animicaorg)
discussions-to: https://github.com/ChainAgnostic/namespaces/pulls
status: Draft
type: Standard
created: 2026-08-22
requires: ["CAIP-2", "CAIP-19", "CAIP-20"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Introduction

Animica's native asset is ANM, the token in which transaction fees are paid and balances are denominated.
This profile identifies ANM with the `slip44` asset namespace defined in [CAIP-20][], using Animica's SLIP-44 coin type.
Assets issued by Animica's Python-VM smart contracts are not addressed by this revision; see the [Additional Considerations section](#additional-considerations).

## Specification

### Semantics

The native asset of an Animica network is identified by the `slip44` asset namespace with coin type `4279885`.
The coin type is `0x414E4D`, the ASCII encoding of `ANM`, and is the value Animica's normative [HD Derivation][] uses at the coin-type level of its BIP-44 path (`m/44'/4279885'/account'/0'/address_index'`).
Registration of coin type `4279885` in the [SLIP-44][] registry is pending at the time of writing.

ANM has 9 decimals: one ANM is 10^9 nano-ANM (nANM), and all node RPC quantities (balances, amounts, gas prices) are expressed in nANM.

### Syntax

```text
asset_id:        chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:        "animica:" + reference          (see the Animica CAIP-2 profile)
asset_namespace: "slip44"
asset_reference: "4279885"
```

A validating regular expression for the native asset on any Animica network:

```regex
^animica:(0|[1-9][0-9]{0,9})/slip44:4279885$
```

No other asset namespace or reference is defined by this revision.

### Resolution Mechanics

The native asset has no on-chain identifier to resolve; it is implied by the chain.
To read an account's holding of the native asset, call `state.getBalance` with a native address on an endpoint for the chain named in the identifier:

```jsonc
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "state.getBalance",
  "params": ["anim1zqpn54yt2fz07wg5zz33qplkh7tewv30tm5s9cdwvag6kf6myvd2d5sj9pzp7"]
}

// Response
{ "jsonrpc": "2.0", "id": 1, "result": "0x0" }
```

The result is a hexadecimal quantity in nANM; divide by 10^9 to obtain ANM.
A plain transfer of the native asset uses a gas limit of 21,000 at the gas price returned by `eth_gasPrice` (currently `0x1` nANM per gas on mainnet), so the fee is 21,000 nANM, or 0.000021 ANM.

## Rationale

Using the `slip44` asset namespace for the native asset follows [CAIP-20][] and the practice of other namespaces in this registry, and it reuses the coin type that Animica wallets already derive keys with.
Pinning the reference to the single value `4279885` keeps the identifier unambiguous while the SLIP-44 registration is in progress.

### Backwards Compatibility

There was no previously registered CAIP-19 profile for Animica.
This profile introduces no new on-chain identifiers.

## Test Cases

### Valid identifiers

```text
# ANM, the native asset of Animica mainnet
animica:1/slip44:4279885

# Native asset of the reference reserved for the public testnet
animica:2/slip44:4279885
```

### Invalid identifiers

```text
# Wrong coin type (60 is Ethereum)
animica:1/slip44:60

# Ticker instead of coin type
animica:1/slip44:ANM

# Hexadecimal coin type
animica:1/slip44:0x414e4d

# Asset namespace not defined by this profile
animica:1/erc20:anim1zqpn54yt2fz07wg5zz33qplkh7tewv30tm5s9cdwvag6kf6myvd2d5sj9pzp7

# Contract-token form reserved for a future revision
animica:1/contract:anim1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq3cshhr
```

## Additional Considerations

Animica smart contracts run in a Python virtual machine and can issue their own assets.
This revision deliberately defines only the native asset.
An asset namespace for contract-issued tokens (for example `animica:1/contract:anim1...`) is reserved for a future revision, to be specified once there is a stable token interface in the Animica ecosystem to reference.
Until then, identifiers using any asset namespace other than `slip44` MUST NOT be treated as valid under this profile.

## References

- [CAIP-2][] - Blockchain ID specification
- [CAIP-19][] - Asset Type and Asset ID specification
- [CAIP-20][] - Asset Reference for the SLIP44 Asset Namespace
- [Animica CAIP-2 Profile][CAIP-2 Profile] - Chain identifiers in this namespace
- [Animica CAIP-10 Profile][CAIP-10 Profile] - Account identifiers in this namespace
- [SLIP-44][] - Registered coin types for BIP-0044
- [HD Derivation][] - Normative derivation path using coin type `4279885` and the ANM unit definition
- [Chain Parameters][] - Animica chain ids, units, and network parameters
- [Public RPC][] - Public JSON-RPC 2.0 endpoint for mainnet
- [NonKYC market][] - Exchange where ANM trades (ANM/USDT)

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[CAIP-20]: https://chainagnostic.org/CAIPs/caip-20
[CAIP-2 Profile]: ./caip2.md
[CAIP-10 Profile]: ./caip10.md
[SLIP-44]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[HD Derivation]: https://github.com/animicaorg/all/blob/36f995f241cd3e54f66c7a5a6f373d4587bbc60d/docs/wallet/HD_DERIVATION.md
[Chain Parameters]: https://github.com/animicaorg/all/blob/36f995f241cd3e54f66c7a5a6f373d4587bbc60d/docs/spec/CHAIN_PARAMS.md
[Public RPC]: https://rpc.animica.org/rpc
[NonKYC market]: https://nonkyc.io/market/ANM_USDT

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
