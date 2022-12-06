---
namespace-identifier: eip155-caip168
title: EVM Namespace - IPLD Timestamp Proof
author: Zach Ferland (@zachferland)
discussions-to: <-->
status: Draft
type: Standard
created: 2022-12-1
updated: 2022-12-1
requires: ["CAIP-168"]
---

## CAIP-168 

For context, see the [CAIP-168 IPLD Timestamp Proof]() specification. 

## Rationale

[CAIP-168 IPLD Timestamp Proof]() specification describes the general construction and verification of IPLD based blockchain timestamp proofs. Transaction verification for these IPLD timestamp proofs are independent to the chain they are published on and the `txType` parameter allows multiple verification methods per blockchain to be supported. This specification describes transaction verification for the `eip-155` namespace. 

## Specification

### `raw` Transaction Type Verification

This section describes transaction verification when a timestamp anchor proof references a `chainId` in the `eip155` namespace and `txType` is `raw`.  Type `raw` refers to the simplest transaction type where a merkle root CID is simply encoded into the data payload of a transaction. 

Example 1
```tsx
{
  root: CID(bafyreiaxdhr5jbabn7enmbb5wpmnm3dwpncbqjcnoneoj22f3sii5vfg74)
  chainID: "eip155:1"
  txHash: CID(bagjqcgzanbud4sqdsywfp2mckuj57qsffsovgyjhh7sxebkqwr335hzy2zbq)
  txType: 'raw'
}
```

**Verification Steps**

1) Resolve blockchain transaction payload by `txHash` CID and `chainId`. CID is expected to be DAG-ETH encoded block. 
2) Get the `data` paramater of the transaction payload, it is expected to be a hex encoded CID. The data value is a byte friendly string and may be prepended with a '0' for a resulting even length hex string. 
3) Verify that the `root` CID of the timestamp anchor proof is equivalent to the `transaction.data` CID. Equivalence should be checked using a CIDs library, rather than string equivalence, as the CIDs may be encoded in different bases. If they are not equivalent, an error MUST be raised. 
4) Determine that the transaction has been included in a valid block on the blockchain referenced by the `chainId`. Number of block confirmations for acceptance is up to an implementation. 


### `f(32bytes)` Transaction Type Verification

This section describes transaction verification when a timestamp anchor proof references a `chainId` in the `eip155` namespace and `txType` is `f(32bytes)`. Type `f(32bytes)` refers to a transaction which makes a function call on a contract with the function signature including a single 32 bytes argument. The 32 byte argument is the merkle root CID. A CID is more than 32bytes, and a partial CID is used to allow the argument to be efficiently packed in the transaction. Function name or contract does not matter, and is up to an implementation. 

Example 2
```tsx
{
  root: CID(bafyreiaxdhr5jbabn7enmbb5wpmnm3dwpncbqjcnoneoj22f3sii5vfg74)
  chainID: "eip155:1"
  txHash: CID(bagiacgzah24drzou2jlkixpblbgbg6nxfrasoklzttzoht5hixhxz3rlncyq)
  txType: 'f(32bytes)'
}
```
**Verification Steps**

1) Resolve blockchain transaction payload by `txHash` CID and `chainId`. CID is expected to be DAG-ETH encoded block. 
2) Get the `data` paramater of the transaction payload, it is expected to be a hex encoded 64 byte string.
3) The first 32 bytes are the function signature and can be discarded, the next 32 bytes is the first argument of the function, which is expected to be a 32 byte hex encoded partial CID.
4) The partial CID is a CID with the first two bytes removed, the first byte being the multibase is not needed in byte format, and the second byte being the CID version is not inlcuded, it is assumed to be CID V1. Verify that the `root` CID of the timestamp anchor proof is equivalent to the transaction partial CID. Equivalence should be checked using a CIDs library, and bytes can be compared. If they are not equivalent, an error MUST be raised. 
5) Determine that the transaction has been included in a valid block on the blockchain referenced by the `chainId`. Number of block confirmations for acceptance is up to an implementation. 


## References

- [CAIP-168](CAIP-168): IPLD Timestamp Proof

