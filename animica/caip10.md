---
namespace-identifier: animica-caip10
title: Animica Namespace - Addresses
author: Animica (@animicaorg)
discussions-to: https://github.com/ChainAgnostic/namespaces/pulls
status: Draft
type: Standard
created: 2026-08-22
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Introduction

An Animica account is identified by a bech32m ([BIP-350][]) string with the human-readable part `anim`, for example `anim1zqpn54yt2fz07wg5zz33qplkh7tewv30tm5s9cdwvag6kf6myvd2d5sj9pzp7`.
The encoded payload carries the id of the signature scheme that controls the account followed by a SHA3-256 digest of the account's public key, so the address format does not depend on the size of the post-quantum public key itself.
An Animica CAIP-10 account id is the [CAIP-2][] chain id followed by a colon and the native address, unchanged.

## Specification

### Semantics

The native address encodes a 34-byte payload:

```text
payload = u16be(alg_id) || SHA3-256(pubkey)
```

- `alg_id` is the 16-bit big-endian identifier of the signature scheme that controls the account.
  User accounts use `0x1003`, ML-DSA-65 ([FIPS 204][]), which is the only scheme the network currently accepts signatures from.
  Contract accounts use `0x0000`; they are keyless and their digest is derived from the deploying transaction rather than from a public key.
  Validators accept `0x0000` or any value in `0x1000` through `0x1fff` so that contract, legacy, and future scheme ids remain addressable as transaction recipients.
- `SHA3-256(pubkey)` is the NIST SHA3-256 digest (not Keccak-256) of the raw 1,952-byte ML-DSA-65 public key.

The 32-byte digest is the account identity that transaction bodies carry; the `alg_id` prefix tells verifiers which scheme the accompanying signature must use.
Only the way `pubkey` is produced and signatures are verified depends on the post-quantum scheme; the address encoding is scheme-agnostic.

The same human-readable part `anim` is used on every Animica network.
The chain id portion of the CAIP-10 identifier is therefore the only thing that distinguishes an account on mainnet from the same account on a test network.

### Syntax

```text
account_id:      chain_id + ":" + account_address
chain_id:        "animica:" + reference          (see the Animica CAIP-2 profile)
account_address: "anim1" + data_chars + checksum_chars
data_chars:      55 characters from the bech32 alphabet (34 bytes re-grouped into 5-bit words)
checksum_chars:  6 characters from the bech32 alphabet (bech32m, constant 0x2bc830a3)
```

The native address is always exactly 66 characters long: the prefix `anim1`, 55 data characters, and 6 checksum characters.
Because the first 15 bits of the payload are the upper bits of `alg_id`, every ML-DSA-65 account address begins with `anim1zqp` and every contract address begins with `anim1qqq`.

Account identifiers MUST be lowercase.
BIP-350 permits an all-uppercase encoding of the same address, but it is not canonical in this namespace and MUST be lowercased before use as a CAIP-10 identifier; mixed-case strings are invalid under BIP-350 and MUST be rejected.

A validating regular expression for the native address:

```regex
^anim1[02-9ac-hj-np-z]{61}$
```

And for the fully-qualified account id:

```regex
^animica:(0|[1-9][0-9]{0,9}):anim1[02-9ac-hj-np-z]{61}$
```

A regular-expression match is necessary but not sufficient.
Implementations MUST decode the string with the bech32m checksum constant `0x2bc830a3` (a plain bech32 checksum MUST be rejected), check that the decoded payload is exactly 34 bytes, and check that the leading `alg_id` is `0x0000` or in the range `0x1000` through `0x1fff`.

### Resolution Mechanics

A valid address does not need to have been seen on chain; querying an address that has never transacted simply returns a zero balance.
To look up an account, call `state.getAccount` on an endpoint for the chain named in the identifier:

```jsonc
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "state.getAccount",
  "params": ["anim1zqpn54yt2fz07wg5zz33qplkh7tewv30tm5s9cdwvag6kf6myvd2d5sj9pzp7"]
}

// Response (from a mainnet node, 2026-08-22)
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "address": "anim1zqpn54yt2fz07wg5zz33qplkh7tewv30tm5s9cdwvag6kf6myvd2d5sj9pzp7",
    "balance": "0x0"
  }
}
```

Balances are hexadecimal quantities in nano-ANM (1 ANM = 10^9 nANM).
`state.getBalance` returns only the balance for the same input.
Node views of transactions report `from` and `to` as the bare 32-byte digest in hexadecimal; to reconstruct the native address, prepend the account's `alg_id` and re-encode with bech32m.

## Rationale

The native address already carries a checksum, a fixed length, and the signature-scheme id, and it is the form that Animica's node, explorer, wallets, and payment lane exchange.
Reusing it unchanged as the `account_address` keeps CAIP-10 identifiers copy-pasteable to and from every existing Animica interface.
Lowercase is required so that each account has exactly one CAIP-10 string and identifiers can be compared byte-for-byte.

