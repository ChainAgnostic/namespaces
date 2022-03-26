---
namespace-identifier: stellar
title: Stellar Namespace - Chains
author: Gleb Pitsevich (@pitsevich), Juan Caballero (@bumblefudge)
discussions-to: https://github.com/ChainAgnostic/CAIPs/pull/44
status: Draft
type: Standard
created: 2021-02-17
updated: 2022-03-26
requires: CAIP-2
supersedes: CAIP-28
---

# CAIP-2.

*For context, see the [CAIP-2][] specification.*

## Rationale

The namespace "stellar" refers to the wider Stellar ecosystem, including private
networks.

Each Stellar network has its own unique passphrase, which is to sign the genesis
block but also  used when validating signatures on a given transaction to ensure
it was intended for that chain. The current passphrases for the Stellar public main-net
and public testnet, commonly referred to as `pubnet` and `testnet` respectively, are:
- Pubnet: `Public Global Stellar Network ; September 2015`
- Testnet: `Test SDF Network ; September 2015`

## Syntax

The reference relies on Stellar's current designation of addresses belonging to
test or main networks by prefixing them with `testnet` or `pubnet`
correspondingly. As these are the only two documented public Stellar networks,
the only known chain IDs are `testnet` and `pubnet`.

As laid out in the [Stellar Network Passphrase][] documentation, private and
future public networks alike are encouraged to use the same convention when
defining their passphrases. As these passphrases need to be unique to avoid
collisions between future and/or private networks, chainIDs should be derived
deterministically from them.  For this reason, we define the chain ID of any
other arbitrary network by the following abridged hash of its passphrase
`first_16_chars(hex(sha256(utf8(passphrase))))`

where:

- `passphrase`= a Stellar network passphrase conforming to the `<name> ; <genesis-month>` convention
- `utf8`= a UTF-8 encoding function
- `sha256`= a SHA256 hash function
- `hex`= a lowercase hex encoder
- `first_16_chars`= a function to extract the first 16 characters of the
  resulting string and dropping the rest

This way, any networks other than the two global/public Stellar networks can be
referenced unambiguously in the future.

### Resolution Method

To resolve a blockchain reference for the Stellar namespace, make a REST GET
request to the Stellar Horizon node with endpoint `/` or REST GET request to the
Stellar Core node with endpoint `/info`, for example:

```jsonc
// Request
curl -X GET "https://horizon.stellar.org/" -H "accept: application/json"

// Response
{
  "_links": {"...": "..."},
  "horizon_version": "2.0.0-rc-89ef5f86ac784d35e29845496e8e1bceac31298a",
  "core_version": "stellar-core 15.2.0 (54b03f755ae5d5aa12a799c8f1ee4d87fc9d1a1d)",
  "ingest_latest_ledger": 34073932,
  "history_latest_ledger": 34073932,
  "history_latest_ledger_closed_at": "2021-02-19T15:50:02Z",
  "history_elder_ledger": 2,
  "core_latest_ledger": 34073932,
  "network_passphrase": "Public Global Stellar Network ; September 2015",
  "current_protocol_version": 15,
  "core_supported_protocol_version": 15
}
```
The response will return a JSON object which will include network information. 

The blockchain reference can be retrieved from `network_passphrase` response of
Horizon or from the `network` response of Stellar Core.

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```
# Testnet (Test SDF Network ; September 2015)
stellar:testnet

# Pubnet (Public Global Stellar Network ; September 2015)
stellar:pubnet

# Foobar Corp Test-net (Test FooBar Network ; August 2025)
stellar:e478179ae8b5b809

```

## References

- [Stellar Specification](https://developers.stellar.org/docs) - 
- [Stellar Asset Types](https://developers.stellar.org/docs/issuing-assets/) -
  Context on asset-types in Stellar
- [Stellar Network Passphrase](https://developers.stellar.org/docs/glossary/network-passphrase/) 

[Stellar Specification]: https://developers.stellar.org/docs 
[Stellar Asset Types]: https://developers.stellar.org/docs/issuing-assets/
[Stellar Network Passphrase]: https://developers.stellar.org/docs/glossary/network-passphrase/

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).