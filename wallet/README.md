---
namespace-identifier: wallet
title: Wallet Namespace
author: ["Vandan Parikh (@vandan)", "Bumblefudge (@bumblefudge)"]
status: Draft
type: Informational
created: 2024-07-16
---

## Rationale

The handling of direct communications channels between cryptographic user-agents (i.e., wallets) and applications vary widely across cryptographic systems.
Rather than being a true namespace defined outside of CASA, this "meta-namespace" informationally groups together the wallet sub-namespaces of other namespaces specified at CASA.
This "meta-namespace" is intended to facilitate an explicit segregation of connection mechanics, methods, and notifications for these channels from the very different mechanics, methods, and notifications used for application <> node purposes in each namespace.

## Governance

This namespace is purely formal and governed in CASA, and as such should only be used as a kind of "alias" or "passthrough" to each other namespace's application<>wallet mechanisms, governed accordingly in each namespace's native governance.
Contributors are discouraged from making any claims or specifying any behaviors not already specified in the referenced namespaces;
furthermore, contributers are encouraged to provide normative references when adding to the profiles for a given CAIP.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
