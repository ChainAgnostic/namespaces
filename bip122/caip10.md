---
namespace-identifier: bip122-caip10
title: BIP122 Namespace - Addresses
author: Simon Warta (@webmaster128), ligi <ligi@ligi.de>, Pedro Gomes (@pedrouid), bumblefudge (@bumblefudge)
discussions-to: https://github.com/ChainAgnostic/namespaces/pulls/3
status: Draft
type: Standard
created: 2019-12-05
updated: 2024-06-05
requires: ["CAIP-2", "CAIP-10"]
replaces: CAIP-4
---

*For context, see the [CAIP-10][] specification.*

## Rationale

While Ethereum "accounts" were the unstated norm in the definition of
[CAIP-10][], the "script hashes" addressing scheme defined by [BIP13][] map
well enough to "account"-model blockchains that these can be described by a
CAIP-10 reference as "addresses". Other aspects of the UTXO wallet and transaction model (choice of inputs, arbitrary data in witness sections of a segwit transaction, multi-party signature methods, etc.) are topics of ongoing research and community input is welcome, although additional CAIPs may be needed to specify them for chain-agnostic purposes.

## Syntax

At time of writing, only three kinds of address are currently in wide use, with a fourth mostly obsolete in modern usage.
All four, in their most common ASCII base-encodings (base-58-btc, bech32, and bech32m; see below) are of a short enough length to simply include them in their entirety as the `account_address` segment of a [CAIP-10] identifier.
This choice not to transform or subset addresses preserves checksum, sortability, and detectability features of all three modern address types, while also minimizing collision risk.

In order of their adoption on Bitcoin mainnet, the four types of addresses in Bitcoin are:

1. Legacy address, aka pay-to-publickey-hash (P2PKH). These begin with `1` and are [base58btc]-encoded. Defined in the [bitcoin whitepaper][], these are exceedingly rare in contemporary practice due to higher transaction fees and limited functionality compared to the newer types described below. Legacy addresses are not derived from "extended keys" as per the subsequent [BIP44] standard, but are rather hashes of unique public keys, which makes them a weak analogue to addresses in "account-model" systems; for these reasons, they are excluded from [CAIP-10] usage.
2. Pay-to-script-hash (P2SH) address. These were specified in the early [BIP13], and swiftly became the dominant address and signature type in the early years of Bitcoin usage after becoming supported by a [soft fork][BIP16] in 2012. They are [base58btc]-encoded and always begin with `3` in ASCII form on Bitcoin mainnet.
3. Native Segregated-Witness Address (SegWit), aka pay-to-wrapped-publickey-hash (P2WPKH) Address. The derivation of these was standardized in [BIP84], and the soft-fork supporting them at the protocol level coordinated by [BIP141]. They are encoded into ASCII according to the [`bech32`][BIP173] algorithm, and always begin with `bc1q` on Bitcoin mainnet. At time of press, these are nearly universal due to lower transaction fees and higher security than older types.
4. Taproot (P2TR). They are encoded into ASCII according to the [`bech32m`][BIP350] algorithm, and always begin with `bc1q`. Not all wallets support taproot addresses at time of writing, but a Taproot address is required to claim the output of an Ordinal-minting transaction (i.e., a special satoshi) and Taproot addresses have certain privacy properties (on-chain obfuscation of multisig scripts, for example) that drive ongoing adoption.

Note that many forks and variants within the BIP122 design space use different literals to compute addresses, leading to different prefixes and checksum mechanisms on Bitcoin testnet and on other chains in the family of related networks.

### Validation

With the exception of the first, all three can be rudimentarily validated with the following regular expression for Bitcoin mainnet:

`^(bc1|3)[a-km-zA-HJ-NP-Z1-9]{25,34}$`

Rough validation for other networks can be achieved by updating the prefixes in the first enumeration of literals for the network-specific address-types targeted, and (if needed) updating the minimum and maximum lengths accordingly.