### Backwards Compatibility

There was no previously registered CAIP-10 profile for Animica.
The address format described here is the one Animica has used since genesis, and this profile does not change it.

## Test Cases

The first three valid examples are the addresses derived from the BIP-39 reference mnemonic (`abandon` x 11, `about`) at the paths given, as published in the normative [HD Derivation][] document; they are real derived addresses and have zero balance on mainnet.

### Valid identifiers

```text
# Mainnet, ML-DSA-65 account at m/44'/4279885'/0'/0'/0'
animica:1:anim1zqpn54yt2fz07wg5zz33qplkh7tewv30tm5s9cdwvag6kf6myvd2d5sj9pzp7

# Mainnet, ML-DSA-65 account at m/44'/4279885'/0'/0'/1'
animica:1:anim1zqpmznku3ddgyhl27d0p38jq7qyjgsnvafzd8pwh27gednh0x09s2egxyv9ej

# Mainnet, ML-DSA-65 account at m/44'/4279885'/1'/0'/0'
animica:1:anim1zqpn2j43cqempqfke6rzvwf6f4529xwrexgpcw8gfd8dg8agmcqw6qqu83f7t

# Mainnet, contract-type address (alg_id 0x0000) with an all-zero digest; format illustration only
animica:1:anim1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq3cshhr
```

### Invalid identifiers

```text
# Mixed case (invalid under BIP-350)
animica:1:anim1ZQPN54YT2Fz07wg5zz33qplkh7tewv30tm5s9cdwvag6kf6myvd2d5sj9pzp7

# All-uppercase encoding of the first valid example (decodes under BIP-350 but is not canonical here)
animica:1:ANIM1ZQPN54YT2FZ07WG5ZZ33QPLKH7TEWV30TM5S9CDWVAG6KF6MYVD2D5SJ9PZP7

# Same payload as the first valid example, encoded with the plain bech32 checksum instead of bech32m
animica:1:anim1zqpn54yt2fz07wg5zz33qplkh7tewv30tm5s9cdwvag6kf6myvd2d5s8e3wyu

# Last character corrupted (bech32m checksum fails)
animica:1:anim1zqpn54yt2fz07wg5zz33qplkh7tewv30tm5s9cdwvag6kf6myvd2d5sj9pzpq

# Bare 32-byte digest in hexadecimal (the node's internal view, not an address)
animica:1:0x3a548b5244ff391410a31007f6bf9797322f5ee902e1ae6751ab275b231aa6d2

# Missing chain id
anim1zqpn54yt2fz07wg5zz33qplkh7tewv30tm5s9cdwvag6kf6myvd2d5sj9pzp7
```

## Security Considerations

A regular-expression match alone does not establish that an address is valid; implementations MUST verify the bech32m checksum, the 34-byte payload length, and the `alg_id` range.
A string that verifies only under the plain bech32 constant encodes the same payload but MUST be rejected, because the Animica node rejects it and accepting it would create two textual forms for one account.
Because the human-readable part does not encode the network, applications MUST take the network from the CAIP-2 portion of the identifier and MUST NOT infer it from the address.

## References

- [CAIP-2][] - Blockchain ID specification
- [CAIP-10][] - Account ID specification
- [Animica CAIP-2 Profile][CAIP-2 Profile] - Chain identifiers in this namespace
- [BIP-350][] - Bech32m format for native segwit version 1 outputs (the checksum used here)
- [FIPS 204][] - Module-Lattice-Based Digital Signature Standard (ML-DSA)
- [HD Derivation][] - Normative derivation and the address test vectors used above
- [Address Implementation][] - Reference address encoder/decoder in the Animica wallet extension
- [Node Address Implementation][] - Node-side Python address encoder/decoder
- [Public RPC][] - Public JSON-RPC 2.0 endpoint for mainnet
- [Explorer][] - Mainnet block explorer (`/address/{anim1...}`)

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[CAIP-2 Profile]: ./caip2.md
[BIP-350]: https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki
[FIPS 204]: https://csrc.nist.gov/pubs/fips/204/final
[HD Derivation]: https://github.com/animicaorg/all/blob/36f995f241cd3e54f66c7a5a6f373d4587bbc60d/docs/wallet/HD_DERIVATION.md
[Address Implementation]: https://github.com/animicaorg/all/blob/36f995f241cd3e54f66c7a5a6f373d4587bbc60d/apps/wallet-extension/src/core/crypto/address.ts
[Node Address Implementation]: https://github.com/animicaorg/all/blob/36f995f241cd3e54f66c7a5a6f373d4587bbc60d/pq/py/address.py
[Public RPC]: https://rpc.animica.org/rpc
[Explorer]: https://explorer.animica.org

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
