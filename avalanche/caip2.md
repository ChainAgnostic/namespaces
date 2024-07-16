---
namespace-identifier: avax-caip2
title: Avalanche Namespace - Chains
author: Gergely Lovas (@gergelylovas)
discussions-to: []
status: Draft
type: Standard
created: 2024-07-16
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for the Avalanche Ecosystem. 
Blockchains in the "avax" namespace are validated by their `blockchainID`. 
The `blockchainID` in Avalanche refers to the [txID][] that created the 
blockchain on the Avalanche P-Chain.
These blockchain IDs require transformations to be used as conformant CAIP-2
references.

## Syntax

The namespace "avax" refers to the Avalanche open-source blockchain platform.

### Reference Definition

The definition for this namespace will use the `blockchainID` as an identifier
for different Avalanche chains. Since the P-Chain's `blockchainID` is the same 
on Testnet and Mainnet, to ensure uniqueness, a testnet prefix is introduced 
for chains on the [Fuji Testnet][].  

The method for calculating the chain ID is as follows with pseudo-code:

```
first_32_chars(base64url(sha256(concat(testnet_prefix, blockchain_id))))
```

- `blockchain_id` = `txID` that created the blockchain on the Avalanche P-Chain
- `testnet_prefix`= `fuji` when the chain was created on the Fuji Testnet; 
  empty string otherwise
- `concat`= a string concatenation function
- `sha256`= a SHA256 hash function
- `base64url`= a Base64URL encoder
- `first_32_chars`= a function to extract the first 32 characters of the
  resulting string and dropping the rest

### Resolution Method

To resolve a blockchain reference for the Avalanche namespace, make a JSON-RPC 
request to the [Info API][] with method `info.getBlockchainID`, for example:

```jsonc
// Request
{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"info.getBlockchainID",
    "params": {
        "alias":"C"
    }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "blockchainID": "2q9e4r6Mu3U68nU1fYjgbR6JvwrRx36CohpAX5UQxse55x1Q5"
  }
}
```

For example, this Node.js code transforms the above response into a CAIP-2 identifier:

```javascript
const isTestnet = false;
const blockchainID = "2q9e4r6Mu3U68nU1fYjgbR6JvwrRx36CohpAX5UQxse55x1Q5";
const testnetPrefix = isTestnet ? 'fuji' : '';
const hash = createHash('sha256')
              .update(testnetPrefix + blockchainID)
              .digest('base64url')
              .substring(0, 32);
const identifier = "avax:" + hash;

console.log(identifier); // prints "avax:8aDU0Kqh-5d23op-B-r-4YbQFRbsgF9a"
```

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```
# Avalanche P Chain Mainnet
# blockchainID: 11111111111111111111111111111111LpoYY
avax:Rr9hnPVPxuUvrdCul-vjEsU1zmqKqRDo

# Avalanche C Chain Mainnet
# blockchainID: 2q9e4r6Mu3U68nU1fYjgbR6JvwrRx36CohpAX5UQxse55x1Q5
avax:8aDU0Kqh-5d23op-B-r-4YbQFRbsgF9a

# Avalanche X Chain Mainnet
# blockchainID: 2oYMBNV4eNHyqk2fjjV5nVQLDbtmNJzq5s3qs3Lo6ftnC6FByM
avax:imji8papUf2EhV3le337w1vgFauqkJg-

# Avalanche P Chain Testnet
# blockchainID: 11111111111111111111111111111111LpoYY
avax:Sj7NVE3jXTbJvwFAiu7OEUo_8g8ctXMG

# Avalanche C Chain Testnet
# blockchainID: yH8D7ThNJkxmtkuv2jgBa4P1Rn3Qpr4pPr7QYNfcdoS6k6HWp
avax:YRLfeDBJpfEqUWe2FYR1OpXsnDDZeKWd

# Avalanche X Chain Testnet
# blockchainID: 2JVSBoinj9C2J33VntvzYtVJNZdN2NKiwwKjcumHUWEb5DbBrm
avax:8AJTpRj3SAqv1e80Mtl9em08LhvKEbkl

```

## References

- [Fuji Testnet][] - Fuji Testnet in Avalanche official documentation
- [Info API][] - Info API reference in Avalanche official documentation
- [txID][] - Create Chain TX reference in Avalanche official documentation

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[Fuji Testnet]: https://docs.avax.network/learn/avalanche/fuji
[Info API]: https://docs.avax.network/reference/avalanchego/info-api
[txID]: https://docs.avax.network/reference/avalanchego/p-chain/txn-format#unsigned-create-chain-tx

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
