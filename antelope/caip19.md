---
namespace-identifier: antelope-caip19
title: Antelope Namespace - Asset Specification
author: ["Billy Rennekamp (@okwme)"]
discussions-to: https://github.com/0xcounting/FAR/issues/1
status: Draft
type: Standard
created: 2026-09-14
requires: ["CAIP-19", "CAIP-2"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Rationale

Antelope has no protocol-level token.
What every Antelope chain has instead is a *token contract*: an account that deploys the `eosio.token` ABI, keeps a `stat` table scoped by symbol code and an `accounts` table scoped by holder, and can issue any number of symbols.
The chain's own system token is one of these — on EOS it is the symbol `EOS` in the contract account `eosio.token`, on WAX the symbol `WAX` in `eosio.token`, on Telos the symbol `TLOS` in `eosio.token` — and the protocol privileges it only through which contract `eosio` happens to trust for staking and fees.

The consequence is the central fact this profile exists to encode: **a symbol code is not an identifier.**
On EOS mainnet today, the symbol `EOS` is issued by `eosio.token` and by at least five other contracts, including `iouiouiou123` (100,000,000.0000 EOS) and `eosiotokenis` (1,000,000 EOS, zero precision).
The symbol `USDT` is issued by `tethertether`, `bcres.net`, `issue.newdex` and `eosbtextoken`.
All of these are live, all return a valid `get_currency_stats` response, and a wallet that keys on symbol alone shows the holder the wrong balance.
An Antelope asset identifier must therefore carry the contract account and the symbol code together, and anything that drops the contract is not an identifier at all.

Both halves are, conveniently, already inside the [CAIP-19][] `asset_reference` charset.
Antelope account names are drawn from `a-z`, `1-5` and `.` only — digits `0` and `6`-`9` and every uppercase letter are unrepresentable in the name encoding — and symbol codes are one to seven characters of `A-Z`.
Nothing here needs percent-encoding, and no character of an Antelope asset identifier is ever escaped.

This profile was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a way to name 6 assets across the EOS, WAX and Telos chains.
The authors do not represent the Antelope ecosystem and offer this for its community to correct, adopt or replace.

## Syntax

After the [CAIP-2][] chain ID, a slash defines an `asset_namespace` and an `asset_reference`.

### Asset Namespaces

| Namespace | Description | Reference Format | `token_id` |
| :--- | :--- | :--- | :--- |
| `token` | A symbol issued by a token contract | `{contract_account}-{SYMBOL_CODE}` | never |
| `nft` | A non-fungible asset in an NFT contract | `{contract_account}-{collection}` | **required** |
| `slip44` | Alias for a chain's system token, where a coin type is registered | see the table below | never |

### Composition: contract first, hyphen, symbol

The reference is the contract account name, then a single `-`, then the symbol code.

The order is contract-then-symbol because the contract is the trust boundary and the symbol is scoped inside it.
Reading left to right narrows scope, which matches how every other [CAIP-19][] profile composes an issuer with a code, and it makes a simple string prefix (`eosio.token-`) select exactly the assets of one contract — the grouping an auditor actually wants, since compromise and rug-pull risk attach to the contract, not to the ticker.

The separator is `-` because it is the one delimiter that cannot occur in either half.
`-` is absent from the Antelope name charset (`.`, `1`-`5`, `a`-`z`) and from the symbol-code charset (`A`-`Z`), so a reference contains exactly one `-` and the split is unambiguous for any valid pair, with no escaping and no longest-match rule.
`.` would have been the obvious alternative and is wrong: account names contain dots (`eosio.token`, `bcres.net`, `wax.token`), so a dot-separated reference would need a parse-from-the-right rule that quietly breaks the first time someone reads it left to right.

A second, free check falls out of the charsets: the two halves have disjoint case.
Everything before the `-` is lowercase or a digit `1`-`5` or `.`, everything after it is uppercase.
An implementation can validate a reference without consulting the chain, and a mis-ordered `EOS-eosio.token` fails on inspection.

### Component Requirements

An Antelope **account name** is 1 to 13 characters from `.12345abcdefghijklmnopqrstuvwxyz`; the thirteenth character, where present, is further restricted by the name encoding.
It is case-sensitive only in the trivial sense that uppercase is not representable.

A **symbol code** is 1 to 7 characters of `A-Z`, uppercase, as carried in the `symbol_code` type.
It is the *code* only: an Antelope `symbol` is a precision-and-code pair written `4,EOS`, and the precision is **not** part of the identifier.
Precision is a property of the issuance, is recoverable from `get_currency_stats`, and including it would make the same asset addressable as both `…-EOS` and `…-4,EOS` while adding a `,` that the CAIP-19 charset does not permit.

A **collection** in an `nft` reference is an account-name-shaped identifier assigned by the NFT contract, subject to the same charset as an account name.

A **`token_id`** is the NFT contract's own asset identifier, a uint64 written in base 10 with no leading zeros.

### System tokens and `slip44`

Three of the chains in this namespace have a registered [SLIP-0044][] coin type:

| Chain | System token | SLIP-0044 line | Equivalent `token` reference |
| :--- | :--- | :--- | :--- |
| EOS | EOS | `\| 194 \| EOS \| EOS \|` | `token:eosio.token-EOS` |
| WAX | WAX | `\| 14001 \| WAX \| Worldwide Asset Exchange \|` | `token:eosio.token-WAX` |
| Telos | TLOS | `\| 977 \| TLOS \| Telos \|` | `token:eosio.token-TLOS` |

The `token` form is RECOMMENDED for every Antelope asset, the system token included, and is the form this profile treats as canonical.
Calling the system token "native" is a category error on Antelope: it is an ordinary contract token whose contract the system happens to trust, most Antelope chains (Libre, Ultra, Proton, UX, ORE, INSTAR) have no registered coin type at all, and a uniform rule is worth more than consistency with chains that do have a protocol-level unit.
A `slip44` reference MAY nonetheless be produced for the three chains above, and consumers SHOULD treat it as denoting the same asset as the `token` form on the same [CAIP-2][] chain.
This is the judgement call in this profile most likely to need an editor's or the community's correction.

## RegEx

```sh
asset_id:           asset_type | asset_type + "/" + token_id
asset_type:         chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:           "antelope:" + blockchain_id (as defined in [CAIP-2])

asset_namespace:    "token" | "nft" | "slip44"

asset_reference:    token_ref | nft_ref | slip44_ref
token_ref:          account_name + "-" + symbol_code
nft_ref:            account_name + "-" + account_name
slip44_ref:         "194" | "977" | "14001"

account_name:       [.1-5a-z]{1,13}
symbol_code:        [A-Z]{1,7}

token_id:           0|[1-9][0-9]{0,19}
```

A `token_ref` is at most 21 characters and an `nft_ref` at most 27, so the 128-character `asset_reference` ceiling is never approached.

## Semantics

### Fungible Tokens

A `token` asset type names the `(contract account, symbol code)` pair, which is exactly the key under which the chain stores the issuance: `eosio.token`'s `stat` table is scoped by the raw symbol code, so one contract holds at most one issuance per symbol code and the pair is unique on a given chain.

Resolution is a single read:

```bash
curl -s -X POST https://eos.greymass.com/v1/chain/get_currency_stats \
  -d '{"code":"eosio.token","symbol":"EOS"}'
# {"EOS":{"supply":"2100000000.0000 EOS","max_supply":"2100000000.0000 EOS","issuer":"eosio"}}
```

The `supply` string carries the precision, which is how a consumer recovers the decimal count that the identifier deliberately omits.
An empty `{}` response means the pair does not exist on that chain, which is the correct answer for a well-formed reference to a non-existent asset.

### Non-Fungible Tokens

Antelope NFTs are contract-defined, not protocol-defined; the dominant implementation is AtomicAssets, deployed at the account `atomicassets` on WAX and several other chains, with SimpleAssets and per-project contracts also in use.
An AtomicAssets asset belongs to exactly one immutable collection and carries a globally unique uint64 `asset_id`, which maps cleanly onto CAIP-19's asset-type/asset-ID split: the collection is the type, the `asset_id` is the token.

```
# "Quantum Chest", asset 1100001940716 of the planetdefnft collection on WAX
antelope:1064487b3cd1a897ce03ae5b6a865651/nft:atomicassets-planetdefnft/1100001940716
```

The `nft` namespace is deliberately contract-qualified for the same reason `token` is: `planetdefnft` is unique within `atomicassets`, not within the chain, and a second NFT contract may use the same collection name.
Consumers **MUST NOT** shorten an `nft` reference to the collection alone.

This is the least-exercised part of the profile — the FAR corpus contains no Antelope NFTs — and is offered for the AtomicAssets and SimpleAssets communities to correct.

## Examples

```sh
# EOS, the EOS mainnet system token, canonical form
antelope:aca376f206b8fc25a6ed44dbdc66547c/token:eosio.token-EOS

# The same asset, slip44 alias
antelope:aca376f206b8fc25a6ed44dbdc66547c/slip44:194

# Tether USDt on EOS, 4 decimals, issued by tethertether
antelope:aca376f206b8fc25a6ed44dbdc66547c/token:tethertether-USDT

# A DIFFERENT asset that also calls itself USDT, issued by bcres.net
antelope:aca376f206b8fc25a6ed44dbdc66547c/token:bcres.net-USDT

# WAX, the WAX mainnet system token
antelope:1064487b3cd1a897ce03ae5b6a865651/token:eosio.token-WAX

# TLOS, the Telos mainnet system token
antelope:4667b205c6838ef70ff7988f6e8257e8/token:eosio.token-TLOS

# AtomicAssets NFT 1100001940716, collection planetdefnft, on WAX
antelope:1064487b3cd1a897ce03ae5b6a865651/nft:atomicassets-planetdefnft/1100001940716
```

## Security Considerations

### Symbol collisions are real, live, and the reason for this profile

Every one of the following was returned by `get_currency_stats` on EOS mainnet while this document was written:

| Contract | Symbol | Supply |
| :--- | :--- | :--- |
| `eosio.token` | EOS | 2100000000.0000 EOS |
| `iouiouiou123` | EOS | 100000000.0000 EOS |
| `eosiotokenis` | EOS | 1000000 EOS (zero precision) |
| `tethertether` | USDT | 85251000.5000 USDT |
| `bcres.net` | USDT | 100000000.0000 USDT |

`eosiotokenis` is the sharpest case: it issues the symbol `EOS` with zero precision, so a consumer that matched on symbol and then applied the system token's precision of 4 would misreport every balance by four orders of magnitude, in addition to reporting a worthless token as the system token.
Producers **MUST** carry the contract account in every identifier and consumers **MUST NOT** fall back to symbol matching when a contract is missing.

### Name squatting is cheap, but `0` and `6`-`9` are not available

The name charset excludes `0` and `6`-`9`, so the classic `eosi0.token` homoglyph is simply not an encodable account name.
That is a small mercy and not a defence: `eosiotokenis` and `iouiouiou123` show that plausible-looking names remain trivially obtainable.
Implementations **SHOULD** treat the set of trusted contract accounts as an explicit allowlist rather than inferring trust from a name's resemblance to a known one.

### The account is the identity, not the code

An Antelope contract account's WASM and ABI can be replaced by a `setcode`/`setabi` transaction from whoever controls the account's `active` permission, and permissions themselves can be reassigned.
A `token` reference pins the account and symbol; it makes no claim about the code that will be running there tomorrow.
This differs from chains where an address commits to its bytecode, and consumers that cache token metadata **SHOULD** re-resolve it rather than treating it as immutable.

### Chain IDs are truncated

This namespace's [CAIP-2][] profile uses the first 32 characters of the 64-character chain ID, which is sufficient to identify a chain but **MUST NOT** be used where the full chain ID is required, notably for signing transactions.
A CAIP-19 identifier is for naming assets, not for authorising transfers of them.

## Backwards Compatibility

Antelope was called EOSIO until 2022 and the `eosio.token` contract interface it defines has been stable since the EOS mainnet launched in June 2018.
The identifiers defined here are constructed entirely from values the `get_currency_stats` and `get_table_by_scope` endpoints have always returned, and introduce no new encoding.

## References

- [Antelope documentation][] - platform documentation for the EOS, WAX, Telos and related chains
- [Antelope Chain API][] - `/v1/chain/get_currency_stats`, used to verify every fungible example here
- [eosio.token contract][] - the reference token contract, whose `stat` table is scoped by symbol code
- [Antelope name encoding][] - the base32 account-name encoding that fixes the `a-z`, `1-5`, `.` charset
- [AtomicAssets][] - the NFT standard used for the `nft` namespace examples
- [SLIP-0044][] - registered coin types, `194` (EOS), `977` (TLOS), `14001` (WAX)
- [CAIP-2][] - the Antelope chain ID profile in this namespace
- [CAIP-19][] - Asset Type and Asset ID Specification

[CAIP-2]: ./caip2.md
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[Antelope documentation]: https://docs.eosnetwork.com/
[Antelope Chain API]: https://docs.eosnetwork.com/apis/leap/latest/
[eosio.token contract]: https://github.com/AntelopeIO/reference-contracts/blob/main/contracts/eosio.token/src/eosio.token.cpp
[Antelope name encoding]: https://github.com/AntelopeIO/spring/blob/main/libraries/chain/name.cpp
[AtomicAssets]: https://github.com/pinknetworkx/atomicassets-contract

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
