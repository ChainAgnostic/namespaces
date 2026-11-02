---
namespace-identifier: quantus-caip19
title: Quantus Namespace - Assets
author: ["Nikolaus Heger (@n13)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/228
status: Draft
type: Standard
created: 2026-09-17
requires: ["CAIP-2", "CAIP-19"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Rationale

Quantus networks currently have a single asset: the native token.
On mainnet it is QTC, and on the Planck testnet it is PLK.
Both have 12 decimals.
Following the convention used by other namespaces for native tokens, the asset is identified by its [SLIP-44][] coin type, which is `189189` for Quantus Network.

There is no on-chain asset registry at present, so no other asset namespaces are defined.
This profile will be extended if Quantus adds fungible or non-fungible asset classes.

## Syntax

The `asset_namespace` is `slip44` and the `asset_reference` is the coin type `189189`:

```
asset_type:        chain_id + "/slip44:189189"
chain_id:          "quantus:" + [a-z0-9]{3,32}
```

A regular expression for validating an asset type is:

```
^quantus:[a-z0-9]{3,32}\/slip44:189189$
```

### Backwards Compatibility

Not applicable.

## Test Cases

This is a list of manually composed examples:

```
# QTC, the native token of Quantus mainnet
quantus:mainnet/slip44:189189

# PLK, the native token of the Planck testnet
quantus:planck/slip44:189189
```

## References

- [SLIP-44][] - the registry of coin types, in which `189189` is assigned to Quantus Network
- [Quantus documentation][] - developer documentation for Quantus Network

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[SLIP-44]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[Quantus documentation]: https://docs.quantus.com/

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
