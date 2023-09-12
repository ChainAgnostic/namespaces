---
namespace-identifier: aleo-caip2
title: Aleo Network - Namespace Chains
author: Jonathan Gonzalez (@jonandgon)
discussions-to: <URL of PR, mailing list, etc>
status: Draft
type: Standard
created: 2023-09-12
requires (*optional): <["CAIP-2"]>
replaces (*optional): <CAIP-2>
---

<!--You can leave these HTML comments in your merged CAIP and delete the 
 visible duplicate text guides, they will not appear and may be helpful to 
 refer to if you edit it again. This is the suggested template for new CAIPs.
 Note that an CAIP number will be assigned by an editor. When opening a pull
 request to submit your EIP, please use an abbreviated title in the 
 filename, `caipX.md`, all lowercase, no `-` between the CAIP and its 
 number.-->

# CAIP-2

*For context, see the [CAIP-2][https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-2.md] specification.*

## Rationale

The namespace `aleo` refers to the Aleo Network Layer 1 blockchain.

Aleo consists of a single network: a testnet network (Testnet3).

An identifier for a Aleo chain consists of the namespace prefix "aleo:"
followed by the chain id.

## Syntax

The Aleo chain ID is the name of the chain. e.g. `testnet3` or `mainnet` when mainnet is released.

### Resolution Mechanics

To obtain the genesis block hash, make a JSON-RPC request to the Aleo api.

Request (aleo testnet3):

```curl
curl --request GET \
  --url https://vm.aleo.org/api/testnet3/block/0 \
```

Response (aleo testnet3):

```json
{
  "block_hash": "ab1cxu7kq6j8yva9nzq394jt90qnpeexsr0fdnqfdzgqrx4fn7czcyqknclrd",
  "previous_hash": "ab1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq5g436j",
  "header": {
  "previous_state_root": "0field",
    "transactions_root": "2421468861514346193702333205411662486965424378250484763660928941797390483657field",
    "finalize_root": "2347499756727239097527357730627929185508370696360031054030113664724940109165field",
    "ratifications_root": "2347499756727239097527357730627929185508370696360031054030113664724940109165field",
    "coinbase_accumulator_point": "0field",
    "metadata": {
      "network": 3,
      "round": 0,
      "height": 0,
      "total_supply_in_microcredits": 1500000000000000,
      "cumulative_weight": 0,
      "cumulative_proof_target": 0,
      "coinbase_target": 4095,
      "proof_target": 32,
      "last_coinbase_target": 4095,
      "last_coinbase_timestamp": 1680307200,
      "timestamp": 1680307200
    }
  },
  "transactions": [ ... ],
  "ratifications": [],
  "signature": "sign1t7lf502e0h23jtvls9lagepv5sfvgpxm7yvzwrfhgpqsyevkwqq7hcxuympx2w6c4pt3nvm929l74q96hx9ed57cyvvrdm7hqlt75qm7rawvssddfv078wthdpqynfu3jh5qeruups7t7vyls3jxccnypxa5z55an3zwd9em29wrjxmpyymwflclchtzhr62hwthyumkge2qgcd950p"
}
```

### Backwards Compatibility

n/a

## Test Cases

This is a manually composed example.

```env
# Aleo Testnet3
aleo:testnet3
```

## Additional Considerations (*OPTIONAL)

Mainnet will release sometime at the end of 2023 / beginning of 2024. The API is subject to change.

## References
<!--Links to external resources that help understanding the CAIP better. This can e.g. be links to existing implementations.-->
- [Aleo Network Documentation][]: Developer docs for the Aleo Network.

[Aleo Network Documentation]: https://developer.aleo.org
[CAIP-2]: https://chainAgnostic.org/CAIPS/caip-2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
