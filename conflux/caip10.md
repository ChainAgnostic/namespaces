---
namespace-identifier: conflux-caip10
title: Conflux Namespace - Addresses
author: iosh(@iosh)
status: Draft
type: Standard
created: 2024-08-09
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

_For context, see the [CAIP-10][] specification._

## Rationale

The Conflux Network EOA address is a base32-encoded address.

These are derived directly from the hexadecimal-encoded public keys corresponding to the private keys controlling them, but calculated over a network identifier, address type, and checksum value, address including a distinctive network prefix ("cfx" "cfxtest" or "net[networkId]").

The hex address is a concatenation of a 4-bit type indicator and the rightmost 156-bit Keccak digest of the associated public key of the private key.

## Syntax

The syntax of Conflux addresses:

```
caip10-like address:    namespace + ":" networkId + ":" + address
namespace:              conflux
address:                conflux address represented as a base32 encoded string
```

## Test Cases

The list of example address generated form the same hex address, composed use the [Address Format Conversion][] or [conflux-address-js][]

```
# hex address
0x1a2f80341409639ea6a35bbcab8299066109aa55

# mainnet
conflux:cfx:aarc9abycue0hhzgyrr53m6cxedgccrmmyybjgh4xg

# testnet
conflux:cfxtest:aarc9abycue0hhzgyrr53m6cxedgccrmmy8m50bu1p

# private net
conflux:net2024:aarc9abycue0hhzgyrr53m6cxedgccrmmy06bvtn67

# private net
conflux:net202408:aarc9abycue0hhzgyrr53m6cxedgccrmmywsh35uak

```

## References

- [Conflux core space docs][]: Conflux core space eveloper documentation
- [Conflux base32 addresses][]: Conflux addresses
- [Address Format Conversion][]: A tool convert hex address to base32

[Conflux core space docs]: https://doc.confluxnetwork.org/docs/core/Overview
[Conflux base32 addresses]: https://doc.confluxnetwork.org/docs/core/core-space-basics/addresses
[conflux-address-js]: https://github.com/conflux-fans/conflux-address-js
[Address Format Conversion]: https://www.confluxscan.io/address-converter
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
