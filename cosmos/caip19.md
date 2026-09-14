---
namespace-identifier: cosmos-caip19
title: Cosmos Namespace - Asset Specification
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

The [Cosmos][] namespace defined in [cosmos-caip2][] covers a large family of sovereign chains that share the CometBFT consensus engine and, in most cases, the [Cosmos SDK][].
Unlike a single-chain namespace, `cosmos:` spans hundreds of independent ledgers, and an asset identifier here is only meaningful relative to the `chain_id` that precedes it.
This profile takes that scoping seriously: every construct below names an asset *as that one chain holds it*, and the profile deliberately declines to express relationships between chains that the chains themselves do not record.

Assets in this ecosystem are held in one of two fundamentally different places.
The [x/bank][] module is the SDK's only native fungible ledger, and everything it holds is keyed by a *denomination* — a plain string such as `uatom`, `ibc/27394FB0…`, `gamm/pool/1` or `factory/osmo1z0q…/wbtc`.
Everything else lives in contract state: [CosmWasm][] contracts implement the [CW20][] fungible and [CW721][] non-fungible interfaces, and [Secret Network][] runs an encrypted CosmWasm fork whose token standards are [SNIP-20][] and [SNIP-25][].

The hard part of writing this profile is the bank denomination charset.
The SDK validates denominations against `[a-zA-Z][a-zA-Z0-9/:._-]{2,127}` ([types/coin.go][sdk-coin-go]), which admits `/`, `:` and `_`.
None of those three characters is in the [CAIP-19][] `asset_reference` charset `[-.%a-zA-Z0-9]{1,128}`.
They are not rare: on `cosmos:osmosis-1` a sample of 2000 registered denominations taken on 2026-09-14 contained 1957 with at least one `/`, 14 with `_` and 7 with `:`.
Section [Percent-encoding of denominations][] defines the escape precisely; `%` is not itself a legal denomination character, so the encoding is unambiguously reversible.

This profile was drafted by the maintainers of FAR, an open cross-reference between CAIP-19, CoinGecko and ISO 24165 identifiers, which needs a way to name 299 assets on Cosmos chains.
The authors do not represent the Cosmos ecosystem and offer this for its community to correct, adopt or replace.

## Syntax

After the [CAIP-2][] namespace and chain reference, a slash defines an `asset_namespace` and an `asset_reference`.

### Asset Namespaces

| Namespace | Description | Reference format |
| :--- | :--- | :--- |
| `slip44` | Native coin identified by its registered [SLIP-0044][] coin type | decimal coin type |
| `bank` | Any [x/bank][] denomination not covered by `ics20` or `factory` | percent-encoded denomination |
| `ics20` | [ICS-20][] fungible-token-transfer voucher ("IBC denom") | 64 uppercase hex characters |
| `factory` | [Token Factory][] denomination | percent-encoded `creator/subdenom` |
| `cw20` | [CW20][] fungible contract token | contract address (bech32) |
| `cw721` | [CW721][] non-fungible contract token | contract address (bech32) |
| `snip20` | [SNIP-20][] / [SNIP-25][] confidential fungible token | contract address (bech32) |
| `snip721` | [SNIP-721][] confidential non-fungible token | contract address (bech32) |

`cw721` and `snip721` form `asset_id`s with a `token_id` suffix.
The other six are `asset_type`s only and take no `token_id`.

### Percent-encoding of denominations

A bank denomination is mapped to an `asset_reference` by replacing exactly three characters, and no others:

| Denomination character | Encoded as |
| :--- | :--- |
| `/` (U+002F) | `%2F` |
| `:` (U+003A) | `%3A` |
| `_` (U+005F) | `%5F` |

These are the complete set difference between the SDK denomination charset and the [CAIP-19][] `asset_reference` charset.
The hex digits MUST be uppercase, as recommended by [CAIP-19][] and [RFC 3986][] section 2.1.
No other octet is encoded; in particular `-` and `.` are legal in both charsets and MUST be left alone.
Because `%` is not a legal denomination character, a `%` appearing in a reference is always the start of an escape, and decoding is a single unambiguous pass.

A producer MUST NOT encode characters that do not require it, and MUST NOT emit lowercase escapes.
A consumer that receives `%2f`, or a redundant escape such as `%61` for `a`, SHOULD decode it but MUST NOT treat the result as a distinct asset from its canonical spelling.

### Selecting the namespace

A bank denomination maps to exactly one of `ics20`, `factory` or `bank`, decided in this order:

1. If the denomination matches `ibc/[0-9A-F]{64}`, the asset_namespace is `ics20` and the reference is the 64 hex characters with the literal `ibc/` prefix removed.
2. Otherwise, if the denomination matches `factory/<creator>/<subdenom>` where `<creator>` is a valid bech32 account address for that chain, the asset_namespace is `factory` and the reference is the percent-encoding of everything after the literal `factory/` prefix.
3. Otherwise, the asset_namespace is `bank` and the reference is the percent-encoding of the whole denomination.

