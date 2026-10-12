---
namespace-identifier: icp
title: Internet Computer
author: Jeff Jafari (@asjn3e)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/238
status: Draft
type: Informational
created: 2026-10-11
---

# Namespace for the Internet Computer

The Internet Computer Protocol (ICP) runs one public network, ICP mainnet.
The network is made of many subnets, and each subnet is a blockchain of its own.
All subnets of a network share one address space and one root of trust: the public key of the Network Nervous System (NNS).
Clients verify certified responses from any subnet against that key.
This namespace identifies an ICP network by its root public key, not by a genesis block.

Users and smart contracts share one identifier type, the principal.
A smart contract is called a canister, and its principal is its canister ID.
A fungible token is a ledger canister that implements the [ICRC-1][] standard.
The ICP ledger canister holds the ICP token and implements ICRC-1 as well.

## Rationale

The namespace is called `icp`, the abbreviation the protocol, its token, and its community standards already use.

Three properties of ICP shape the profiles in this folder.

First, a [CAIP-2][] chain in this namespace is a whole network, not a subnet.
Principals are unique across all subnets of a network.
A canister keeps its ID when the protocol moves it to another subnet, so subnet-level chain IDs would give one canister several identities over its lifetime.

Second, there is no genesis block to hash.
The network's root public key takes that role.
Agent libraries pin this key to verify responses, and canisters can read it on-chain.

Third, the protocol itself knows only principals.
Subaccounts are a convention of the [ICRC-1][] ledger standard, and each ledger keeps its own.
The [CAIP-10][] profile therefore addresses principals, and leaves ledger subaccounts to a later profile.

## Governance

The NNS is the on-chain governance system of ICP mainnet.
Protocol upgrades and community standards both pass through NNS proposals.

Community standards are called ICRCs.
Technical working groups draft them in public repositories such as [dfinity/ICRC][] and [dfinity/wg-token-standards][], reach rough consensus following [ICRC-0][], and then submit them to the NNS for acceptance.
The [IC Interface Specification][] defines principals, the HTTPS interface, and certification.

ICP working groups have discussed CAIP identifiers since 2023, and their drafts are listed in the References section.
In 2023 the working groups agreed twice on a hash of the root public key as the network reference, and this namespace follows that agreement.
As of this writing, the NNS has not accepted any ICRC on CAIP identifiers.

## Planned profiles

This folder does not yet define the profiles that wallet integrators will need next:

- [CAIP-25][] and [CAIP-27][]: which methods an `icp:` session scope exposes, and how a wallet receives requests for them.
- [CAIP-122][]: signing in with an ICP account. This profile needs to cover the delegation model of ICP, including Internet Identity, where a session key signs on behalf of a principal instead of the principal's own key.

## References

- [IC Interface Specification][]: principals, their textual form, the status endpoint, and certification.
- [ICRC-0][]: how ICP working groups operate and reach decisions.
- [ICRC-1][]: the fungible token standard that the CAIP-19 profile builds on.
- [ICRC-1 Textual Encoding][]: the textual form of ICRC-1 accounts, including subaccounts.
- [icvc/icp-namespace][]: 2023 working group drafts of CAIP-2 and CAIP-10 profiles for ICP, by Quint Daenen.
- [Working group notes on CAIP-2][]: notes from the 2023-05-30 session that agreed on the root key hash.
- [Ledger WG notes][]: the 2023-10-31 Ledger and Tokenization Working Group decision for the root key hash over `icp:mainnet`.
- [ICP Network Identifiers draft][]: 2025 working group draft of ICP network identifiers.
- [ICRC-22 draft][]: payment request URIs that use the chain ID defined here.

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[CAIP-25]: https://chainagnostic.org/CAIPs/caip-25
[CAIP-27]: https://chainagnostic.org/CAIPs/caip-27
[CAIP-122]: https://chainagnostic.org/CAIPs/caip-122
[IC Interface Specification]: https://docs.internetcomputer.org/references/ic-interface-spec/
[ICRC-0]: https://github.com/dfinity/ICRC/blob/main/README.md
[ICRC-1]: https://github.com/dfinity/ICRC-1/blob/main/standards/ICRC-1/README.md
[ICRC-1 Textual Encoding]: https://github.com/dfinity/ICRC-1/blob/main/standards/ICRC-1/TextualEncoding.md
[dfinity/ICRC]: https://github.com/dfinity/ICRC
[dfinity/wg-token-standards]: https://github.com/dfinity/wg-token-standards
[icvc/icp-namespace]: https://github.com/icvc/icp-namespace
[Working group notes on CAIP-2]: https://github.com/icvc/icp-namespace/pull/1#issuecomment-1568619120
[Ledger WG notes]: https://github.com/dfinity/ICRC-1/blob/main/Charters.md#2023-10-31
[ICP Network Identifiers draft]: https://github.com/dfinity/wg-token-standards/pull/2
[ICRC-22 draft]: https://github.com/dfinity/ICRC/pull/101

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
