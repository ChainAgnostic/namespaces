---
namespace-identifier: tezos
title: Blockchain Reference for the Tezos Namespace - Chains
author: Stanly Johnson (@stanly-johnson)
discussions-to: ["https://github.com/ChainAgnostic/CAIPs/pull/36", "https://gitlab.com/tezos/tezos/-/issues/1029"]
status: Draft
type: Standard
created: 2020-12-12
updated: 2022-03-27
requires: CAIP-2
supersedes: CAIP-26
---


# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

In CAIP-2 a general blockchain identification scheme is defined. This is the
implementation of CAIP-2 for the chain identification system of the Tezos
namespace.

## Syntax

Blockchains in the "tezos" namespace are identified by their chain ID derived deterministically from a short, prefixed Blake-2B hash of their genesis block. 

### Reference Definition

The method for calculating the hash of a given chain's genesis block (for use as a CAIP-2 chain ID) is as follows:

```
tezosB58CheckEncode('Net',
  firstFourBytes(
    blake2b(msg = tezosB58CheckDecode('B', genesisBlockHash),
            size = 32)))
```

Note that in the [Base58 Function in Reference Implementation][], the BTC-58
alphabet is the default, but `ripple` and `flickr` are also present as
alternatives; for the purposes of the genesis block hash, assume BTC alphabet.

### Backwards Compatibility

Not applicable

## Test Cases

This is a list of manually composed examples

```
# Tezos Mainnet
tezos:NetXdQprcVkpaWU

# Tezos DelphiNet (Current active testnet)
tezos:NetXm8tYqnMWky1
```

## References

- [Tezos Address types][] - Important context on the Tezos system of addresses and key representations.
- [Tezos RPC Interface][] - Important context on communicating with Tezos nodes over RPC.
- [Chain_ID Reference Implementation][]
- [Base58 Function in Reference Implementation][] - Note support for additional Base58 alphabets 

[Tezos RPC Interface]: https://tezos.gitlab.io/introduction/howtouse.html#rpc-interface
[Tezos Address types]: https://tezos.gitlab.io/introduction/howtouse.html#implicit-accounts-and-smart-contracts
[Chain_ID Reference Implementation]: https://gitlab.com/tezos/tezos/blob/e7612c5ffa46570cdcc612f7bcead771edc24283/src/lib_crypto/chain_id.ml
[Base58 Function in Reference Implementation]: https://github.com/LedgerHQ/TzScan/blob/9f02015d872014c2b114e600f9212b00c6b281b3/src/common/blake2b.ml#L91
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[Base58]: https://datatracker.ietf.org/doc/html/draft-msporny-base58-03

## Rights

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).