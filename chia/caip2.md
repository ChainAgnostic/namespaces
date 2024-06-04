---
namespace-identifier: chia-caip2
title: Chia Namespace - Chains
author: Jeff Cruikshank (@paninaro)
status: Draft
type: Standard
created: 2023-05-24
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Abstract

In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for the Chia blockchain.

### Chia Namespace

The namespace "chia" refers to the Chia open-source blockchain platform.

## Rationale

Chia maintains multiple blockchains: a production blockchain (mainnet) and one
or more test blockchains (testnet). Each blockchain is identified by its unique
genesis challenge. The genesis challenge is a hex-encoded string representing a
256-bit value that serves as the previous block hash of the first block in the
blockchain.

An identifier for a Chia blockchain consists of the namespace prefix "chia:"
followed by a truncated form of the blockchain's genesis challenge.

To conform to the CAIP-2 reference spec, references to Chia's genesis
challenges are truncated to the first 32 hex characters of the 256-bit value.

Example:

Mainnet's full genesis challenge:
`ccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb`

Truncation of the full genesis challenge:
`trunc("ccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb", 32)`  
`  --> "ccd5bb71183532bff220ba46c268991a"`

CAIP-2 Chia blockchain reference:
`"chia:ccd5bb71183532bff220ba46c268991a"`

### Resolution Method

To resolve a blockchain reference for the Chia namespace, the block record
for block 0 can be inspected. The block record will contain a previous block
hash. The previous block hash for block height 0 will contain the genesis
challenge for the blockchain.

Using a Chia blockchain explorer API like [Spacescan], or [FireAcademy's] Node as a Service API can simplify the task of
inspecting block records. Note: [FireAcademy] requires an API key which can be created with a free account.

Examples requesting the block record for height 0:

```
# Request for mainnet ('xch' currency symbol) using Spacescan
$ curl 'https://api2.spacescan.io/1/xch/block/height/0' | jq '.data.foliage.prev_block_hash'

OR

# Request for mainnet using FireAcademy
$ curl -X POST \
       -H "Content-Type: application/json" \
       https://kraken.fireacademy.io/[api-key]/leaflet/get_block_record_by_height \
       -d '{"height": 0}' \
  | jq '.block_record.prev_hash'
```

```
# Response for mainnet
"0xccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb"
```

```
# Request for testnet10 ('txch' currency symbol) using Spacescan
$ curl 'https://api2.spacescan.io/1/txch10/block/height/0' | jq '.data.foliage.prev_block_hash'

OR

# Request for testnet10 using FireAcademy
$ curl -X POST \
       -H "Content-Type: application/json" \
       https://kraken.fireacademy.io/[api-key]/leaflet-testnet10/get_block_record_by_height \
       -d '{"height": 0}' \
  | jq '.block_record.prev_hash'
```

```
# Response for testnet10
"0xae83525ba8d1dd3f09b277de18ca3e43fc0af20d20c4b3e92ef2a48bd291ccb2"
```

It is also possible to retrieve block records from a local full node by making
JSON RPC requests to the `get_block_record_by_height` endpoint documented at
[Full Node RPC Endpoints][]. The value of the `prev_hash` property will contain
the genesis challenge for the blockchain. Instructions for installing and
running a full node can be found at [Chia Installation Instructions][].

Example:

```
# Request
$ curl -X POST \
       --insecure \
       --cert ~/.chia/mainnet/config/ssl/full_node/private_full_node.crt \
       --key ~/.chia/mainnet/config/ssl/full_node/private_full_node.key \
       -H "Accept: application/json" \
       -H "Content-Type: application/json" \
       https://localhost:8555/get_block_record_by_height \
       -d '{"height":0}' \
  | jq '.block_record.prev_hash'
```

```
# Response
0xccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb
```

In the above examples, the previous block's hash is the string  `"0xccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb"`.

The CAIP-2 chain reference can be obtained by skipping the `0x` prefix and truncating the remaining hex string to the first 32 characters, yielding:  
`ccd5bb71183532bff220ba46c268991a`

The fully resolved namespace can be obtained by joining the strings `"chia"`, `":"`, `<chain reference>`
Using the above example, the fully resolved namespace would be:
`chia:ccd5bb71183532bff220ba46c268991a`

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```
# Chia Mainnet
chia:ccd5bb71183532bff220ba46c268991a

# Chia Testnet10
chia:ae83525ba8d1dd3f09b277de18ca3e43

```

## References

- [Full Node RPC Endpoints][] - Full Node RPC reference in Chia official documentation
- [Chia RPC Reference][] - RPC reference for Chia

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[Chia RPC Reference]: https://docs.chia.net/rpc
[Chia Installation Instructions]: https://docs.chia.net/installation
[Full Node RPC Endpoints]: https://docs.chia.net/full-node-rpc
[Spacescan]: https://spacescan.io
[FireAcademy]: https://fireacademy.io/
[FireAcademy's]: https://fireacademy.io/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).