Rule 1 and rule 2 strip a prefix that the `asset_namespace` already asserts, so no information is lost and the round-trip is a literal re-prepend.
Stripping is not cosmetic in case 2: see [Reference length][].

A producer MUST NOT express an `ibc/` or `factory/` denomination under `bank`.
`bank:ibc%2F27394FB0…` is syntactically well-formed and semantically wrong, and a consumer that accepts it MUST canonicalise it to the `ics20` form before comparison.

### Per-component requirements

**`slip44`** — a decimal coin type registered in [SLIP-0044][], with no leading zeros.
Its use is narrowly constrained; see [Coin type 118 is not a chain][].

**`ics20`** — the 64-character uppercase hexadecimal SHA-256 defined in [ADR-001][] and computed by [ibc-go][ibc-go-denom] as `sha256(trace + "/" + base_denom)`.
The hash MUST be uppercase, because the bank denomination itself is uppercase and bank state is byte-compared.
A query endpoint may accept a lowercase hash, but a lowercase `asset_reference` will not round-trip to a denomination the chain recognises.

**`factory`** — the percent-encoding of `<creator>/<subdenom>`.
The creator is a bech32 account address and by construction contains no `/` ([Osmosis x/tokenfactory][tokenfactory-denoms]).
The subdenom is at most 44 bytes and MAY itself contain `/`, so the decoded reference has two or more segments.

**`bank`** — the percent-encoding of the full denomination, which MUST satisfy `[a-zA-Z][a-zA-Z0-9/:._-]{2,127}` after decoding.

**`cw20`, `cw721`, `snip20`, `snip721`** — a bech32 contract address as emitted by the chain, in lowercase, including its human-readable prefix.
The address MUST NOT be percent-encoded; the bech32 charset is already a subset of the `asset_reference` charset.

**`token_id`** — the contract's own token identifier, percent-encoded by the same rule where it contains `/`, `:` or `_`.
See [Token identifiers are unbounded strings][] for the cases this cannot express.

## RegEx

The RegEx validation strings are as follows:

```sh
asset_id:          asset_type + "/" + token_id
asset_type:        chain_id + "/" + asset_namespace + ":" + asset_reference
chain_id:          "cosmos:" + reference (as defined in [CAIP-2] and [cosmos-caip2])

asset_namespace:   "slip44" | "bank" | "ics20" | "factory"
                 | "cw20" | "cw721" | "snip20" | "snip721"

asset_reference:   slip44_ref | bank_ref | ics20_ref | factory_ref | bech32_ref

slip44_ref:        0|[1-9][0-9]{0,9}
ics20_ref:         [0-9A-F]{64}
factory_ref:       bech32_ref + "%2F" + pct_seq
bank_ref:          pct_head + pct_seq
bech32_ref:        [a-z][a-z0-9]{1,15}1[02-9ac-hj-np-z]{38,58}

pct_head:          [a-zA-Z]
pct_seq:           ([a-zA-Z0-9.-]|%2F|%3A|%5F){2,}

token_id:          [-.%a-zA-Z0-9]{1,78}
```

Two constraints are not expressible in the grammar and MUST be checked separately.

The `asset_reference` MUST be at most 128 characters *after* encoding, per [CAIP-19][].
The decoded `bank_ref` or `factory_ref` (with `factory/` re-prepended) MUST match the SDK denomination regex `[a-zA-Z][a-zA-Z0-9/:._-]{2,127}`.

`bech32_ref` is written for the 20-byte (38 data characters) and 32-byte (58 data characters) addresses that Cosmos SDK chains emit today; the bech32 character class excludes `1`, `b`, `i` and `o`.
A consumer MUST accept any length its chain actually produces rather than treating the bound as normative.

## Semantics

### Native and staking denominations

A Cosmos chain's native unit has no special status in state: it is an ordinary [x/bank][] denomination that the staking, fee and mint modules happen to reference.
It is conventionally the base unit rather than the display unit, and conventionally carries an SI-style prefix — `u` for 10⁻⁶ (`uatom`, `uosmo`, `uinit`, `utia`), `a` for 10⁻¹⁸ (`aarch`) — but nothing enforces this and some chains use the bare ticker (`inj`).
The exponent is advisory metadata published by `/cosmos/bank/v1beta1/denoms_metadata`, and many chains publish none at all; `aarch` on `cosmos:archway-1` has a live supply but returns `client metadata for denom aarch` when queried for metadata.

The canonical identifier for a native unit in this profile is therefore its bank denomination:

```
cosmos:osmosis-1/bank:uosmo
cosmos:archway-1/bank:aarch
cosmos:interwoven-1/bank:uinit
```

### Coin type 118 is not a chain

[SLIP-0044][] registers coin type `118` as `ATOM`, "Atom" ([slip-0044.md line 151][slip44-118]).
[CAIP-20][] makes `slip44:118` a portable name for that asset, and on the Cosmos Hub it is unambiguous:

```
cosmos:cosmoshub-4/slip44:118
```

