---
namespace-identifier: icp-caip2
title: Blockchain ID Specification for the Internet Computer Namespace
author: Jeff Jafari (@asjn3e)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/238
status: Draft
type: Standard
created: 2026-10-11
requires: ["CAIP-2"]
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

This profile identifies an ICP network by its root public key.
On ICP mainnet this is the public key of the Network Nervous System (NNS), and it certifies every subnet of the network.
The CAIP-2 reference is a truncated SHA-256 hash of that key.

One reference covers the whole network, including all of its subnets.

## Specification

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [BCP 14][] ([RFC 2119][], [RFC 8174][]) when, and only when, they appear in all capitals, as shown here.

### Semantics

Each ICP network has one root public key: a BLS12-381 public key in DER encoding.
The [IC Interface Specification][] calls it "the public key (a DER-encoded BLS key) of the root key of this instance of the Internet Computer Protocol".
On ICP mainnet the DER encoding is 133 bytes long.

The input to the hash MUST be exactly the byte string that the network serves as the `root_key` field of its [status endpoint][Status endpoint].
For ICP mainnet, the agent libraries pin the same byte string.
Implementations MUST NOT re-encode the key before hashing it.
Hashing the 96-byte raw BLS key inside the DER encoding gives `c110ba599921d585d6b10aba2766c5fc` for mainnet, which is not a valid reference.

### Syntax

```
chain_id:    "icp" + ":" + reference
reference:   [0-9a-f]{32}
```

To compute the reference:

1. Get the root key bytes as described in the Semantics section.
2. Compute the SHA-256 hash of those bytes.
3. Encode the hash as lowercase hexadecimal.
4. Keep the first 32 characters.

A reference MUST be exactly 32 lowercase hexadecimal characters.
`icp:737BA355E855BD4B61279056603E0550` is not a valid chain ID.

Every other reference that [CAIP-2][] allows is reserved for future revisions of this profile.
A revision that adopts registry names can therefore only add valid references, and no chain ID that is valid under this version can change its meaning.
The strings `icp:1` and `icp:mainnet` are reserved for ICP mainnet; see the Backwards Compatibility section.

### Resolution Mechanics

For ICP mainnet, use the root key that the official agent libraries ship with.
Agents use this pinned key to verify certified responses, and the [IC Interface Specification][] tells them not to fetch it from the network.
The following command computes the mainnet reference from that key:

```bash
echo 308182301d060d2b0601040182dc7c0503010201060c2b0601040182dc7c05030201036100814c0e6ec71fab583b08bd81373c255c3c371b2e84863c98a4f1e08b74235d14fb5d9c0cd546d9685f913a0c0b2cc5341583bf4b4392e467db96d65b9bb4cb717112f8472e0d5a4d14505ffd7484b01291091c5f87b98883463f98091a0baaae \
  | xxd -r -p | shasum -a 256 | cut -c 1-32
# 737ba355e855bd4b61279056603e0550
```

A canister can compute the reference of the network it runs on.
The system API functions `ic0.root_key_size` and `ic0.root_key_copy` return the root key in replicated execution.
In Rust, `ic_cdk::api::root_key()` wraps them.
The [IC Interface Specification][] describes the key they return as "the public key (a DER-encoded BLS key) of the IC root key of this instance of the Internet Computer Protocol".

Any network also serves its root key at the [status endpoint][Status endpoint], `/api/v2/status`, as the `root_key` field of a CBOR map.
The endpoint is not certified, so use it to compare against a pinned key, or to discover the key of a local development network.
The following example reads the key with `@dfinity/agent`:

```js
import { HttpAgent } from '@dfinity/agent';
import { createHash } from 'node:crypto';

const agent = await HttpAgent.create({ host: 'https://icp-api.io' });
const { root_key } = await agent.status();
const reference = createHash('sha256').update(root_key).digest('hex').slice(0, 32);
console.log(`icp:${reference}`);
// icp:737ba355e855bd4b61279056603e0550
```

## Rationale

The root public key is the identity of an ICP network.
It plays the role that a genesis block hash plays in the `bip122` and `solana` namespaces: anyone can check the reference against the network itself.
Truncating the hash to 32 hexadecimal characters fits the CAIP-2 reference limit and keeps 128 bits of the hash.

ICP working groups have chosen this form twice.
A working group session on 2023-05-30 reached consensus on the truncated hash of the root key ([notes][Working group notes on CAIP-2]).
On 2023-10-31 the Ledger and Tokenization Working Group confirmed it over `icp:mainnet` ([notes][Ledger WG notes]).
Later working group drafts, [ICRC-22][ICRC-22 draft] among them, use it in their examples.

A 2025 draft, [ICP Network Identifiers][ICP Network Identifiers draft], adds a second option: short decimal names from a network registry, with `icp:1` for mainnet.
This profile defines only the hash form, for three reasons:

- Wallets and session protocols compare chain IDs as exact strings, for example the scopes in [CAIP-25][] sessions.
  Two valid strings for one network make every consumer keep an alias table.
  For example, [Oisy][Oisy CAIP-10 chains], the wallet DFINITY maintains, still maps a legacy Solana mainnet reference next to the current one.
- A registry name cannot be checked against the network.
  A hash of the root key can.
- The registry ([ICRC-113][ICP Network Registry draft]) is an open draft, and the NNS has not accepted it.

