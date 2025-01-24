---
namespace-identifier: cosmos-caip2
title: Cosmos Namespace - Chains
author: Simon Warta (@webmaster128)
discussions-to: https://github.com/ChainAgnostic/CAIPs/issues/5, https://github.com/ChainAgnostic/CAIPs/issues/6, https://github.com/ChainAgnostic/CAIPs/pull/1
status: Draft
type: Standard
created: 2022-03-01
updated: 2022-03-01
requires: CAIP-2
supersedes: CAIP-5
---

# CAIP-2

*For context, see the [CAIP-2] specification.*

## Rationale

Cosmos chains consist of the namespace prefix `cosmos:` and a reference.

Each reference is a `chain_id` derived from a hash of the entire contents of the
genesis file used to initiate (or re-initiate) a Tendermint blockchain. This
file consists of a JSON object, and thus the `chain_id` is a unique, JSON-compatible
unicode string. For an example, see the [configuration objects] section of the
Tendermint core specification.  It can be referenced directly or by its hash
according to an algorithm defined below.  All nodes of any given network also
return the string when queried for basic configuration information, as described
below. 

Note: An empty or null `chain_id` must be treated as an error.

## Syntax 

### Direct References

If a CASA reference matches the case-sensitive pattern `[-a-zA-Z0-9]{1,32}` and
does not start with "hashed-", it can be assumed to refer directly to a
`chain_id` in its entirety.  If the first 7 characters are `hashed-`,
however, it should be assumed to be a hash of a `chain_id`; the original can be
retrieved from any node of that chain as described below.  

Note: some `chain_id`s include a version in the format `-X` where X is an
integer counter increased with each successive interruption or upgrade to the
network protocol; at such events, chainstate carries over to the "heir" chain,
but for addressing purposes, this new chain is a distinct chain with a new
`chain_id`.  Some Tendermint clients abstract out this chain identity issue, but
this is standardized at the Tendermint protocol level, not the broader Cosmos
SDK level or its IBC coordination protocol.