It is not unambiguous anywhere else, and the reason is a genuine ecosystem-wide overload.
The [Cosmos chain registry][chain-registry] declares `slip44: 118` for the large majority of chains — Osmosis, Juno, Celestia, Archway, Neutron and Stargaze all do — because that field governs BIP-44 key derivation, not asset identity.
A reader of `cosmos:osmosis-1/slip44:118` cannot tell whether it was written to mean OSMO (the native unit of a chain that derives at 118) or ATOM (the asset SLIP-0044 registers at 118) as held on Osmosis, which is a different asset with a different identifier.

This profile resolves the ambiguity by restriction rather than by convention.
`slip44` MAY be used only where [SLIP-0044][] registers the coin type against that chain's *own* native ticker, and MUST NOT be used otherwise.
`cosmos:cosmoshub-4/slip44:118` and `cosmos:secret-4/slip44:529` are permitted; `cosmos:osmosis-1/slip44:118` and `cosmos:juno-1/slip44:118` are not.
Note that SLIP-0044 separately registers `10000118` for OSMO while the chain registry declares Osmosis at `118`, so even the permitted form inherits a registry disagreement; `bank:` is RECOMMENDED for every native unit, including ATOM, and consumers MUST treat `cosmos:cosmoshub-4/slip44:118` and `cosmos:cosmoshub-4/bank:uatom` as the same asset.

### ICS-20 vouchers, and why their references are chain-relative

This is the most consequential property of the namespace, and it is worth stating before the mechanics.

When a token moves over [IBC][], the receiving chain does not mint "the same token".
It mints a *voucher*: a fresh bank denomination whose name is the SHA-256 of the full path the token travelled, expressed as `ibc/<HASH>` where `HASH = uppercase_hex(sha256(trace + "/" + base_denom))` ([ADR-001][], [ibc-go/modules/apps/transfer/types/denom.go][ibc-go-denom]).
The trace is a sequence of `port/channel` hops, and **channel identifiers are allocated locally and sequentially by each chain**.
`channel-0` on Osmosis and `channel-0` on Juno are unrelated objects that happen to share a name.

The consequence is that the hash is a name in one chain's local namespace and nowhere else.
ATOM as held on Osmosis arrived over `transfer/channel-0`, so it is:

```
cosmos:osmosis-1/ics20:27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2
```

The identical economic asset on any other chain carries a different reference, because it arrived over a different channel number, and the reference above is meaningless on any other chain.
Queried against Celestia, that same hash returns `denomination trace not found`.
An implementer must therefore read `cosmos:<chain>/ics20:<hash>` as "the voucher this chain stores under this hash", never as "this asset, on this chain".

**Within one chain, a single base denomination can have many vouchers.**
On `cosmos:celestia` the native denomination is `utia`, and there are additionally at least three distinct bank denominations whose resolved `base_denom` is also `utia` — TIA that left Celestia and returned over `transfer/channel-279`, over `transfer/channel-395`, and over the three-hop path `transfer/channel-2/transfer/channel-122/transfer/channel-152`.
Those are four separate balances that are not fungible with one another in `x/bank`, and each gets its own identifier.
`base_denom` alone identifies nothing.

**The profile cannot express the relationship, and does not pretend to.**
There is no derivation from `cosmos:osmosis-1/ics20:27394FB0…` to `cosmos:cosmoshub-4/bank:uatom`, and this profile defines none.
Three separate obstacles stand in the way, and only the first is solvable offline:

1. The trace is not recoverable from the hash; SHA-256 is one-way, so recovering `transfer/channel-0/uatom` requires querying the chain that holds the voucher.
2. The counterparty `chain_id` is not recoverable from a channel identifier either; it requires a second query walking channel → connection → client to read the client state's chain ID, and that client can be superseded.
3. Unwinding is not uniquely defined even with both, because an asset may reach a chain over several paths simultaneously, packet-forward middleware may collapse some hops and not others, and a chain that undergoes the `chain_id`-changing reboot described in [cosmos-caip2][] keeps the vouchers while changing the identity of the chain that holds them.

A registry that needs equivalence classes — "these seventeen identifiers are all ATOM" — MUST carry them as separate, explicitly-curated metadata alongside the identifiers.
Encoding the claim inside the identifier would assert something neither chain records.

It is worth noting that the ecosystem reached the same conclusion.
Osmosis "alloyed assets" make several bridged variants of one asset mutually redeemable by minting a *new* Token Factory denomination backed by a transmuter pool, for example `factory/osmo1z6r6qdknhgsc0zeracktgpcxf43j6sekq07nw8sxduc9lg0qjjlqfu25e3/alloyed/allBTC`.
The equivalence is expressed as a new asset with its own identifier, not as a relation between existing ones.

### Token Factory denominations

`x/tokenfactory` lets any account mint a permissionless bank denomination of the form `factory/<creator>/<subdenom>` ([Osmosis x/tokenfactory][tokenfactory-denoms]).
The creator is a bech32 address — a 20-byte account or a 32-byte contract address, both occur — and the subdenom is at most 44 bytes chosen freely by the creator.
Subdenoms routinely contain `/` themselves (`alloyed/allBTC`, `transmuter/poolshare`), `.` (`Bitcoin-runes-DOG.GO.TO.THE.MOON`), `_` and `:`, so a factory denomination can have four or more slash-separated segments.