If the NNS later accepts a network registry, a revision of this profile can adopt registered names.
Each network still needs exactly one canonical string.
Because this version reserves every reference that is not a hash, such a revision can only add references and cannot make an existing chain ID ambiguous.

### Backwards Compatibility

Some ICP drafts used other forms.
An early [ICRC-22][ICRC-22 draft] draft used `icp:mainnet`, and the ICP Network Identifiers draft proposes `icp:1`.
Neither draft was accepted, and neither string is a valid chain ID under this profile.

- Producers MUST emit only the hash form, `icp:737ba355e855bd4b61279056603e0550`.
- Consumers MAY accept `icp:mainnet` and `icp:1` from legacy sources.
  A consumer that accepts either string MUST treat it as `icp:737ba355e855bd4b61279056603e0550`, and MUST NOT treat it as a different network.

This profile reserves both strings for ICP mainnet.

## Test Cases

```bash
# ICP mainnet
icp:737ba355e855bd4b61279056603e0550
```

| Network | DER root key, SHA-256 | Chain ID |
|---------|-----------------------|----------|
| ICP mainnet | `737ba355e855bd4b61279056603e05501db5e5bad147c6eba7be8c2a13f4b6b3` | `icp:737ba355e855bd4b61279056603e0550` |

The mainnet root key in DER encoding, 133 bytes:

```
308182301d060d2b0601040182dc7c0503010201060c2b0601040182dc7c05030201036100814c0e6ec71fab583b08bd81373c255c3c371b2e84863c98a4f1e08b74235d14fb5d9c0cd546d9685f913a0c0b2cc5341583bf4b4392e467db96d65b9bb4cb717112f8472e0d5a4d14505ffd7484b01291091c5f87b98883463f98091a0baaae
```

## Additional Considerations

### Subnets are not chains

A subnet is a blockchain, but this profile does not give subnets their own chain IDs.
Principals are unique across the network, and the protocol routes each call to the subnet that hosts the canister.
A canister keeps its principal when the protocol moves it to another subnet.

### Root key changes

The mainnet root key has not changed since the network launched in May 2021.
The working group drafts describe one case that would change it: a recovery of the NNS subnet in which the threshold signing key is lost, so the network has to generate a new key.
A new key gives a new reference.
The Ledger and Tokenization Working Group discussed this case on 2023-10-31 and treated it as a hard fork: the old network stops, and a new network starts with the same state.

### Local and private networks

Local development networks have their own root keys.
This includes networks started by the [`icp` CLI][icp CLI] (formerly `dfx`) and PocketIC test instances.
The reference of each one is the hash of its own root key.
This profile defines no fixed or well-known reference for local networks.
Such a reference could not be checked against the network, and that check is the property that motivates the hash form.

Current tools derive a local network's root key from the network's configuration.
The same tool, tool version, and subnet layout produce the same root key again, even after the network's state is discarded, so the reference stays the same from run to run.
A different tool, tool version, or subnet layout can produce a different root key and therefore a different reference.
Two separate local networks can therefore share a reference.

Private deployments of the ICP stack also have their own root keys and therefore their own references.

Tooling that targets a local or private network SHOULD read the root key from the status endpoint at startup and derive the reference from it, rather than hard-code a chain ID.

## References

- [CAIP-2][]: the Blockchain ID Specification.
- [BCP 14][]: the meaning of the requirement key words, defined by [RFC 2119][] and [RFC 8174][].
- [IC Interface Specification][]: the root key, certification, and the system API.
- [Status endpoint][]: the `/api/v2/status` endpoint and its `root_key` field.
- [icvc/icp-namespace][]: the 2023 working group draft of this profile, by Quint Daenen.
- [Working group notes on CAIP-2][]: the 2023-05-30 agreement on the truncated hash of the root key.
- [Ledger WG notes][]: the 2023-10-31 Ledger and Tokenization Working Group decision for the hash form over `icp:mainnet`.
- [ICP Network Identifiers draft][]: the 2025 working group draft with the hash and registry options.
- [ICP Network Registry draft][]: the 2025 draft registry of short network names.
- [ICRC-22 draft][]: payment request URIs that use this chain ID.
- [icp CLI][]: the command-line tool that starts local networks.

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-25]: https://chainagnostic.org/CAIPs/caip-25
[BCP 14]: https://www.rfc-editor.org/info/bcp14
[RFC 2119]: https://www.rfc-editor.org/rfc/rfc2119
[RFC 8174]: https://www.rfc-editor.org/rfc/rfc8174
[icp CLI]: https://github.com/dfinity/icp-cli
[IC Interface Specification]: https://docs.internetcomputer.org/references/ic-interface-spec/
[Status endpoint]: https://docs.internetcomputer.org/references/ic-interface-spec/https-interface#api-status
[icvc/icp-namespace]: https://github.com/icvc/icp-namespace/pull/1
[Working group notes on CAIP-2]: https://github.com/icvc/icp-namespace/pull/1#issuecomment-1568619120
[Ledger WG notes]: https://github.com/dfinity/ICRC-1/blob/main/Charters.md#2023-10-31
[ICP Network Identifiers draft]: https://github.com/dfinity/wg-token-standards/pull/2
[ICP Network Registry draft]: https://github.com/dfinity/wg-token-standards/pull/1
[ICRC-22 draft]: https://github.com/dfinity/ICRC/pull/101
[Oisy CAIP-10 chains]: https://github.com/dfinity/oisy-wallet/blob/main/src/frontend/src/env/caip10-chains.env.ts

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
