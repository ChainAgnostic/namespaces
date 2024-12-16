---
namespace-identifier: partisia-caip2
title: Partisia Blockchain - Networks
author: Partisia Blockchain Foundation
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/130
status: Draft
type: Standard
created: 2024-10-22
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

<!--"If you can't explain it simply, you don't understand it well enough." Provide a simplified and layman-accessible explanation of the CAIP.-->

CAIP-2 defines a general identification scheme for blockchains. This is the implementation of CAIP-2
for Partisia Blockchain.

## Rationale

<!--A short (~200 word) description of the technical issue being addressed.-->
Partisia Blockchain consists of multiple networks: mainnet, testnet and potentially other private
networks.
Each network has a unique chain id that can be used to identify the network.

The Partisia Blockchain networks are identified by the `partisia` namespace prefix, followed by the
chain id of the particular network.

## Syntax

The chain id of Partisia Blockchain is a human-readable identifier of the particular chain. Due to
the character limitations of CAIP-2, all characters that are not allowed in the CAIP-2 characterset (i.e.,
`[^-_a-zA-Z0-9]`) are replaced with `_`.

### Resolution Mechanics

To resolve the blockchain reference for a Partisia Blockchain chain, a GET request can be made to a
running reader node on the path `/blockchain/chainId`. This will return a JSON object with the key
`chainId` that are the human-readable chain id of this chain.

For example:

```
# Request
curl -s https://reader.partisiablockchain.com/blockchain/chainId

#Response
{
  "chainId": "Partisia Blockchain"
}
```

To convert this to a valid CAIP-2 identifier one need only replace any characters not allowed by the
specification and prefix with the namespace.

An example of the conversion using curl and jq:
```bash
curl -s https://reader.partisiablockchain.com/blockchain/chainId  | jq -r '.chainId | "partisia:" +gsub("[^a-zA-Z0-9]"; "_")' # Outputs: partisia:Partisia_Blockchain
```

### Backwards Compatibility

Not applicable

## Test Cases

```
# Partisia Blockchain mainnet
partisia:Partisia_Blockchain

# Partisia Blockchain testnet
partisia:Partisia_Blockchain_Testnet
```

## References

- [Partisia Blockchain Developer Documentation][]
- [CAIP-2][]

[Partisia Blockchain Developer Documentation]: https://partisiablockchain.gitlab.io/documentation/index.html
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-2.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