The `factory` namespace exists rather than folding these into `bank` for two reasons.
It makes the creator machine-extractable without re-implementing the module's parsing rules, and it removes ten characters of encoded prefix, which real denominations need (see below).

### Reference length

The SDK caps a denomination at 128 characters, which is coincidentally the `asset_reference` cap — but percent-encoding expands, so the caps do not line up.

Of 2000 denominations sampled from `cosmos:osmosis-1` on 2026-09-14, seven encode to 130 characters if the `factory/` prefix is retained, and so could not be expressed at all.
The longest is 116 raw characters and contains two `_`, one `:` and four `/`:

```
factory/osmo1t07v4996zca9cxh6f498xnjcdfjvrune67fnsf4fsthzx9lrrktqnlpuv6/VT_4T2/osmosis/picasso-pica_osmosis-osmo:con
```

Stripping the prefix brings every sampled denomination inside the limit, with the longest encoded reference at 120 characters.
That is a measurement, not a proof.
A worst-case legal denomination — a 75-character creator with a 44-character slash-dense subdenom — would encode to well over 128 characters even after stripping.

An implementation that encounters a denomination it cannot encode within 128 characters MUST reject it and report the failure.
It MUST NOT truncate, re-hash or otherwise substitute a shortened reference, because a truncated reference is a valid-looking identifier for the wrong asset.

### Module-minted and other bank denominations

Several modules mint bank denominations that are neither IBC vouchers nor Token Factory tokens, and the `bank` namespace is the fallback that catches them all.
Osmosis GAMM liquidity-pool shares are `gamm/pool/<id>`.
Initia's MoveVM assets are `move/<64 lowercase hex>`.
Evmos-lineage `x/erc20` registrations produce denominations such as `erc20/tether/usdt`.
All of them percent-encode cleanly and none of them needs a bespoke namespace:

```
cosmos:osmosis-1/bank:gamm%2Fpool%2F1
cosmos:interwoven-1/bank:move%2F06fe99f11021425b7c28e5b8cb99ed1966ce79f0ed439f7a551120b661caeb29
```

### CW20 fungible contract tokens

[CW20][] tokens are not bank denominations.
They are balances inside a [CosmWasm][] contract, addressed by that contract's bech32 address, and a chain can carry both CW20 tokens and bank denominations with no relationship between them.
Metadata is read with a `{"token_info":{}}` smart query.

```
cosmos:juno-1/cw20:juno168ctmpyppk90d34p3jjy658zf5a5l3w8wk35wht6ccqj4mr0yv8s4j5awr
```

A CW20 token sent over IBC by the `cw20-ics20` contract appears on the receiving chain as an ordinary `ics20` voucher whose `base_denom` is the string `cw20:<address>`, which is why `:` appears in real denominations.
The two identifiers name different things — a contract balance on the origin chain and a bank balance on the destination — and, as with every IBC case, the profile does not relate them.

### CW721 non-fungible tokens

[CW721][] is the CosmWasm analogue of ERC-721.
The contract address is the `asset_type`; appending a `token_id` yields the `asset_id` for one token.
Unlike ERC-721, `token_id` is an arbitrary `String` chosen by the contract, not a `uint256`.
Both small integers and content identifiers are common in the wild.

[ICS-721][] interchain NFT transfer creates a CW721 voucher contract on the destination chain wrapping a foreign class.
Syntactically that is just another `cw721` address; semantically it inherits the whole of the chain-relativity problem described above, one level up, and this profile defines no way to relate a voucher class to its origin class.

[CW1155][] exists but has negligible deployment and is left for a future revision.

### Secret Network SNIP-20 and SNIP-721

[Secret Network][] (`cosmos:secret-4`) runs CosmWasm inside a trusted execution environment.
Contract *state* is encrypted, and so are the inputs and outputs of smart queries and executions.
The `snip20` and `snip721` namespaces exist because the standards genuinely differ from CW20 and CW721 — different message schemas, plus viewing keys and query permits — and because the identifier should signal that the asset is not publicly readable.

What is observable without a viewing key is exactly the chain-level metadata every CosmWasm contract exposes: the address, its `code_id`, creator, admin and label.
Querying `secret1k0jntykt7e4g3y88ltc60czgjuqdy4c9e8fzek` returns `code_id 2280`, label `sscrt`, and nothing about the token.

What is **not** observable to a third party: any balance, the holder set, transfer history and amounts, and — for contracts that have not opted into [SNIP-25][] public metadata — the token's own name, symbol, decimals and total supply.
An indexer cannot enumerate holders, cannot reconstruct supply, and cannot in general confirm from the chain alone that a given address implements SNIP-20 rather than some other interface; the reliable signal is the `code_id`, which identifies the uploaded WASM.

