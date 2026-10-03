# Settlement Statement Translator

A folder that turns Claude into a translator for **HUD-1 settlement statements**.

Give it the settlement statement from a closing. It gives back a **close-out sheet**: nine fixed sections, every figure carrying the line number it came from, every gap marked `not in source`, and the form's own arithmetic re-added so you can see whether it closes.

Same input kind in. Same nine sections out. Every time.

**It is not a summarizer, an analyst or an auditor.** It does not tell you whether a fee was high or a deal was good. It converts a document into a structure, and it says what it could not map.

## Who does this by hand today

Everyone who touches a closing.

A real estate investor reads the settlement statement line by line to work out what they actually paid beyond the purchase price. A transaction coordinator copies payoffs and liens into a file. A bookkeeper turns it into journal entries. A seller's agent checks that the net matches what was promised. A paralegal confirms the recording fees and transfer stamps.

It is fifteen to forty minutes a closing, it is pure transcription, and it gets skipped when things are busy -- which is the point at which a lien on line 507 or a $6,000 disbursement pointing at an exhibit nobody attached goes through unread.

## Why a HUD-1 and not something looser

Because the output can be checked.

Every row on a HUD-1 has a number. The instructions for those numbers are published by the federal government, they ship in `reference/`, and the form states its own totals -- so a translator's arithmetic can be re-added by anyone holding the same page.

There is no judgement call in "line 504 says 112,480.36." Either the sheet says that, with that citation, or it is wrong.

## The thing this gets right that most tools get wrong

**There are two different forms called the HUD-1, and they use the same line numbers for different things.**

| Line | Pre-2010 form | 2010-and-later form |
|---|---|---|
| 801 | Loan Origination Fee | "Our origination charge" |
| 803 | Appraisal Fee | "Your adjusted origination charges" |
| 1101 | the settlement agent's fee | "Title services and lender's title insurance" |

The 2010 form came out of the 2008 RESPA rule. The older one is still what you get on a cash purchase or a commercial deal -- which is most of what an investor signs. Every statement in `inputs/` is the older form.

So this translator treats the **line number as a citation anchor** and the **printed caption as the meaning**. A tool that maps by line number alone will read an appraisal fee as a net origination charge and never mention it.

Both versions of the instructions are in `reference/`, as the government published them. `reference/SOURCE.md` shows where they came from and how to verify them.

## What's in the folder

| File | Job |
|---|---|
| `identity.md` | What it converts, from what, to what, and what it refuses to do |
| `rules.md` | The mapping, in order: transcription, what to do with a gap, what to never add, when to compute, what goes to "could not map" |
| `examples.md` | Three worked pairs, with what a summarizer would have written instead |
| `reference/output-schema.md` | **The contract.** The nine sections, every field, and the shape test |
| `reference/hud1-line-dictionary.md` | What each line means, on both vintages, with the traps |
| `reference/SOURCE.md` | Provenance, SHA-256 fingerprints, how to re-verify |
| `reference/*-official.xml` | The two appendices exactly as the government serves them |
| `inputs/` | Four statements to run it against, and a note on what is real and what was changed |
| `outputs/` | The four finished close-out sheets |
| `tools/trace_check.py` | Traces every figure, name, date, cash direction and line placement in a sheet back to the statement. Has a self-test (12 injected failures) |
| `tools/extract_hud.py` | Your own PDF to the text format the translator reads |
| `tools/convert_appendix.py` | Regenerates the citable markdown from the official XML |

## How to use it

### In a Claude Project

1. Create a project. Add `identity.md`, `rules.md`, `examples.md`, `reference/output-schema.md` and `reference/hud1-line-dictionary.md` to its knowledge. The XML files are optional -- they are there for people checking the work.
2. Paste this into the project instructions:

   > You are the translator described in identity.md. Follow rules.md step by step and produce the output defined in reference/output-schema.md. Every value carries a line citation or says "not in source." See examples.md for the expected depth and format.

3. Start a chat and paste in a settlement statement.

### In Claude Code

Open this folder and say:

> Read identity.md and rules.md, then translate `inputs/02-purchase-with-prorations.txt`.

### With your own statement

```
python tools/extract_hud.py "C:\path\to\your_statement.pdf" -o inputs/05-my-deal.txt
```

Then translate `inputs/05-my-deal.txt` the same way. The extractor deliberately does not tidy the text -- run-together words like `CountyTaxes` are what the PDF produced, and the translator is required to transcribe them as they arrive.

## Checking that it did not make anything up

That is the whole claim, so it ships with the test.

```
python tools/trace_check.py
```

Every dollar figure in each sheet must be a figure the input prints -- matched on whole tokens, so `2.00` cannot pass by hiding inside `1,412.00`. Every `[L###]` must be a line the input actually shows. Every expression in section 7 is re-evaluated. The nine headings must be present and in order.

Current state of the four shipped pairs:

```
PAIR: 01-cash-purchase-prelim.md      sections 9  figures  67  citations 50  expressions  7  PASS
PAIR: 02-purchase-with-prorations.md  sections 9  figures  73  citations 51  expressions  6  PASS
PAIR: 03-cash-purchase-alt-layout.md  sections 9  figures  67  citations 50  expressions  7  PASS
PAIR: 04-seller-side-payoffs.md       sections 9  figures 116  citations 58  expressions 12  PASS

OVERALL: PASS -- 4 pair(s), every figure traced to source
```

A checker that only ever says PASS proves nothing, so it also injects four failures into a passing sheet and confirms each is caught:

```
python tools/trace_check.py --selftest
```

```
invented figure      caught
dangling citation    caught
bad arithmetic       caught
dropped section      caught
SELFTEST: PASS -- all 4 injected failures were caught
```

## What it does when the statement is incomplete

Nothing clever. That is the design.

- A blank line is **`not in source`**, never `0.00` and never "none." A blank line and a zero are different facts about a closing.
- A missing settlement date does not become the date in the file number. `inputs/01` has no settlement date, so the sheet calls it **preliminary** and says why.
- An arithmetic check with a missing operand is **`cannot check`**, not a sum with a plausible number filled in. On `inputs/02` the entire seller side is empty, so six checks resolve that way and the sheet says so.
- A total that does not add up is **reported, not repaired**. On `inputs/04` the seller column adds to 14,308.00 against a stated 14,310.00. The sheet reports the two-dollar difference and does not decide which is right.
- Anything the schema has no home for goes to **section 9**, quoted and cited. A 6,000.00 disbursement pointing at an exhibit that was not supplied is named there rather than dropped.

## Limits worth knowing

- **It reads text, not pictures.** A scanned statement needs OCR first, and OCR errors will be transcribed faithfully, because the translator cannot tell a bad scan from a bad typist.
- **Text extraction loses column position.** On `inputs/04` a single address sits under two names and cannot be assigned to the buyer or the seller, so both address fields are `not in source` and section 9 explains why. Someone holding the PDF can settle it in a second.
- **It is built for the HUD-1.** A TRID Closing Disclosure, an ALTA settlement statement or a state-specific form has different anchors. The method carries over; this folder's line dictionary does not.
- **It is not advice.** A close-out sheet is a faithful restatement of a document. What to do about anything on it is a question for your attorney, your title company or your accountant.

## Not a translator's job

If a sheet ever tells you a fee looks high, a payoff seems wrong, or a deal was good, something has gone wrong with it. That is analysis, it requires knowledge from outside the statement, and the moment it enters the output the sheet stops being checkable.

The job is fidelity. Nothing invented, nothing silently dropped, same shape every time.
