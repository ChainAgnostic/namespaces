---
namespace-identifier: bip122-caip2
title: BIP122 Namespace - Chains
author: Simon Warta (@webmaster128), ligi <ligi@ligi.de>, Pedro Gomes (@pedrouid)
discussions-to: https://github.com/ChainAgnostic/namespaces/pulls/3
status: Draft
type: Standard
created: 2022-02-09
updated: 2022-02-09
requires: CAIP-2
supersedes: CAIP-4
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

The chain ID identifiers for BIP122 are specified in [BIP122's chain ID
definition](https://github.com/bitcoin/bips/blob/master/bip-0122.mediawiki#definition-of-chain-id).

## Syntax

The syntax for BIP122 chain ID can be summarized as a 32-character prefix from
the hash of the genesis block of a given chain, in lowercase hex
representation.

### Resolution Method

To query for a Chain ID to represent or checksum a BIP122 reference, make a
JSON-RPC request to the blockchain node with method `getblockhash`, for example:

```jsonc
// Request
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "getblockhash",
  "params": [0]
}

// Response
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
}
```

The response will return as a result value the hash for the block with height 0
that should be sliced to its first 16 bytes (32 characters for base 16) to be
compatible with the reference syntax defined above.

## Test Cases

This is a list of manually composed examples:

```
# Bitcoin mainnet (see [chain ID section of BIP122](https://github.com/bitcoin/bips/blob/master/bip-0122.mediawiki#definition-of-chain-id))
bip122:000000000019d6689c085ae165831e93

# Litecoin
bip122:12a765e31ffd4059bada1e25190f6e98

# Feathercoin (Litecoin fork)
bip122:fdbe99b90c90bae7505796461471d89a
```

## References

- [BIP13][]: Bitcoin Improvement Proposal specifying "Script Hash" addresses
- [BIP21][]: Bitcoin Improvement Proposal specifying `bitcoin` URI scheme
- [BIP122][]: Bitcoin Improvement Proposal specifying `blockchain` URI scheme

[BIP13]: https://github.com/bitcoin/bips/blob/master/bip-0013.mediawiki
[BIP21]: https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki
[BIP122]: https://github.com/bitcoin/bips/blob/master/bip-0122.mediawiki
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-21]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-21.md
[CAIP-22]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-22.md

## Rights

Copyright and related rights waived via CC0.