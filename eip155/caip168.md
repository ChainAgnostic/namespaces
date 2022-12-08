---
namespace-identifier: eip155-caip168
title: EVM Namespace - IPLD Timestamp Proof
author: Zach Ferland (@zachferland), Joel Thorstensson (@oed)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/42
status: Draft
type: Standard
created: 2022-12-1
updated: 2022-12-1
requires: ["CAIP-168"]
---

## CAIP-168 

For context, see the [CAIP-168][] IPLD Timestamp Proof specification. 

## Rationale

[CAIP-168][] IPLD Timestamp Proof specification describes the general
construction and verification of IPLD based blockchain timestamp proofs.
Transaction verification for these IPLD timestamp proofs are independent of the
chain on which they are published and the `txType` parameter allows multiple
verification methods per namespace to be supported. This specification
describes transaction verification for the `eip-155` namespace. 

## Specification

### `raw` Transaction Type Verification

This section describes transaction verification when a timestamp anchor proof
references a `chainId` in the `eip155` namespace and `txType` is `raw`.  Type
`raw` refers to the simplest transaction type where a merkle root CID is simply
encoded into the data payload of a transaction. 

#### Example anchor proof

```tsx
{
  root: CID(bafyreiaxdhr5jbabn7enmbb5wpmnm3dwpncbqjcnoneoj22f3sii5vfg74)
  chainID: "eip155:1"
  txHash: CID(bagjqcgzanbud4sqdsywfp2mckuj57qsffsovgyjhh7sxebkqwr335hzy2zbq)
  txType: 'raw'
}
```

#### Verification Steps

1) Resolve blockchain transaction payload by `txHash` CID and `chainId`. CID is
   expected to be a [DAG-ETH][]-encoded block, and `chainId` MUST be a valid
   [CAIP-2][] identifier.
2) Get the `data` paramater of the transaction payload, it is expected to be a
   hex-encoded CID. The data value is a byte-friendly string, and if its length
   is odd, a single '0' may be prepended to make its length even. 
3) Verify that the `root` CID of the timestamp anchor proof is equivalent to the
   `transaction.data` CID. Note: as the CIDs MAY be encoded in different bases,
   their equivalence should be checked using a CID parsing library, rather than
   simple string equivalence. If they are not equivalent, verification MUST fail. 
4) Determine that the transaction has been included in a valid block on the
   blockchain referenced by the `chainId`. Number of block confirmations for
   acceptance is up to an implementation. 


### `f(bytes32)` Transaction Type Verification

This section describes transaction verification when a timestamp anchor proof
references a `chainId` in the `eip155` namespace and `txType` is `f(bytes32)`.
Type `f(bytes32)` refers to a transaction which makes a function call on a
contract with the function signature including a single 32 bytes argument. The
32 byte argument is the merkle-root CID. A CID is more than 32 bytes, and a
partial CID is used to allow the argument to be efficiently packed in the
transaction. Function name or contract does not matter, and is up to the
implementation.  Use of a root CID encoded in [DAG-CBOR][] is recommended.

#### Example anchor proof

```tsx
{
  root: CID(bafyreiaxdhr5jbabn7enmbb5wpmnm3dwpncbqjcnoneoj22f3sii5vfg74)
  chainID: "eip155:1"
  txHash: CID(bagiacgzah24drzou2jlkixpblbgbg6nxfrasoklzttzoht5hixhxz3rlncyq)
  txType: 'f(bytes32)'
}
```

#### Verification Steps

1) Resolve blockchain transaction payload by `txHash` CID and `chainId`. CID is
   expected to be [DAG-ETH][]-encoded block, and `chainId` MUST be a valid
   [CAIP-2][] identifier.
2) Get the `data` paramater of the transaction payload, it is expected to be a
   hex encoded 64 byte string.
3) The first 4 bytes are the function signature and can be discarded, the next
   32 bytes is the first argument of the function, which is expected to be a 32
   byte hex encoded partial CID.
4) The partial CID is the **multihash portion** of the original CIDv1 (refer the
   section [How does it
   work?](https://github.com/multiformats/cid#how-does-it-work) in the
   [Multiformats CID][] specification for context). It does not include the
   multibase, the CID version or the IPLD codec segments. It is assumed that the
   IPLD codec is dag-cbor. Verify that the first 32bytes of the `root` CID of
   the timestamp anchor proof is equivalent to the 32-byte partial CID extracted
   from the transaction data. Equivalence should be checked using a CIDs
   library, which can compare oprtions of multihashes encoded in bytes. If the two partial multihashes are not equivalent, verification MUST fail.
5) Determine that the transaction has been included in a valid block on the
   blockchain referenced by the `chainId`. Number of block confirmations for
   acceptance is up to an implementation. 

## References

- [CAIP-168][]: IPLD Timestamp Proof
- [Multiformats CID][] Specification
- [DAG-ETH][] Codec Specification at IPLD.io
- [DAG-CBOR][] Codec Specification on Github
  
[CAIP-168]: https://chainagnostic.org/CAIPs/CAIP-168  
[DAG-ETH]: https://ipld.io/specs/codecs/dag-eth/
[DAG-CBOR]: https://github.com/ipld/specs/blob/master/block-layer/codecs/dag-cbor.md
[Multiformats CID]: https://github.com/multiformats/cid