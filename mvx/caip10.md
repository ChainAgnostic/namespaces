---
namespace-identifier: mvx-caip10
title: MultiversX Namespace - Addresses
author: MultiversX Team <contact@multiversx.com>
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/87
status: Draft
type: Standard
created: 2023-09-11
requires: ["CAIP-2", "CAIP-10"]
---

# CAIP-10

_For context, see the [CAIP-10][] specification._

## Rationale

The MultiversX Address format is bech32, specified by the [BIP_0173][].
The human-readable-part of the bech32 addresses is "erd" which means that the MultiversX address always starts with an `erd1` ("1" is a separator) e.g.: `erd1sea63y47u569ns3x5mqjf4vnygn9whkk7p6ry4rfpqyd6rd5addqyd9lf2`.

The MultiversX network defines the address of an account as the bech32 representation of the public key of its corresponding pair of keys (the secret key remains known only to the user that owns the key pair). The public key is 32 bytes in length (64 hex characters), while the address (bech32) is 62 characters long.

On MultiversX, Smart Contracts and only Smart Contracts have their hex (raw) addresses prefixed with 8 zero bytes (meaning that their bech32 address will begin with `erd1qqqqqqqqqqqq` )

## Syntax

```
caip10-like address:    namespace + ":" chainId + ":" + address
namespace:              mvx
chain Id:               1, D or T
address:                bech32 formatted MultiversX address (erd1...)
```

## Test Cases

```
MultiversX Mainnet
mvx:1:erd1uapegx64zk6yxa9kxd2ujskkykdnvzlla47uawh7sh0rhwx6y60sv68me9
mvx:1:erd1qqqqqqqqqqqqqpgqhe8t5jewej70zupmh44jurgn29psua5l2jps3ntjj3 ( Smart Contract )

MultiversX Devnet
mvx:D:erd1devnet6uy8xjusvusfy3q83qadfhwrtty5fwa8ceh9cl60q2p6ysra7aaa

MultiversX Testnet
mvx:T:erd1sea63y47u569ns3x5mqjf4vnygn9whkk7p6ry4rfpqyd6rd5addqyd9lf2
```

## References

- [MultiversX Docs](https://docs.multiversx.com/)
- [MultiversX Specifications](https://github.com/multiversx/mx-specs)
- [Integrators Guide](https://docs.multiversx.com/integrators/overview)
- [BIP_0173](https://en.bitcoin.it/wiki/BIP_0173)
- [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md)
- [CAIP-10](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md)

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
