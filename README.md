# Namespaces

Chain Agnostic Namespaces (CANs) are folders in this repository that describe a blockchain ecosystem or set of ecosystems as an autonomous `namespace`. 
They consist of a 1 high-level "README.md" file to contextualize the ecosystem, its history, its boundaries, and its authorities, and 0 or more "profiles" of specific [CAIPs][] specifications.
Each "CAIP profile" defines the namespace's syntax, semantics, and context for that CAIP (i.e., it's address format, actor model, asset addressing model, etc.).
The intended audience of both the general "README.md" and each profile is a developer familiar with the CAIP being profiled but not familiar with the ecosystem being described, so the best namespaces provide all the links and entry-level explanations of the context needed for developers to build wallet and/or dapp interfaces that interact with assets, contracts, and accounts of a given namespace.

The namespaces are best read as rendered on the [namespaces][] website rather than in github. To contribute see the [Contributing file](./CONTRIBUTING.md).

## How it works
Each namespace implements one or more [CAIPs](https://github.com/ChainAgnostic/CAIPs). The most important CAIPs to consider for a namespace are:

- [Blockchain ID](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md) - A unique way to represent individual blockchains, also gives the namespace its name
- [Account ID](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md) - Unique representations of blockchain accounts (also used in [DID PKH](https://github.com/w3c-ccg/did-pkh/))
- [Asset Type and Asset ID](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md) - Uniquely refer to assets within the namespace
- [SIWx](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-122.md) - Namespaces that support SIWx (Sign In With X) can be used with [CACAO](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-74.md)

## CAN Status Terms

* **Draft** - an CAN that is undergoing rapid iteration and changes.
* **Last Call** - an CAN that is done with its initial iteration and ready for review by a wide audience.
* **Accepted** - a core CAN that has been in Last Call for at least 2 weeks and any technical changes that were requested have been addressed by the author.

## Frequently Asked Questions

> Is a network a namespace?  Is a custom chain a namespace? Is a "Layer-2" Blockchain a namespace? 

Think of a namespace as a set of architectural assumptions, security models, actor models, and standards-- addressing standards, runtimes, etc. 
The superset of possible chains sharing the same tooling and interfaces and languages. 
One namespace might include a few overlapping RPC interfaces with more or less commands, but all wallets and nodes would at least be using the same RPC *protocol* and recognize each other as variants (or versions) if there are multiple interfaces supported.  
Some namespaces (like Polkadot and Cosmos) have complex interoperability and coordination/transport mechanisms between chains; others (like the Bitcoin family and its forks) basically live in ignorance of one another, making each chain feel like a namespace all its own. 
Different versions or variations of the protocol might exist (particularly on highly "composable" or customizable runtimes like Polkadot or Cosmos, where consensus and block structure can vary from chain to chain);
Some "Layer 2" chains even might add additional layers to the actor/account model or signing mechanisms, but if interoperability (even one-way) is possible between chains, they are (for developers, if not always for end-users) one namespace.

An additional consideration, if you're not sure whether the network or community you are describing should be in its own namespace, is to remember that the target audience is a Dapp or Wallet or Crypto-curious Web developer who maybe knows Rust or Solidity and Solana or Ethereum or Bitcoin basics, but... nothing about your namespace, or the other namespace of which yours is debatably a subset or neighborhood. If you can't decide, ask yourself, would they be better

> What if I decide a whole new namespace isn't justified or accurate, but I still have a custom runtime or network that I want to define?

Pull requests adding a `### Your Network Here` section to the `README.md` and CAIP profiles of another namespace are totally acceptible, and we encourage "Layer 2"s and custom networks within a namespace to make the caveats and special cases of their specific context known to cross-chain developers who may not be familiar.
That said, if your "Layer 2" does not require any custom validation logic, and does not break any assumptions as defined already in the existing namespace documentation, please do NOT open a pull request adding sections and prose text just to inform developers namespace-wide of the existence of your CAIP-2 and the many use-cases you support; simply adding an example to the CAIP-2 profile is enough!

> What about an EVM-mode or BTC-mode layer-2?

The special-case of "custom RPC layer-2s" that adopt the RPC interfaces of another namespace for interoperability purposes mostly fall under the case above; they are, in the case of EVM-mode interfaces for other namespaces, simply another EVM chainID listed in the `ethereum-lists` repository on GitHub.
If, however, the *native* RPC interface, actor model, deployed-contract addressing, etc. of your *native* namespace nodes and tooling have ways of interacting with assets exposed to external/cross-chain interfaces, that might be worth mentioning in the relevant CAIP profiles of your native namespace documentation.

## References

[CAIPs]: https://github.com/ChainAgnostic/CAIPs
[namespaces]: https://namespaces.chainagnostic.org/
