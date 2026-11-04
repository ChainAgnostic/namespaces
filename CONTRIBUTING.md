# Contributing

 1. Review [CAIP-104][] and a good sampling of the `README.md` files of other [namespaces][], particularly the ones architecturally most similar to yours.
 2. Fork the repository locally.
 3. Make a copy of the `_template` folder, and rename it to anything else.
 4. In your copy of the template folder, start by filling out the template for README.md, according to [CAIP-104][].
 5. When you have proposed an abbreviation for your namespace, rename your template folder to that short string, all lowercase.
 6. Review [CAIP-2][] and a good sampling of the `CAIP2.md` files of other [namespaces][], particularly the ones architecturally most similar to yours.
 7. Submit a Pull Request to Chain Agnostics's [`namespaces` repository](https://github.com/ChainAgnostic/namespaces).

Your first PR should be a complete draft of the README.md for your namespace with at least CAIP-2 addressed, but we also welcome additional CAIPs. 
An editor will manually review the first PR for a new CAN and assign it a number before merging it. 
Make sure you include a `discussions-to` header with one or more URLs a GitHub issue, GitHub Discussion, or other forum where people can discuss the CAN going forward; if you requested feedback from other teams or counterparties in your namespace before submitting, an issue or discussion on a fork of the namespaces repo is also a helpful addition to the `discussions-to` entry, which can be an array.
It is also acceptable to tag interlocutors and reviewers familiar with the namespace in the initial PR; you may be asked to do so later by the editors if they are not familiar with the community.

If your CAN requires images, the image files should be included in a subdirectory of the `assets` folder for that CAN as follows: `assets/namespace-N` (where **N** is to be replaced with the CAN name).
When linking to an image in the CAN, use relative links such as `../assets/namespace-{N}/image.png`.

It is greatly appreciated if you can render your PR locally to check the Jekyll syntax; to do so, run `bundle exec jekyll serve`.

## Machine-readable Supplements

To facilitate validation and multi-chain registries, you may choose to include (or editors may include) a secondary copy of each profile's validation sections and test cases in the form of a `.json` file, with the following format:

### Example: eip155/caip2.json

```json
{
    "standard":"caip2",
    "validation":"[0-9]{1-32}",
    "test cases": [
        "Ethereum mainnet": "eip155:1",
        "Görli": "eip155:5",
        "Auxilium Network Mainnet": "eip155:28945486"
    ]
}
```

These machine-readable records are for illustrative purposes only, and any time they contradict or grow out-of-date with their corresponding specifications, the latter should be considered authoritative.

## Style Guide

Github-flavored Markdown is encouraged for all CAIP documents, with the following conventions observed:

Line breaks:
- One line per sentence (or independent clause in the case of semicolons) makes for easier parsing of diffs in PR review and is preferred but not required

Link formatting:
- All external documents cited should be defined at the end of the `## References` section of each document, one per line, in the form `[CAIP-1]: https://chainAgnostic.org/CAIPs/CAIP-1` - these link alias definitions are invisible in rendered markdown, but serves as footnotes to readers viewing the files in a text editor.
- All references to other namespaces or to CAIPs should refer to the rendered form on the domain controlled by CASA (e.g. `https://chainagnostic.org/CAIPs/caip-104`) rather than to the current public git repository that it renders from (currently, `https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-104.md?plain=1`, but subject to change)
- All references elsewhere in the text should be by link-alias (e.g. `[CAIP Syntax][CAIP-1]`) rather than self-contained (e.g. `[CAIP syntax](https://ChainAgnostic.org/CAIPs/caip-1)`); note that in this example, `[CAIP-1][CAIP-1]`, `[CAIP-1][]` and `[CAIP-1]` will all link to the same URL if the alias has been defined elsewhere in the document when rendered. This makes the document easier to read in a text editor.
- Links to other sections should always take the form of markdown section heading links rather than HTML anchors or any other reference, e.g. `For further detail, see the [Security Considerations section](#security-considerations)`
- Providing lists of normative and non-normative references according to, e.g., the [IETF style guide for references](https://www.ietf.org/archive/id/draft-flanagan-7322bis-07.html#section-4.8.6) is welcomed but not required; a short list of useful documents or additional resources with captions or explanations is also welcome.

## References

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-104]: https://ChainAgnostic.org/CAIPs/caip-104
[namespaces]: https://namespaces.chainagnostic.org/
