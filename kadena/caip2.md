---
namespace-identifier: kadena-caip2
title: Kadena Namespace - Chains
author: ["Billy Rennekamp (@okwme)"]
discussions-to: https://github.com/0xcounting/FAR/issues/1
status: Draft
type: Standard
created: 2026-09-14
requires: CAIP-2
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Introduction

Every Chainweb network is configured with a `ChainwebVersionName`, a short text
label that Kadena tooling calls the `networkId`.
The `kadena` CAIP-2 profile identifies a network by that string, verbatim.
Mainnet's network id is `mainnet01`, so its chain ID is `kadena:mainnet01`.

A Chainweb network is made of many parallel chains — twenty on mainnet, numbered
`0` to `19` — and the number of a Chainweb chain is **not** part of the CAIP-2
reference.
The reasoning is set out in [Chainweb chains are not CAIP-2 references][] below,
because it is the single thing most likely to surprise an implementer.

## Specification

### Semantics

A Kadena chain ID consists of the literal namespace `kadena`, a colon, and a
reference containing the network's `networkId`.
Two nodes reporting the same `networkId` claim membership in the same network.
The `networkId` is the value a node requires in the `networkId` field of a
signed Pact command; a command carrying any other value is rejected, which makes
it the replay-protection domain for the network.

### Syntax

```text
chain_id:  "kadena:" + reference
namespace: kadena
reference: networkId
```

The reference must match the following regular expression:

```regex
^[-_a-zA-Z0-9]{1,32}$
```

The reference is the `networkId` copied without transformation: no case folding,
no trimming, no normalisation.
References are case-sensitive, and every network id issued to date is lowercase
ASCII.

Chainweb does not itself constrain the character set or length of a
`ChainwebVersionName`; it is an arbitrary text field in the node implementation.
Every registered network id — `mainnet01`, `testnet04`, `testnet06`,
`development`, `recap-development` — is at most 17 characters and already
matches the expression above, so no truncation rule is needed today.
A network id that did not fit could not be expressed under this profile and must
not be registered here until this document defines an encoding for it; the
`hashed-` prefix used by the `cosmos` namespace is the recommended precedent.

### Resolution Mechanics

To resolve the network id reported by a Chainweb node, make a GET request to
the `/cut` endpoint of the network you believe the node serves.

```shell
curl https://fr-1.chainweb-community.org/chainweb/0.0/mainnet01/cut
```

The network id appears twice: once in the request path, and once in the
`instance` field of the response body.
The following is an abbreviated response captured on 2026-09-14:

```json
{
  "hashes": {
    "0": { "height": 7228173, "hash": "aUeRrSH_fN3Gj_xA6bicsTgdOmYjIjk5Tkv1zmg8_7w" },
    "19": { "height": 7228173, "hash": "jDy40lpL9ssQz0bYuJRmcdFyM5m0Q2j-KUDnrBJIucg" }
  },
  "id": "XEMFxOJwp0RgHS7f5wOoxmcW4BxK3_ltv15cRryswTQ",
  "height": 144563450,
  "instance": "mainnet01"
}
```

Two checks together make the result meaningful.
The network id is part of the routing, so a node that does not serve the
requested network answers `404` rather than answering for a different one — the
host above returns `404` for both `/chainweb/0.0/testnet04/cut` and
`/chainweb/0.0/mainnet02/cut` — and the `instance` field must then equal the
network id used in the path, or the response must be discarded.
Prefix the confirmed value with `kadena:`; the example above therefore resolves
to `kadena:mainnet01`.

A node's `/info` endpoint reports the same string as `nodeVersion`, alongside
`nodeNumberOfChains` and `nodeChains`, and may be used where the service API is
exposed.

## Chainweb Chains Are Not CAIP-2 References

The obvious alternative to this profile is a compound reference such as
`kadena:mainnet01-0`, one CAIP-2 per Chainweb chain, in the way that `cosmos`
and `polkadot` give each zone and each parachain its own chain ID.
This profile rejects that, for four reasons.

