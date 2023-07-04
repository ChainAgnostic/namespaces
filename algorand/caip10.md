---
namespace-identifier: algorand-caip10
title: Algorand Namespace - Addresses
author: Kevin Wellenzohn (@k13n)
status: Draft
type: Standard
created: 2023-06-05
updated: 2023-06-05
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

Algorand addresses are canonically represented as 58-character long strings, written in all-upper-case. Account addresses are independent of the network in which they are used, and should be prefixed by the chainID of mainnet when stored in CAIP-10 format unless another chainID is significant in context (i.e. in a chainID-specific transaction). Addresses are derived from a base32-encoding of a 32-byte key followed by a 4-byte checksum. The base32 padding (`=`) is dropped.

Algorand accounts, smart contracts, and logic signatures all share the same address format. They differ in how the 32-byte key is computed:

1. [Accounts]: The 32-byte key is the public key of a Ed25519 key-pair.
2. [Smart Contracts][]: The 32-byte key is the SHA512/256 hash of the byte-string `0x6170704944` (hexadecimal representation of the ASCII string `appID`) concatenated with the smart contract's ID as 64-bit big-endian integer.
3. [Logic Signatures][]: The 32-byte key is the SHA512/256 hash of the byte-string `0x50726F6772616D` (hexadecimal representation of the ASCII string `Program`) concatenated with the smart signature's compiled byte-code.

The checksum is computed as the four last bytes in the SHA512/256 hash of the 32-byte key.

A raw address, consisting of the 32-byte key plus 4-byte checksum, contains `(32+4)*8 = 288` bits of information. The base32-encoding of this address contains 58 characters, each encoding 5 bits of information, hence `58 * 5 = 290` bits in total. This means the last two bits of the base32-encoding are redundant and Algorand enforces that they be zero. This means a valid Algorand address must end in one of the following characters: `[A, E, I, M, Q, U, Y, 4]`.


## Syntax

Algorand addresses match the following regular expression:

```
[A-Z2-7]{57}[AEIMQUY4]
```


## Test Cases

Account address:

```
# Public key (in HEX format)
e12d647d2dade456f311c03a3637bba7db43e05dc4985f7ca0b8db158ec3458c

# Algorand MainNet
algorand:wGHE2Pwdvd7S12BL5FaOP20EGYesN73k:4EWWI7JNVXSFN4YRYA5DMN53U7NUHYC5YSMF67FAXDNRLDWDIWGM5DQGBA

# Algorand TestNet
algorand:SGO1GKSzyE7IEPItTxCByw9x8FmnrCDe:4EWWI7JNVXSFN4YRYA5DMN53U7NUHYC5YSMF67FAXDNRLDWDIWGM5DQGBA

# Algorand BetaNet
algorand:mFgazF-2uRS1tMiL9dsj01hJGySEmPN2:4EWWI7JNVXSFN4YRYA5DMN53U7NUHYC5YSMF67FAXDNRLDWDIWGM5DQGBA
```


Smart contract address:

```
# App ID
1002541853

# Algorand MainNet
algorand:wGHE2Pwdvd7S12BL5FaOP20EGYesN73k:XSKED5VKZZCSYNDWXZJI65JM2HP7HZFJWCOBIMOONKHTK5UVKENBNVDEYM

# Algorand TestNet
algorand:SGO1GKSzyE7IEPItTxCByw9x8FmnrCDe:XSKED5VKZZCSYNDWXZJI65JM2HP7HZFJWCOBIMOONKHTK5UVKENBNVDEYM

# Algorand BetaNet
algorand:mFgazF-2uRS1tMiL9dsj01hJGySEmPN2:XSKED5VKZZCSYNDWXZJI65JM2HP7HZFJWCOBIMOONKHTK5UVKENBNVDEYM
```


Logic signature address:

```
# Logic signature (byte-code in HEX):
0120010022

# Algorand MainNet
algorand:wGHE2Pwdvd7S12BL5FaOP20EGYesN73k:KI4DJG2OOFJGUERJGSWCYGFZWDNEU2KWTU56VRJHITP62PLJ5VYMBFDBFE

# Algorand TestNet
algorand:SGO1GKSzyE7IEPItTxCByw9x8FmnrCDe:KI4DJG2OOFJGUERJGSWCYGFZWDNEU2KWTU56VRJHITP62PLJ5VYMBFDBFE

# Algorand BetaNet
algorand:mFgazF-2uRS1tMiL9dsj01hJGySEmPN2:KI4DJG2OOFJGUERJGSWCYGFZWDNEU2KWTU56VRJHITP62PLJ5VYMBFDBFE
```


## References

- [Algorand Developer Documentation][]: Homepage for developer documentation


[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[Accounts]: https://developer.algorand.org/docs/get-details/accounts/#keys-and-addresses
[Smart Contracts]: https://developer.algorand.org/docs/get-details/dapps/smart-contracts/apps/
[Logic Signatures]: https://developer.algorand.org/docs/get-details/dapps/smart-contracts/smartsigs/
[Algorand Developer Documentation]: https://developer.algorand.org/docs/


## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
