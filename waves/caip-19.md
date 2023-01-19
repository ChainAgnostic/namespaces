---
caip: 2
title: Waves Blockchain ID Specification
author: Maxim Smolyakov (@msmolyakov), Yury Sidorov (@darksyd94)
discussions-to:
status: Draft
type: Standard
created: 2023-01-19
---

## Rationale
Any account that has enough native token(Waves) to pay a fee can issue its own token. The new token is immediately available.

In Waves token can be enabled sponsorship, that is, allow all users to pay a fee in this token for numbers of transactions.

A token issued on another blockchain cannot be used directly on the Waves blockchain. A new token representing the original one can be issued on the Waves blockchain, and a gateway that pegs the two tokens 1:1 can be deployed.

## Specification of Asset ID

In Waves blockchain Asset is equal to transaction ID, that issued this asset. That right for non-fungible and fungible tokens.

## Examples

| Network name | Asset ID                            |
|--------------|-------------------------------------|
| Mainnet      | DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p |
| Testnet      | DjU9JHRZfNVG22XU518hANGBRL5J12KhAihtkWnZKLNp |

## Links

- [Official website](https://waves.tech)
- [Waves Documentation](https://docs.waves.tech)
- [Waves Developer Portal](https://dev.waves.tech)
- [Waves Asset Documentation Page](https://docs.waves.tech/en/blockchain/token)
- [CAIP-2]()

## Copyright

Copyright and related rights waived via [CC0](../LICENSE).
