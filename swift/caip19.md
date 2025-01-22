---
namespace-identifier: swift-caip19
title: SWIFT Network - Asset Identifiers
author: Bumblefudge (@bumblefudge), Daniel Rocha (@danroc)
status: Draft
type: Informational
created: 2025-01-22
updated: 2025-01-22
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Rationale

A common data model was needed to represent fiat balances in multichain networks, and rather than invent an arbitrary new one, using SWIFT/ISO notation seemed more forward-compatible.
As no SWIFT namespace was yet defined, an "empty" one with a special-case for off-network/out-of-band usage, "chainId 0", was added and ISO 4217 codes were used for internationally-recognized fiat currencies and notations.

## Syntax

The fiat currency standard used across most modern SWIFT tooling and accounting systems is ISO 4217, which assigns a 3-letter code to each national currency on Earth, as well as a few supranational ones (`EUR` for the Euro), and a special category, all prefixed with `X`, for major rare metals.
The 3-letter codes are here capitalized, following the legacy convention.

The template for validating these namespace is as follows:
```
chain_id:    "swift:" + network_id + "/iso4217:" + currencycode
network_id:  0 for off-network usage or TBD for specific SWIFT networks
currencycode:   [A-Z]{3}
```

Other asset standards (such as the [ISO 15022] standard for securities accounting or the more verbose [ISO 20022] data model for assets) may be specified at a later time, pending community interest.

## Test Cases

```
# Euro (€)
swift:0/iso4217:EUR

# US Dollar ($)
swift:0/iso4217:USD

# Argentine Peso ($)
swift:0/iso4217:ARS

```

## References

- [ISO 4217:2015][]: Identifier scheme for national and extranational fiat currencies
- [ISO 4217 Registry][]: Current list of current and historical 4217 currency codes

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[ISO 4217:2015]: https://www.iso.org/standard/64758.html
[ISO 4217 Registry]: https://www.iso.org/iso-4217-currency-codes.html
[ISO 15022]: https://www.iso20022.org/welcome-iso-15022
[ISO 20022]: https://www.iso20022.org/

## Rights

Copyright and related rights waived via CC0.
