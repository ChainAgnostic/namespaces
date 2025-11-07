---
namespace-identifier: iota-caip10
title: IOTA - Account ID Specification
author: Enrico Marconi (@UMR1352)
status: Draft
type: Informational
created: 2025-07-28
requires: CAIP-2, CAIP-10
---

<!--You can leave these HTML comments in your merged CAIP and delete the 
 visible duplicate text guides, they will not appear and may be helpful to 
 refer to if you edit it again. This is the suggested template for new CAIPs.
 Note that an CAIP number will be assigned by an editor. When opening a pull
 request to submit your EIP, please use an abbreviated title in the 
 filename, `caipX.md`, all lowercase, no `-` between the CAIP and its 
 number.-->

# CAIP-10

*For context, see the [CAIP-10] specification.*

## Introduction 

This document defines how IOTA addresses can be encoded as [CAIP-10]'s account IDs.

## Specification

### Semantics

<!-- Explain (and refer to/add links in the `## References` section) any inputs 
or namespace-specific constructs needed to generate or interpret the valid 
possible values of a CAIP-10 in this namespace. Assume your reader has already
read the CAIP-2 profile and understands how to form a valid CAIP-2 segment. -->

In IOTA's object-based model, account addresses are just a subset of the whole
address namespace, which is shared among objects, packages, and accounts.

Therefore, an IOTA address may refer to either an object, a package or a more
traditional key-based account. Most importantly, it is impossible to distinguish
what an IOTA address refers to without querying a node.

Nonetheless, all IOTA addresses can own assets (i.e. other objects), with the
only difference being that key-derived address are the only types of address that
can execute transactions.

### Syntax

<!-- Explain the actual algorithm or transformation needed to transform inputs 
(sometimes just a native address, other times additional context is needed) into
a conformant and unique CAIP-10 deterministically.  Consider including a regular 
expression for validation as well, as some consumers or toolmakers may want to
support this CAIP-10 scheme without a deep understanding of any specifications, 
devdocs, or improvement proposals on which this specification depends. If there 
are canonicalization guarantees, checksums, or other assumptions in the native
format,  explain how they exist (or can be made to exist) in the CAIP-10 
equivalent as well. -->

An IOTA [CAIP-10]'s account ID is a case-sensitive string that is computed by appending
an IOTA address to an IOTA [CAIP-2 Profile]'s chain ID, interlieved by the `:` character.

The syntax of an IOTA address matches the following regular expression:

```
0x[0-9a-f]{64}
```

Hence, the regular expression that matches the whole [CAIP-10]'s account ID is:

```
iota:(mainnet|testnet|devnet|[0-9a-f]{8}):0x[0-9a-f]{64}
```

### Resolution Mechanics

<!-- Many blockchain systems allow for transactions, asset-states, etc. to be
validated against the chain they are targeting or depending to to avoid replay
attacks or other unintended outcomes. This is often done by an API or RPC call
to a node to validate the targetted chain or network. Include a sample
request/response and add the relevant documentation to the `## References`
section below if possible, as well as an explanation of any steps needed to
validate the results, calculate checksums, persist session metadata or nonces,
 etc. -->

Any Account ID conforming to the aforementioned syntax is a valid IOTA Account ID,
independently of whether it is already in use by a wallet or on-chain object.

It is possible to check whether a given Account ID refers to a key-pair derived address,
an object, or a smart contract package by invoking the `iota_getObject` JSON-RPC API.

For instance, checking IOTA address `0x53e4567ccafa5f36ce84c80aa8bc9be64e0d5ae796884274aef3005ae6733809` with

```json 
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "iota_getObject",
  "params": [
    "0x53e4567ccafa5f36ce84c80aa8bc9be64e0d5ae796884274aef3005ae6733809",
    {
      "showType": true,
      "showOwner": true,
      "showPreviousTransaction": false,
      "showDisplay": false,
      "showContent": false,
      "showBcs": false,
      "showStorageRebate": false,
    }
  ]
}
```

