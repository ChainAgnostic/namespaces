---
namespace-identifier: massa
title: Massa
author: ["Billy Rennekamp (@okwme)"]
discussions-to: https://github.com/0xcounting/FAR/issues/1
status: Draft
type: Informational
created: 2026-09-14
---

# Namespace for Massa blockchains

Massa is a layer-1 blockchain whose block production is spread over 32 parallel threads, giving it a block graph rather than a single chain of blocks.
It also runs autonomous smart contracts, which can schedule their own future execution without an external caller, and hosts websites on chain through DeWeb.
The `massa` namespace covers networks that run the Massa node software and expose its JSON-RPC and gRPC interfaces.
Individual networks in the namespace are identified by the node's `chain_id`, as specified in the [Massa CAIP-2 profile][].

## Address prefixes

Massa addresses are structured strings rather than opaque blobs, and reading them saves an implementer a surprising amount of work.
An address is the character `A`, then a category character, then a base58check-encoded payload.
The category character is `U` for a user address, which is derived from a public key, and `S` for a smart contract address.
So `AU1…` is a wallet and `AS1…` is a deployed contract, and the distinction is visible without any node round trip.

The `1` that almost every Massa address carries in third position is **not** part of a fixed prefix.
The base58check payload encodes a varint version number followed by the 32-byte hash, and the current address version is `0`.
A varint `0` is the single byte `0x00`, and base58 renders a leading zero byte as the digit `1`, so the version shows through as a `1`.
An implementer who hard-codes the literal three-character prefixes `AU1` and `AS1` will therefore break on the first address issued under address version 1.
The correct parse is: match `A`, read the category character `U` or `S`, base58check-decode the remainder, and read the leading varint as the version.

The burn address `AU1111111111111111111111111111111112m1s9K` is a useful worked example, since its hash is all zero bytes and every one of those bytes renders as another `1`.

## Rationale

`massa` is the ecosystem's own name, is five characters long, and uses only lowercase letters, so it satisfies the CAIP-2 namespace production `[-a-z0-9]{3,8}` directly.
No abbreviation or disambiguation was needed, and no competing spelling is in circulation.

Massa's `chain_id` is a `u64` that was added, explicitly citing [EIP-155][] and [EIP-1344][] as precedent, so that an operation signed for one Massa network cannot be replayed on another.
It is therefore exactly the discriminator CAIP-2 is asking for: a value that already defines, inside the protocol, which network a signed payload belongs to.
The values are also a small joke that is worth knowing, because it makes them memorable and self-checking.
MainNet's `77658377` is the ASCII code points of `MASM` written out in sequence — `M`=77, `A`=65, `S`=83, `M`=77.
BuildNet's `77658366` is `MASB`, and SecureNet's `77658383` is `MASS`.

This namespace was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a CAIP-2 for this chain in order to name the assets that exist on it.
The authors do not represent the Massa ecosystem.
It is offered as a starting point for the Massa community to correct, adopt or replace, and the authors would rather it carry a maintainer's name than theirs.

## Governance

Massa's protocol is developed by Massa Labs in the open, in the [Massa reference implementation][].
Protocol-level parameter and behaviour changes are shipped as Massa Improvement Proposals (MIPs) through an in-protocol versioning mechanism: a MIP is announced, votes are gathered from block producers, and the network activates it at an agreed point.
The currently active version is reported by the node as `current_mip_version` in the [`get_status`][] response, which was `1` at the time of writing, corresponding to MIP-0001.
Application-level conventions, including the MRC-20 fungible token standard, live in [Massa standards][] rather than in the node repository.

## References

- [Massa documentation][] - Concepts, node operation, and network constants
- [Massa reference implementation][] - The Rust node, and the source of the `CHAINID` constant
- [Massa network constants][] - Published `CHAINID`, genesis timestamp, and thread count per network
- [`get_status`][] - JSON-RPC method that reports a node's `chain_id`
- [Massa public networks][] - Endpoints for MainNet and BuildNet
- [Massa operation format][] - Binary serialization and the base58check encoding used by addresses
- [Massa standards][] - Community token and wallet standards, including MRC-20
- [Massa CAIP-2 profile][] - The chain ID specification in this namespace

[Massa documentation]: https://docs.massa.net/
[Massa reference implementation]: https://github.com/massalabs/massa
[Massa network constants]: https://docs.massa.net/docs/node/constants
[`get_status`]: https://docs.massa.net/docs/build/api/jsonrpc
[Massa public networks]: https://docs.massa.net/docs/build/networks-faucets/public-networks
[Massa operation format]: https://docs.massa.net/docs/learn/operation-format-execution
[Massa standards]: https://github.com/massalabs/massa-standards
[Massa CAIP-2 profile]: ./caip2.md
[EIP-155]: https://eips.ethereum.org/EIPS/eip-155
[EIP-1344]: https://eips.ethereum.org/EIPS/eip-1344

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
