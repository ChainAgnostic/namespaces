---
namespace-identifier: casper-caip2
title: Casper Chains
author: "FirstName1 LastName1 (@GitHubUsername1)", "David Hernando <david.hernando@make.services>"
status: Draft
type: Standard
created: 2024-01-12
requires: ["CAIP-2"]
---

# CAIP-2

*For context, see the [CAIP-2][] specification.*

## Rationale

The Chain ID is a human-readable identifier for a Casper network blockchain. It should not be confused with the `genesis_hash`, which is the true and unique identifier of a chain.

## Syntax

It consists of the prefix `casper:` followed by the chainspec name of that network. Such name is a string that permits to easily identify the network and protect from replay attacks.

### Resolution Method

To resolve the chainspec name for a Casper network chain send an RPC request with method `info_get_status` to a Casper node in that network. The result object in the RPC response will contain the field `chainspec_name` with the chainspec name of that network.

For example:

```jsonc
// Command
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0", "id": 1, "method":"info_get_status", "params":{}}' \
  http://52.35.59.254:7777/rpc | jq .result.chainspec_name

// Result
"casper-test"
```

Append the prefix `"casper:"` to form the Chain Id for that chain. In the example above: `casper:casper-test`.

## Test Cases

This is a list of manually composed Chain Id examples

```
# Casper Mainnet
casper:casper

# Casper Testnet
casper:casper-test
```

For testing purposes, the Casper Association maintains the following RPC endpoints:

* Casper Mainnet: http://34.224.191.55:7777/rpc
* Testnet: http://52.35.59.254:7777/rpc


## References

- [Casper Docs site][]
- [Casper Chain Specification][Chainspec]
- [CAIP-2][]

[CAIP-2]: https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md
[Casper Docs site]: https://docs.casper.network/
[Chainspec]: https://docs.casper.network/operators/setup-network/chain-spec/

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).