On `cosmos:secret-4` a fungible token contract MUST be named with `snip20` and MUST NOT be named with `cw20`, so that the two namespaces stay disjoint and the confidentiality signal is not lost.

```
cosmos:secret-4/snip20:secret1k0jntykt7e4g3y88ltc60czgjuqdy4c9e8fzek
```

No `snip721` example is given in this draft, and the reason is the point of the section.
The authors could not verify a candidate collection address against public chain state, because the interface a Secret contract implements is not observable without either a viewing key or independent knowledge of the `code_id`.
A `snip721` example should be contributed by someone holding that knowledge rather than inferred.

### Resolution

A `bank`, `ics20` or `factory` reference is resolved by decoding it to a denomination and querying the chain's x/bank module, for example `/cosmos/bank/v1beta1/supply/by_denom?denom=<denom>` or `/cosmos/bank/v1beta1/denoms_metadata/<denom>`.

An `ics20` reference is additionally resolved to its trace with `/ibc/apps/transfer/v1/denom_traces/<HASH>`, which returns the `path` and `base_denom`.
In `ibc-go` v9 and later this type is renamed and the endpoint becomes `/ibc/apps/transfer/v1/denoms/<HASH>`; nodes serving either path return the same information, and the `asset_reference` is unaffected by the rename.

`cw20`, `cw721`, `snip20` and `snip721` references are resolved with `/cosmwasm/wasm/v1/contract/<address>` for chain-level metadata, and with a base64-encoded smart query at `/cosmwasm/wasm/v1/contract/<address>/smart/<query>` for interface metadata.
On Secret the smart query is encrypted and the equivalent chain-level endpoint is `/compute/v1beta1/info/<address>`.

## Examples

Every identifier below was resolved against a live endpoint on 2026-09-14; the query that produced it is shown.

