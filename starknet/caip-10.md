---
namespace-identifier: starknet-caip10
title: StarkNet Namespace - Addresses
author: Argent Labs
discussions-to:
status: Draft
type: Standard
created: 2022-11-18
updated: 2022-11-18
requires: ["CAIP-2", "CAIP-10"]
supersedes: CAIP-5
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

The address of a StarkNet account is represented by an element of a field, whose maximum
value is slightly less than `2**256 - 1`. Because of this, 32-byte hex representations of 
these addresses always have a leading zero.

## Syntax

Like on Ethereum, StarkNet addresses begin with `0x` followed by 64 hexadecimal characters
representing the zero-padded address number, totaling 66 characters.

It's recommended to checksum the address using capitalization according to
[EIP55][], as is common elsewhere on EVM systems.

## Test Cases

```
# StarkNet mainnet alpha (valid/checksummed)
starknet:SN_MAIN:0x02DdfB499765c064eaC5039E3841AA5f382E73B598097a40073BD8B48170Ab57

# StarkNet mainnet alpha (may not validate in checksum-conformant systems)
starknet:SN_MAIN:0x02ddfb499765c064eac5039e3841aa5f382e73b598097a40073bd8b48170ab57

# StarkNet goerli alpha
starknet:SN_GOERLI:0x02DdfB499765c064eaC5039E3841AA5f382E73B598097a40073BD8B48170Ab57
```


## References

- [addresses][]: Address format on StarkNet
- [Length of addresses][]: Decision fixing the length of addresses on StarkNet

[addresses]: https://starknet.io/docs/how_cairo_works/cairo_intro.html#field-elements
[Length of addresses]: https://github.com/starkware-libs/starknet-specs/pull/58
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-21]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-21.md
[CAIP-22]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-22.md
[EIP55]: https://eips.ethereum.org/EIPS/eip-55

## Rights

Copyright and related rights waived via CC0.