---
namespace-identifier: alephium-caip19
title: Alephium Namespace - Assets
author: Hongchao Liu (@h0ngcha0)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/xxxx
status: Draft
type: Standard
created: 2024-06-20
updated: 2024-06-20
requires: ["CAIP-2", "CAIP-19"]
---

## Rationale

Tokens are first class citizens on Alephium. Just like the native
token `ALPH`, all tokens on Alephium are managed by UTXOs, which is
battle tested for secure asset management.

New tokens are deployed through the deployment of new contracts, with
token's id matching the id of the issuing contract. The process of
token issuance is the same for both fungible and non-fungible tokens.

## Specification of token id

Token's id is the same as its issuing contract's id, which is a 32
bytes blake2b hash encoded as a hex string.

## Syntax

Alepihum token id represented as 32 byte array encoded as hex string.

## Examples

```
383bc735a4de6722af80546ec9eeb3cff508f2f68e97da19489ce69f3e703200
```

## References

- [Token](https://docs.alephium.org/dapps/concepts/tokens)
- [Fungible token standard](https://docs.alephium.org/dapps/standards/fungible-tokens)
- [Non-fungible token standard](https://docs.alephium.org/dapps/standards/non-fungible-tokens)

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
