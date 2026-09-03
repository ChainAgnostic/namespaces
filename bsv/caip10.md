---
namespace-identifier: bsv-caip10
title: BSV Blockchain - Account Identifiers
author: Deggen (@sirdeggen) <d.kellenschwiler@bsvassociation.org>
discussions-to: ["https://github.com/ChainAgnostic/namespaces/pull/202", "https://github.com/ChainAgnostic/namespaces/pull/190", "https://github.com/x402-foundation/x402/pull/2890"]
status: Draft
type: Standard
created: 2026-09-03
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

*For context, see the [CAIP-10][] specification.*

## Introduction

A BSV account in this namespace is a [BRC-100][] wallet **identity public key**,
not a Bitcoin address.

Each BRC-100 wallet has a master secp256k1 keypair.
The public half is the identity key: a 33-byte compressed point that applications
use to name the wallet as a counterparty (payments, encryption, certificates,
signatures).
It is the value returned by `getPublicKey({ identityKey: true })`.

That key is *not* an on-chain destination.
On-chain outputs pay [BRC-42][] child keys derived from it, and those children
are unlinkable to the identity by default.
Hashing the identity key into a P2PKH address and paying that address is not a
[BRC-29][] payment and is not how BRC-100 names an account.

This is the opposite of the assumptions encoded in the [bip122 CAIP-10][]
profile for BTC and related chains, and it is the reason this profile exists.

## Specification

### Semantics

The `account_address` segment of a [CAIP-10][] identifier in this namespace is
the wallet's identity public key, encoded as compressed secp256k1 hex
([BRC-100][] `PubKeyHex`).

The `chain_id` segment is a [CAIP-2][] identifier from the [CAIP-2 profile][]
of this namespace (`bsv:mainnet`, `bsv:testnet`, `bsv:ttn`, or `bsv:tstn`).
The same identity-key bytes on two networks are two different accounts:
the chain prefix is what binds the key to a network.

The identifier names the wallet, not a UTXO, not a locking script, and not a
derived child key.
A [BRC-42][] child public key is a compressed secp256k1 point of the same
shape, so syntactic validity does not prove that a given point is an identity
key.
By definition of this profile, a conformant `account_address` *is* an identity
key; consumers MUST NOT treat an arbitrary compressed pubkey recovered from a
P2PKH output as a CAIP-10 account.

### Syntax

```
account_id:        chain_id + ":" + account_address
chain_id:          See the [CAIP-2 profile][]
account_address:   compressed_pubkey
compressed_pubkey: ("02" | "03") + 32-byte-x-coordinate, hex
```

`account_address` is 66 hex characters.
The first byte is the compressed-point prefix: `02` if the y-coordinate is even,
`03` if it is odd.
There is no `0x` prefix.
Uncompressed points (`04` + 64-byte XY) are not valid.

A validating regular expression for the fully-qualified account ID, against the
networks registered in the [CAIP-2 profile][]:

```
bsv:(mainnet|testnet|ttn|tstn):0[23][0-9a-fA-F]{64}
```

This pattern is a structural check only.
Implementations SHOULD also verify that the 32-byte X-coordinate is a valid
secp256k1 point (the curve equation `y^2 = x^3 + 7 (mod p)` has a solution
whose y-parity matches the prefix).

#### Canonicalization

Hex MAY be mixed-case on the wire.
The canonical form is lowercase.
Comparison of `account_address` MUST be case-insensitive.

#### Explicitly not valid

The following MUST be rejected as `account_address` values in this namespace,
even when they are well-formed identifiers elsewhere:

- Base58 P2PKH or P2SH addresses (mainnet `1…` / `3…`, testnet `m…` / `n…` / `2…`).
  These are on-chain destinations, not BRC-100 identity keys.
  A P2PKH address derived from the identity key itself is still not the account.
- Native SegWit / Bech32 / Bech32m (`bc1…`, `tb1…`).
  BSV does not use SegWit or Taproot.
- Bitcoin Cash CashAddr (`q…` / `p…`, with or without a `bitcoincash:` prefix).
  BSV did not adopt CashAddr.
