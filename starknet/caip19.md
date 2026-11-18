---
namespace-identifier: starknet-caip19
title: Starknet Namespace - Asset Specification
author: ["Billy Rennekamp (@okwme)"]
discussions-to: https://github.com/0xcounting/FAR/issues/1
status: Draft
type: Standard
created: 2026-09-14
requires: ["CAIP-19", "CAIP-2"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Rationale

Every asset on Starknet is a contract.
There is no chain-native balance of the kind `slip44` was written for: fees are paid in ETH or in STRK, and both of those are ordinary token contracts that a transaction calls, not a protocol-level account field.
So this profile has exactly one job to do well, and it is not choosing asset namespaces — it is saying, unambiguously, what a Starknet contract address looks like when it is written into a [CAIP-19][] identifier.

That is harder than it sounds, because a Starknet address is a **field element**, not a fixed-width byte string.
A felt is an integer modulo the Stark prime, so it has a value but no intrinsic width, and the ecosystem serialises it inconsistently: leading zeros are routinely dropped.
The Starknet JSON-RPC node used to verify this document returns the ETH token's class hash as `0xb45dbc3714180381c5680e41931172d67194d77d504413465390e0bef194ec`, which is 62 hex digits, and the STRK token's as `0x2e77ee61d4df3d988ee1f42ea5442e913862cc82c2584d212ecda76666498fc`, which is 63.
Queried on that same node, `0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7`, `0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7`, `0x049D36570D4E46F48E99674BD3FCC84644DDD6B96F7C741B1562B82F9E004DC7` and the same string with no `0x` at all are four spellings of one contract, and all four are made only of characters the `asset_reference` charset permits.

Without a normalisation rule, therefore, two CAIP-19 identifiers can be unequal as strings and equal as assets, on a chain where that happens by default rather than by accident.
Any consumer that deduplicates, indexes or joins on the identifier would silently double-count.
Fixing that is the contribution of this profile, and the rule is given normatively below rather than left to implementers.

This profile was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a way to name 40 assets on Starknet.
The authors do not represent the Starknet ecosystem and offer this for its community to correct, adopt or replace.

## Syntax

After the [CAIP-2][] namespace and chain id, a slash introduces an `asset_namespace` and an `asset_reference`.
For non-fungibles a further slash introduces a `token_id`, as defined in [CAIP-19][].

### Asset Namespaces

| Namespace | Description                                                | Reference format             |
| :-------- | :--------------------------------------------------------- | :--------------------------- |
| `erc20`   | A fungible token contract implementing the [SNIP-2][] token interface | Canonical contract address |
| `erc721`  | A non-fungible token contract implementing the [SNIP-3][] interface   | Canonical contract address; `token_id` is the item's `u256` id |

The two namespaces are named after the interfaces rather than after the SNIP numbers.
Starknet's own standards are [SNIP-2][] and [SNIP-3][], both `Final`, and both state that they are inspired by EIP-20 and EIP-721 respectively; the reference implementations, wallets, explorers and the Cairo traits themselves spell them `IERC20` and `IERC721`.
`snip2` and `snip3` were considered and would be equally well-formed; `erc20` and `erc721` were chosen because they are the names the Starknet ecosystem actually uses for these interfaces, and because Starknet is an Ethereum layer 2 whose assets are frequently the counterpart of an `eip155:1/erc20:…` asset, so one interface vocabulary across both namespaces is less confusing than two.

Which namespace applies to a given contract is determined by the interface that contract implements, discoverable on chain through [SNIP-5][] `supports_interface`.
It is not inferable from supply or decimals, and implementations MUST NOT guess.

### Canonical address form

The `asset_reference` of both asset namespaces is a Starknet contract address in canonical form, which is defined as:

- the two-character prefix `0x`, followed by
- **exactly 64 hexadecimal digits**, zero-padded on the left, in **lowercase**.

A reference in any other spelling is invalid and MUST be rejected rather than silently repaired, so that a producer's mistake surfaces at the producer rather than as a duplicate row downstream.
Producers normalise by parsing the address as an integer and re-rendering it with `%064x`.
The canonical form is 66 characters, comfortably inside the 128-character `asset_reference` limit.

Three choices in that rule deserve their justification stated:

**Why pad rather than strip.**
Stripping leading zeros is the other self-consistent option and it is what the RPC itself emits, but it leaves the padded spelling — the one almost every indexer, database column and wallet stores — permanently non-canonical, so nearly every producer would still have to run a bignum parse before emitting an identifier.
Padding costs the same one-time normalisation and yields a fixed-width reference, which means byte-for-byte string equality is exactly asset equality: no parser, no bignum, no locale, and a plain `=` in a database index is correct.

**Why 64 digits and never more.**
A felt is an element of the field of order `P = 2^251 + 17 * 2^192 + 1`, so every valid felt fits in 252 bits and therefore in 64 hex digits, and 64 is an upper bound that cannot be exceeded rather than a convention.
A reference with more than 64 digits MUST be rejected even if its numeric value is a valid felt; a public Starknet node already refuses such a string with a hex parsing error rather than trimming it.
Implementations SHOULD additionally reject any value greater than or equal to `P`, and MAY reject any value greater than or equal to `2^251`, since the Cairo core library documents the value range of a `ContractAddress` as `[0, 2**251)` — a tighter bound than the field itself, and one that still occupies at most 63 significant hex digits inside the 64-digit canonical form.

**Why lowercase.**
Starknet has no checksummed address encoding.
Unlike [EIP-55][], where the case pattern of a hex address carries a checksum and so is information, case on Starknet carries nothing at all, which makes an uppercase and a lowercase spelling pure duplicates.
Lowercase is therefore mandated to collapse them, and this is a deliberate divergence from the `eip155` namespace, where mixed case must be preserved.

### Token id form

The `token_id` of an `erc721` asset is a Cairo `u256`, written in base ten with no leading zeros, no sign and no `0x` prefix.
The largest `u256` is 78 decimal digits, which is exactly the `token_id` length limit in [CAIP-19][], so every valid Starknet token id fits and none has room to spare.
Hexadecimal token ids MUST NOT be used, because permitting two renderings of one id would reintroduce at the item level precisely the ambiguity this profile removes at the contract level.

### No percent-encoding is required

Every reference and every `token_id` defined here is drawn from `[0-9a-fx]` or `[0-9]`, so nothing in this profile can produce an octet outside the `asset_reference` or `token_id` charset, and no percent-encoding is defined.
This is a constraint the profile keeps rather than a coincidence: the identifier is bound to the contract address and the numeric item id, never to a token's `name` or `symbol`, which on Starknet are Cairo `ByteArray` values holding arbitrary UTF-8 and would require an escape as well as being non-unique.

## RegEx

The RegEx validation strings are as follows:

```sh
asset_id:           asset_type + "/" + token_id
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           namespace + ":" + blockchain_id (as defined in [CAIP-2])

asset_namespace:    "erc20" | "erc721"

asset_reference:    0x[0-9a-f]{64}

token_id:           0|[1-9][0-9]{0,77}
```

The `asset_reference` expression is deliberately exact rather than a range: it accepts the canonical form and nothing else.
A validator that also wishes to recognise non-canonical input in order to reject it with a useful message can match `0x?[0-9a-fA-F]{1,64}` and then compare the normalised value, but it MUST NOT emit anything but the canonical form.

## Semantics

### Fungible tokens

`erc20` names a contract implementing the [SNIP-2][] token interface, which is the Starknet analogue of an ERC-20.
The asset is the contract, so an `erc20` identifier is an `asset_type` and never carries a `token_id`.

### ETH and STRK are contracts, not chain-native units

Starknet accounts hold no protocol-level balance.
ETH on Starknet is an ERC-20 at `0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7`, whose `name()` returns `Ether` and whose `symbol()` returns `ETH`, and it exists because ETH was bridged from Ethereum and minted by that contract.
STRK is an ERC-20 at `0x04718f5a0fc34cc1af16a1cdee98ffb20c31f5cd61d6ab07201858f4287c938d`, whose `name()` returns `Starknet Token`.
Both are used to pay transaction fees, but paying a fee with them is a contract call, not a debit of an account field.

This profile therefore defines no `slip44` asset namespace, and implementations MUST NOT write `starknet:SN_MAIN/slip44:9004` or `starknet:SN_MAIN/slip44:60`.
[SLIP-0044][] does register coin type `9004` for `STRK` and `60` for `ETH`, but a SLIP-0044 coin type is an HD key-derivation path component, and its presence says that wallets derive Starknet keys at that path, not that the chain has a native balance at protocol level.
Writing a `slip44` identifier here would create a second name for an asset that already has a correct one, which is the ambiguity the rest of this document exists to avoid.

### Non-fungible tokens

`erc721` names a contract implementing the [SNIP-3][] interface.
Without a `token_id` the identifier is an `asset_type` naming the collection as a class; with a `token_id` it is an `asset_id` naming one item, whose current holder is the address returned by that contract's `owner_of` entry point for that id.

## Examples

```sh
# STRK, the Starknet Token, on Starknet mainnet
starknet:SN_MAIN/erc20:0x04718f5a0fc34cc1af16a1cdee98ffb20c31f5cd61d6ab07201858f4287c938d

# ETH on Starknet -- a bridged ERC-20 contract, not a chain-native balance
starknet:SN_MAIN/erc20:0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7

# USD Coin (USDC) on Starknet mainnet
starknet:SN_MAIN/erc20:0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8

# The Starknet.id identity collection, as a class
starknet:SN_MAIN/erc721:0x05dbdedc203e92749e2e746e2d40a768d966bd243df04a6b712e222bc040a9af

# Starknet.id identity number 1
starknet:SN_MAIN/erc721:0x05dbdedc203e92749e2e746e2d40a768d966bd243df04a6b712e222bc040a9af/1

# The same asset type on the public testnet, whose chain id resolves to SN_SEPOLIA
starknet:SN_SEPOLIA/erc20:0x04718f5a0fc34cc1af16a1cdee98ffb20c31f5cd61d6ab07201858f4287c938d
```

## Test Cases

The following spellings of the Starknet mainnet ETH contract all denote the same contract on chain, and all consist only of characters the `asset_reference` charset permits.
Exactly one of them is a valid [CAIP-19][] asset reference under this profile.

| Input reference                                                      | Digits | Valid | Normalises to                                                        |
| :------------------------------------------------------------------- | -----: | :---- | :------------------------------------------------------------------- |
| `0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7` |     64 | yes   | itself                                                               |
| `0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7`  |     63 | no    | `0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7` |
| `0x049D36570D4E46F48E99674BD3FCC84644DDD6B96F7C741B1562B82F9E004DC7` |     64 | no    | `0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7` |
| `049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7`   |     64 | no    | `0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7` |
| `0x00049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7` | 66   | no    | invalid input: more than 64 digits, MUST be rejected, not trimmed    |

The same four-way spread applies to values whose minimal form is shorter still.
The class hash of the ETH contract is returned by a public node as `0xb45dbc3714180381c5680e41931172d67194d77d504413465390e0bef194ec`, 62 digits, whose canonical 64-digit form is `0x00b45dbc3714180381c5680e41931172d67194d77d504413465390e0bef194ec`; class hashes are not asset references, but they illustrate that the unpadded spelling is what the network itself emits, so producers cannot assume their input is padded.

```sh
# Valid
starknet:SN_MAIN/erc20:0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7

# Invalid -- same asset, unpadded
starknet:SN_MAIN/erc20:0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7

# Invalid -- same asset, uppercase
starknet:SN_MAIN/erc20:0x049D36570D4E46F48E99674BD3FCC84644DDD6B96F7C741B1562B82F9E004DC7

# Invalid -- same asset, no 0x prefix
starknet:SN_MAIN/erc20:049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7

# Valid -- token id zero is written without padding
starknet:SN_MAIN/erc721:0x05dbdedc203e92749e2e746e2d40a768d966bd243df04a6b712e222bc040a9af/0

# Invalid -- token id may not be padded or hexadecimal
starknet:SN_MAIN/erc721:0x05dbdedc203e92749e2e746e2d40a768d966bd243df04a6b712e222bc040a9af/01
starknet:SN_MAIN/erc721:0x05dbdedc203e92749e2e746e2d40a768d966bd243df04a6b712e222bc040a9af/0x1
```

## Collisions and Security Considerations

### Variable-width addresses are the primary hazard

The four spellings above are not an edge case reachable only by a careless producer.
They are what different parts of the ecosystem emit as a matter of course, and a consumer that stores the identifier as given will hold several rows for one asset with no way to notice.
The failure is silent in both directions: a balance lookup keyed on the unpadded spelling misses a position stored under the padded one, and a portfolio total that sums both double-counts.
This is why the canonical form is mandated and why non-canonical input MUST be rejected rather than normalised in place: rejection makes the defect visible at the boundary where it can still be fixed.

### Case is not a checksum here

An implementer carrying `eip155` code across is likely to preserve case, because in [EIP-55][] case is a checksum and destroying it destroys an integrity check.
On Starknet there is no such scheme, so preserving case preserves only noise, and an `eip155`-style implementation reused unchanged will produce duplicate identifiers.

### One contract, two interfaces

Nothing prevents a Starknet contract from implementing both the [SNIP-2][] and [SNIP-3][] interfaces, in which case the same canonical address is a well-formed reference under both `erc20` and `erc721` and the two identifiers differ only in the asset namespace.
Such a contract has no single correct identifier under this profile.
Producers SHOULD detect the case with [SNIP-5][] and SHOULD refuse to emit an identifier rather than pick one, and consumers MUST NOT assume that the asset namespace can be recovered from the reference.

### Bridged assets are distinct assets

ETH on Starknet and ETH on Ethereum are different identifiers — `starknet:SN_MAIN/erc20:0x049d36…` and `eip155:1/slip44:60` — and so are STRK on Starknet and the STRK ERC-20 on Ethereum mainnet.
They are held in different places under different assumptions about the bridge, and merging them is an accounting decision for the consumer, not a normalisation this profile performs.

### Metadata is not an identifier

`name()` and `symbol()` return Cairo `ByteArray` values chosen freely by the deployer, are not unique, and are not part of any identifier defined here.
They MUST NOT be used to construct or to match a CAIP-19 identifier.

## Backwards Compatibility

No [CAIP-19][] profile previously existed for this namespace, so no existing identifier changes meaning.
The [CAIP-2][] and [CAIP-10][] profiles for `starknet` are unaffected, and this document adopts their chain-id semantics unchanged: the reference is the ASCII decoding of the field element returned by `starknet_chainId`.

The examples above use `SN_MAIN` and `SN_SEPOLIA`.
`SN_SEPOLIA` is what the resolution method in the [CAIP-2][] profile returns from the current public testnet; the `SN_GOERLI` shown in that profile's own test cases dates from 2022 and the Goerli network it names has since been decommissioned.
That is a fact about the testnet rather than a change to the chain-id rule, and this profile proposes no amendment to it.

The `starknet` namespace also carries a [CAIP-350][] profile, which addresses chain-id serialisation and not asset identity; nothing here conflicts with it.

## References

- [CAIP-19][]: Asset Type and Asset ID Specification
- [SNIP-2][]: Starknet Token Standard, the fungible interface behind the `erc20` namespace
- [SNIP-3][]: Starknet Non-Fungible Token Standard, the interface behind the `erc721` namespace
- [SNIP-5][]: Standard Interface Detection, used to determine which asset namespace applies
- [Starknet ContractAddress][]: the core-library type whose documented value range is `[0, 2**251)`
- [Cairo field elements][]: the felt type whose variable-width serialisation this profile normalises
- [SLIP-0044][]: the registry from which `9004 STRK` and `60 ETH` are deliberately not used here
- [EIP-55][]: the Ethereum checksum scheme that Starknet does not have

[CAIP-2]: ./caip2.md
[CAIP-10]: ./caip10.md
[CAIP-350]: ./caip350.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[SNIP-2]: https://github.com/starknet-io/SNIPs/blob/main/SNIPS/snip-2.md
[SNIP-3]: https://github.com/starknet-io/SNIPs/blob/main/SNIPS/snip-3.md
[SNIP-5]: https://github.com/starknet-io/SNIPs/blob/main/SNIPS/snip-5.md
[Starknet ContractAddress]: https://docs.starknet.io/build/corelib/core-starknet-contract_address-ContractAddress
[Cairo field elements]: https://docs.starknet.io/build/corelib/core-felt252/
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[EIP-55]: https://eips.ethereum.org/EIPS/eip-55

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
