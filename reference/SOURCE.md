# Where the reference text came from

The contract in this folder is built on two U.S. government works. Both are shipped here unaltered so a reader can check any claim in `hud1-line-dictionary.md` against the source rather than taking this folder's word for it.

## The two sources

### Current instructions -- the 2010-and-later HUD-1

**Appendix A to Part 1024, Title 12** -- *Instructions for Completing HUD-1 and HUD-1a Settlement Statements; Sample HUD-1 and HUD-1a Statements*

Issued by the Consumer Financial Protection Bureau as part of Regulation X.

- Retrieved: 20 September 2026
- Source: eCFR versioner API, title 12, part 1024, issue date 2026-09-17
- `https://www.ecfr.gov/api/versioner/v1/full/2026-09-17/title-12.xml?part=1024&appendix=Appendix%20A%20to%20Part%201024`
- Citation key prefix in this folder: `1024-A`

### Prior instructions -- the pre-2010 HUD-1

**Appendix A to Part 3500, Title 24** -- *Instructions for Completing HUD-1 and HUD-1A Settlement Statements; Sample HUD-1 and HUD-1A Statements*

Issued by the Department of Housing and Urban Development. This is the annual CFR edition **revised as of April 1, 2007**, which predates the 2008 RESPA final rule that reworked the form.

- Retrieved: 20 September 2026
- Source: govinfo.gov, annual CFR edition
- `https://www.govinfo.gov/content/pkg/CFR-2007-title24-vol5/xml/CFR-2007-title24-vol5-part3500-appA.xml`
- Citation key prefix in this folder: `3500-A`

## Why the 2007 edition, specifically

The 2008 RESPA rule was published in November 2008 with a January 1, 2010 compliance date, and the CFR text was amended ahead of that date. **The April 1, 2009 edition already carries the new instructions** -- its line 801 reads "Our origination charge," not "Loan Origination Fee."

So 2009 is not the pre-2010 vintage despite its date. The April 1, 2007 edition is the one that matches the form real settlement agents still produce for cash and commercial closings, and it was checked before being used: its line 801 is "the fee charged by the Lender for processing or originating the loan" and its line 1101 is "the settlement agent's fee."

That check is the entire basis for the two-vintage rule in `hud1-line-dictionary.md`.

## Copyright

Both are works of the United States Government and are not subject to copyright protection in the United States. They can be redistributed in full, which is why they are in this folder rather than merely linked.

The HUD-1 form itself carries OMB control number 2502-0265.

## Files and fingerprints

| File | Bytes | SHA-256 |
|---|---|---|
| `12-cfr-1024-appendix-a-2026-official.xml` | 40903 | `38cb3d09c46249e94f5f9ba10b92307e7d40290a1a8adeee5ff17c9c6b1e922c` |
| `12-cfr-1024-appendix-a-2026.md` | 41124 | `36dd39df6a538d2c8114a06543442c0a3ad51c913814a7f3bd1d6270fd05b3e0` |
| `24-cfr-3500-appendix-a-2007-official.xml` | 33794 | `71d3ebfff65ab8c7cc87f1d134d96daf98bc1442afb76d84c9fb7d8b480bdaac` |
| `24-cfr-3500-appendix-a-2007.md` | 31908 | `c87984a77930db7364add7295a8aa03ba7f9509d8f48eda7075bb5708a432e69` |
| `hud1-line-dictionary.md` | 9423 | `ae3bc2b4b5e9eb3896cefedefd2f6f8847234884a8155e2f0a3c83217e48ba6e` |
| `output-schema.md` | 9354 | `a033a88b53c56b7dc0c8b1c7f8af542d86acbcac7f3c99ff6676e7c9a5822d27` |

The `-official.xml` files are byte-for-byte what the government servers returned. The two `.md` files are generated from them by `tools/convert_appendix.py`, which strips tags and numbers each paragraph so it can be cited.

## Verifying this yourself

Regenerate the markdown from the shipped XML and confirm nothing changed:

    python tools/convert_appendix.py

Re-download the sources and compare hashes against the table above. The eCFR URL is pinned to issue date 2026-09-17; a later issue date may legitimately differ, and if it does, the dictionary needs rechecking rather than the hash being updated.

## What is not from a government source

The captions listed for the pre-2010 1100 series in `hud1-line-dictionary.md` -- "Settlement or Closing Fee," "Lien Letter Reimbursement," "Deed Prep Fee" -- are transcribed from the statements in `inputs/`, not from the appendix. The appendix says what a line is *for*; settlement software prints its own wording. That is exactly why `rules.md` makes the printed caption govern and the dictionary advisory.
