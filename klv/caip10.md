---
namespace-identifier: klv-caip10
title: Klever Namespace - Addresses
author: Nicollas Gabriel da Silva (@nickgs1337)
discussions-to: https://forum.klever.org/, https://github.com/klever-io/klever-go/discussions
status: Draft
type: Standard
created: 2026-05-13
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

_For context, see the [CAIP-10][] specification._

## Rationale

The Klever address format is Bech32, specified by [BIP_0173][]. The
human-readable-part is `klv` with the universal separator `1`, so every
Klever address starts with `klv1`, e.g.:

```
klv1edd0ymfmv9r2mxk7mdtsk4zfeql5cp9vyn7t4y4adq58vp2r9alslfglw8
```

The Klever protocol defines the address of an account as the Bech32 encoding
of the public key of its corresponding ed25519 keypair (the secret key
remains known only to the user that owns the keypair). The raw address is 32
bytes; the resulting Bech32 string is 62 characters total (the `klv1` prefix
plus 58 base32-encoded data and checksum characters). The encode/decode
routine in the Klever node sets `fromBits = 8, toBits = 5, pad = true` (see
[`crypto/pubkeyConverter/bech32PubkeyConverter.go`][klever-pkc]).

Deployed smart contracts on Klever have their raw address prefixed by 8
zero bytes followed by 2 bytes of VM-type marker (10 prefix bytes total —
see [`core/address.go`][klever-addr], constants
`NumInitCharactersForScAddress = 10` and `VMTypeLen = 2`). In Bech32 form
those addresses always start with `klv1qqqqqqqqqqqq...`. Externally-owned
accounts and deployed smart contracts share the same CAIP-10 syntax.

## Syntax

```
caip10-like address:    namespace + ":" + chainId + ":" + address
namespace:              klv
chainId:                108 (Mainnet), 109 (Testnet), or 100001 (Devnet) — see CAIP-2
address:                Bech32-formatted Klever address (klv1...)
```

The address segment always fits within the `[-.%a-zA-Z0-9]{1,128}` envelope
mandated by [CAIP-10][].

## Test Cases

Live mainnet addresses from `https://api.mainnet.klever.org/v1.0`:

```
# Wallet address on Klever Mainnet
klv:108:klv1edd0ymfmv9r2mxk7mdtsk4zfeql5cp9vyn7t4y4adq58vp2r9alslfglw8
klv:108:klv16shscvyg2mrxex4zukdsn6rhqje52ekcw8s4kkx69k25jaky943s89u22d

# Deployed smart contract on Klever Mainnet (note klv1qqqqqqqqqqqq... prefix)
klv:108:klv1qqqqqqqqqqqqqpgqpg2ff85tljne96d2jwedj4mkrhsu3up5c0nq0x8g69

# Klever Testnet
klv:109:klv1elm4p3z6y66pgdezxcplwnmarwq5np3cvgwr32s335djpa3zqwus5f92gx
```

## References

- [Klever Wallet documentation][klever-wallet] — End-user surface for Klever
  addresses.
- [Klever Connect SDK][klever-connect] — TypeScript reference implementation
  of the address encode/decode flow.
- [klever-go node source][klever-go] — Reference implementation of the
  address layout, the Bech32 converter, and the smart-contract address
  prefix.
- [BIP_0173][] — Bech32 specification used for Klever addresses.

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[BIP_0173]: https://en.bitcoin.it/wiki/BIP_0173
[klever-wallet]: https://klever.org/wallet
[klever-connect]: https://github.com/klever-io/klever-connect
[klever-go]: https://github.com/klever-io/klever-go
[klever-pkc]: https://github.com/klever-io/klever-go/blob/develop/crypto/pubkeyConverter/bech32PubkeyConverter.go
[klever-addr]: https://github.com/klever-io/klever-go/blob/develop/core/address.go

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
