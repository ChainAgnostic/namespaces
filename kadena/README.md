---
namespace-identifier: kadena
title: Kadena
author: ["Billy Rennekamp (@okwme)"]
discussions-to: https://github.com/0xcounting/FAR/issues/1
status: Draft
type: Informational
created: 2026-09-14
---

# Namespace for Kadena chains

Kadena is a proof-of-work platform whose networks run Chainweb, a braided
parallel-chain consensus, and execute smart contracts written in Pact.
The `kadena` namespace covers networks that run the Chainweb protocol and
expose its HTTP node API.
A network in the namespace is identified by its Chainweb network id, as
specified in the [Kadena CAIP-2 profile][caip2].

The one thing to internalise before reading further is that a Kadena network is
not a single chain.
Chainweb mainnet is twenty parallel chains, numbered `0` through `19`, mined
together and braided into one consensus object called a *cut*.
Every chain carries its own copy of the Pact database, so an account or a
deployed module exists separately on each of the twenty, and moving value
between them is a native cross-chain transfer rather than a bridge.
Despite that, the twenty chains share one network id, one native token, one
difficulty regime and one API host, and the [CAIP-2 profile][caip2] therefore
identifies the network and not the individual Chainweb chain.

## Rationale

Kadena's own [KIP-0017][] already defines CAIP-2 identifiers for this ecosystem
and uses the namespace string `kadena` with the Chainweb network id as the
reference, for example `kadena:mainnet01`.
That document is Final and is deployed in Kadena wallets through WalletConnect,
so registering any other shape here would fork identifiers that are already in
production.
This registration writes down what the ecosystem settled on rather than
inventing something new, and the [CAIP-2 profile][caip2] records why the
Chainweb chain number is deliberately left out of the reference.

Implementers writing a CAIP-19 profile for Kadena should be warned about Pact
module naming before they start.
A fully qualified Pact module name is `namespace.module`, and `.` is legal in a
CAIP-19 `asset_reference` — but Kadena's *principal* namespaces are a BLAKE2b
hash prefixed with `n_`, as in
`n_14912521e87a6d387157d526b281bde8422371d1.my-calculator`, and `_` is **not**
in the `asset_reference` character class `[-.%a-zA-Z0-9]{1,128}`.
Percent-encoding (`n%5F14912521…`) is the only escape the grammar allows.
A future `kadena` CAIP-19 profile has to pick one and say so; this document does
not.

This namespace was drafted by the maintainers of FAR, an open cross-reference
between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a CAIP-2 for
Kadena in order to name KDA and the Pact fungibles issued alongside it.
The authors do not represent the Kadena ecosystem.
It is offered as a starting point for the Kadena community to correct, adopt or
replace, and the authors would rather it carry a maintainer's name than theirs.

## Governance

Technical standards for Kadena are proposed as Kadena Improvement Proposals
(KIPs) in the [KIPs repository][], which covers token interfaces
([fungible-v2][KIP-0005], [poly-fungible-v1][KIP-0011]), account formats
([KIP-0012][]) and wallet interfaces ([KIP-0017][], [KIP-0039][]).

Kadena Inc., the company that built Chainweb and Pact, announced on 2025-10-21
that it was ceasing business operations and active maintenance, and the
`kadena-io` GitHub organisation was archived.
Mainnet has continued to produce blocks under independent miners, and protocol
maintenance moved to the community fork at [kda-community/chainweb-node][].
A first-time implementer should expect the [KIPs repository][] to be a frozen
historical record rather than a live process, and should treat the community
fork and its bootstrap node list as the current source of truth.

## References

- [Chainweb node][] - Reference implementation, community-maintained fork; `src/Chainweb/Version/Mainnet.hs` defines the `mainnet01` network id
- [Chainweb OpenAPI][] - Machine-readable description of the node HTTP API, including `/cut` and `/info`
- [Kadena documentation][] - Concepts, Pact language reference and node operation
- [KIPs repository][] - Kadena Improvement Proposals
- [KIP-0017][] - Kadena's WalletConnect v2 profile; the source of the `kadena:mainnet01` identifier shape
- [KIP-0039][] - `kadena_getNetwork_v1`, which returns `networkId` and treats the Chainweb chain as a separate URL component
- [Pact][] - The smart contract language whose module names raise the `_` question described above
- [CAIP-19][] - Asset type specification whose `asset_reference` character class excludes `_`

[Chainweb node]: https://github.com/kda-community/chainweb-node
[kda-community/chainweb-node]: https://github.com/kda-community/chainweb-node
[Chainweb OpenAPI]: https://github.com/kadena-io/chainweb-openapi/blob/main/chainweb.openapi.yaml
[Kadena documentation]: https://docs.kadena.io/
[KIPs repository]: https://github.com/kadena-io/KIPs
[KIP-0005]: https://github.com/kadena-io/KIPs/blob/master/kip-0005.md
[KIP-0011]: https://github.com/kadena-io/KIPs/blob/master/kip-0011/kip-0011.md
[KIP-0012]: https://github.com/kadena-io/KIPs/blob/master/kip-0012/kip-0012.md
[KIP-0017]: https://github.com/kadena-io/KIPs/blob/master/kip-0017.md
[KIP-0039]: https://github.com/kadena-io/KIPs/blob/master/kip-0039.md
[Pact]: https://github.com/kadena-io/pact
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[caip2]: ./caip2.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
