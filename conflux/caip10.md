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

The Conflux core space hex address is a concatenation of a 4-bit type indicator and the rightmost 156-bit Keccak digest of the associated public key of the private key.

There are currently three types of indicators:

(0x)1: Represents the address of an EOA account.
(0x)8: Represents the address of a contract
(0x)0: Represents the address of an internal contract,

Constructing an address:

```
encode(0x1a2f80341409639ea6a35bbcab8299066109aa55, "cfx") // cfx:aarc9abycue0hhzgyrr53m6cxedgccrmmyybjgh4xg
```

1. Network Prefix: cfx(mainnet network ID 1029), cfxtest(testnet network ID 1), net + network ID (ID is not 1 or 1029)

   Network Prefix: `cfx`

2. Payload: Concatenate version-byte: concatenate the version-byte(0x00) with hex address to get a 21-byte array.

   Payload: `[0x00, 0x1a, 0x2f, 0x80, 0x34, 0x14, 0x09, 0x63, 0x9e, 0xa6, 0xa3, 0x5b, 0xbc, 0xab, 0x82, 0x99, 0x06, 0x61, 0x09, 0xaa, 0x55]`

3. Base32 encode: encode the above result left-to-right, mapping each 5-bit sequence to the corresponding ASCII character Pad to the right with zero bits(should be 2 bit 0-padding) to complete any unfinished chunk at the end.

   5-bit base32: `[0x00, 0x00, 0x0d, 0x02, 0x1f, 0x00, 0x01, 0x14, 0x02, 0x10, 0x04, 0x16, 0x07, 0x07, 0x15, 0x06, 0x14, 0x0d, 0x0d, 0x1b, 0x19, 0x0a, 0x1c, 0x02, 0x13, 0x04, 0x03, 0x06, 0x02, 0x02, 0x0d, 0x0a, 0x0a, 0x14]`

   base32-encoded: `aarc9abycue0hhzgyrr53m6cxedgccrmmy`

4. Checksum Prepare checksum input: data is used as the input of checksum function. It contains:
   4.1 The lower 5 bits of each character of the network-prefix, e.g. "cfx..." becomes 0x03, 0x06, 0x18, ...

   network-prefix cfx: `0x03, 0x06, 0x18`

   4.2 A zero for the separator (5 zero bits).

   `0x00`

   4.3 The payload by chunks of 5 bits. If necessary, the payload is padded to the right with zero bits to complete any unfinished chunk at the end.

   checksum input data:
```
   //↓ network-prefix   //↓separator //↓ 5-bit base32 with zero padding
    [0x03, 0x06, 0x18,    0x00,        0x00, 0x00, 0x0d, 0x02, 0x1f, 0x00, 0x01, 0x14, 0x02, 0x10, 0x04, 0x16, 0x07, 0x07, 0x15, 0x06, 0x14, 0x0d, 0x0d, 0x1b, 0x19, 0x0a, 0x1c, 0x02, 0x13, 0x04, 0x03, 0x06, 0x02, 0x02, 0x0d, 0x0a, 0x0a, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
```

5. Calculate checksum: calculate using [Bitcoin Cash checksum algorithm][]over the data

   checksum output: `688543492710`

6. Base32 encode: encode the output

   checksum base32 encode: `ybjgh4xg`

concatenated result: `cfx:aarc9abycue0hhzgyrr53m6cxedgccrmmyybjgh4xg`

## Syntax

The syntax of Conflux addresses:

```
caip10-like address:    namespace + ":" chain_id + ":" + address
namespace:              conflux
chain_id                cfx or cfxtest or net[network ID]
address:                base32 address
```

## Test Cases

The list of example address generated form the same hex address, composed use the [Address Format Conversion][] or [conflux-address-js][]

```
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
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[Bitcoin Cash checksum algorithm]: https://github.com/bitcoincashorg/bitcoincash.org/blob/master/spec/cashaddr.md#checksum

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
