---
namespace-identifier: hedera-caip2
title: Hedera Namespace - Chains
author: Danno Ferrin (@shemnon)
discussions-to: https://github.com/hashgraph/hedera-improvement-proposal/discussions/169
status: Draft
type: Standard
created: 2021-11-01
updated: 2021-11-01
requires: 2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

The reference relies on Hedera's current network topology addresses being a
single production network (mainnet), two persistent testing networks (testnet
and previewnet) and one refers to local development work (devnet). The
identification and resolution of each network is hard-coded into the various
Hedera SDKs at time of press.

Blockchains in the 'hedera' namespace are referenced by name as the number of
total hedera blockchains should be very small: one mainnet and two testnets at
present. Various governance mechanisms in the Hedera governance structure work
to ensure that small number.

## Syntax

Reference should only be populated with one of the following enumerated strings:
- `mainnet`, 
- `testnet`, 
- `previewnet`, and 
- `devnet`

A regular expression for validating the above or any other theoretically
possible Hedera network identifier string (that fits under the CAIP-20 limit of
32 characters) can be defined as:

```
hedera:[-a-zA-Z0-9]{5,32}
```

### Resolution Method

There is no in-protocol resolution method at present. The particular network
configurations defined in the various SDKs set the networks up for mainnet,
testnet, and previewnet. 

To validate a connection to a specific network, specific account checksums
defined in [HIP-15][] can be used.

## Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```
# Hedera mainnet
hedera:mainnet

# Hedera testnet
hedera:testnet

# Hedera previewnet
hedera:previewnet
```

## Additional Considerations

### Rejected Idea: Using the ethereum blockchain namespace

One possibility for blockchain identifier is to use the `eip155` namespace and
have the networks be represented as `eip155:295`, `eip155:296`, `eip:297`
and `eip:298` for Mainnet, Testnet, Previewnet, and devnet. The EIP155 number
would be derived by the EVM `CHAINID` operation.

Using this identifier, however, would misrepresent the level of compatibility
between Hedera and Ethereum chains. While Hedera does provide an EVM execution
environment that is where the compatibility ends. First, Hedera uses the Edwards
25519 curve, and does not use the chain identifier as part of the signature (
which is the express purpose of EIP-155). Neither does it expose Ethereum
standard JSON-RPC apis at this time.

## References

- [HIP-30][]: CAIP Identifiers for the Hedera Network
- [Hedera Developer Documentation](https://docs.hedera.com/guides/)

[CAIP-2]: https://github.com/chainAgnostic/CAIPS/caip-2.md
[CAIP-10]: https://github.com/chainAgnostic/CAIPS/caip-10.md
[CAIP-19]: https://github.com/chainAgnostic/CAIPS/caip-19.md
[HIP-15]: https://github.com/hashgraph/hedera-improvement-proposal/blob/master/HIP/hip-15.md
[HIP-30]: https://github.com/hashgraph/hedera-improvement-proposal/blob/master/HIP/hip-30.md
[Hedera Developer Documentation]: https://docs.hedera.com/guides/
[Native Account Syntax]: https://docs.hedera.com/guides/core-concepts/accounts#account-id
[Hedera Token Service SDK Docs]: https://docs.hedera.com/guides/docs/sdks/tokens
[ERC20 & ERC721 Compatibility]: https://docs.hedera.com/guides/core-concepts/smart-contracts/supported-erc-token-standards

## Copyright

Copyright and related rights waived
via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).****