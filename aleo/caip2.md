---
namespace-identifier: aleo-caip2
title: Aleo Network - Namespace Chains
author: Jonathan Gonzalez (@jonandgon, jonathan@puzzle.online)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/129
status: Draft
type: Standard
created: 2023-09-12
requires (*optional): CAIP-2
replaces (*optional): CAIP-2
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

An identifier for a Aleo chain consists of the namespace prefix "aleo:" followed by the chain id.

## Syntax

The Aleo chain ID system maps between a human-readabe string (used to discriminate networks in the paths of [node endpoints][], for example) and an unsigned 16-bit binary integer, known colloquially as an "`u16` number", ranging from 0 to 65535 which is used internally.
For example, at time or writing, the u16 number `1` maps to `testnet` and `0` maps to `mainnet`. 
The canonical location of the mapping of u16 integers to network name strings is still to be determined by the community, but in the case of conflicts between the community documentation and this document, the former should be taken as canonical. 

### Backwards Compatibility

n/a

### Resolution Method

To resolve a reference for the Aleo namespace, get the latest block information from the chain you are interested in from an Aleo API node. An example using Javascript:

```env
fetch('https://api.explorer.provable.com/v1/mainnet/latest/block')
  .then(response => response.json())
  .then(response => console.log(response.header.metadata.network))
```

will log `0`.

## Test Cases

This is a manually composed example.

```env
# Aleo Testnet
aleo:1

# Aleo Mainnet
aleo:0
```

## Additional Considerations

Testnet3 has been deprecated and shut down in favor of Testnet.

## References
<!--Links to external resources that help understanding the CAIP better. This can e.g. be links to existing implementations.-->
- [Aleo Network Documentation][]: Developer docs for the Aleo Network.

[Aleo Network Documentation]: https://developer.aleo.org
[node endpoints]: https://developer.aleo.org/testnet/getting_started/overview/#query-the-network
[CAIP-2]: https://chainAgnostic.org/CAIPS/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