For more precise validation, it is recommended to first detect the type from the prefix as mentioned above, then compute the type-specific checksum as specified in the corresponding Bitcoin Improvement Proposals linked above (taking into account different literals for most networks).

### Decorators

In the Bitcoin development community, certain user experience conventions have arisen that can be opted into by applications and wallets, yet are, strictly speaking, not part of the bitcoin protocol and leave no on-chain artefacts in transaction history.
By analogy to web standards, these are best designated with a matrix parameter (i.e., a `#parameter` suffix on the URI), which might be meaningful or useful to clients but are not native to the underlying URL protocol and are traditionally omitted when sent over the wire for resolution.

For example, some wallets segregate Ordinals from regular native-currency balance by receiving them in a dedicated address, to avoid an Ordinal being counted towards spendable balance, or being included unwittingly as an input to a regular (non-Ordinal) transaction.
In this case, the matrix parameter `#ordinal` could be added to communicate to a counterparty that the preceding address has been specifically earmarked for receiving only Ordinal-marked Satoshis and not for general use.
Conversely, Ordinal-aware wallets might mark the other side of this segregation by explicitly marking an address as a `#payment` address.
A client unaware of this convention could, of course, ignore or drop these matrix parameters and treat both as addresses capable of payments, and developers are advised not to assume Ordinals-awareness in a given wallet just because it uses the [CAIP-10] standard or a CAIP-10-aware library.

### Backwards Compatibility

Previously, the legacy CAIP-10 schema was defined by appending as suffix the
CAIP-2 chainId delimited by the at sign (@)

#### Legacy example

`35PBEaofpUeH8VnnNSorM1QZsadrZoQp4N@bip122:000000000019d6689c085ae165831e93`

## Test Cases

```bash
# Bitcoin mainnet, P2SH address
bip122:000000000019d6689c085ae165831e93:35PBEaofpUeH8VnnNSorM1QZsadrZoQp4N

# Bitcoin testnet, Segwit address
bip122:000000000933ea01ad0ee984209779ba:tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sl5k7

# Bitcoin mainnet, Taproot address type (Ordinals Decorator)
bip122:000000000019d6689c085ae165831e93:bc1pmzfrwwndsqmk5yh69yjr5lfgfg4ev8c0tsc06e#ordinal

# Dogecoin, Legacy address
bip122:1a91e3dace36e2be3bf030a65679fe82:AC8Q9Z4i4sXcbW7TV1jqrjG1JEWMdLyzcy

# Dogecoin, Native Segwit address
bip122:1a91e3dace36e2be3bf030a65679fe82:DLCDJhnh6aGotar6b182jpzbNEyXb3C361

# Litecoin, Native SegWit 
bip122:12a765e31ffd4059bada1e25190f6e98:ltc1q8c6fshw2dlwun7ekn9qwf37cu2rn755u9ym7p0

```

## References

- [BIP13][]: Bitcoin Improvement Proposal specifying "Script Hash" addresses
- [BIP21][]: Bitcoin Improvement Proposal specifying `bitcoin` URI scheme
- [BIP122][]: Bitcoin Improvement Proposal specifying `blockchain` URI scheme

[base58btc]: https://datatracker.ietf.org/doc/html/draft-msporny-base58-02
[BIP13]: https://github.com/bitcoin/bips/blob/master/bip-0013.mediawiki
[BIP16]: https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki
[BIP21]: https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki
[BIP44]: https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki
[BIP84]: https://github.com/bitcoin/bips/blob/master/bip-0084.mediawiki
[BIP122]: https://github.com/bitcoin/bips/blob/master/bip-0122.mediawiki
[BIP141]: https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki
[BIP173]: https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki
[BIP350]: https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki
[bitcoin whitepaper]: https://www.ussc.gov/sites/default/files/pdf/training/annual-national-training-seminar/2018/Emerging_Tech_Bitcoin_Crypto.pdf
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md

## Rights

Copyright and related rights waived via CC0.