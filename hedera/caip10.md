---
namespace-identifier: hedera-caip10
title: Hedera Namespace - Accounts
author: Danno Ferrin (@shemnon)
discussions-to: https://github.com/hashgraph/hedera-improvement-proposal/discussions/169
status: Draft
type: Standard
created: 2021-11-01
updated: 2022-03-27
requires: ["CAIP-2", "CAIP-10"]
replaces: CAIP-75
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

In CAIP-10, a string-based general account address scheme is defined. The
canonical representation of a Hedera Address encodes a three-part Hedera
account ID as a string by separating the three parts with `.`s; this
future-proofs the implementation of realms and shards, although in today's
usage, effectively all known addresses still begin with `0.0.`.

### Syntax

The `account_id` is a case-sensitive string in the form:

```
account_id:        chain_id + ":" + account_address + checksum{0,1}
chain_id:          [:-a-zA-Z0-9]{5,32}
account_address:   [0-9]{1,19} + "." + [0-9]{1,19} + "." + [0-9]{1,19}
optional checksum: "-" + [a-z]{5}
```

A regular expression for validating the above can be defined as:
```
hedera:[-a-zA-Z0-9]{5,32}:[0-9]{1,19}\.[0-9]{1,19}\.[0-9]{1,19}(\-[a-z]{5}){0,1}
```

### Semantics

The `chain_id` is specified by the [CAIP-2][] which describes the blockchain id.
The `account_address` is the realm, shard, and account id, where each is
separated by a dot (`.`) and each number is a non-negative signed 64-bit
integer. The default value for realm and shard are 0.

The optional checksum is described in
[HIP-15](https://github.com/hashgraph/hedera-improvement-proposal/blob/master/HIP/hip-15.md).
Addresses with or without checksum are both valid, so deduplication or
canonicalization may be required. Note that intermediaries have no duty to
validate the address against its 5-digit checksum.

## Test Cases

This is a list of manually composed examples

```
# Devnet funding account
hedera:devnet:0.0.98

# Mainnet treasury
hedera:mainnet:0.0.2

# Previewnet app properties account
hedera:previewnet:0.0.121

# Mainnet account with checksum
hedera:mainnet:0.0.123-vfmkw

# Largest possible testnet account
hedera:testnet:9223372036854775807.9223372036854775807.9223372036854775807
```

## Backwards Compatibility

Since the checksum is optional, in pathological account numbering scenarios it
may need to be dropped. It is not expected that we will see this event in normal
usage.

## References

- [Hedera Developer Documentation][]
  - [Native Account Syntax][]: Explanation of shard + realm prefix usage within
        Hedera ecosystem
- [HIP-15][]: Hedera Improvment Proposal for Network Address Checksums
- [HIP-30][]: CAIP Identifiers for the Hedera Network


[CAIP-2]: https://chainAgnostic.org/CAIPS/caip-2
[CAIP-10]: https://chainAgnostic.org/CAIPS/caip-10
[CAIP-19]: https://chainAgnostic.org/CAIPS/caip-19
[HIP-15]: https://github.com/hashgraph/hedera-improvement-proposal/blob/master/HIP/hip-15.md
[HIP-30]: https://github.com/hashgraph/hedera-improvement-proposal/blob/master/HIP/hip-30.md
[Hedera Developer Documentation]: https://docs.hedera.com/guides/
[Native Account Syntax]: https://docs.hedera.com/guides/core-concepts/accounts#account-id
[Hedera Token Service SDK Docs]: https://docs.hedera.com/guides/docs/sdks/tokens
[ERC20 & ERC721 Compatibility]: https://docs.hedera.com/guides/core-concepts/smart-contracts/supported-erc-token-standards

## Copyright

Copyright and related rights waived
via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).****