- Uncompressed secp256k1 public keys (`04` prefix).
- BIP32 extended public keys (`xpub` / `tpub`) and BIP44 derivation paths.
  BRC-100 does not use BIP32.
- [bip122][] CAIP-10 identifiers.
  A `bip122:` prefix names a different namespace; a genesis-only bip122 chain
  id is also ambiguous across BTC/BCH/BSV.

### Resolution Mechanics

Structural validation of the identifier does not require a node.

To bind an identifier to a live [BRC-100][] wallet:

1. Confirm `chain_id` against the [CAIP-2 profile][].
2. Ask the wallet for its network and identity key.
3. Accept the identifier only if both match.

```js
const { network } = await wallet.getNetwork({})
const { publicKey } = await wallet.getPublicKey({ identityKey: true })
```

`getNetwork()` returns `{ network: "mainnet" }` or `{ network: "testnet" }`
for the baseline networks (map `mainnet` → `bsv:mainnet`, `testnet` →
`bsv:testnet`).
Wallets operating on Teranode test networks SHOULD report `ttn` or `tstn` so
the CAIP-2 reference matches without translation, as specified in the
[CAIP-2 profile][].

`getPublicKey({ identityKey: true })` returns `{ publicKey }`, a 66-character
compressed hex string.
Compare it to `account_address` case-insensitively.

There is no JSON-RPC on a BSV node that lists this account.
Identity keys do not appear in transaction outputs.
An explorer lookup of the P2PKH address formed from `hash160(identityKey)`
answers a different question (who can spend outputs locked to that hash) and
MUST NOT be treated as confirmation of the CAIP-10 account.

On-chain payments to the wallet are [BRC-29][] outputs locked to [BRC-42][]
child keys.
Those outputs cannot be discovered from the identity key alone.
Proving that a specific output belongs to an identity is a voluntary
[BRC-69][] / [BRC-94][] key-linkage disclosure, not part of CAIP-10 resolution.

## Rationale

Cross-chain tooling that has implemented [bip122 CAIP-10][] will smuggle in
several assumptions that are false for BSV:

1. **Legacy P2PKH is "not a CAIP-10 address."**
   The bip122 profile excludes `1…` P2PKH as obsolete.
   On BSV, P2PKH is the ordinary locking script, including for [BRC-29][]
   payments.
2. **Accounts are SegWit or Taproot addresses.**
   BSV has neither.
   Bech32 strings are not BSV addresses.
3. **BCH CashAddr is how the fork names payees.**
   BSV kept Bitcoin's original Base58 P2PKH encoding, so a BSV P2PKH address
   is visually identical to a BTC P2PKH address.
   The CAIP-2 prefix is what distinguishes them; the address string alone
   cannot.
4. **BIP32/BIP44 HD paths name the account.**
   [BRC-100][] forbids BIP32.
   Counterparties are named by identity keys; per-payment destinations are
   [BRC-42][] ECDH children.

The BRC-100 identity key is the identifier BSV wallets already exchange:
`getPublicKey`, [BRC-29][] `senderIdentityKey`, [BRC-52][] certificate
subjects, and application-layer payment protocols such as x402 `payTo`.
Encoding that key as the CAIP-10 `account_address` maps the native account
onto [CAIP-10][] without a hash, a version byte, or a Base58 payload that
would collide with BTC.

This follows the [casper CAIP-10][] precedent of using a public key as the
account identifier rather than a hashed on-chain address.

### Backwards Compatibility

No prior CAIP or namespace assigns BSV account identifiers, so there are no
legacy forms to accept.
Tooling that wants to identify a raw on-chain P2PKH destination (an explorer
address, an exchange deposit account that is not a BRC-100 wallet) is outside
this profile.
Such destinations MUST NOT be written as `bsv:<network>:<base58-address>`.

## Test Cases

This is a list of manually composed examples.
The two identity keys are valid compressed secp256k1 points.

Valid:

