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
Make sure you include a `discussions-to` header with the URL to a discussion forum or open GitHub issue where people can discuss the CAN as a whole; if you requested feedback from other teams or counterparties in your namespace before submitting, a private fork of the namespaces repo containing these discussions is a perfectly valid and helpful `discussions-to` entry.
Note that `discussions-to` can be a single value or an array, too much discussion is more helpful than not enough.
It is also acceptable to tag interlocutors and reviewers familiar with the namespace in the initial PR; you may be asked to do so by the editors.

If your CAN requires images, the image files should be included in a subdirectory of the `assets` folder for that CAN as follows: `assets/namespace-N` (where **N** is to be replaced with the CAN name).
When linking to an image in the CAN, use relative links such as `../assets/namespace-{N}/image.png`.

It is greatly appreciated if you can render your PR locally to check the Jekyll syntax; to do so, run `bundle exec jekyll serve`.

## References

[CAIP-104]: https://ChainAgnostic.org/CAIPs/CAIP-104
[namespaces]: https://namespaces.chainagnostic.org/
