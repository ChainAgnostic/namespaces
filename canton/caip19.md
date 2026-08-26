---
namespace-identifier: canton-caip19
title: Canton Namespace - Assets
author: Marc Juchli (@mjuchli-da) <marc.juchli@digitalasset.com>, Greg May (@mnrgreg)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/201
status: Draft
type: Standard
created: 2026-08-21
requires: ["CAIP-2", "CAIP-19"]
---

# CAIP-19

For context, see the [CAIP-19](https://chainagnostic.org/CAIPs/caip-19) specification.


## Syntax

The Canton ecosystem defines a standardized token representation through CIP-0056. To enable interoperability with chain-agnostic tooling, Canton assets are identified using the CAIP-19 asset identification format.

The `asset type` follows `chain_id + "/" + asset_namespace + ":" + asset_reference`, whereas:
- `chain_id` is the Canton CAIP-2
- `asset_namespace` identifies the asset identification scheme (`[-a-z0-9]{3,8}`)
- `asset_reference` identifies the asset within that scheme (`[-.%a-zA-Z0-9]{1,128}`)

### Assets with SLIP-44

For assets with a SLIP-44 registered coin type, such as `CC` with `6767`, the format is:
```
asset_namespace = slip44
asset_reference = 6767 // CC
asset_type = {chain_id}/slip44:6767
```

Hence, for `CC` on `canton:mainnet-global`, the `asset_type` is `canton:mainnet/slip44:6767`.


### Assets without SLIP-44

For CIP-0056 assets without a SLIP-44 coin type, we leverage CIP-0056 that identifies an instrument by an `InstrumentId`, comprising an administrating party (`admin`) and an instrument identifier (`id`).
Both components are required to identify the instrument: a single administrator **MAY** administer multiple instruments, so `admin` alone does not identify an asset.
The `asset_reference` therefore combines the two.

```
asset_namespace = cip-56
asset_reference = percentEncode({instrumentId.admin}) + "." + percentEncode({instrumentId.id})

asset_type = {chain_id}/cip-56:{asset_reference}
```

For Example:
```
canton:mainnet-global/cip-56:decentralized-usdc-interchain-rep%3A%3A12208115f1e168dd7e792320be9c4ca720c751a02a3053c7606e1c1cd3dad9bf60ef/USDCx
```

**Note:** CAIP-19 defines a maximum length of 128 characters for the `asset_reference` component.
 A Canton party identifier of the form `{hint}::{fingerprint}` consumes 68 characters for the fingerprint, 6 for the percent-encoded `::`, and the delimiter consumes 1, leaving 53 characters to be shared between the administrator's party hint and the percent-encoded instrument identifier.
 Implementations **MUST** ensure that the resulting `asset_reference` complies with the CAIP-19 length constraint.

The optional `token_id` component is not used by CIP-0056, as both InstrumentId components identify an instrument rather than an individual unit of it.
Should a per-unit identifier become necessary, `token_id` remains available for that purpose, in which case an `asset_id` follows `asset_type + "/" + token_id`

## References

- [Canton CAIP-2](./caip2.md): Canton chain identifier profile
- [CIP-0056](https://github.com/canton-foundation/cips/blob/main/cip-0056/cip-0056): Canton token standard
- [SLIP-44](https://github.com/satoshilabs/slips/blob/master/slip-0044.md): Registered coin types

## Rights

Copyright and related rights waived via CC0.
