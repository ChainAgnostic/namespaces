---
namespace-identifier: cosmos
title: Cosmos Namespace
author: Simon Warta (@webmaster128)
discussions-to: https://github.com/ChainAgnostic/CAIPs/issues/5, https://github.com/ChainAgnostic/CAIPs/issues/6, https://github.com/ChainAgnostic/CAIPs/pull/1
status: Draft
type: Standard
created: 2022-03-01
updated: 2022-03-01
requires: CAIP-2, CAIP-10
supercedes: CAIP-5
---

# Namespace for Cosmos chains

This document describes the syntax and structure of the [Cosmos][] namespace,
which formalized a URI scheme for references on the broader Cosmos ecosystem.
This ecosystem includes many different kinds of blockchains, variously
interoperable and interconnected, but share the consensus rules and
[configuration objects][] of the Tendermint consensus engine.  The namespace thus
defined includes blockchains generated using the [Cosmos
SDK](https://github.com/cosmos/cosmos-sdk) such as Cosmoshub, Binance, and the
Cosmos Testnets, but also [Weave](https://github.com/iov-one/weave)-based
blockchains, like IOV.

## CAIP-2

*For context, see the [CAIP-2][] specification.*

### Reference basics

Cosmos chains consist of the namespace prefix `cosmos` and a reference.

Each reference is a `chain_id` from the genesis file used to initiate a
Tendermint blockchain; this file is a JSON object, and thus the `chain_id` is a
unique, JSON-compatible unicode string. For an example, see the [configuration
objects][] section of the tendermint core specification.  It can be referenced
directly or by its hash according to an algorithm defined below.  All nodes of
any given network also return the string when queried for basic configuration
information, as described below. 

Note: An empty or null `chain_id` must be treated as an error.

### Direct References

If the `chain_id` matches the case-sensitive pattern `[-a-zA-Z0-9]{1,32}` and
does not start with "hashed-", it can be assumed to refer to a `chain_id`.  If
the first 7 characters are `hashed-`, however, it should be assumed to be a hash
of a `chain_id`; the original can be retrieved from any node as described below.  

Note: some `chain_id`s include a version in the format `-version-X` where X is
an integer. For more information, see [ICB#517][].

### Hashed References

References prefixed by `hashed-` are defined as
`first_16_chars(hex(sha256(utf8(chain_id))))`, with:

- `chain_id`= the Tendermint `chain_id` from the genesis file (see above)
- `utf8`= a UTF-8 encoding function
- `sha256`= a SHA256 hash function
- `hex`= a lowercase hex encoder
- `first_16_chars`= a function to extract the first 16 characters of the
  resulting string and dropping the rest

### Resolution Method

To resolve a blockchain reference for the Cosmos namespace, make a REST GET
request to the blockchain node with endpoint `/node_info`, for example:

```jsonc

//TODO -- RPC ENDPOINT IS OUT OF DATE

// Request
curl -X GET "https://stargate.cosmos.network/node_info" -H "accept: application/json"

// Response
{
  "application_version": {
    "build_tags": "string",
    "client_name": "string",
    "commit": "string",
    "go": "string",
    "name": "string",
    "server_name": "string",
    "version": "string"
  },
  "node_info": {
    "id": "string",
    "moniker": "validator-name",
    "protocol_version": {
      "p2p": 7,
      "block": 10,
      "app": 0
    },
    "network": "gaia-2",
    "channels": "string",
    "listen_addr": "192.168.56.1:26656",
    "version": "0.15.0",
    "other": {
      "tx_index": "on",
      "rpc_address": "tcp://0.0.0.0:26657"
    }
  }
}
```
The response will return a JSON object which will include node information and
the `chain_id` defined above can be retrieved from `node_info.network`; this can
be used directly as the `reference` section of a CAIP-2 or CAIP-10 .

## Rationale

While there is no enforced restriction on `chain_id`, the authors of this
document did not find a chain ID in the wild that does not conform to the
restrictions of the direct reference definition above.

Cosmos blockchains with a chain ID not matching `[-a-zA-Z0-9]{1,32}` or prefixed
with "hashed-" would need to be hashed in order to conform to this namespace
specification. No real world example of this case is known to the author yet.

One unique trait of the Cosmos ecosystem is that if chainstate is broken, chains
can be "rebooted" at a later time; when this happens, a new genesis block is
generated from a new configuration object and new `chain_id`. This requires a
versioning syntax for `chain_id`s using the `-version-X` suffix (where X is a
sequential integer counter). The Cosmos hub itself is also versioned (in
so-called "epochs"), but without the `-version` suffix, leading to `chain_id`s
like `cosmoshub-1`, `cosmoshub-2`, `cosmoshub-3`, etc.

For the purposes of this specification and of interoperability on the CASA
model, we treat each rebooted chain as a distinct blockchain reference;
translation between them or dereferencing from an older version to a newer
version is out of scope of this specification. It is the responsibility of a
higher-level application to interpret some chains as "sequels" or heirs of
earlier ones and to define equality sets, pending standardization in [ICS][].

## Backwards Compatibility

Before the `-version-` suffix convention was widely adopted, the "epoch"
terminology and the suffix `-epoch-` was used (until late 2020). Otherwise,
there are no backwards compatibility issues.

## Test Cases

This is a list of manually composed examples

```
# Cosmos Hubs (Tendermint + Cosmos SDK)
cosmos:cosmoshub-2
cosmos:cosmoshub-3

# Binance chain (Tendermint + Cosmos SDK; see https://dataseed5.defibit.io/genesis)
cosmos:Binance-Chain-Tigris

# IOV Mainnet (Tendermint + Weave)
cosmos:iov-mainnet

# chain_ids "x", "hash-", "hashed" (direct references to `chain_id`s)
cosmos:x
cosmos:hash-
cosmos:hashed

# chain_ids "hashed-", "hashed-123" (invalid prefix for the direct definition)
cosmos:hashed-c904589232422def
cosmos:hashed-99df5cd68192b33e

# chain_id "123456789012345678901234567890123456789012345678" (too long for direct reference)
cosmos:hashed-0204c92a0388779d

# chain_ids " ", "wonderland🧝‍♂️" (invalid character for the direct definition)
cosmos:hashed-36a9e7f1c95b82ff
cosmos:hashed-843d2fc87f40eeb9
```


## References

- [ChainID tips][]: A useful thread on chainIDs on the Cosmos SDK github repo
- [IOV Core TS]: A reference implementation of the CAIP-2 section of this specification in the IOV Core SDK
- [configuration objects][]: Tendermint core requires each chain have a unit genesis block and genesis block timestamp, and derives a chain ID (`chain_id` in their semantics) deterministically from those values; these
- [ICS]: The InterChain Standards are canonically maintained in this repo, and cover all aspects of interop and addressing between/across Cosmos chains and networks
- [ICP]: The InterChain Protocol is used to enable bridges and multi-chain compatibility between Tendermint chains
- [ICB#517]: A placeholder for a more up-to-date specification on `chain_id` validation/constraints 

[IBC#517]: https://github.com/cosmos/ibc/issues/517
[ICS]: https://github.com/cosmos/ibc
[configuration objects]: https://docs.tendermint.com/v0.35/tendermint-core/using-tendermint.html#fields
[ChainID tips]: https://github.com/cosmos/cosmos-sdk/issues/5363
[IOV Core TS]: https://github.com/iov-one/iov-core/blob/1cd39e708b/packages/iov-cosmos/src/caip5.ts
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-21]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-21.md
[CAIP-22]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-22.md

## Rights

Copyright and related rights waived via CC0.