First, the ecosystem has already chosen.
[KIP-0017][], a Final Kadena Improvement Proposal deployed in wallets through
WalletConnect, defines exactly these identifiers — `kadena:mainnet01`,
`kadena:testnet04`, `kadena:development` — and states in terms that they "are
not equivalent to a Kadena Chain ID (e.g. chain 1)" but are "more closely
related to Kadena's `networkId` field".
[KIP-0039][] repeats the split: a wallet returns a `networkId` and a host, and
the caller appends the Chainweb `chainId` to build a request URL.

Second, the analogy to Cosmos and Polkadot does not hold.
A Cosmos zone and a Polkadot parachain each have their own validator set and can
finalise blocks without the others; that independence is what earns them
separate chain IDs.
Chainweb chains cannot.
Each block header commits to the current headers of its adjacent chains, and a
cut is valid only if all twenty chains braid consistently, so the twenty share
one proof-of-work security budget and one consensus object.
The right mental model is a sharded chain, not a family of chains.

Third, the Chainweb chain number is a payload field, not a network identity.
It travels in `meta.chainId` inside a signed Pact command, next to `sender`,
`gasLimit` and `ttl`, while `networkId` sits outside as the replay-protection
domain.
CAIP-2 names replay-protection domains.

Fourth, addressing a specific Chainweb chain is a CAIP-10 and CAIP-19 concern
and can be solved there without a second CAIP-2 shape.
[KIP-0017][] takes this route: its CAIP-10 `account_address` is a public key,
which is chain-independent because a keyset is valid on all twenty chains, and
the per-chain detail is returned separately by `kadena_getAccounts_v1` as a
`chains` array.
Balances and deployed modules genuinely are per-chain, so a profile that needs
to name one must carry the chain number — but in the account or asset segment,
where the existing network identifiers stay valid, rather than multiplying the
network's CAIP-2 by twenty.

## Rationale

The `networkId` is the only value Chainweb itself treats as the identity of a
network: it selects the fork schedule and genesis set in the node, it appears in
the path of every node API call, it is echoed in every block header as
`chainwebVersion`, and it is the field a node checks before accepting a
transaction.
Using it requires no registry and no transformation.

Taking it verbatim, rather than hashing or lowercasing it, keeps the CAIP-2
reference and the node API path segment textually identical, so an
implementation can build a request URL from a chain ID by substitution and
validate the response by string comparison.

The namespace string `kadena` names the ecosystem and matches the string
[KIP-0017][] already uses in production WalletConnect sessions.

## Well-Known Networks

The following table lets clients label well-known networks without a round trip.
It is informative; the resolution method above remains authoritative.

| Network | `networkId` | Chains | CAIP-2 chain ID |
| --- | --- | ---: | --- |
| Kadena Mainnet | `mainnet01` | 10 then 20 | `kadena:mainnet01` |
| Testnet04 | `testnet04` | 10 then 20 | `kadena:testnet04` |
| Testnet06 | `testnet06` | 20 | `kadena:testnet06` |
| Devnet | `development` | 20 | `kadena:development` |
| Legacy devnet | `recap-development` | 10 then 20 | `kadena:recap-development` |

The values are defined in `src/Chainweb/Version/*.hs` in the [Chainweb node][]
source.
Mainnet ran ten chains from genesis and expanded to twenty at block height
852,054; both graphs live under the same network id, which is one more reason
the chain count cannot be part of the identifier.

## Backwards Compatibility

There was no previously registered CAIP-2 profile for Kadena.
This profile is identical to the identifiers already defined by [KIP-0017][] and
changes nothing about Kadena's native network ids.

## Test Cases

### Valid identifiers