For more context on mutable `chain_id`s and so-called "state-dumps" across
blockheight-resetting protocol upgrades, see [IBC#517] and [clients].
Addresses and state survive across such `chain_id`-modifying events, but since
transactions targeting an older `chain_id` will not be executed by an upgraded
network, cross-chain implementers are recommended to proceed with caution and to
do further research on how to best ensure they are only sending transactions to
live/current chains.

### Hashed References

References prefixed by `hashed-` are defined as
`first_16_chars(hex(sha256(utf8(chain_id))))`, with:

- `chain_id`= the Tendermint `chain_id` from the genesis file (see above)
- `utf8`= a UTF-8 encoding function
- `sha256`= a SHA256 hash function
- `hex`= a lowercase hex encoder
- `first_16_chars`= a function to extract the first 16 characters of the
  resulting string and dropping the rest

As `chain_id`s can be up to 50 characters long, `chain_id`s with a length of
over 32 characters will need to be referred to by hash to fit the length limits
of CAIP-2.

### Rationale

While there is no enforced restriction on `chain_id`, the authors of this
document did not find a chain ID in the wild that does not conform to the
restrictions of the direct reference definition above.

Cosmos blockchains with a chain ID not matching `[-a-zA-Z0-9]{1,32}` or prefixed
with "hashed-" would need to be hashed in order to conform to this namespace
specification. No real world example of this case is known to the author yet.

One unique trait of the Cosmos ecosystem is that if chainstate is broken, chains
can be "rebooted" at a later time; when this happens, a new genesis block is
generated from a new configuration object and the "snapshot" of state at the
last block. To allow ordering of blocks after block height is thus reset to 0, a
versioning syntax for `chain_id`s is use. The `chain_id`s of blockchains that
support this versioning pattern take the suffix `-X` (where X is a sequential
integer counter). The Cosmos hub (a coordination chain) is also versioned this
way, leading to `chain_id`s like `cosmoshub-1`, `cosmoshub-2`, and `cosmoshub-4`
(the current one at time of writing).

For the purposes of this specification and of interoperability on the CASA
model, we treat each rebooted chain as a distinct blockchain reference;
translation between them or dereferencing from an older version to a newer
version is out of scope of this specification. It is the responsibility of a
clients and higher-level applications to interpret some chains as "sequels" or
heirs of earlier ones and to define equality sets.

### Resolution Method

To resolve a blockchain reference for the Cosmos namespace, make a GET request
to the Tendermint RPC enpoint of the blockchain node with path `/status`, for
example:

```jsonc

// Request
curl -sS https://rpc.cosmos.network/status | jq .result.node_info

// Response
{
  "protocol_version": {
    "p2p": "8",
    "block": "11",
    "app": "0"
  },
  "id": "d8a79ceb43ac6215452f00ffabfa7d2a9f533d56",
  "listen_addr": "tcp://0.0.0.0:26020",
  "network": "cosmoshub-4",
  "version": "v0.34.14",
  "channels": "40202122233038606100",
  "moniker": "nodeasy",
  "other": {
    "tx_index": "on",
    "rpc_address": "tcp://0.0.0.0:26021"
  }
}
```
The response will return a JSON object which will include node information and
the `chain_id` defined above can be retrieved from the `network` property of the
response object; this can be used directly as the `reference` section of a
CAIP-2 or CAIP-10 if it matches the regular expression listed above, or hashed
if not.

### Backwards Compatibility

Early (pre-Q32020) `chain_id`s included a prefix `-epoch-` before the number in
automatically-iterating chains, and client methods from the period referred to
"versions" as "epochs"; for more information, see
[cosmos/cosmos-sdk#7483](https://github.com/cosmos/cosmos-sdk/pull/7483).

## Test Cases

This is a list of manually composed examples:

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

# chain_ids " ", "wonderland🧝‍♂️" (invalid characters for the direct definition)
cosmos:hashed-36a9e7f1c95b82ff
cosmos:hashed-843d2fc87f40eeb9
```

## References

- [ChainID tips]: A useful thread on chainIDs on the Cosmos SDK github repo
- [IOV Core TS]: A reference implementation of the CAIP-2 section of this specification in the IOV Core SDK
- [configuration objects]: Tendermint core requires each chain have a unit
      genesis block and genesis block timestamp, and derives a chain ID
      (`chain_id` in their semantics) deterministically from those values; these
- [IBC]: The Inter Blockchain Communication Protocol is used to enable bridges and multi-chain compatibility between Tendermint chains
- [channels]: The Inter-Blockchain Communication protocol establishes
      persistent "channels" between the clients of independent Cosmos-based
      blockchains; these can maintain state for assets across two chains like a
      bridged asset or smart contract.
- [ICS]: The InterChain Standards are canonically maintained in this repo, and
      cover all aspects of interop and addressing between/across Cosmos chains
      and networks; these are equivalent to BIPs, EIPs, and CAIPs.
- [IBC#517]: A GitHub thread containing a concise explanation of `chain_id` validation/constraints across Cosmos contexts 

[addresses]: https://docs.cosmos.network/v0.42/basics/accounts.html
[IBC#517]: https://github.com/cosmos/ibc/issues/517
[IBC]: https://github.com/cosmos/ibc-go/blob/main/docs/ibc/overview.md
[ICS]: https://github.com/cosmos/ibc
[ChainID tips]: https://github.com/cosmos/cosmos-sdk/issues/5363
[channels]: https://github.com/cosmos/ibc-go/blob/main/docs/ibc/overview.md#channels
[clients]: https://github.com/cosmos/ibc-go/blob/main/docs/ibc/overview.md#clients
[configuration objects]: https://docs.tendermint.com/v0.35/tendermint-core/using-tendermint.html#fields
[IOV Core TS]: https://github.com/iov-one/iov-core/blob/1cd39e708b/packages/iov-cosmos/src/caip5.ts
[BIP_0173]: https://en.bitcoin.it/wiki/BIP_0173
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-21]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-21.md
[CAIP-22]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-22.md

## Rights

Copyright and related rights waived via CC0.