yields the following response:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "data": {
      "objectId": "0x53e4567ccafa5f36ce84c80aa8bc9be64e0d5ae796884274aef3005ae6733809",
      "version": "1",
      "digest": "33K5ZXJ3RyubvYaHuEnQ1QXmmbhgtrFwp199dnEbL4n7",
      "type": "0x2::coin::Coin<0x2::iota::IOTA>",
      "owner": {
        "AddressOwner": "0xc8ec1d5b84dd6289e193b9f88de4a994358c9f856135236c3e75a925e1c77ac3"
      }
    }
  },
  "id": 1
}
```

which shows that address `0x53e4567ccafa5f36ce84c80aa8bc9be64e0d5ae796884274aef3005ae6733809` is actually
an IOTA object of type `0x2::coin::Coin<0x2::iota::IOTA>` - i.e. an IOTA Coin - owned by address
`0xc8ec1d5b84dd6289e193b9f88de4a994358c9f856135236c3e75a925e1c77ac3`.

If we were to do the same for the coin owner's address
`0xc8ec1d5b84dd6289e193b9f88de4a994358c9f856135236c3e75a925e1c77ac3` we'd get the following response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "error": {
      "code": "notExists",
      "object_id": "0xc8ec1d5b84dd6289e193b9f88de4a994358c9f856135236c3e75a925e1c77ac3"
    }
  }
}
```

Which hints at the fact that address `0xc8ec1d5b84dd6289e193b9f88de4a994358c9f856135236c3e75a925e1c77ac3` is not
an object, but a key-derived address.

## Rationale

<!-- Explain here how the mapping or translation between native identifiers and
CAIP-10 identifiers was arrived at, history and pre-history, etc.-->

IOTA addresses are lowercase-hex encoded 32 bytes string, which in the case of key-pair derived addresses - i.e.
traditional accounts - are computed by hashing with the `blake2b` algorithm a public key's bytes.  If the signature scheme to be computed with those bytes is anything other than `Ed25519`, the public key bytes have a sigil prepended **before** hashing.
IOTA address currently supports pure Ed25519, Secp256k1, Secp256r1, and MultiSig with corresponding flag bytes of 0x00 (not prepended), 0x01, 0x02, and 0x03, respectively.

As already mentioned above, all IOTA addresses can own assets and funds.

## Test Cases

<!-- A list of manually-composed and validated examples is the **most important**
section, and by far the most read! be sure to check often that this stays in sync
with any changes or additions in the preceding sections. -->

```
# IOTA Mainnet
iota:mainnet:0x7b4a34f6a011794f0ecbe5e5beb96102d3eef6122eb929b9f50a8d757bfbdd67

# IOTA Testnet
iota:testnet:0x2d3eef6122eb929b9f50a8d757bfbdd677b4a34f6a011794f0ecbe5e5beb9610

# IOTA Devnet
iota:devnet:0x929b9f50a8d757bfbdd677b4a34f6a011794f0ecbe5e5beb96102d3eef6122eb

# IOTA custom network
iota:f3aa51bd:0xe5e5beb96102d37b4a34f6a011794f0ecbeef6122eb929b9f50a8d757bfbdd67
```

## References

<!-- Links to external resources that help understanding the namespace or the
specification/applied-CAIP better in this context. This can also include links
to existing implementations.

The preferred format, for browser-rendering and long-term maintenance, is a
bulletted list of [Name][] links (rather than classical [Name](referent) links),
followed by ` - ` and a summary or explanation of the content.  In a separate
section below, add the name-referent pairs in the `[Name]: https://{referent} `
format-- this will be invisible in any Github-flavored Markdown rendering
(including jekyll/github pages, aka github.io, but also docusaurus and many
dev-docs rendering engines). -->

[CAIP-2 Profile]: ./caip2.md
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[IOTA Docs]: https://docs.iota.org
[IOTA RPC API]: https://docs.iota.org/iota-api-ref
[IOTA Object Model]: https://docs.iota.org/developer/iota-101/objects/object-model

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
