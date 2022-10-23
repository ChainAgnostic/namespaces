---
namespace-identifier: bip122
title: Bitcoin-based Networks (BIP122)
author: Simon Warta (@webmaster128), ligi <ligi@ligi.de>, Pedro Gomes (@pedrouid)
status: Draft
type: Informational
created: 2019-12-05
updated: 2022-03-27
replaces: CAIP-4
---

# Namespace for BIP122 chains

This document describes the syntax and structure of the [BIP122][] namespace,
which formalized a URI scheme for references on Bitcoin-based networks that
conform to the convention, abstracting out specifics of block explorer
interfaces. 

## Context

[BIP122][] is a draft specification from the Bitcoin improvement process from
2015 which has achieved wide adoption. It defines a `blockchain://` URI scheme,
although it has not, to date, been registered with IANA. Note: an IANA
registration has been
[proposed](https://www.iana.org/assignments/uri-schemes/prov/bitcoin) for
`bitcoin://` URIs, based on the older, and less chain-agnostic [BIP21][].

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
