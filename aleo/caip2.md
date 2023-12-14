---
namespace-identifier: aleo-caip2
title: Aleo Network - Namespace Chains
author: Jonathan Gonzalez (@jonandgon)
discussions-to: <URL of PR, mailing list, etc>
status: Draft
type: Standard
created: 2023-09-12
requires (*optional): <["CAIP-2"]>
replaces (*optional): <CAIP-2>
---

<!--You can leave these HTML comments in your merged CAIP and delete the 
 visible duplicate text guides, they will not appear and may be helpful to 
 refer to if you edit it again. This is the suggested template for new CAIPs.
 Note that an CAIP number will be assigned by an editor. When opening a pull
 request to submit your EIP, please use an abbreviated title in the 
 filename, `caipX.md`, all lowercase, no `-` between the CAIP and its 
 number.-->

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

The namespace `aleo` refers to the Aleo Network Layer 1 blockchain.

To date, Aleo consists of a single network: a testnet network (Testnet3).

An identifier for a Aleo chain consists of the namespace prefix "aleo:"
followed by the chain id.

## Syntax

The Aleo chain ID is the name of the chain. e.g. `3` for testnet3 or `0` for when mainnet is released. The chain id is a `u16` number ranging from 0 to 65535.

### Backwards Compatibility

n/a

## Test Cases

This is a manually composed example.

```env
# Aleo Testnet3
aleo:3

# Aleo mainnet
aleo:0
```

## Additional Considerations (*OPTIONAL)

Mainnet will release sometime Q1 2024. 
The API is subject to change and the example above (particularly other properties) may become inaccurate over time.

## References
<!--Links to external resources that help understanding the CAIP better. This can e.g. be links to existing implementations.-->
- [Aleo Network Documentation][]: Developer docs for the Aleo Network.

[Aleo Network Documentation]: https://developer.aleo.org
[CAIP-2]: https://chainAgnostic.org/CAIPS/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
