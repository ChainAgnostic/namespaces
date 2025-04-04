---
namespace-identifier: eip155-caip25
title: EIP155 Namespace, aka EVM Chains - JSON-RPC Provider Authorization
author: Pedro Gomes (@pedrouid), Hassan Malik (@hmalik88), bumblefudge (@bumblefudge)
discussions-to: 
status: Draft
type: Standard
created: 2024-02-05
updated: 2024-02-05
requires: ["CAIP-25", "CAIP-211", "CAIP-217"]
---

# CAIP-25

_For context, see the [CAIP-25][] specification._

## Rationale

In the Ethereum space, many networks interact in a given application or session, and as such it is necessary for applications and user-agents like wallets to negotiation and authorize interfaces dynamically and mutually.
The [CAIP-25] negotiation allows for multiple [CAIP-217] authorization scopes to be negotiated together. 

## Network-specific versus Namespace-wide Scopes

Authorizing permissions and capabilities to each network separately (i.e., in its own [CAIP-217] authorization object) is recommended in most use-cases, so that over the session and across sessions, each network can granularly gain or attenuate permissions and capabilities separately. 
Conversely, an authorization object scoped to all of `eip155` can only add or substract individual networks from the `chains` array, or add and substract capabilities to all enumerated networks in that array.

It is also worth mentioning that if a network supports any capabilities NOT supported by other networks, they should never share an authorization object, as the semantics of [CAIP-217] interpret this as supporting EVERY capability listed on EVERY network listed.

In such cases, not only is a separate authorization object recommended, but an explicit [CAIP-211] declaration of the RPC authority where these network-specific capabilities are specified is also recommended;
see the [eip155/caip211.md](./caip211.md) profile for further guidance on using `method` and `notification` definitions which are not universal to the eip155 namespace.

## Session Properties

No namespace-wide or network-specific session properties have yet been proposed for standardization.
When crafting such properties for contextual/in-network usage, it is recommended to align one's semantics and syntax (including case-sensitive style guides for property names!) with the [EIP-6963] wallet provider interface (which extends the [EIP-1193] interface) for common properties across architectures, making sure to avoid any collisions.

Similarly, wherever possible, session properties should align closely with information passed as JSON objects by `wallet_` RPC methods, like capabilities or permissions. 
For example, the capability objects specified in [EIP-5792] get passed via the `wallet_getCapabilities` RPC method inside of partition objects keyed to the hexadecimal chainId when chain-specific, and inside of an object keyed `0x00` (following the chainId 0 convention; see the [`eip155`/caip2 profile](caip2)) when universal to the `eip155` namespace.
Should an application request and a wallet choose to pre-declare at time of connection, both parties can put such objects in the appropriately-keyed `scopedProperties` partition for chain-specific capabilities and in the `sessionProperties` (unpartitioned) for `eip155`-wide capabilities.
See the example below, equivalent to the illustrative examples in [EIP-5792].

## Examples

### Example Request

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "provider_authorize",
  "params": {
    "requiredScopes": {
      "eip155": {
        "scopes": ["eip155:1", "eip155:137"],
        "methods": ["eth_sendTransaction", "eth_signTransaction", "eth_sign", "get_balance", "personal_sign"],
        "notifications": ["accountsChanged", "chainChanged"]
      },
      "eip155:8453": {
        "methods": ["get_balance"],
        "notifications": ["accountsChanged", "chainChanged"]
      },
      "wallet": {
        "methods": ["wallet_getPermissions", "wallet_switchEthereumChain", "wallet_creds_store", "wallet_creds_verify", "wallet_creds_issue", "wallet_creds_present", "wallet_getCapabilities"],
        "notifications": []
      },
      "cosmos": {
        ...
      }
    },
    "optionalScopes":{
      "eip155:84532": {
        "methods": ["eth_sendTransaction", "eth_signTransaction", "get_balance", "personal_sign"],
        "notifications": ["accountsChanged", "chainChanged"]
    },
    "sessionProperties": {
      "expiry": "2022-12-24T17:07:31+00:00",
      "caip154": {
        "supported":"true"
      },
      "flow-control": {
        "loose": [], 
        "strict": [], 
        "exoticThirdThing": [] //caller is requesting a configuration-set which the wallet will drop as unrecognized      
      }
    },
    "scopedProperties": {
      "8453": {
        "paymasterService": {
          "supported": true
        },
        "sessionKeys": {
          "supported": true
        },
        "atomic": true
      },
      "84532": {
        "auxiliaryFunds": {
          "supported": true
        },
        "atomic": false
      }
    }
  }
}
```

### Example Response

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": {
    "sessionId": "0xdeadbeef",
    "sessionScopes": {
      "eip155": {
        "chains": ["eip155:1", "eip155:137"],
        "methods": ["eth_sendTransaction", "eth_signTransaction", "get_balance", "eth_sign", "personal_sign"]
        "notifications": ["accountsChanged", "chainChanged"],
        "accounts": ["eip155:1:0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb", "eip155:137:0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb"]
      },
      "eip155:83532": {
        "methods": ["personal_sign"],
        "notifications": ["accountsChanged", "chainChanged"],
        "accounts":["eip155:83532:0x0910e12C68d02B561a34569E1367c9AAb42bd810"]
      },
      "wallet": {
        "methods": ["wallet_getPermissions", "wallet_switchEthereumChain", "wallet_getCapabilities"],
        "notifications": []
      },
      "cosmos": {
        ...
      }
    },      
    "sessionProperties": {
      "expiry": "2022-12-24T17:07:31+00:00",
      "caip154": {
        "supported":"true"
      },
      "flow-control": {
        "loose": ["halt", "continue"],
        "strict": ["continue"]
      }
    },
    "scopedProperties": {
      "eip155:84532": {
        "auxiliaryFunds": {
          "supported": false
        }
      }
    }
  }
}
```

## References

- [EIP155][]: Ethereum Improvement Proposal specifying generation and validation of ChainIDs

[execution API]: https://github.com/ethereum/execution-apis?tab=readme-ov-file#execution-api-specification
[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[CAIP-10]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md
[CAIP-19]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md
[CAIP-25]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-25.md
[CAIP-211]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-211.md
[CAIP-217]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-217.md
[EIP]: https://eips.ethereum.org/EIPS/eip-1
[EIP-155]: https://eips.ethereum.org/EIPS/eip-155
[EIP-1193]: https://eips.ethereum.org/EIPS/eip-1193
[EIP-5792]: https://eips.ethereum.org/EIPS/eip-5792
[EIP-6963]: https://eips.ethereum.org/EIPS/eip-6963

## Rights

Copyright and related rights waived via CC0.
