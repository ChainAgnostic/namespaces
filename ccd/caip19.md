---
namespace-identifier: ccd-caip19
title: Concordium - Asset ID Specification
author: "Concordium development team <ops+caip@concordium.com>"
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/229
status: Draft
type: Standard
created: 2026-09-17
requires: CAIP-2
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Introduction

Concordium has three distinct kinds of assets that can be referenced:

- **The native CCD coin**: the chain's own currency token, not managed by a smart contract.
- **Protocol Level Tokens (PLTs)**: tokens implemented at the protocol level via a chain-governance operation (see [CIS-7][]), rather than through a smart contract.
- **CIS-2 tokens**: fungible or non-fungible tokens managed by a smart contract that implements the [CIS-2][] token standard (Concordium's analogue of ERC-20/ERC-721/ERC-1155).

Each is given its own `asset_namespace` below.

## Specification

### Semantics

All three profiles are built on top of the Concordium [CAIP-2 Profile][], which identifies a Concordium network by a 32-character prefix of its genesis block hash.

The native CCD coin is identified using the `slip44` asset namespace, per [SLIP-0044][], the same convention used by other namespaces (e.g. `eip155`) for their native currencies.

A PLT is identified by its **Token ID**, a short, case-insensitive text symbol assigned to the token at creation time (see [CIS-7][]).

A CIS-2 token is identified by its **token address**: a single Base58btc-encoded string that already encodes the token's smart contract (index and subindex) together with the token's own ID, per the [CIS-2][] specification. Because the contract and token ID are both embedded in this one string, no separate `token_id` path segment is required.

### Syntax

For all assets, the format is `namespace` + ":" + `chainId` + "/" + `assetNamespace` + ":" + `assetReference`.

For each asset type, `assetReference` is assigned based on the table below:

| Asset Namespace | Asset Reference |
| slip-44 | coinType |
| plt | token ID |
| cis-2 | Token Address |

#### Details for each asset type

Concordium native CCD coin:

```
CAIP-19 Asset ID: namespace + ":" + chainId + "/" + "slip-44" + ":" + coinType
namespace: ccd
chainId: 32-char prefix from the hash of the genesis block
assetNamespace: slip-44
coinType: 919, the SLIP-44 coin type registered for CCD

Native CCD asset ID can be validated with the following regular expression:

`ccd:[a-zA-Z0-9]{32}/slip44:919`
```

Concordium Protocol-Level Tokens (PLTs):

```
CAIP-19 Asset ID: namespace + ":" + chainId + "/" + "plt" + ":" + tokenId
namespace: ccd
chainId: 32-char prefix from the hash of the genesis block
tokenId: 2-128 character case-insensitive string, characters [a-zA-Z0-9-.%]
assetNamespace: plt
PLT asset IDs can be validated with the following regular expression:

`ccd:[a-zA-Z0-9]{32}/plt:[a-zA-Z0-9\-.%]{2,128}`
```

Concordium CIS-2 tokens:

```
CAIP-19 Asset ID: namespace + ":" + chainId + "/" + "cis-2" + ":" + tokenAddress
namespace: ccd
chainId: 32-char prefix from the hash of the genesis block
assetNamespace: cis-2
tokenAddress: Base58Check encoding (version byte 0x02) of ULEB128(contract index) + ULEB128(contract subindex) + (1-byte length prefix + token id bytes), per the CIS-2 Token Address representation

CIS-2 asset IDs can be validated with the following regular expression:

`ccd:[a-zA-Z0-9]{32}/cis-2:[1-9A-HJ-NP-Za-km-z]+`
```

### Resolution Mechanics

<!-- CAVEAT (leave for reviewers): the CIS-2 token address test values below were
computed independently from the documented ULEB128 + Base58Check(version=0x02)
algorithm in the CIS-2 spec, not copied from an official test vector -- there is
no published example string in the CIS-2 spec or SDK docs. Please cross-check
against `tokenAddressToBase58` from `@concordium/web-sdk` or `concordium-client`
before merging. -->

Native CCD and Protocol Level Token (PLT) asset IDs require no resolution beyond the [CAIP-2 Profile][] chain identifier. A PLT's existence and metadata can be looked up via the `GetTokenInfo` gRPC call against a Concordium node (see [Concordium gRPC][]).

A CIS-2 token address already encodes the target contract and token ID, so no additional RPC round-trip is required to parse the identifier itself; decoding requires implementing the ULEB128 and Base58Check (version byte `0x02`) algorithm described in the [CIS-2][] specification. Whether the referenced token actually exists can be checked via a CIS-2 contract's `balanceOf`/`tokenMetadata` entrypoints (see [CIS-2][]).

## Rationale

In addition to the chain native CCD asset, which is also the token used to pay for chain transactions, and PLTs which are externally issued but built into the protocol layer, Concordium also supports Fungible and Non-Fungible tokens with the CIS-2 standard for smart contract defined assets.

This CAIP-19 profile reuses the [CAIP-2][CAIP-2 Profile] genesis-hash-derived chain identifier as-is, so that CAIP-19 addresses stay consistent with the network identification scheme already defined for Concordium, and uniquely define each asset across both the protocol native, and contract defined assets.


### Backwards Compatibility

N/A

## Test Cases

### CIS-2 Tokens

```
# Concordium mainnet CIS-2 token (contract 10082/0, token id 0x00)
ccd:9dd9ca4d19e9393877d2c44b70f89acb/cis-2:AQ4hxc1eH3QuK

# Current Concordium testnet CIS-2 token (contract 12802/0, token id 0x01)
ccd:4221332d34e1694168c2a0c0b3fd0f27/cis-2:9BFjQGHJYuvsC
```

### Native CCD

```
# Concordium mainnet CCD
ccd:9dd9ca4d19e9393877d2c44b70f89acb/slip44:919

# Current Concordium testnet CCD
ccd:4221332d34e1694168c2a0c0b3fd0f27/slip44:919
```

### Protocol-Level Tokens

```
# Concordium mainnet PLT
ccd:9dd9ca4d19e9393877d2c44b70f89acb/plt:USDQ

# Current Concordium testnet PLT
ccd:4221332d34e1694168c2a0c0b3fd0f27/plt:USDQ
```


## References

- [Concordium Developer Documentation][] - Concordium Developer Documentation
- [Concordium gRPC][] - Interacting with a Concordium node: Description of the Concordium gRPC API.
- [CIS-2][] - Concordium Token Standard 2: fungible and non-fungible tokens, including the Token Address textual representation.
- [CIS-7][] - Concordium's Protocol-Level Tokens (PLTs) specification, including the Token ID format.
- [SLIP-0044][] - Registry of coin types for BIP-0044, including CCD's registered coin type 919.

- [CCD CAIP-2][CAIP-2 Profile] - Details of the Concordium CAIP-2 Chain Identifier
- [CAIP-2][CAIP-2] - The Blockchain ID Specification
- [CAIP-19][CAIP-19] - The Asset ID Specification

[CAIP-2 Profile]: ./caip2.md
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19

[Concordium Developer Documentation]: https://developer.concordium.software/en/mainnet/index.html
[Concordium gRPC]: http://developer.concordium.software/concordium-grpc-api/
[CIS-2]: https://proposals.concordium.com/CIS/cis-2.html
[CIS-7]: https://proposals.concordium.com/CIS/cis-7.html
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
