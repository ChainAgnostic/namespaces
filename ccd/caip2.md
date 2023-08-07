---
namespace-identifier: ccd-caip2
title: Concordium - Networks
author: "Concordium development team <developers@concordium.com>"
discussions-to: ""
status: Draft
type: Standard
created: 2023-04-01
---

<!--You can leave these HTML comments in your merged EIP and delete the 
 visible duplicate text guides, they will not appear and may be helpful to 
 refer to if you edit it again. This is the suggested template for new EIPs.
 Note that an EIP number will be assigned by an editor. When opening a pull
 request to submit your EIP, please use an abbreviated title in the 
 filename, `caipX.md`, all lowercase, no `-` between the CAIP and its 
 number.-->
This is the suggested template for new CAIPs.

# CAIP-2

*For context, see the [CAIP-2][] specification.*

<!-- Provide a simplified and layman-accessible explanation of the CAIP.-->

This CAIP defines an identification schema for Concordium networks.
The Concordium networks are identified by `ccd` namespace followed by the hash of the network's genesis block.

## Rationale
<!--A short (~200 word) description of the technical issue being addressed.-->
Concordium has one mainnet and potentially several testnets.
These networks are uniquely identified by a hash of their genesis blocks.

## Syntax

<!-- Explain the actual algorithm or transformation needed to transform inputs into a
conformant and unique CAIP deterministically.  Consider including a regular
expression for validation as well, as some consumers or toolmakers may want to
support this CAIP without a deep understanding of any specifications, devdocs,
or improvement proposals on which this specification depends. -->

Concordium's network ID is a hash of its genesis block in the `hex` encoding truncated to the first 32 bytes.

<!-- TODO: add some details, e.g. something like pseudocode `truncate(SHA512(block_data), 32)` -->

### Resolution Mechanics

A hash of the genesis block can be obtained using the gRPC interface of a Concordium node (see [Concordium gRPC][]).

The request using a CLI tool `concordium-client` looks as follows:

```
concordium-client raw GetConsensusInfo
```

Example response for the `testnet` node:

```json
{
    "bestBlock": "fa03132dbd8e5d0a2871c47a50bfbd532f3ef4c598098e64eed5a07a169f2574",
    "bestBlockHeight": 3541516,
    "blockArriveLatencyEMA": 0.1463579781506756,
    "blockArriveLatencyEMSD": 5.644804435079067e-2,
    "blockArrivePeriodEMA": 10.773324091402692,
    "blockArrivePeriodEMSD": 10.96881296245654,
    "blockLastArrivedTime": "2023-08-07T16:05:09.799512996Z",
    "blockLastReceivedTime": "2023-08-07T16:05:09.791343727Z",
    "blockReceiveLatencyEMA": 0.13744546306746866,
    "blockReceiveLatencyEMSD": 5.6358647255823326e-2,
    "blockReceivePeriodEMA": 10.773406674300828,
    "blockReceivePeriodEMSD": 10.96849563757842,
    "blocksReceivedCount": 229906,
    "blocksVerifiedCount": 229906,
    "currentEraGenesisBlock": "7687b54a59fa29d40c69278a01ddd33a40a8fdd6775a3a01343b3576205db1e1",
    "currentEraGenesisTime": "2022-11-22T11:05:19.5Z",
    "epochDuration": 3600000,
    "finalizationCount": 206332,
    "finalizationPeriodEMA": 11.586703983078877,
    "finalizationPeriodEMSD": 11.25944943176555,
    "genesisBlock": "4221332d34e1694168c2a0c0b3fd0f273809612cb13d000d5c2e00e85f50f796",
    "genesisIndex": 2,
    "genesisTime": "2022-06-13T10:00:00Z",
    "lastFinalizedBlock": "fa03132dbd8e5d0a2871c47a50bfbd532f3ef4c598098e64eed5a07a169f2574",
    "lastFinalizedBlockHeight": 3541516,
    "lastFinalizedTime": "2023-08-07T16:05:10.728847984Z",
    "protocolVersion": 5,
    "slotDuration": 250,
    "transactionsPerBlockEMA": 2.739314019392612e-2,
    "transactionsPerBlockEMSD": 0.16322608879784517
}
```

Truncating the value of the `genesisBlock` attribute to the first 32 bytes gives `4221332d34e1694168c2a0c0b3fd0f27`

<!-- Many blockchain systems allow for transactions, asset-states, etc. to be
validated against the chain they are targeting or depending to to avoid replay
attacks or other unintended outcomes. This is often done by an API or RPC call
to a node to validate the targetted chain or network. Include a sample
request/response and add the relevant documentation to the `## References`
section below if possible, as well as an explanation of any steps needed to
validate the results, calculate checksums, etc. -->

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples:

```
# Concordium mainnet
ccd:...

# Concordium testnet
ccd:4221332d34e1694168c2a0c0b3fd0f27
```

## References

- [Documentation][] - Concordium Developer Documentation
- [Concordium gRPC][] - Interacting with a Concordium node: Description of the Concordium gRPC API.

[Documentation]: https://developer.concordium.software/en/mainnet/index.html
[Concordium gRPC]: https://github.com/Concordium/concordium-grpc-api


[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