```
# BSV mainnet, compressed identity key (y-odd, 03 prefix)
bsv:mainnet:036d239847413cdf9f15c0faad7c658bede087d3f601f2e2427d1f90ce84c0718a

# BSV mainnet, compressed identity key (y-even, 02 prefix)
bsv:mainnet:023e6e10f218052ca3266123303b9ba7caa2b85e0d29bc67fddf73d79c442c8056

# Same identity key on testnet is a different account
bsv:testnet:036d239847413cdf9f15c0faad7c658bede087d3f601f2e2427d1f90ce84c0718a

# Teranode Test Net
bsv:ttn:036d239847413cdf9f15c0faad7c658bede087d3f601f2e2427d1f90ce84c0718a

# Teranode Scaling Test Net
bsv:tstn:023e6e10f218052ca3266123303b9ba7caa2b85e0d29bc67fddf73d79c442c8056

# Mixed-case hex is accepted and canonicalizes to lowercase
bsv:mainnet:036D239847413CDF9F15C0FAAD7C658BEDE087D3F601F2E2427D1F90CE84C0718A
```

Invalid:

```
# P2PKH address of the first identity key — an on-chain destination, not the account
bsv:mainnet:175cFtPS7dYr39e1Bx6HXChGje2f9nG5gZ

# Well-known BTC/BSV-format P2PKH (Satoshi's genesis output)
bsv:mainnet:1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

# Native SegWit (not used on BSV)
bsv:mainnet:bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4

# Bitcoin Cash CashAddr
bsv:mainnet:qpm2qsznhks23z7629mms6s4cwef74vcwvy22gdx6a

# Uncompressed secp256k1 public key (04 prefix)
bsv:mainnet:046d239847413cdf9f15c0faad7c658bede087d3f601f2e2427d1f90ce84c0718a78c02f3a3a365ec626f30217879a94463e01d0ca1ade04007cc29e64aa5edb33

# Wrong compressed prefix
bsv:mainnet:016d239847413cdf9f15c0faad7c658bede087d3f601f2e2427d1f90ce84c0718a

# Truncated
bsv:mainnet:036d239847413cdf9f15c0faad7c658bede087d3f601f2e2427d1f90ce84c071
```

## Additional Considerations

A future profile could define identifiers for on-chain P2PKH destinations if
cross-chain tooling needs to name them distinctly from BRC-100 wallets.
That work is out of scope here: mixing Base58 addresses into `account_address`
would re-introduce the BTC visual collision this namespace exists to avoid.

Payment protocols that already take a BRC-100 identity key (for example x402
`exact` on BSV, whose `payTo` is this `account_address`) SHOULD treat a full
CAIP-10 identifier as `chain_id` plus that key, not as an address to hash.

## References

- [BRC-100][] - wallet-to-application interface; `PubKeyHex`, `getPublicKey`, `getNetwork`
- [BRC-42][] - ECDH child-key derivation used for per-payment destinations
- [BRC-29][] - P2PKH payment protocol whose `senderIdentityKey` is this account
- [BRC-52][] - identity certificates, which name subjects by identity key
- [BRC-69][] - voluntary key-linkage revelation (identity ↔ derived child)
- [BRC-94][] - Schnorr ZKP used to verify a BRC-69 linkage
- [CAIP-2 profile][] - network identifiers for this namespace
- [bip122 CAIP-10][] - Bitcoin-family address profile whose assumptions this document rejects
- [casper CAIP-10][] - public-key-as-account precedent
- [CAIP-10][] - account identifier specification
- [CAIP-2][] - chain identifier specification

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[CAIP-2 profile]: ./caip2.md
[BRC-100]: https://github.com/bitcoin-sv/BRCs/blob/master/wallet/0100.md
[BRC-42]: https://github.com/bitcoin-sv/BRCs/blob/master/key-derivation/0042.md
[BRC-29]: https://github.com/bitcoin-sv/BRCs/blob/master/payments/0029.md
[BRC-52]: https://github.com/bitcoin-sv/BRCs/blob/master/peer-to-peer/0052.md
[BRC-69]: https://github.com/bitcoin-sv/BRCs/blob/master/key-derivation/0069.md
[BRC-94]: https://github.com/bitcoin-sv/BRCs/blob/master/key-derivation/0094.md
[bip122]: https://namespaces.chainagnostic.org/bip122/README
[bip122 CAIP-10]: https://namespaces.chainagnostic.org/bip122/caip10
[casper CAIP-10]: https://namespaces.chainagnostic.org/casper/caip10

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