```sh
# Native ATOM on the Cosmos Hub, by coin type and by denomination
# SLIP-0044 line 151: | 118 | ATOM | Atom |
cosmos:cosmoshub-4/slip44:118
cosmos:cosmoshub-4/bank:uatom

# Native OSMO on Osmosis
# GET https://lcd.osmosis.zone/cosmos/bank/v1beta1/denoms_metadata/uosmo
#  -> {"base":"uosmo","display":"osmo","denom_units":[{"denom":"uosmo","exponent":0},
#                                                     {"denom":"osmo","exponent":6}]}
cosmos:osmosis-1/bank:uosmo

# Native ARCH on Archway (18 decimals, no published metadata)
# GET https://api.mainnet.archway.io/cosmos/bank/v1beta1/supply/by_denom?denom=aarch
#  -> {"denom":"aarch","amount":"1177249308905843727564334902"}
cosmos:archway-1/bank:aarch

# Native INIT on Initia
# GET https://rest.initia.xyz/cosmos/bank/v1beta1/supply/by_denom?denom=uinit
#  -> {"denom":"uinit","amount":"1000000000000000"}
cosmos:interwoven-1/bank:uinit

# ATOM as held on Osmosis -- the flagship ICS-20 voucher
# GET https://lcd.osmosis.zone/ibc/apps/transfer/v1/denom_traces/27394FB0...5EB2
#  -> {"denom_trace":{"path":"transfer/channel-0","base_denom":"uatom"}}
# and sha256("transfer/channel-0/uatom")
#  =  27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2
cosmos:osmosis-1/ics20:27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2

# TIA as held on Osmosis, over a different channel
#  -> {"denom_trace":{"path":"transfer/channel-6994","base_denom":"utia"}}
cosmos:osmosis-1/ics20:D79E7D83AB399BFFF93433E54FAA480C191248FC556924A2A8351AE2638B3877

# TIA that left Celestia and came back -- three of many, all base_denom "utia",
# none of them fungible with cosmos:celestia/bank:utia
# GET https://celestia-rest.publicnode.com/ibc/apps/transfer/v1/denom_traces/<hash>
cosmos:celestia/bank:utia
cosmos:celestia/ics20:93E113CD8DF31891647AE56271673AEFA7E125A686AEC6CAD8D5106FE9600892  # transfer/channel-279
cosmos:celestia/ics20:9AA817383E011194E56352F01273E0A0004B2681B7BCC68A3A8E5C350A8831B4  # transfer/channel-395
cosmos:celestia/ics20:A7CA7C8986D88CAC9D6D1F4D65EA6F45D2C5B2A22789A967509781B83FD2942A  # transfer/channel-2/transfer/channel-122/transfer/channel-152

# WBTC on Osmosis -- a Token Factory denomination
# GET https://lcd.osmosis.zone/cosmos/bank/v1beta1/supply/by_denom
#     ?denom=factory/osmo1z0qrq605sjgcqpylfl4aa6s90x738j7m58wyatt0tdzflg2ha26q67k743/wbtc
#  -> {"amount":"8595526778"}
cosmos:osmosis-1/factory:osmo1z0qrq605sjgcqpylfl4aa6s90x738j7m58wyatt0tdzflg2ha26q67k743%2Fwbtc

# allBTC on Osmosis -- a subdenom that itself contains a slash
#  -> {"amount":"11057094432"}
cosmos:osmosis-1/factory:osmo1z6r6qdknhgsc0zeracktgpcxf43j6sekq07nw8sxduc9lg0qjjlqfu25e3%2Falloyed%2FallBTC

# The longest sampled Osmosis denomination, exercising %2F, %5F and %3A at once.
# Raw 116 chars; 130 encoded with the "factory/" prefix (over the limit), 120 without.
cosmos:osmosis-1/factory:osmo1t07v4996zca9cxh6f498xnjcdfjvrune67fnsf4fsthzx9lrrktqnlpuv6%2FVT%5F4T2%2Fosmosis%2Fpicasso-pica%5Fosmosis-osmo%3Acon

# Osmosis GAMM pool-1 share, a module-minted denomination with slashes
# GET .../supply/by_denom?denom=gamm/pool/1 -> {"amount":"35170433777319927825802400"}
cosmos:osmosis-1/bank:gamm%2Fpool%2F1

# An Initia MoveVM asset
# GET https://rest.initia.xyz/cosmos/bank/v1beta1/supply -> {"denom":"move/06fe...eb29","amount":"10100000"}
cosmos:interwoven-1/bank:move%2F06fe99f11021425b7c28e5b8cb99ed1966ce79f0ed439f7a551120b661caeb29

# NETA, a CW20 contract on Juno
# GET https://juno-rest.publicnode.com/cosmwasm/wasm/v1/contract/<addr>/smart/eyJ0b2tlbl9pbmZvIjp7fX0=
#  -> {"name":"NETA","symbol":"NETA","decimals":6,"total_supply":"31886600000"}
cosmos:juno-1/cw20:juno168ctmpyppk90d34p3jjy658zf5a5l3w8wk35wht6ccqj4mr0yv8s4j5awr

# That same CW20, as an ICS-20 voucher on Secret -- base_denom is "cw20:<address>",
# which is where the ":" in real denominations comes from
#  -> {"denom_trace":{"path":"transfer/channel-33",
#                     "base_denom":"cw20:juno19rqljkh95gh40s7qdx40ksx3zq5tm4qsmsrdz9smw668x9zdr3lqtg33mf"}}
cosmos:secret-4/ics20:081CD0D6115E5850FBCF3D58B5E650A66D4A504A349116274872E638DA9BB24D

# A Token Factory denomination that has itself travelled over IBC:
# the base_denom contains slashes, and the trace/base boundary is a parsing heuristic
#  -> {"denom_trace":{"path":"transfer/channel-1",
#                     "base_denom":"factory/osmo1g8qypve6l95xmhgc0fddaecerffymsl7kn9muw/squosmo"}}
cosmos:secret-4/ics20:03FB4E4D1043755015ABF1A84773EA334B2726EF464CF90D926C888ECE2D64FD

# A CW721 collection on Juno, and one token in it (asset_type then asset_id)
# {"contract_info":{}} -> {"name":"All Time High","symbol":"ATH"}
# {"all_tokens":{"limit":5}} -> {"tokens":["QmZn7u8n3jqaxiYbs9QtiEzUy5FGMqUuMRCzbbTtzobUkN"]}
cosmos:juno-1/cw721:juno1qg5ega6dykkxc307y25pecuufrjkxkagxar70q
cosmos:juno-1/cw721:juno1qg5ega6dykkxc307y25pecuufrjkxkagxar70q/QmZn7u8n3jqaxiYbs9QtiEzUy5FGMqUuMRCzbbTtzobUkN

# A CW721 with integer token ids
# {"all_tokens":{"limit":5}} -> {"tokens":["0","1"]}
cosmos:juno-1/cw721:juno1kqpaj0n2cyleckhv6lj7858g4akefaw7phjzy8c8wauklu6pfylsmmlvtz/0

# sSCRT, a SNIP-20 on Secret Network
# GET https://rest.lavenderfive.com/secretnetwork/compute/v1beta1/info/secret1k0j...fzek
#  -> {"contract_info":{"code_id":"2280","label":"sscrt", ...}}   (no token data is public)
cosmos:secret-4/snip20:secret1k0jntykt7e4g3y88ltc60czgjuqdy4c9e8fzek
```

Round-trip of the three escapes, in full:

```sh
denomination:      factory/osmo1t07v4996zca9cxh6f498xnjcdfjvrune67fnsf4fsthzx9lrrktqnlpuv6/VT_4T2/osmosis/picasso-pica_osmosis-osmo:con
strip prefix:      osmo1t07v4996zca9cxh6f498xnjcdfjvrune67fnsf4fsthzx9lrrktqnlpuv6/VT_4T2/osmosis/picasso-pica_osmosis-osmo:con
encode / : _ :     osmo1t07v4996zca9cxh6f498xnjcdfjvrune67fnsf4fsthzx9lrrktqnlpuv6%2FVT%5F4T2%2Fosmosis%2Fpicasso-pica%5Fosmosis-osmo%3Acon
decode:            osmo1t07v4996zca9cxh6f498xnjcdfjvrune67fnsf4fsthzx9lrrktqnlpuv6/VT_4T2/osmosis/picasso-pica_osmosis-osmo:con
re-prepend:        factory/osmo1t07v4996zca9cxh6f498xnjcdfjvrune67fnsf4fsthzx9lrrktqnlpuv6/VT_4T2/osmosis/picasso-pica_osmosis-osmo:con
```

