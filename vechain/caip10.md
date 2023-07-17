---
namespace-identifier: vechain-caip10
title: Vechain Namespace - Addresses
author: Darren Kelly (@darrenvechain)
status: Draft
type: Standard
created: 2023-07-17
updated: 2023-07-17
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

VechainThor addresses are hex-encoded strings with a length of 42 characters, prefixed with `0x`.

## Syntax

Vechain addresses match the following regular expression:

```
0x[a-fA-F0-9]{40}
```


## Test Cases

Account address:

```
# Vechain Thor MainNet
vechain:b1ac3413d346d43539627e6be7ec1b4a:0xf077b491b355E64048cE21E3A6Fc4751eEeA77fa

# Vechain Thor TestNet
vechain:87721b09ed2e15997f466536b20bb127:0xf077b491b355E64048cE21E3A6Fc4751eEeA77fa
```

Contract address:
```
# Vechain Thor MainNet
vechain:b1ac3413d346d43539627e6be7ec1b4a:0x0000000000000000000000000000456E65726779

# Vechain Thor TestNet
vechain:87721b09ed2e15997f466536b20bb127:0x0000000000000000000000000000456E65726779
```

## References

- [Vechain Developer Documentation](https://docs.vechain.org/)

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
