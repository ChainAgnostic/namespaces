---
namespace-identifier: tezos-caip2
title: Tezos Namespace - Blockchain ID Specification
author: Stanly Johnson (@stanly-johnson), Carlo van Driesten (@jdsika)
discussions-to: ["https://github.com/ChainAgnostic/CAIPs/pull/36", "https://gitlab.com/tezos/tezos/-/issues/1029", https://github.com/ChainAgnostic/namespaces/pull/40]
status: Draft
type: Standard
created: 2020-12-12
updated: 2024-02-20
requires: CAIP-2
supersedes: CAIP-26
---


# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

In CAIP-2 a general blockchain identification scheme is defined. This is the implementation of CAIP-2 for the chain identification system of the Tezos namespace.

## Syntax

Blockchains in the "tezos" namespace are identified by their chain ID derived deterministically from a short, prefixed Blake-2B hash of their `genesis-block-hash`.

### Reference Definition

The method for calculating the hash of a given chain's genesis block (for use as a CAIP-2 chain ID) is as follows from the [Base58 Check Encoded Blake2B Hash][] reference implementation:

```ocaml
tezosB58CheckEncode('Net',
  firstFourBytes(
    blake2b(msg = tezosB58CheckDecode('B', genesisBlockHash),
            size = 32)))
```

### Chain ID alias

The Tezos community recognizes the different chains according to human readable names, the so called [Networks][]. The Octez RPC allows you to connect to three predefined networks:

```bash
# mainnet (this is the default)
# sandbox
# ghostnet

> ./octez-node run --data-dir ~/tezos-ghostnet --network ghostnet
```

There is currently no algorithm to connect the `chain ID` to the `network` as it is determined by social consensus what is considered the `tezos:mainnet`. 

### Backwards Compatibility

Not applicable.

## Test Cases

This is a list of manually composed examples. See [Tezos test network infrastructure][] for available public chains. You can use the [Tezos RPC Interface][] to compute the chain id from a block hash as follows:

```bash
# Tezos Ghostnet (Long-running test network)
> ./octez-client compute chain id from block hash BLockGenesisGenesisGenesisGenesisGenesis1db77eJNeJ9
NetXnHfVqm9iesp
```

Now the CAIP-2 compliant chain ID can be constructed using the Tezos namespace as prefix:

```bash
# Tezos Mainnet
# Genesis block hash: BLockGenesisGenesisGenesisGenesisGenesisf79b5d1CoW2
tezos:NetXdQprcVkpaWU

# Tezos Ghostnet (Long-running test network)
# Genesis block hash: BLockGenesisGenesisGenesisGenesisGenesis1db77eJNeJ9
tezos:NetXnHfVqm9iesp
```
The following table includes the chain ID aliases through their human readable network names:

| Alias          | Chain ID                         |
| -------------- | -------------------------------- |
| tezos:mainnet  | tezos:NetXdQprcVkpaWU            |
| tezos:ghostnet | tezos:NetXnHfVqm9iesp            |

## References

- [Tezos Address Types][] - Important context on the Tezos system of addresses and key representations further specified in the `tezos-caip10` derived from [CAIP-10].
- [Tezos RPC Interface][] - Important context on communicating with Tezos nodes over RPC.
- [Tezos Block Explorer][] - Can be used to investigate block hashs on Mainnet and Ghostnet.
- [Chain ID Reference Implementation][] - Octez implementation for Tezos.
- [Octez][] - Main implementation for the Tezos standard.
- [Base58 Check Encoded Blake2B Hash][] - Octez reference implementation.
- [Taquito Typescript Library][] - Available Base58 functions in Typescript for Tezos.

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[Tezos Address Types]: https://tezos.gitlab.io/introduction/howtouse.html#implicit-accounts-and-smart-contracts
[Tezos RPC Interface]: https://tezos.gitlab.io/introduction/howtouse.html#rpc-interface
[Networks]: http://tezos.gitlab.io/user/multinetwork.html?highlight=network%20name#test-networks
[Tezos Block Explorer]: https://tzstats.com/
[Chain ID Reference Implementation]: https://gitlab.com/tezos/tezos/-/blob/5bb8fd589cc8777f44c795b71acf3e0a5dcac06f/src/lib_crypto/chain_id.ml
[Octez]: https://research-development.nomadic-labs.com/announcing-octez.html
[Base58 Check Encoded Blake2B Hash]: https://gitlab.com/tezos/tezos/-/blob/5bb8fd589cc8777f44c795b71acf3e0a5dcac06f/src/lib_crypto/blake2B.ml
[Taquito Typescript Library]: https://tezostaquito.io/typedoc/functions/_taquito_utils.b58decode#b58decode
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[Tezos test network infrastructure]: https://teztnets.com/

## Rights

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