## Collisions and Security Considerations

### The same reference under two chain_ids is not the same asset

An `ics20` reference is a hash over locally-allocated channel identifiers, so it is a name in one chain's namespace only.
`cosmos:osmosis-1/ics20:27394FB0…5EB2` is ATOM; the same 64 characters under `cosmos:celestia` resolve to nothing at all.
It would be entirely possible for two chains to mint vouchers that collide on hash while representing different assets, because both chains number their channels from zero and neither is aware of the other's numbering.
Software that caches asset metadata MUST key the cache on the full `asset_type`, never on the `asset_reference` alone.
A user interface that shows a truncated hash without the `chain_id` is displaying an ambiguous identifier.

### The same asset under two chain_ids has unrelated references

The converse is the harder operational problem: nothing in `cosmos:osmosis-1/ics20:27394FB0…` connects it to `cosmos:cosmoshub-4/bank:uatom`, and this profile deliberately defines no connection.
Portfolio, accounting and tax software that treats CAIP-19 identifiers as an equivalence key will report the same holding as several unrelated assets, or silently merge assets that are not fungible.
Equivalence MUST come from curated metadata, and that metadata is a claim about economics, not a fact derivable from the identifier.

### A chain's own native asset can also arrive as a voucher

The `bank` and `ics20` namespaces can name what a user would call one asset on one chain.
On `cosmos:celestia`, `bank:utia` and the three `ics20` references listed in the Examples are four separate, non-fungible bank balances.
Merging them because `base_denom` matches would overstate a balance; they are only redeemable for one another by sending them back out over IBC.

### The trace/base_denom boundary is a heuristic, not a delimiter

ICS-20 concatenates the trace and the base denomination with `/` and provides no delimiter, while base denominations legitimately contain `/` — `factory/osmo1g8q…/squosmo` and `erc20/tether/usdt` are both live.
`ibc-go` recovers the split by consuming `port/channel` pairs while the second element parses as a valid channel or client identifier ([ExtractDenomFromPath][ibc-go-denom]), and its own source notes that "if an intermediate hop prefixes the full denom with a channel identifier format different from our own, the base denomination will be incorrectly parsed".
A chain whose base denomination begins with something that looks like `transfer/channel-N` would be mis-split.
The `asset_reference` is unaffected — the hash is computed over the whole string either way — but anything a consumer infers *from* a trace inherits the ambiguity, which is a further reason not to build equivalence on it.

### `slip44:118` is overloaded

Discussed above; the restriction in [Coin type 118 is not a chain][] exists precisely to make this collision unrepresentable rather than merely discouraged.
Implementers consuming CAIP-19 identifiers written before this profile should expect to find `cosmos:<any chain>/slip44:118` in the wild and should resolve it against the chain's native denomination rather than against SLIP-0044.

### Aliasing between namespaces

Without the ordered rule in [Selecting the namespace][], one denomination could be written three ways — `ics20:2739…`, `bank:ibc%2F2739…`, or with redundant percent-escapes — and string equality would fail on identical assets.
Producers MUST emit the canonical form; consumers SHOULD canonicalise before comparing, and MUST NOT treat differing spellings of one denomination as distinct assets.
The same applies to `cw20` versus `snip20` on `cosmos:secret-4`.

### References that cannot be encoded

Seven live Osmosis denominations exceed the 128-character `asset_reference` limit if the `factory/` prefix is retained, and the worst legal case exceeds it even without.
Truncation produces a well-formed identifier for a different asset, and re-hashing produces one this profile cannot resolve.
Implementations MUST fail loudly instead.

### Token identifiers are unbounded strings

`cw721-base` types `token_id` as a `String` with no length or charset constraint, while [CAIP-19][] caps `token_id` at 78 characters.
A contract may mint token ids containing spaces, `#`, or non-ASCII characters; percent-encoding can express the bytes, but a long identifier will exceed 78 characters once encoded, and such tokens cannot be named by this profile.
This is a real gap, not a theoretical one, and the same rule applies: reject rather than truncate.

### Case sensitivity

`ics20` references are uppercase hex and bech32 addresses are lowercase; both are byte-compared against chain state, and changing case produces an identifier the chain does not recognise.
Bech32's charset omits `1`, `b`, `i` and `o`, which removes the usual `1`/`l` and `0`/`O` confusions, but Token Factory subdenoms are free-form and are a plausible homograph surface: `allBTC` and `alIBTC` differ by one character in a 63-character context.
Consumers SHOULD render the creator address and subdenom in full when a user is authorising a transfer.

### Chain identity is mutable, asset identity is not

