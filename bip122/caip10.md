---
namespace-identifier: bip122-caip10
title: BIP122 Namespace - Addresses
author: Simon Warta (@webmaster128), ligi <ligi@ligi.de>, Pedro Gomes (@pedrouid)
discussions-to: https://github.com/ChainAgnostic/namespaces/pulls/3
status: Draft
type: Standard
created: 2019-12-05
updated: 2022-03-27
requires: [CAIP-2, CAIP-10]
replaces: CAIP-4
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

While Ethereum "accounts" were the unstated norm in the definition of
[CAIP-10][], the "script hashes" addressing schemed defined by [BIP13][] map
well enough to "account"-model blockchains that these can be described by a
CAIP-10 reference.   

## Syntax

See [Specification section of BIP13](https://github.com/bitcoin/bips/blob/master/bip-0013.mediawiki#Specification).

### Backwards Compatibility

Previously, the legacy CAIP-10 schema was defined by appending as suffix the
CAIP-2 chainId delimited by the at sign (@)

#### Legacy example

`128Lkh3S7CkDTBZ8W7BbpsN3YYizJMp8p6@bip122:000000000019d6689c085ae165831e93`

## Test Cases

```
# Bitcoin mainnet
bip122:000000000019d6689c085ae165831e93:128Lkh3S7CkDTBZ8W7BbpsN3YYizJMp8p6

# Litecoin
bip122:12a765e31ffd4059bada1e25190f6e98:128Lkh3S7CkDTBZ8W7BbpsN3YYizJMp8p6
```

## References

- [BIP13][]: Bitcoin Improvement Proposal specifying "Script Hash" addresses
- [BIP21][]: Bitcoin Improvement Proposal specifying `bitcoin` URI scheme
- [BIP122][]: Bitcoin Improvement Proposal specifying `blockchain` URI scheme

[BIP13]: https://github.com/bitcoin/bips/blob/master/bip-0013.mediawiki
[BIP21]: https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki
[BIP122]: https://github.com/bitcoin/bips/blob/master/bip-0122.mediawiki
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-21]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-21.md
[CAIP-22]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-22.md

## Rights

Copyright and related rights waived via CC0.
