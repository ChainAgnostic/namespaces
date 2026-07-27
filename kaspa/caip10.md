---
namespace-identifier: kaspa-caip10
title: Kaspa Namespace - Addresses
author: Luke Dunshea (@elldeeone)
discussions-to: https://kas-smiths.org/t/kaspa-x402-pay-per-request-kas-payments-for-apis-and-ai-agents/15
status: Draft
type: Standard
created: 2026-07-27
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Rationale

Kaspa uses a UTXO model rather than persistent balance-bearing accounts.
For CAIP-10 purposes, a Kaspa account identifier represents a native recipient or locking address.

Native Kaspa addresses use the form `<prefix>:<payload>`.
The prefix identifies the network type, and the payload contains an address version, public key or script hash, and checksum.
Because [CAIP-10][] does not allow `:` inside `account_address`, this profile uses the native payload without its prefix.
The CAIP-2 portion already identifies the network.

## Specification

A Kaspa CAIP-10 account identifier MUST follow:

```text
kaspa:<reference>:<address_payload>
```

Where:

- `kaspa` is the namespace
- `<reference>` is defined by the Kaspa CAIP-2 profile
- `<address_payload>` is the portion after the colon in a valid native Kaspa address

The native prefix is determined by the CAIP-2 identifier:

| CAIP-2 identifier | Native address prefix |
|-------------------|-----------------------|
| `kaspa:mainnet` | `kaspa` |
| `kaspa:testnet-10` | `kaspatest` |

### Address Format

Kaspa defines the following address versions:

| Version | Address type | Body length | Encoded payload length |
|---------|--------------|-------------|------------------------|
| `0` | Schnorr public key | 32 bytes | 61 characters |
| `1` | ECDSA public key | 33 bytes | 63 characters |
| `8` | Script hash | 32 bytes | 61 characters |

The preliminary regular expression for an address payload is:

```regex
^(?:[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{61}|[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{63})$
```

A regular-expression match is necessary but not sufficient because the decoded version, body length, and checksum must also be valid.

### Resolution

To validate a Kaspa CAIP-10 identifier:

1. Validate the CAIP-2 reference according to the [Kaspa CAIP-2 Profile][].
2. Restore the native prefix associated with that reference.
3. Decode the reconstructed native address.
4. Validate the address version, body length, and prefix-dependent checksum.

After validation, an implementation can use Kaspa node or SDK address utilities to derive the corresponding transaction script public key.
Address validity does not depend on whether the address currently has unspent outputs.

### Backwards Compatibility

Not applicable.

## Security Considerations

A regular-expression match alone does not establish that an address payload is valid.
Implementations MUST decode the reconstructed native address and validate its version, body length, and checksum.

The native prefix MUST be derived from the CAIP-2 reference rather than accepted as separate input.
A payload paired with the wrong network reference fails the prefix-dependent checksum and MUST be rejected.
When displaying a native Kaspa address, applications SHOULD restore and display its network prefix to avoid ambiguity.

A Kaspa address identifies a locking condition, not a persistent account, owner, or balance.
Applications MUST NOT infer control of an address or the existence of spendable outputs from a valid CAIP-10 identifier.

## Test Cases

Valid:

```text
# Mainnet Schnorr public-key address
kaspa:mainnet:qp0l70zd5x85ttwd6jv7g3s3a8llzj96d8dncn4zmhv4tlzx5k2jyqh70xmfj

# Mainnet script-hash address
kaspa:mainnet:pqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqlmtfk4dg

# Testnet-10 Schnorr public-key address
kaspa:testnet-10:qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqhqrxplya

# Testnet-10 ECDSA public-key address
kaspa:testnet-10:qxaqrlzlf6wes72en3568khahq66wf27tuhfxn5nytkd8tcep2c0vrse6gdmpks
```

Invalid:

```text
# Mainnet payload paired with testnet-10
kaspa:testnet-10:qp0l70zd5x85ttwd6jv7g3s3a8llzj96d8dncn4zmhv4tlzx5k2jyqh70xmfj

# Native prefix incorrectly retained inside account_address
kaspa:mainnet:kaspa:qp0l70zd5x85ttwd6jv7g3s3a8llzj96d8dncn4zmhv4tlzx5k2jyqh70xmfj

# Unsupported CAIP-2 reference
kaspa:testnet-11:qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqhqrxplya
```

## References

- [Address Implementation][] - Native prefixes, address versions, and payload lengths
- [Address Encoding][] - Base32 alphabet and prefix-dependent checksum
- [Rusty Kaspa][] - Kaspa full-node implementation and related SDK libraries

[Kaspa CAIP-2 Profile]: ./caip2.md
[Address Implementation]: https://github.com/kaspanet/rusty-kaspa/blob/78257f273a26c4be085bab0f79437dee99ca8835/crypto/addresses/src/lib.rs
[Address Encoding]: https://github.com/kaspanet/rusty-kaspa/blob/78257f273a26c4be085bab0f79437dee99ca8835/crypto/addresses/src/bech32.rs
[Rusty Kaspa]: https://github.com/kaspanet/rusty-kaspa
[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