[cosmos-caip2][] treats a chain reboot as producing a distinct `chain_id`, so `cosmos:cosmoshub-3` and `cosmos:cosmoshub-4` are different chains.
Bank balances, IBC vouchers and contract state carry across such an event unchanged, which means the same asset legitimately acquires a new `asset_type` at the moment the `chain_id` changes.
Whether identifiers under the old `chain_id` should be treated as referring to the same assets is, as in [cosmos-caip2][], left to higher-level applications and their equality sets.

## Backwards Compatibility

No CAIP-19 profile previously existed for this namespace, so nothing is superseded.

[CAIP-20][] `slip44` references remain valid on the Cosmos Hub and on chains with their own registered coin type, subject to the restriction above.

The `ics20` namespace is named for the interchain standard rather than for the `ibc/` prefix, so it is stable across the `ibc-go` v9 rename of `DenomTrace` to `Denom` and the corresponding move of the query endpoint from `/denom_traces/` to `/denoms/`.
The hash construction is unchanged by that rename and dates to [ADR-001][] in 2020.

Identifiers minted under this profile are stable as long as the chain holds the denomination.
They are not stable across a channel being closed and a replacement channel being opened, which produces a new voucher denomination and therefore a new identifier for what users will describe as the same asset.

## References

- [CAIP-19][] — Asset Type and Asset ID Specification
- [CAIP-20][] — Asset Reference for the SLIP44 Asset Namespace
- [cosmos-caip2][] — the chain identifiers this profile is scoped by
- [SLIP-0044][] — registered coin types; line 151 registers `118 ATOM Atom`
- [sdk-coin-go][] — the Cosmos SDK denomination regex `[a-zA-Z][a-zA-Z0-9/:._-]{2,127}`
- [ADR-001][] — ICS-20 coin source tracing, which defines the `ibc/{hash}` construction
- [ibc-go-denom][] — the reference implementation of the hash and of `ExtractDenomFromPath`
- [ICS-20][] — fungible token transfer
- [ICS-721][] — non-fungible token transfer
- [Token Factory][] and [tokenfactory-denoms][] — permissionless bank denominations and their length limits
- [CW20][], [CW721][], [CW1155][] — CosmWasm token interfaces
- [SNIP-20][], [SNIP-25][], [SNIP-721][] — Secret Network confidential token interfaces
- [chain-registry][] — the community registry of chain IDs, bech32 prefixes and declared coin types

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-20]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-20.md
[cosmos-caip2]: ./caip2.md
[Cosmos]: ./README.md
[Cosmos SDK]: https://github.com/cosmos/cosmos-sdk
[x/bank]: https://docs.cosmos.network/main/build/modules/bank
[sdk-coin-go]: https://github.com/cosmos/cosmos-sdk/blob/main/types/coin.go
[SLIP-0044]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
[slip44-118]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md#registered-coin-types
[IBC]: https://github.com/cosmos/ibc-go
[ICS-20]: https://github.com/cosmos/ibc/tree/main/spec/app/ics-020-fungible-token-transfer
[ICS-721]: https://github.com/cosmos/ibc/tree/main/spec/app/ics-721-nft-transfer
[ADR-001]: https://github.com/cosmos/ibc-go/blob/main/docs/architecture/adr-001-coin-source-tracing.md
[ibc-go-denom]: https://github.com/cosmos/ibc-go/blob/main/modules/apps/transfer/types/denom.go
[Token Factory]: https://github.com/osmosis-labs/osmosis/tree/main/x/tokenfactory
[tokenfactory-denoms]: https://github.com/osmosis-labs/osmosis/blob/main/x/tokenfactory/types/denoms.go
[CosmWasm]: https://github.com/CosmWasm/cosmwasm
[CW20]: https://github.com/CosmWasm/cw-plus/blob/main/packages/cw20/README.md
[CW721]: https://github.com/public-awesome/cw-nfts/blob/main/packages/cw721/README.md
[CW1155]: https://github.com/CosmWasm/cw-nfts/tree/main/packages/cw1155
[Secret Network]: https://docs.scrt.network
[SNIP-20]: https://github.com/SecretFoundation/SNIPs/blob/master/SNIP-20.md
[SNIP-25]: https://github.com/SecretFoundation/SNIPs/blob/master/SNIP-25.md
[SNIP-721]: https://github.com/SecretFoundation/SNIPs/blob/master/SNIP-721.md
[chain-registry]: https://github.com/cosmos/chain-registry
[RFC 3986]: https://datatracker.ietf.org/doc/html/rfc3986#section-2.1
[Percent-encoding of denominations]: #percent-encoding-of-denominations
[Selecting the namespace]: #selecting-the-namespace
[Reference length]: #reference-length
[Coin type 118 is not a chain]: #coin-type-118-is-not-a-chain
[Token identifiers are unbounded strings]: #token-identifiers-are-unbounded-strings
[CC0]: https://creativecommons.org/publicdomain/zero/1.0/

## Rights

Copyright and related rights waived via [CC0][].
