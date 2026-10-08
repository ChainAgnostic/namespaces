---
namespace-identifier: sui-caip10
title: Sui Namespace - Account ID Specification
author: William Robertson (@williamrobertson13), Omer Sadika (@omersadika)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/236
status: Draft
type: Informational
created: 2026-10-08
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

_For context, see the [CAIP-10][] specification._

## Introduction

A Sui address is 32 bytes, written as `0x` followed by hexadecimal digits.
Account addresses, derived from a public key, multisig or other authentication scheme, share this space with object IDs, including packages and shared objects.
Sui objects can own other objects and receive transfers like accounts, so both kinds are valid account identifiers in this profile.

A CAIP-10 ID joins a [CAIP-2 Profile][] chain ID and an address, e.g. `sui:mainnet:0x…`.

## Specification

### Semantics

The chain ID follows the [CAIP-2 Profile][], e.g. `sui:mainnet`, `sui:localnet` or `sui:35834a8a`.

The address is `0x` followed by exactly 64 lowercase hexadecimal characters.

Sui tools also accept short forms that drop leading zeros, such as `0x2` for the Sui framework package.
Normalize these before use: remove `0x`, left-pad with zeros to 64 digits, lowercase, and restore `0x`.

The chain ID part can name one network two ways (`sui:mainnet` and `sui:35834a8a`), and four-byte chain identifiers can collide.
To compare accounts, compare canonical addresses and full genesis digests resolved as the [CAIP-2 Profile][] describes.

### Syntax

The account ID is:

```
sui:<network>:0x<64 lowercase hex characters>
```

It matches the following regular expression:

```
^sui:(mainnet|testnet|devnet|localnet|[0-9a-f]{8}):0x[0-9a-f]{64}$
```

The account address part is 66 characters, within the 128-character limit of [CAIP-10][].

### Resolution Mechanics

Every 32-byte value is a valid Sui address and needs no on-chain state to receive coins or objects, so an account ID can be validated without a node.

To learn whether an address currently names an object, ask a full node for the object with that ID (`sui.rpc.v2.LedgerService/GetObject` over gRPC, or the `object` query over GraphQL).
No object at an address does not make it an account: it may belong to a deleted or wrapped object, or to one not yet created.

**Sample request (the shared `Clock` object, on mainnet):**

```
curl -s https://graphql.mainnet.sui.io/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ object(address: \"0x6\") { address } }"}'
```

**Sample response:**

```json
{
  "data": {
    "object": {
      "address": "0x0000000000000000000000000000000000000000000000000000000000000006"
    }
  }
}
```

The same query for an address with no object returns `"object": null`.

To check the node's network, follow the [CAIP-2 Profile][].

## Rationale

This profile uses Sui's canonical address form.
Rejecting short forms gives each address one spelling for string comparisons.

### Backwards Compatibility

Early Sui releases used 20-byte addresses.
Those are no longer used on any live Sui network and are not valid in this profile.

## Test Cases

```
# An account on Sui Mainnet
sui:mainnet:0x90eb19346f76a7d5e0a8e2630d3b3728039d41fd8f1062dd3776f95e0b8ce5f0

# The same account, with the chain named by its chain identifier
sui:35834a8a:0x90eb19346f76a7d5e0a8e2630d3b3728039d41fd8f1062dd3776f95e0b8ce5f0

# An account on Sui Testnet
sui:testnet:0xb5835b953f4f74cc88a87d9af6374fef9154a2a78f8ba48e7ff850a4ae37b0da

# An account on a local network
sui:localnet:0xac93bf4a973ae33b60710b0af4faff31dc04b4af02795fa2103690dc08585f67

# Normalized from the native short form 0x2 (the Sui framework package)
sui:mainnet:0x0000000000000000000000000000000000000000000000000000000000000002

# Normalized from a native upper-case form
# native: 0x90EB19346F76A7D5E0A8E2630D3B3728039D41FD8F1062DD3776F95E0B8CE5F0
sui:mainnet:0x90eb19346f76a7d5e0a8e2630d3b3728039d41fd8f1062dd3776f95e0b8ce5f0

# Invalid: short form not normalized
sui:mainnet:0x2

# Invalid: upper-case hexadecimal
sui:mainnet:0x90EB19346F76A7D5E0A8E2630D3B3728039D41FD8F1062DD3776F95E0B8CE5F0

# Invalid: 20-byte address
sui:mainnet:0x0000000000000000000000000000000000000002
```

## Additional Considerations

`sui:devnet` and `sui:localnet` name whichever devnet or local network the reader is connected to, so account IDs using them are for development.
For persistent records, use the chain identifier form, such as `sui:35834a8a:0x…`, and retain the full genesis digest to distinguish chains with the same four-byte identifier.

One key derives the same address on every Sui network, with separate objects and balances on each.
Signed personal messages don't name a network, so protocols that need one should include the chain ID in the message.

SuiNS names, such as `example.sui` or `@example`, are not addresses and must be resolved to one first.

A valid account ID is not always a safe destination.
Objects and funds sent to an object's address can only be retrieved through that object's own Move module, and never from a package or other immutable object, such as `0x2` ([Sui Transfer to Object]).
Senders should check what an address is first, as [Resolution Mechanics](#resolution-mechanics) describes.

An account ID names an address, not a key.
[Address aliases][Sui Address Aliases] let an address authorize other signers and revoke its original key.
Alias state is network-specific; control on one network does not prove control on another.

## References

- [Sui Docs][] - Developer documentation, including address formats.
- [Sui Address Normalization][] - The canonical address form in Sui's TypeScript library.
- [Sui gRPC API][] - `LedgerService`, including `GetObject` and `GetServiceInfo`.
- [Sui GraphQL API][] - Reference for Sui's GraphQL RPC, including the `object` query.
- [Sui Transfer to Object][] - How objects receive objects sent to their address.
- [Sui Address Aliases][] - The Move module that lets an address authorize other signers.
- [CAIP-2 Profile][] - This namespace's chain IDs.

[Sui Docs]: https://docs.sui.io/
[Sui Address Normalization]: https://sdk.mystenlabs.com/sui/utils
[Sui gRPC API]: https://github.com/MystenLabs/sui-apis/blob/main/proto/sui/rpc/v2/ledger_service.proto
[Sui GraphQL API]: https://docs.sui.io/references/sui-graphql
[Sui Transfer to Object]: https://docs.sui.io/develop/objects/transfers/transfer-to-object
[Sui Address Aliases]: https://github.com/MystenLabs/sui/blob/main/crates/sui-framework/packages/sui-framework/sources/address_alias.move
[CAIP-2 Profile]: ./caip2.md
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
