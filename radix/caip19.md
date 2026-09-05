---
namespace-identifier: radix-caip19
title: Radix DLT Namespace - Assets
author: ["Avaunt (@AVaunt-consulting)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/198
status: Draft
type: Standard
created: 2026-08-01
requires: ["CAIP-2", "CAIP-19"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Introduction

On Radix, tokens are **resources**: native ledger primitives created through
the Radix Engine's resource system rather than balances inside deployed
contracts. Every resource — fungible or non-fungible, including the native
token XRD — is identified by a global resource address with the entity
specifier `resource_`. There is no special-cased "native currency"
identifier: XRD is simply the well-known resource
`resource_rdx1tknxxxxxxxxxradxrdxxxxxxxxx009923554798xxxxxxxxxradxrd` on
mainnet.

Fungible resources have a divisibility of 0–18 decimal places and balances
are expressed as `Decimal` quantities. Non-fungible resources additionally
contain individual non-fungible units distinguished by a local ID.

## Specification

### Semantics

#### Asset Namespace

This profile defines a single asset namespace, `resource` (case-sensitive),
covering both fungible and non-fungible resources. Fungibility is a property
of the resource manager, discoverable on-ledger; it is not encoded in the
address string (the entity-type byte inside the address differs between
fungible and non-fungible resource managers, e.g. `0x5d` vs `0x9a`).

#### Asset Reference

The asset reference is the native bech32m resource address, verbatim. Its
structure mirrors account addresses (see the [CAIP-10 Profile][]): the HRP is
`resource_` + the network specifier (`rdx`, `tdx_2_`), followed by the
separator `1`, 48 data characters (1 entity-type byte + 29 address bytes) and
a 6-character checksum. The HRP's network specifier MUST match the [CAIP-2][]
segment of the identifier.

### Syntax

```
asset_type:        chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:          radix:[a-z0-9]{1,32} (see the [CAIP-2 Profile][])
asset_namespace:   resource
asset_reference:   resource_ + hrp_suffix + "1" + [02-9ac-hj-np-z]{54}
hrp_suffix:        rdx | tdx_2_ | (other registered network specifiers)
```

Per-network validation regular expressions:

```
# Mainnet
radix:mainnet/resource:resource_rdx1[02-9ac-hj-np-z]{54}

# Stokenet
radix:stokenet/resource:resource_tdx_2_1[02-9ac-hj-np-z]{54}
```

Addresses MUST be lowercase (see Canonicalization in the [CAIP-10
Profile][]).

### Resolution Mechanics

Resource metadata (symbol, name, divisibility, fungibility, total supply) can
be queried from the Gateway API:

```
POST /state/entity/details
{ "addresses": ["resource_rdx1tknxxxxxxxxxradxrdxxxxxxxxx009923554798xxxxxxxxxradxrd"] }
```

Well-known native resources (XRD, system badges) for each network are
published in the official [Well-Known Addresses][] registry.

## Rationale

The resource address is the canonical asset identifier across all Radix APIs,
wallets, and tooling, and is self-describing in the same way as account
addresses (checksummed, network-bound, entity-typed). A single `resource`
asset namespace reflects the ledger's own model, where fungible and
non-fungible resources share one address space and their fungibility is an
on-ledger property rather than a syntactic distinction.

### Backwards Compatibility

Olympia-era resource identifiers ("RRIs", e.g. `xrd_rr1...`) are a retired
format and are not valid in this namespace.

## Test Cases

This is a list of manually composed examples using officially published
well-known addresses:

```
# XRD (native token, fungible) on mainnet
radix:mainnet/resource:resource_rdx1tknxxxxxxxxxradxrdxxxxxxxxx009923554798xxxxxxxxxradxrd

# XRD on Stokenet
radix:stokenet/resource:resource_tdx_2_1tknxxxxxxxxxradxrdxxxxxxxxx009923554798xxxxxxxxxtfd2jc

# Ed25519 signature virtual badge (a non-fungible resource) on mainnet
radix:mainnet/resource:resource_rdx1nfxxxxxxxxxxed25sgxxxxxxxxx002236757237xxxxxxxxxed25sg
```

## Additional Considerations

### Individual non-fungible units

Radix non-fungible local IDs come in four types whose native delimiters
(`#123#`, `<name>`, `[hex]`, `{uuid}`) fall outside the CAIP-19 token-ID
charset. Identification of individual non-fungible units (as opposed to the
non-fungible resource as a collection) is therefore out of scope for this
initial profile and may be specified in a future revision, e.g. by
percent-encoding the native local-ID representation.

### Underscores

As with CAIP-10 identifiers in this namespace, asset references contain
underscore (`_`) characters from the native HRP, which the formal CAIP-19
reference charset predating this namespace does not include. The same
handling applies: native form is canonical, `%5F` percent-encoding is
acceptable for strict-conformance consumers (see the [CAIP-10 Profile][] for
details and precedent).

## References

- [Radix Resources][] - the resource model for fungible and non-fungible assets.
- [Well-Known Addresses][] - canonical registry of native resources per network.
- [Gateway API][] - `/state/entity/details` endpoint documentation.
- [Radix Dashboard][] - explorer showing resource metadata and holders.

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-2 Profile]: ./caip2.md
[CAIP-10 Profile]: ./caip10.md
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[Radix Resources]: https://docs.radixdlt.com/docs/resources
[Well-Known Addresses]: https://docs.radixdlt.com/docs/well-known-addresses
[Gateway API]: https://radix-babylon-gateway-api.redoc.ly/
[Radix Dashboard]: https://dashboard.radixdlt.com/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