| Identifier | Reason |
| --- | --- |
| `kadena:mainnet01` | Kadena Mainnet |
| `kadena:testnet04` | Long-running public testnet |
| `kadena:testnet06` | Current public testnet in the community node |
| `kadena:development` | Local development network |
| `kadena:recap-development` | Legacy development network, exercises `-` in a reference |

### Invalid identifiers

| Identifier | Reason |
| --- | --- |
| `kadena:` | Empty reference |
| `kadena:mainnet01-0` | Chainweb chain number appended; not a network id |
| `kadena:mainnet01/0` | `/` is not in the reference character class |
| `kadena:Mainnet01` | Incorrect network id casing; references are case-sensitive |
| `KADENA:mainnet01` | Incorrect namespace casing |
| `kadena: mainnet01` | Leading whitespace |
| `kadena:mainnet` | Not a registered network id |
| `kadena:recap-development-with-a-longer-name` | Exceeds 32 characters |

## Additional Considerations

Kadena's Chainweb EVM chains are out of scope for this namespace.
They are Chainweb chains that run the EVM rather than Pact, and each carries its
own EIP-155 chain id — `5920` through `5924` on the Chainweb EVM testnet — so
they are already addressable as `eip155:5920` and so on.
A Chainweb network can therefore span two CAIP-2 namespaces, and a future
revision of this profile may need to say how the Pact and EVM halves of one
network relate.

Kadena Inc. ceased operations in October 2025 and its `kadena-io` GitHub
organisation is archived.
Its public node hosts under `chainweb.com`, including the `api.chainweb.com`
endpoint cited throughout Kadena's own documentation and OpenAPI description, no
longer resolve in DNS as of 2026-09-14.
Mainnet itself is still producing blocks — the cut height advanced from
144,563,274 to 144,563,305 over 45 seconds while this document was written — and
is reachable through the community bootstrap nodes listed in
`src/P2P/BootstrapNodes.hs` of the [Chainweb node][] fork.
Implementers should resolve chain IDs against a node of their own choosing
rather than a hard-coded vendor host.

## Security Considerations

Resolving a chain ID through `/cut` establishes only what the queried endpoint
reports.
It does not authenticate the endpoint, and a `networkId` is a self-declared
label that any operator can configure, so a private network can claim
`mainnet01`; matching `instance` against the path defeats a misrouted response
but not a dishonest one.
Applications relying on a trusted chain identity should use endpoints they trust
and corroborate the result against known block hashes.

## References

- [CAIP-2][] - Blockchain ID specification
- [Chainweb node][] - Community-maintained reference implementation; `src/Chainweb/Version/Mainnet.hs` sets `ChainwebVersionName "mainnet01"`
- [Chainweb OpenAPI][] - Definitions and examples for `/cut` (`instance`) and `/info` (`nodeVersion`, `nodeNumberOfChains`)
- [Chainweb overview][] - Kadena documentation on the braided parallel-chain construction that makes the twenty chains one consensus object
- [KIP-0017][] - Kadena's WalletConnect v2 profile, which defines `kadena:mainnet01` and separates it from the Chainweb chain id
- [KIP-0039][] - `kadena_getNetwork_v1`, which returns `networkId` and leaves `chainId` to the caller
- [Chainweb EVM testnet guide][] - EIP-155 chain ids for the EVM Chainweb chains

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[Chainweb node]: https://github.com/kda-community/chainweb-node
[Chainweb OpenAPI]: https://github.com/kadena-io/chainweb-openapi/blob/main/chainweb.openapi.yaml
[Chainweb overview]: https://docs.kadena.io/
[KIP-0017]: https://github.com/kadena-io/KIPs/blob/master/kip-0017.md
[KIP-0039]: https://github.com/kadena-io/KIPs/blob/master/kip-0039.md
[Chainweb EVM testnet guide]: https://github.com/kadena-docs/kadena-docs/blob/main/docs/guides/nodes/evm-testnet.md
[Chainweb chains are not CAIP-2 references]: #chainweb-chains-are-not-caip-2-references

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
