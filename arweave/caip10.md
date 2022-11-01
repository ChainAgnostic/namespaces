---
namespace-identifier: arweave-caip10
title: Arweave Namespace - Addresses
author: Rohit Pathare (@ropats16), Phil Billingsby (@pbillingsby), Dan MacDonald (@DanMacDonald)
discussions-to:
status: Draft
type: Standard
created: 2022-09-01
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Abstract
In CAIP-10 an account identification scheme is defined. This is the implementation of CAIP-10 for Arweave network.

## Rationale

Particularities of syntax for Arweave "accounts" have been specified.  

## Syntax

Arweave addresses have a normalization of lowercase letters, uppercase letters, numbers and `-`s. The addresses are encoded in base64Url format.

### Backwards Compatibility

Not applicable.

## Test Cases

```
# Arweave mainnet
arweave:7wIU:kY9RAgTJEImkBpiKgVeXrsGV02T-D4dI3ZvSpnn7HSk
```

## References

- [Arweave](https://github.com/ArweaveTeam/arweave-standards)
- [Hash of Genesis Block](https://viewblock.io/arweave/block/0)
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md)
- [CAIP-10](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md)
- [CAIP-122](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-122.md)



## Rights

Copyright and related rights waived via CC0.