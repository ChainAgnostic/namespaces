---
namespace-identifier: aleo-caip10
title: Aleo Network - Namespace Accounts
author: Jonathan Gonzalez (@jonandgon)
discussions-to: <URL of PR, mailing list, etc>
status: Draft
type: Standard
created: 2023-09-12
requires (*optional): <["CAIP-10"]>
---

<!--You can leave these HTML comments in your merged CAIP and delete the 
 visible duplicate text guides, they will not appear and may be helpful to 
 refer to if you edit it again. This is the suggested template for new CAIPs.
 Note that an CAIP number will be assigned by an editor. When opening a pull
 request to submit your EIP, please use an abbreviated title in the 
 filename, `caipX.md`, all lowercase, no `-` between the CAIP and its 
 number.-->

# CAIP-10

*For context, see the [CAIP-10][] specification.*
<!--"If you can't explain it simply, you don't understand it well enough." Provide a simplified and layman-accessible explanation of the CAIP.-->

## Rationale
<!--A short (~200 word) description of the technical issue being addressed.-->
An Aleo account address is a unique identifier that allows users to transfer value and record data to one another in transactions.

The account address is comprised of a public key for the account encryption scheme.

## Syntax

Address Format Example
`aleo1dg722m22fzpz6xjdrvl9tzu5t68zmypj5p74khlqcac0gvednygqxaax0j`

An account address is formatted as a `Bech32` string, comprised of 63 characters. The account address is encoded with an address prefix that reads `aleo1`.

A regular expression for validating an Aleo address can be defined as:

`^aleo1[a-z0-9]{58}$`

## Test Cases

```env
# Aleo Testnet3
aleo:testnet3:aleo1ml2xr6fawppd6uaf8gn95uy2fpqqg8gk74k0lu8na7uvayk64v8qu8hw5u
```

## Additional Considerations (*OPTIONAL)

Account addresses / keys are chain-agnostic.

Mainnet will release sometime at the end of 2023 / beginning of 2024. The API is subject to change.

## References
<!--Links to external resources that help understanding the CAIP better. This can e.g. be links to existing implementations.-->
- [Aleo Network Documentation][]: Developer docs for the Aleo Network.
- [Aleo Account Documentation][]: Developer docs for account creation.

[Aleo Network Documentation]: https://developer.aleo.org
[Aleo Account Documentation]: https://developer.aleo.org/concepts/accounts
[CAIP-2]: https://chainAgnostic.org/CAIPS/caip-2
[CAIP-10]: https://chainAgnostic.org/CAIPS/caip-10
[aleo CAIP-2]: aleo/caip2

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
