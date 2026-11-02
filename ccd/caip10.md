---
namespace-identifier: ccd-caip10
title: Concordium - Account ID Specification
author: "Concordium development team <ops+caip@concordium.com>"
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/229
status: Draft
type: Standard
created: 2026-09-17
requires: CAIP-2
---

<!--You can leave these HTML comments in your merged CAIP and delete the
 visible duplicate text guides, they will not appear and may be helpful to
 refer to if you edit it again. This is the suggested template for new CAIPs.
 Note that an CAIP number will be assigned by an editor. When opening a pull
 request to submit your EIP, please use an abbreviated title in the
 filename, `caipX.md`, all lowercase, no `-` between the CAIP and its
 number.-->

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Introduction

<!--"If you can't explain it simply, you don't understand it well enough."
Provide a simplified and layman-accessible explanation of the identifier system
used in this namespace, i.e., the system for addressing actors and/or accounts.
Caveats or mental model differences from other common ID systems
can be mentioned here upfront, but not implementation details like validation,
confirmation from a live connection.-->

Concordium Account addresses are 32 byte arrays, represented as 50 char [Base58btc][]-encoded strings with version byte `0x01`

Each account has 16,777,216 alias addresses that can be used to send and receive funds.
The first 29 bytes of an address byte array uniquely identify the account, with the final 3 bytes used to create account aliases.


Concordium Smart contracts are represented by a tuple containing both a u64 index, and a u64 subindex, `<Index, Subindex>`. At the time of writing, all smart contracts have subindex 0.

## Specification


### Semantics

<!-- Explain (and refer to/add links in the `## References` section) any inputs
or namespace-specific constructs needed to generate or interpret the valid
possible values of a CAIP-10 in this namespace. Assume your reader has already
read the CAIP-2 profile and understands how to form a valid CAIP-2 segment. -->
A Concordium [CAIP-10] account or alias address is a case-sensitive string that comprises the Concordium [CAIP-2][CAIP-2 Profile] Chain Identifier followed by a `:` then the [Base58btc][] representation of the address.


A Concordium [CAIP-10] Smart contract address is a case sensitive string that comprises the Concordium [CAIP-2][CAIP-2 Profile] Chain Identifier followed by a `:` then the Index and subindex as integers in the most compact form, separated by a `.`.

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

Concordium Account addresses:

```
CAIP-10 Account address: namespace + ":" + chainId + ":" + address
namespace: ccd
chainId: 32-char prefix from the hash of the genesis block
address: Base58btc-encoded string of address bytes with version byte 0x01

Account addresses can be validated with the following regular expression:

`ccd:[a-zA-Z0-9]{32}:[a-zA-Z0-9]{50}`
```

Concordium Smart Contract addresses:

```
CAIP-10 Smart Contract address: namespace + ":" + chainId + ":" + index + "." + subindex
namespace: ccd
chainId: 32-char prefix from the hash of the genesis block
index: smallest decimal string representation of u64 integer
subindex: smallest decimal string representation of u64 integer

Smart Contract addresses can be validated with the following regular expression:

`ccd:[a-zA-Z0-9]{32}:[0-9]{1,20}[.][0-9]{1,20}`
```


### Resolution Mechanics

Account and smart contract addresses are self-contained once the [CAIP-2][CAIP-2 Profile] chain identifier segment has been resolved (see the "Resolution Mechanics" section of the [CAIP-2 Profile]).
No further RPC or node round-trip is required to validate the identifier's syntax; parsing the Base58btc address or the index/subindex pair is sufficient.
Whether the referenced account or contract actually exists on that network can be checked with the `GetAccountInfo` or `GetInstanceInfo` gRPC calls against a Concordium node (see [Concordium gRPC][]).

## Rationale

This CAIP-10 profile reuses the [CAIP-2][CAIP-2 Profile] genesis-hash-derived chain identifier as-is, so that CAIP-10 addresses stay consistent with the network identification scheme already defined for Concordium.

Smart contract addresses are included alongside account addresses because, like externally-owned accounts, Concordium smart contracts are independently addressable actors that can hold CCD balances and be the target of transactions.

### Backwards Compatibility

<!-- If earlier CAIPs or earlier stages in the governance of the namespace created
legacy addresses that break or extend the specification above, please add a
section for "Legacy" compatibility and an explanation of what contexts and/or
what time-frames would require catching those cases.-->
N/A

## Test Cases

### Account Addresses

```
# Concordium mainnet Account
ccd:9dd9ca4d19e9393877d2c44b70f89acb:3fVAEHWRiKt9GU53PiXGLszLKFdpw2RYwLqYGwbzxd2qef3wvs

# Current Concordium testnet Account
ccd:4221332d34e1694168c2a0c0b3fd0f27:3SJtC6z8DstACLCA7mmJYvKV4pZcxuiRciWdZCkG1PFAbM7uq7
```

### Smart Contract Addresses

<!-- A list of manually-composed and validated examples is the **most important**
section, and by far the most read! be sure to check often that this stays in sync
with any changes or additions in the preceding sections. -->
```
# Concordium mainnet Smart Contract
ccd:9dd9ca4d19e9393877d2c44b70f89acb:10082.0

# Current Concordium testnet Smart Contract
ccd:4221332d34e1694168c2a0c0b3fd0f27:12802.0
```

## Additional Considerations (*OPTIONAL)

<!-- Future topics? Upcoming protocol upgrades that will require new specifications,
in the namespace and/or in the CAIPs? -->
N/A

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

- [Concordium Developer Documentation][] - Concordium Developer Documentation
- [Concordium gRPC][] - Interacting with a Concordium node: Description of the Concordium gRPC API.
- [Concordium Account Aliases][protocol-3] - Introduction of Concordium Account Aliases in P3.

- [CCD CAIP-2][CAIP-2 Profile] - Details of the Concordium CAIP-2 Chain Identifier
- [CAIP-2][CAIP-2] - The Blockchain ID Specification
- [CAIP-10][CAIP-10] - The Account ID Specification
- [Base58Check][base58btc] - Conversion between binary and Base58btc representation

[CAIP-2 Profile]: ./caip2.md
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10

[base58btc]: https://en.bitcoin.it/wiki/Base58Check_encoding#Base58_symbol_chart

[Concordium Developer Documentation]: https://developer.concordium.software/en/mainnet/index.html
[Concordium gRPC]: http://developer.concordium.software/concordium-grpc-api/
[protocol-3]: https://proposals.concordium.com/updates/P3.html

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
