---
namespace-identifier: <CAIP-2 id>
binary-key: <two bytes in RFC-4616 base16 (no 0x-prefix)>
title: <{namespace common name} [, aka ecosystem name]>
discussions-to: <url of where to provide feedback of this spec>
author: <["FirstName1 LastName1 (@GitHubUsername1)", "AnonHandle2 <foo2@bar.com>"]>
status: Draft
type: Informational
created: <date created on, in ISO 8601 (yyyy-mm-dd) format>
requires: <list of standards required to understand this one>
---

## Chain reference

ChainType binary key: `0xXXXX`
[CAIP-104] namespace: `XXXXX`

<!-- check existing caip350 profiles on namespaces chainagnostic.org as well as open PRs for collisions with previously-registered binary keys -->

### Text representation

<!-- a description of the format of chain namespace + reference intended for the text representation of ERC-7930 Interoperable Addresses -->
<!-- MUST include how to represent the ChainType without a reference, since that is supported by [ERC-7930] -->

##### Text representation -> CAIP-2 conversion

<!-- instructions for how to convert from the above to a CAIP-2 string -->

##### CAIP-2 - text representation conversion

<!-- instructions for how to convert from a CAIP-2 string to the Interoperable Address format -->

#### Binary representation

<!-- description of how will chain references be laid out in binary Interoperable Addresses' `ChainReference` field -->

#### Text -> binary conversion

<!-- instructions for converting from the text representation to the binary one -->

#### Binary -> text conversion

<!-- instructions for converting from the text representation to the binary one -->

#### Examples

## Addresses

### Text representation

<!-- a description of the format of addresses intended for the text representation of ERC-7930 Interoperable Addresses -->

##### Text representation -> native representation conversion

<!-- instructions for how to convert from the above to the native address formats normally used in the ecosystem -->
<!-- MUST cover all address types used in the ecosystem -->
<!-- Note: actor addresses should be addressed here natively, i.e. in the native representation format -->

##### Native representation -> text representation conversion

<!-- instructions for how to convert from native address formats normally used in the ecosystem to the Interoperable Address text representation -->
<!-- MUST cover all address types used in the ecosystem -->

#### Binary representation

<!-- description of how will addresses be laid out in binary Interoperable Addresses' `Address` field -->

#### Text -> binary conversion

<!-- instructions for converting from the text representation to the binary one -->

#### Binary -> text conversion

<!-- instructions for converting from the binary representation to the text one -->

#### Examples

### Error handling

<!-- _(Optional section)_ -->

<!-- Document any error handling considerations specific to this namespace, such as:
- Scenarios where loss of information may occur during conversions (e.g., CAIP-2 -> CAIP-350 when full chainId can't be determined)
- Error types and how they should be handled -->

### Implementation considerations

<!-- _(Optional section)_ -->

<!-- Document any implementation considerations specific to this namespace, such as:
- Account types that cannot be chain-specified
- Chain-wildcard limitations
- Other implementation footguns specific to this ecosystem -->

### Extra considerations

<!-- Anything that is particular to this namespace and of interest to users, such as not being able to satisfy canonicity requirements or imminent expansions/revisions to the conventions of the ecosystem -->

