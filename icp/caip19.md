---
namespace-identifier: icp-caip19
title: Asset Type and Asset ID Specification for the Internet Computer Namespace
author: Jeff Jafari (@asjn3e)
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/238
status: Draft
type: Standard
created: 2026-10-11
requires: ["CAIP-2", "CAIP-10", "CAIP-19", "CAIP-20"]
---

# CAIP-19

*For context, see the [CAIP-19][] specification.*

## Introduction

On ICP, a fungible token is a ledger canister.
The ledger keeps all balances and implements the [ICRC-1][] standard.
The ICP token works the same way: the ICP ledger canister holds it.

An asset type in this namespace is the canister ID of a token's ledger, under the asset namespace `icrc1`.

## Specification

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [BCP 14][] ([RFC 2119][], [RFC 8174][]) when, and only when, they appear in all capitals, as shown here.

### Semantics

The asset namespace `icrc1` refers to a fungible token whose ledger canister implements [ICRC-1][].
The asset reference is the principal of that ledger canister.

Symbols do not identify tokens on ICP.
Any canister can report any symbol, so only the ledger's canister ID identifies a token.

### Syntax

```
asset_type:        chain_id + "/" + "icrc1" + ":" + ledger_canister_id
chain_id:          "icp:" + [0-9a-f]{32}   (see the CAIP-2 profile)
ledger_canister_id: ([a-z2-7]{5}-){1,10}[a-z2-7]{1,5}
```

The `ledger_canister_id` is the textual form of the ledger's principal.
It MUST follow the same rules as the `account_address` in the [CAIP-10 profile][]: lowercase, with dashes, and canonical.

Fungible tokens have no asset ID, so an `icrc1` asset type MUST NOT have a `token_id` suffix.

### Resolution Mechanics

To confirm that a canister is an ICRC-1 ledger, call its `icrc1_supported_standards` query method.
The result MUST include an entry with the name `ICRC-1`.
The `icrc1_metadata` query method returns the symbol, name, and decimals.

The following example reads both with `@dfinity/agent`:

```js
import { HttpAgent, Actor } from '@dfinity/agent';

const idlFactory = ({ IDL }) => {
  const Value = IDL.Variant({ Nat: IDL.Nat, Int: IDL.Int, Text: IDL.Text, Blob: IDL.Vec(IDL.Nat8) });
  return IDL.Service({
    icrc1_supported_standards: IDL.Func([], [IDL.Vec(IDL.Record({ name: IDL.Text, url: IDL.Text }))], ['query']),
    icrc1_metadata: IDL.Func([], [IDL.Vec(IDL.Tuple(IDL.Text, Value))], ['query']),
  });
};

const agent = await HttpAgent.create({ host: 'https://icp-api.io' });
const ledger = Actor.createActor(idlFactory, { agent, canisterId: 'ryjl3-tyaaa-aaaaa-aaaba-cai' });
console.log(await ledger.icrc1_supported_standards());
// [ { url: '...', name: 'ICRC-1' }, { url: '...', name: 'ICRC-2' }, ... ]
console.log(await ledger.icrc1_metadata());
// [ [ 'icrc1:decimals', { Nat: 8n } ], [ 'icrc1:name', { Text: 'Internet Computer' } ], [ 'icrc1:symbol', { Text: 'ICP' } ], ... ]
```

## Rationale

Every fungible token on ICP, the ICP token included, is an ICRC-1 ledger canister.
One asset namespace therefore covers all of them, and each token has exactly one asset type.

[CAIP-20][] names native coins with the `slip44` asset namespace, for example `eip155:1/slip44:60` for ether, because ether has no contract.
The ICP token does have one: the ICP ledger.
This profile identifies the ICP token by its ledger, like every other token.

The asset namespace is named after the standard, `icrc1`, in the same way that `eip155` uses `erc20`.

### Backwards Compatibility

Not applicable.

## Test Cases

The following ledgers reported `ICRC-1` in `icrc1_supported_standards` and the listed metadata on ICP mainnet on 2026-10-11.

```bash
# ICP (8 decimals)
icp:737ba355e855bd4b61279056603e0550/icrc1:ryjl3-tyaaa-aaaaa-aaaba-cai

# ckBTC (8 decimals)
icp:737ba355e855bd4b61279056603e0550/icrc1:mxzaz-hqaaa-aaaar-qaada-cai

# ckETH (18 decimals)
icp:737ba355e855bd4b61279056603e0550/icrc1:ss2fx-dyaaa-aaaar-qacoq-cai

# ckUSDC (6 decimals)
icp:737ba355e855bd4b61279056603e0550/icrc1:xevnm-gaaaa-aaaar-qafnq-cai
```

## Additional Considerations

### The ICP token and SLIP-44

[SLIP-44][] registers coin type 223 for ICP.
Under [CAIP-20][], `icp:737ba355e855bd4b61279056603e0550/slip44:223` would also refer to the ICP token.

- Producers MUST emit only the `icrc1` form, `icp:737ba355e855bd4b61279056603e0550/icrc1:ryjl3-tyaaa-aaaaa-aaaba-cai`.
- Consumers MAY accept the `slip44:223` form.
  A consumer that accepts it MUST resolve it to the `icrc1` form above.

Some CAIP-19 consumers find a chain's native asset by looking for the `slip44` asset namespace.
Such a consumer might not recognize `icrc1:ryjl3-tyaaa-aaaaa-aaaba-cai` as the native token of ICP.
Because a consumer that accepts `slip44:223` MUST map it to the ICP ledger, such a consumer can match both forms to the same token.

### Non-fungible tokens

[ICRC-7][] is the ICP standard for non-fungible tokens, and the NNS accepted it.
A later revision can add an `icrc7` asset namespace, with the collection's canister ID as the reference and the token ID as the asset ID.
ICRC-7 token IDs are natural numbers of any size, but CAIP-19 limits a `token_id` to 78 characters, so that revision has to define how to handle larger IDs.

### Subaccounts

ICRC-1 balances belong to accounts. An account is a principal, with or without a subaccount.
A CAIP-10 ID in this namespace names a principal, which on a ledger means its default account.
The [CAIP-10 profile][] explains why it leaves out subaccounts.

## References

- [CAIP-19][]: the Asset Type and Asset ID Specification.
- [CAIP-20][]: the `slip44` asset namespace.
- [BCP 14][]: the meaning of the requirement key words, defined by [RFC 2119][] and [RFC 8174][].
- [CAIP-2 profile][]: how this namespace forms the chain ID.
- [CAIP-10 profile][]: the textual form of principals in this namespace.
- [ICRC-1][]: the fungible token standard, including `icrc1_supported_standards` and `icrc1_metadata`.
- [ICRC-7][]: the non-fungible token standard.
- [SLIP-44][]: the registry of coin types.

[CAIP-2 profile]: ./caip2.md
[CAIP-10 profile]: ./caip10.md
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[CAIP-20]: https://chainagnostic.org/CAIPs/caip-20
[BCP 14]: https://www.rfc-editor.org/info/bcp14
[RFC 2119]: https://www.rfc-editor.org/rfc/rfc2119
[RFC 8174]: https://www.rfc-editor.org/rfc/rfc8174
[ICRC-1]: https://github.com/dfinity/ICRC-1/blob/main/standards/ICRC-1/README.md
[ICRC-7]: https://github.com/dfinity/ICRC/blob/main/ICRCs/ICRC-7/ICRC-7.md
[SLIP-44]: https://github.com/satoshilabs/slips/blob/master/slip-0044.md

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
