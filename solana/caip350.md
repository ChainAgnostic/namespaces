---
namespace-identifier: solana-caip350
title: Solana Namespace - Interoperable Address
author: Teddy (@0xteddybear), Joxes (@0xJoxess), Skeletor Spaceman (@skeletor-spaceman), Racu (@0xRacoon), TiTi (@0xtiti), Gori (@0xGorilla), Ardy (@0xArdy), Onizuka (@onizuka-wl)
discussions-to: https://ethereum-magicians.org/t/erc-7930-interoperable-addresses/23365
status: Draft
type: Standard
created: 2025-04-23
requires: CAIP-2
---

ChainType binary key: `0x0002`
CAIP-2 namespace: `solana`

## Chain reference
Solana networks are distinguished by its genesis blockhash, which is normally represented as 44 base58btc characters, corresponding to 32 bytes. We chose to use the blockhash in full, as opposed to CAIP-2, for consistency with `eip155` and to avoid the complexity of slicing base58btc-encoded text [^1].

[^1]: CAIP-2 limits chain references to 32 characters, so the `solana` namespace instructs to only use the first 32 characters of the base58btc-encoded genesis blockhash.
Truncating the base58btc-encoded representation instead of the binary data, however, means the binary representation will differ significantly from what the Solana node might store in its own memory. e.g while truncating the text yields a string representing a 23-byte long result, it does not correspond to simply slicing the first 23 bytes from the genesis blockhash.

### Text representation
The full base58btc-encoded genesis blockhash used used. This is larger than the CAIP-2 representation.

##### Text representation -> CAIP-2 conversion
The leading 32 characters are used, and the rest discarded.

##### CAIP-2 - text representation conversion
This transformation is not fully deterministic. It is assumed wallets and other software will be able to differentiate between chains with just the leading 32 base58btc-encoded characters, and use a lookup table of popular chains to complete the missing information to convert CAIP-2 identifiers to this standard.

#### Binary representation
To obtain the binary representation from the base58btc-encoded genesis blockhash, first truncate the base58btc-encoded text to its first 32 characters as described above and then decode it to raw bytes.

#### Text -> binary conversion
Text should be base58btc decoded into raw bytes

#### Binary -> text conversion
Raw bytes should be base58btc encoded into text

#### Examples
Solana Mainnet
: `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d`
: `0x45296998a6f8e2a784db5d9f95e18fc23f70441a1039446801089879b08c7ef0`

Note that Solana Mainnet's blockhash is:
- base58btc `5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d`
- base16 `45296998a6f8e2a784db5d9f95e18fc23f70441a1039446801089879b08c7ef0`

## Addresses
Solana addresses are 32-byte public keys, usually shown to users as base58btc-encoded text

### Text representation
base58btc-encoded text

##### Text representation -> customary text address formats conversion
Used as-is

##### customary text addresses -> text representation conversion
Used as-is

#### Binary representation
32-byte public key

#### Text -> binary conversion
base58btc decoding

#### Binary -> text conversion
base58btc encoding

#### Examples
`7S3P4HxJpyyigGzodYwHtCxZyUQe9JiBMHyRWXArAaKv` -> `0x5F90554BB3D8C2FC82B6EE59C49AAA143E77F7D49A83E956CE1DBEF17A43F805`

`DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK` -> `0xBA7A74F374AB05B70D114A78112EF0D3F0695A819572C79710B5372000D81AE2`

### Extra considerations
Wallets and other software are expected to be able to fetch the extra information needed to convert from CAIP-2 to this standard.
