---
namespace-identifier: arweave-caip2
title: Arweave Namespace - Chains
author: Rohit Pathare (@ropats16), Phil Billingsby (@pbillingsby), Dan MacDonald (@DanMacDonald)
discussions-to:
status: Draft
type: Standard
created: 2022-09-01
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Abstract
In CAIP-2 a general blockchain identification scheme is defined. This is the implementation of CAIP-2 for Arweave network.

### Arweave Namespace

The namespace "arweave" refers to the wider Arweave ecosystem.

#### Reference Definition

The reference relies on Arweave's current designation of addresses belonging to main network by prefixing them with `7wIU` which is the representation of the [hash of the genesis block](https://viewblock.io/arweave/block/0) truncated to the first 4 characters.


## Rationale

Arweave has one blockchain, the [Blockweave](https://www.arweave.org/technology#blockweaves).

## Backwards Compatibility

Not applicable.

## Test Cases

This is a manually composed example.

```
# Arweave Mainnet
arweave:7wIU7KolICAjClMl
```

## References

- [Arweave](https://github.com/ArweaveTeam/arweave-standards)
- [Hash of Genesis Block](https://viewblock.io/arweave/block/0)
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md)
- [CAIP-10](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md)
- [CAIP-122](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-122.md)



## Rights

Copyright and related rights waived via CC0.