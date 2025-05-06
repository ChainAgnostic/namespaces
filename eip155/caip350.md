---
namespace-identifier: eip155-caip350
title: eip155 Namespace - Interoperable Address
binary-key: 0000
author: Teddy (@0xteddybear), Joxes (@0xJoxess), Skeletor Spaceman (@skeletor-spaceman), Racu (@0xRacoon), TiTi (@0xtiti), Gori (@0xGorilla), Ardy (@0xArdy), Onizuka (@onizuka-wl)
discussions-to: https://ethereum-magicians.org/t/erc-7930-interoperable-addresses/23365
status: Draft
type: Standard
created: 2025-04-23
requires: CAIP-2
---

ChainType binary key: `0x0000`
CAIP-2 namespace: `eip155`

## Chain reference

### Text representation

```
eip155:<number>
```
Where `<number>` is the decimal representation of the chain's `chainid`, without leading zeroes.

##### Text representation -> CAIP-2 conversion

In the case where the `chainid` is larger than what can be represented in 32 decimal characters, the leading 32 characters should be used

##### CAIP-2 - text representation conversion

This transformation would not be fully deterministic in the case where chainids larger than 10^32 are used. It is assumed wallets and other software will be able to differentiate between chains with just the leading 32 decimal characters, and use a lookup table of popular chains to complete the missing information to convert CAIP-2 identifiers to this standard.

#### Binary representation

The bare `chainid` encoded as a big-endian unsigned integer of the minimum necessary amount of bytes will be used [^1], and leading zeroes will be prohibited.

[^1]: This makes it possible to represent some chains using the full word as their chainid, which CAIP-2 does not support since the set of values representable with 32 `a-zA-Z0-9` characters has less than `type(uint256).max` elements. This is done in an effort to support chains whose ID is the output of `keccak256`, as proposed in [ERC-7785].

#### Text -> binary conversion

Encode the decimal integer as a big-endian unsigned integer using the minimum necessary amount of bytes.

#### Binary -> text conversion

Compute the decimal representation of the stored big-endian unsigned integer

#### Examples

Ethereum Mainnet: `0x01` (1, encoded as uint8)

Optimism Mainnet: `0x0A` (10, encoded as uint8)

Ethereum Sepolia: `0xaa36a7` (11155111, encoded as uint24)

## Addresses

Bytes of EVM addresses are trivially stored as the payload.
It's worth noting that addresses are currently 20 bytes, but that might change in the future, most likely to 32 bytes [^2]

[^2]: With EVM Object Format as a prerequisite, Address Space Expansion could be implemented. If that happens, expanded addresses may be represented in 32 bytes, but pre-expansion addresses must remain 20 bytes in order to preserve a consistent address.

### Text representation

For text representation, the 20 bytes of EVM addresses should be hexadecimal-encoded according to [EIP-55].
This standard deliberately does not define the text representation of EVM addresses if they are extended in the future, since it's not possible to know which human-readable representation will be more familiar to users in such hypothetical scenario. This CASA profile should be ammended in the future to reflect it in such case.

##### Text representation -> customary text address formats conversion

Not needed since it matches [EIP-55]

##### Customary text addresses -> text representation conversion

Not needed since it matches [EIP-55]

#### Binary representation

Bytes of evm addresses are trivially stored as the payload.
It's worth noting that addresses are currently 20 bytes, but that might change in the future, most likely to 32 bytes [^2]

#### Text -> binary conversion

Described in [EIP-55]

#### Binary -> text conversion

Described in [EIP-55]

#### Examples

Refer to [EIP-55]

### Extra considerations

Wallets and other software are expected to be able to fetch the extra information needed to convert from CAIP-2 to this standard.

[EIP-55]: https://eips.ethereum.org/EIPS/eip-55
