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

To resolve a blockchain reference for the Chia namespace, make a JSON RPC
request for block 0 using the `get_block_record_by_height` endpoint documented
at [Full Node RPC Endpoints][]. The value of the `prev_hash` property will
contain the genesis challenge for the blockchain.

Example:

```
# Request
$ curl -X POST
       --insecure
       --cert ~/.chia/mainnet/config/ssl/full_node/private_full_node.crt
       --key ~/.chia/mainnet/config/ssl/full_node/private_full_node.key
       -H "Accept: application/json"
       -H "Content-Type: application/json"
       https://localhost:8555/get_block_record_by_height
       -d '{"height":0}'
```

```
# Response
{
  "block_record": {
    "challenge_block_info_hash": "0x45e3beae0441bab860109a977c94d9d8accb1927d7ad6e70faf84d18b9b96aaa",
    "challenge_vdf_output": {
      "data": "0x0000dafd52467f3f66cf25c7de3e432188b9c3000b95a09170ace441a214cffc5fa65a39a66f11085fea9c7a121cf7f86a74142506b6d51d6036097bff862707185dbba577707c248f2fca5877337e56905879a2ee840d28860c50ebcacaaaf53a660100"
    },
    "deficit": 15,
    "farmer_puzzle_hash": "0x3d8765d3a597ec1d99663f6c9816d915b9f68613ac94009884c4addaefcce6af",
    "fees": 0,
    "finished_challenge_slot_hashes": [
      "0xccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb"
    ],
    "finished_infused_challenge_slot_hashes": null,
    "finished_reward_slot_hashes": [
      "0xccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb"
    ],
    "header_hash": "0xd780d22c7a87c9e01d98b49a0910f6701c3b95015741316b3fda042e5d7b81d2",
    "height": 0,
    "infused_challenge_vdf_output": null,
    "overflow": false,
    "pool_puzzle_hash": "0xd23da14695a188ae5708dd152263c4db883eb27edeb936178d4d988b8f3ce5fc",
    "prev_hash": "0xccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb",
    "prev_transaction_block_hash": "0xccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb",
    "prev_transaction_block_height": 0,
    "required_iters": 1313186,
    "reward_claims_incorporated": [],
    "reward_infusion_new_challenge": "0xbdde7b5b2bc6025c07a9f5233d8eae167bea654146b272652262b362524c3e85",
    "signage_point_index": 2,
    "sub_epoch_summary_included": null,
    "sub_slot_iters": 134217728,
    "timestamp": 1616162474,
    "total_iters": 11798946,
    "weight": 7
  },
  "success": true
}
```

In the above example response, the `prev_hash` is the string  `"0xccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb"`.

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
[Full Node RPC Endpoints]: https://docs.chia.net/full-node-rpc

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).