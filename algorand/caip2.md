---
namespace-identifier: algorand-caip2
title: Algorand Namespace - Chains
author: Jason Paulos (@jasonpaulos)
status: Draft
type: Standard
created: 2023-01-11
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Abstract

In CAIP-2 a general blockchain identification scheme is defined. This is the implementation of CAIP-2 for Algorand network.

### Algorand Namespace

The namespace "algorand" refers to the wider Algorand ecosystem.

## Rationale

Algorand consists of multiple networks: a production network (MainNet), a testing network (TestNet), a network where new features are trialed (BetaNet), and many more, including private networks used for development. Each network has a unique genesis hash that can be used to identify it.

An identifier for an Algorand chain consists of the namespace prefix "algorand:" followed by a truncated form of the chain's genesis hash.

## Syntax

Due to length and character limitations of CAIP-2 reference identifiers (references must adhere to `[-_a-zA-Z0-9]{1,32}`), the commonly referenced standard base64-encoded genesis hash of an Algorand chain cannot be used directly as a reference.

Instead, two changes must be made:
1. The genesis hash must be encoded with a URL-safe base64 alphabet (i.e. the characters `+` and `/` must be replaced with `-` and `_`, respectively).
2. Only the first 32 characters of the URL-safe base64-encoding will be used.

### Resolution Method

To resolve the blockchain reference for an Algorand chain, a GET request can be made to an Algorand node on the path `/v2/transactions/params`. This will return a JSON object with the the key `genesis-hash`, whose value is the base64-encoded genesis hash of the current chain.

For example:

```jsonc
// Request
curl -H "X-Algo-API-Token:${YOUR_AUTH_TOKEN}" "https://example.algorand.node/v2/transactions/params"

// Response (formatted)
{
  "consensus-version": "https://github.com/algorandfoundation/specs/tree/44fa607d6051730f5264526bf3c108d51f0eadb6",
  "fee": 0,
  "genesis-hash": "mFgazF+2uRS1tMiL9dsj01hJGySEmPN28B/TjjvpVW0=",
  "genesis-id": "betanet-v1.0",
  "last-round": 23473050,
  "min-fee": 1000
}
```

Note that the `genesis-hash` value returned must be re-encoded with the URL-safe base64 alphabet, and a 32 byte prefix must be taken from this to serve as the CAIP-2 chain reference.

For example, this Node.js code transforms the above response into a CAIP-2 identifier:

```javascript
const genesisHash = "mFgazF+2uRS1tMiL9dsj01hJGySEmPN28B/TjjvpVW0=";
const urlSafe = Buffer.from(genesisHash, "base64").toString("base64url");
const prefix = urlSafe.substring(0, 32);
const identifier = "algorand:" + prefix;

console.log(identifier); // prints "algorand:mFgazF-2uRS1tMiL9dsj01hJGySEmPN2"
```

## Backwards Compatibility

Not applicable.

## Test Cases

```
# Algorand MainNet has the genesis hash wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=
algorand:wGHE2Pwdvd7S12BL5FaOP20EGYesN73k

# Algorand TestNet has the genesis hash SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=
algorand:SGO1GKSzyE7IEPItTxCByw9x8FmnrCDe

# Algorand BetaNet has the genesis hash mFgazF+2uRS1tMiL9dsj01hJGySEmPN28B/TjjvpVW0=
algorand:mFgazF-2uRS1tMiL9dsj01hJGySEmPN2
```

## References

- [Algorand Networks](https://developer.algorand.org/docs/get-details/algorand-networks/)
- [Algorand REST API](https://developer.algorand.org/docs/rest-apis/algod/v2/)
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md)

## Rights

Copyright and related rights waived via CC0.
