---
namespace-identifier: stellar-caip19
title: Stellar Namespace - Assets
author: Pelle Braendgaard (@pelle)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/157
status: Draft
type: Standard
created: 2025-11-06
requires: ["CAIP-2", "CAIP-10", "CAIP-19", "CAIP-20"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Rationale

In the Stellar ecosystem, assets can be represented in several distinct formats. The native asset (lumens/XLM) is identified using the SLIP-44 coin type registry (coin type 148), while issued assets are uniquely identified by combining an asset code (1-12 characters) with an issuer account address, separated by a hyphen. Additionally, Protocol 18 introduced liquidity pool shares (CAP-38) which represent fractional ownership in automated market maker pools, and Protocol 20 introduced Soroban smart contract tokens following the SEP-41 token interface standard.

## Syntax

After the CAIP-2 namespace+chainID, a slash defines an `asset_namespace` and an `asset_reference`. Stellar supports multiple asset types with different identification schemes:

### Asset Namespaces

| Namespace | Description | Reference Format |
| :--- | :--- | :--- |
| `slip44` | Native lumens (XLM) via SLIP-44 | `148` (Stellar's coin type) |
| `asset` | Issued asset with code and issuer | `{asset_code}-{issuer_address}` |
| `cap38` | Liquidity pool shares (CAP-38) | `{pool_id}` (64-char hex hash) |
| `sep41` | Soroban smart contract token (SEP-41) | `{contract_address}` (56-char strkey) |

### Asset Code Requirements

Asset codes for issued assets must:

- Consist of printable ASCII characters (octets 0x21 through 0x7e)
- Be 1-12 characters in length
- Be case-sensitive
- Not contain the hyphen character (`-`) as it is used as the delimiter

### Issuer Address

The issuer address must be a valid Stellar G-address (56 characters, starting with `G`).

### Liquidity Pool ID

Liquidity pool IDs are deterministically calculated as:

- SHA-256 hash of the liquidity pool parameters
- Pool parameters include: pool type and both assets in lexicographical order
- Represented as a 64-character lowercase hexadecimal string
- Only one pool can exist for a given asset pair

### Contract Address

Soroban contract addresses are:
- Stellar strkey-encoded contract addresses (56 characters, starting with `C`)
- For Stellar Asset Contracts (SAC), the address can be derived from the classic asset identifier
- Can be obtained using: `stellar contract id asset --asset {code}:{issuer} --network {network}`

## RegEx

The RegEx validation strings are as follows:

```
asset_id:           asset_type
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           namespace + ":" + blockchain_id (as defined in CAIP-2)

asset_namespace:    "slip44" | "asset" | "cap38" | "sep41"

asset_reference:    slip44_ref | asset_ref | cap38_ref | sep41_ref
slip44_ref:         "148"
asset_ref:          asset_code + "-" + issuer_address
asset_code:         [!-,.-~]{1,12}
issuer_address:     G[A-Z2-7]{55}
cap38_ref:          [0-9a-f]{64}
sep41_ref:          C[A-Z2-7]{55}
```

Note: The `asset_code` regex `[!-,.-~]` excludes the hyphen character (ASCII 0x2D) from the printable ASCII range (0x21-0x7E) since hyphen is used as the delimiter.

## Semantics

### Native Asset (XLM/Lumens)

The native asset is identified using the `slip44` namespace with coin type `148` as registered in the SLIP-44 registry. The native asset is unique and does not require an issuer. It is used for:

- Transaction fees (which are burned/destroyed)
- Minimum account balance requirements (base reserves)
- Bridge currency for cross-asset transactions

Example: `stellar:pubnet/slip44:148`

### Issued Assets

Issued assets are created by issuers and must be explicitly trusted by recipients before they can be received. The combination of asset code (1-12 characters) and issuer address uniquely identifies an asset. On the Stellar network, asset codes of 1-4 characters are stored as AlphaNum4, while codes of 5-12 characters are stored as AlphaNum12, but both use the same `asset` namespace in CAIP-19.

Examples:
- USDC issued by Circle: `asset:USDC-{issuer_address}`
- Custom 8-character code: `asset:MYTOKEN8-{issuer_address}`

### Liquidity Pool Shares (CAP-38)

Liquidity pool shares represent fractional ownership in constant product automated market maker pools (CPAMM) as defined in CAP-38. These shares:

- Are non-transferable (cannot be sent between accounts)
- Can be minted by depositing assets into the pool
- Can be redeemed for the underlying assets
- Are identified by a deterministic pool ID hash
- Use the `cap38` namespace

### Soroban Contract Tokens (SEP-41)

Soroban contract tokens follow the SEP-41 token interface standard and include:
- Stellar Asset Contracts (SAC): Wrapped versions of classic Stellar assets with smart contract functionality
- Custom CAP-46-6 compliant tokens: Fully custom tokens implemented as Soroban smart contracts
- All tokens use the `sep41` namespace and are identified by their contract address

## Examples

```
# Native asset (lumens/XLM) on Pubnet
stellar:pubnet/slip44:148

# Native asset on Testnet
stellar:testnet/slip44:148

# USDC (4-character code) on Pubnet
stellar:pubnet/asset:USDC-GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN

# Custom token with 8-character code on Pubnet
stellar:pubnet/asset:MYCOIN88-GDQP2KPQGKIHYJGXNUIYOMHARUARCA7DJT5FO2FFOOKY3B2WSQHG4W37

# Single character asset code on Testnet
stellar:testnet/asset:X-GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ

# Liquidity pool (XLM-USDC pool) on Pubnet
stellar:pubnet/cap38:67260c4c1807b262ff851b0a3fe141194936bb0215b2f77447f1df11998eabb9

# Soroban token contract (USDC) on Pubnet
stellar:pubnet/sep41:CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75

# Custom Soroban token contract on Testnet
stellar:testnet/sep41:CAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABSC4
```

## Backwards Compatibility

Issued Stellar assets (represented here as the `asset` namespace) correspond to the native Stellar `alphanum4` and `alphanum12` asset types, which have been supported since the genesis of the Stellar network and maintain full backward compatibility.

Liquidity pool shares were introduced in Protocol 18 (November 2021) and may not be supported by older clients.

Soroban contract tokens were introduced in Protocol 20 (February 2024) and require Soroban-aware clients and tooling.

## References

- [Stellar Assets Overview][] - Overview of asset types on Stellar
- [SLIP-44][] - Registered coin types for HD wallets
- [CAIP-20][] - Asset Reference for the SLIP44 Asset Namespace
- [CAP-38: Automated Market Makers][] - Liquidity pools specification
- [CAP-46-6: Smart Contract Standardized Asset][] - Soroban token standard
- [SEP-41: Token Interface][] - Standard token interface for Soroban
- [Stellar Asset Contract][] - Documentation for Stellar Asset Contracts
- [Liquidity Pools Guide][] - Guide to using liquidity pools on Stellar


[CAIP-2]: ./caip2.md
[CAIP-10]: ./caip10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-20]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-20.md
[SLIP-44]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[Stellar Assets Overview]: https://developers.stellar.org/docs/learn/fundamentals/stellar-data-structures/assets
[CAP-38: Automated Market Makers]: https://github.com/stellar/stellar-protocol/blob/master/core/cap-0038.md
[CAP-46-6: Smart Contract Standardized Asset]: https://github.com/stellar/stellar-protocol/blob/master/core/cap-0046-06.md
[SEP-41: Token Interface]: https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0041.md
[Stellar Asset Contract]: https://developers.stellar.org/docs/tokens/stellar-asset-contract
[Liquidity Pools Guide]: https://developers.stellar.org/docs/learn/encyclopedia/sdex/liquidity-on-stellar-sdex-liquidity-pools

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
