---
caip: 2
title: Waves Blockchain ID Specification
author: Maxim Smolyakov (@msmolyakov), Yury Sidorov (@darksyd94)
discussions-to:
status: Draft
type: Standard
created: 2023-01-19
---

## CAIP-10

For context, see the [CAIP-10][] specification.

## Rationale

Waves addresses are 26 byte array and in UIs the address is displayed as base58 encoded string.

## Syntax

The syntax of waves addresses:

| Field order number | Field                   | Field type     | Field size in bytes | Comments                                                                                                                                                                             |
|--------------------|-------------------------|----------------|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1                  | Entity type             | Byte           | 1                   | Value must be 1                                                                                                                                                                      |
| 2                  | Chain ID                | Byte           | 1                   | For context, see the [CAIP-2][] specification.  87 — for Mainnet 84 — for Testnet 83 — for Stagenet                                                                                  |
| 3                  | Account public key hash | Array of bytes | 20                  | First 20 bytes of the result of the Keccak256 hashing function. Here publicKey is the array of bytes of the account public key                                                       |
| 4                  | Checksum                | Array of bytes | 4                   | First 4 bytes of the result of the Keccak256 hashing function.  Here data is the array of bytes of three fields put together: 1. Entity type  2. Chain ID 3. Account public key hash |

## Test Cases

| Network name | Address                             |
|--------------|-------------------------------------|
| Mainnet      | 3PGC6BSrwRkuGAUj12WjWQTTPhK7cnbFQZR |
| Testnet      | 3MvbutkV3xapQVUcGBGWCongwfdH8LKTm8w |

## Links

- [Official website](https://waves.tech)
- [Waves Documentation](https://docs.waves.tech)
- [Waves Developer Portal](https://dev.waves.tech)
- [Waves Address Documentation Page](https://docs.waves.tech/en/blockchain/account/address)

## Copyright

Copyright and related rights waived via CC0.
