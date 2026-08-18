---
namespace-identifier: tenzro-caip10
title: Tenzro Namespace - Addresses
author: Tenzro Engineering (eng@tenzro.com)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/184
status: Draft
type: Standard
created: 2026-05-02
updated: 2026-05-02
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

_For context, see the [CAIP-10][] specification._

## Rationale

A Tenzro address is a 32-byte identifier shared across the EVM, SVM, and
Canton/DAML VM façades — there is one address per account, and the same
underlying balance is visible through all three VMs (the pointer model).

Two textual encodings are accepted, mirroring the two ecosystems Tenzro
interoperates with most directly:

- **Hex (EIP-55-style)**: `0x` followed by 64 lowercase hexadecimal
  characters. Used by EVM-aware tooling and the `eth_*` JSON-RPC surface.
- **Base58btc**: 32-byte address encoded with the Bitcoin/Solana
  Base58btc alphabet (44 characters for a full 32-byte input). Used by
  SVM-aware tooling and the Wallet Standard surface.

CAIP-10 references for Tenzro accounts SHOULD use the **hex** form for
parity with EVM tooling and CAIP-122 (SIWx) signatures. Implementations
MUST accept either form on input and SHOULD normalize to lowercase hex
on storage and display.

## Syntax

A Tenzro CAIP-10 account identifier matches:

```
account_id := chain_id ":" account_address
account_address := hex_address | base58_address
hex_address := "0x" [0-9a-f]{64}
base58_address := [1-9A-HJ-NP-Za-km-z]{43,44}
```

where `chain_id` is the CAIP-2 identifier defined in `caip2.md`.

## Chain IDs

_For context, see the [CAIP-2][] specification and `caip2.md`._

| Network Name | Chain ID                             |
| ------------ | ------------------------------------ |
| Testnet      | tenzro:92bd27db9713293097f0e63476e3911e |
| Mainnet      | TBD                                  |

## Test Cases

```
# Tenzro Testnet — hex form (canonical)
tenzro:92bd27db9713293097f0e63476e3911e:0x0000000000000000000000000000000000000000000000000000000000000000

# Tenzro Testnet — base58 form (also accepted)
tenzro:92bd27db9713293097f0e63476e3911e:11111111111111111111111111111111
```

## References

- [CAIP-2][]
- [CAIP-10][]
- [Tenzro Network repository][repo]

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[repo]: https://github.com/tenzro/tenzro-network

## Rights

Copyright and related rights waived via CC0.
