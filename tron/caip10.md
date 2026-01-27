---
namespace-identifier: tron-caip10
title: Tron Namespace - Account ID Specification
author: WalletConnect Team
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/XXX
status: Draft
type: Standard
created: 2026-01-27
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

Tron addresses use Base58Check encoding and are derived from ECDSA public keys using the secp256k1 curve (same as Ethereum).
All Tron addresses:
- Start with the letter `T` (due to the `0x41` address prefix)
- Are exactly 34 characters in length
- Include a 4-byte checksum for error detection
- Are case-sensitive

The address format provides both human readability and built-in validation through the checksum mechanism.

## Syntax

The syntax of a Tron address follows Base58Check encoding with the following constraints:

**Regular Expression**: `^T[1-9A-HJ-NP-Za-km-z]{33}$`

Where:
- First character is always `T`
- Remaining 33 characters use Base58 alphabet (excluding 0, O, I, l)
- Total length is exactly 34 characters

### Address Generation

Tron addresses are generated through the following process:
1. Generate ECDSA key pair using secp256k1 curve
2. Extract 64-byte public key
3. Hash with Keccak256 (SHA3)
4. Take last 20 bytes of hash
5. Prepend address prefix byte `0x41`
6. Double SHA256 hash and append first 4 bytes as checksum
7. Base58 encode the result

## Chain IDs

*For context, see the [CAIP-2][] specification.*

| Network        | Chain ID (Hex) | Chain ID (CAIP-2)  |
|----------------|----------------|--------------------|
| Mainnet        | `0x2b6653dc`   | `tron:0x2b6653dc`  |
| Shasta Testnet | `0xcd8690dc`   | `tron:0xcd8690dc`  |
| Nile Testnet   | `0x94a9059e`   | `tron:0x94a9059e`  |

## Test Cases

This is a list of manually composed and validated examples:

```bash
# Tron Mainnet - Standard account address
tron:0x2b6653dc:TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL

# Tron Mainnet - USDT TRC-20 contract address
tron:0x2b6653dc:TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t

# Tron Shasta Testnet
tron:0xcd8690dc:TQQg4EL8o1BSeKJY4MJ8TB8XK7xufxFBvK

# Tron Nile Testnet
tron:0x94a9059e:TLyqzVGLV1srkB7dToTAEqgDSfPtXRJZYH
```

## Address Validation

### Valid Address Examples

```
TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL  ✓ Valid mainnet address
TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t  ✓ Valid mainnet address (USDT contract)
TLyqzVGLV1srkB7dToTAEqgDSfPtXRJZYH  ✓ Valid address
```

### Invalid Address Examples

```
tNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL  ✗ Lowercase 't' (must be uppercase 'T')
TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYq    ✗ Too short (33 characters)
TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeLL  ✗ Too long (35 characters)
0x742d35Cc6634C0532925a3b844Bc9e759  ✗ Hex format (not Base58Check)
```

## Account Types

Tron supports two types of accounts:

1. **Externally Owned Account (EOA)**:
   - Controlled by private key
   - Can initiate transactions
   - Example: `TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL`

2. **Contract Account**:
   - Smart contract address
   - No private key
   - Can only respond to transactions
   - Example: `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` (USDT TRC-20)

Both account types use the same address format and are indistinguishable at the address level.

## Backwards Compatibility

Tron's address format has remained consistent since mainnet launch.
All existing addresses are compatible with the CAIP-10 specification.

## Additional Considerations

### Checksum Validation

The Base58Check encoding includes a 4-byte checksum that should be validated when accepting addresses.
Invalid checksums indicate:
- Typographical errors in address entry
- Data corruption
- Invalid address generation

### Address Activation

Tron addresses must be activated by receiving TRX or TRC-10 tokens before they appear on-chain.
Unactivated addresses:
- Are valid addresses (correct format and checksum)
- Do not appear in blockchain state queries
- Will be created upon receiving first transaction

### Multi-signature Addresses

Tron supports multi-signature accounts with the same address format.
Multi-sig addresses cannot be distinguished from regular addresses without querying account permissions on-chain.

## Resolution Method

To verify an address exists on-chain, make a JSON-RPC request using Tron's native RPC methods:

```jsonc
// Request - Get account balance
{
  "jsonrpc": "2.0",
  "method": "tron_getBalance",
  "params": {
    "address": "TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL"
  },
  "id": 1
}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "balance": "1000000000"
  },
  "id": 1
}
```

Alternatively, using Tron's native HTTP API:

```bash
curl -X POST https://api.trongrid.io/wallet/getaccount \
  -d '{"address":"TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL","visible":true}'
```

## References

- [CAIP-10][]: Account ID Specification
- [CAIP-2][]: Chain ID Specification
- [Tron Developer Hub - Accounts][]: Official account documentation
- [Tron Address Format][]: Technical specification for address generation
- [Base58Check Encoding][]: Bitcoin Base58Check encoding specification

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[Tron Developer Hub - Accounts]: https://developers.tron.network/docs/account
[Tron Address Format]: https://tronprotocol.github.io/documentation-en/mechanism-algorithm/account/
[Base58Check Encoding]: https://en.bitcoin.it/wiki/Base58Check_encoding

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
