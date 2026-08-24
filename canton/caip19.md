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
- `token_id`: Optional asset identifer (`[-.%a-zA-Z0-9]{1,78}`)

### Assets with SLIP-44

For assets with a SLIP-44 registered coin type, such as `CC` with `6767`, the format is:
```
chain_id = canton:{networkIdentifier} // CAIP-2
asset_namespace = slip44
asset_reference = 6767 // CC
asset_type = canton:{networkIdentifier}/slip44:6767
```

Hence, for `CC` on `mainnet`, the `asset_type` is `canton:mainnet/slip44:6767`.


### Assets without SLIP-44

For CIP-0056 assets without a SLIP-44 coin type leveraging optional Asset ID (identified by `token_id` for fungibles):
```
chain_id = canton:{synchronizer} // see CAIP-2
asset_namespace = cip-56
asset_reference = percentEncode({instrumentId.admin})
token_id = percentEncode({instrumentId.id})

asset_type = canton:mainnet/cip-56:{instrumentId.admin}/{token_id}
```

For Example:
```
canton:mainnet/cip-56:decentralized-usdc-interchain-rep%3A%3A12208115f1e168dd7e792320be9c4ca720c751a02a3053c7606e1c1cd3dad9bf60ef/USDCx
```

**Note:** CAIP-19 defines a maximum length of 78 characters for the optional `token_id` component. The compatibility of this mapping depends on the serialized length of the corresponding Canton `instrumentId.id` value after any required encoding. Implementations **MUST** ensure that the resulting token_id complies with the CAIP-19 length constraint.


## References

- [Canton CAIP-2](./caip2.md): Canton chain identifier profile
- [CIP-0056](https://github.com/canton-foundation/cips/blob/main/cip-0056/cip-0056): Canton token standard
- [SLIP-44](https://github.com/satoshilabs/slips/blob/master/slip-0044.md): Registered coin types

## Rights

Copyright and related rights waived via CC0.
