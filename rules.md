# Rules

How every translation runs. Follow the steps in order. The output shape is fixed by `reference/output-schema.md` and does not change to suit an input.

---

## 1. Take in the statement

Record, before mapping anything:

- **What you were given:** a PDF, extracted text, or pasted text
- **How many pages**
- **Whether the text is machine-extracted.** Extraction mangles spacing on HUD-1s. `NorthgateHoldings, LLC` and `CountyTaxes` are extraction artifacts, not the document. Transcribe them as they reached you and note the reading separately (see rule 3).

If you were given a PDF and cannot read it, say so and stop. Do not translate a statement you could not open.

## 2. Identify the vintage

Find the form stamp. Set the vintage per `reference/hud1-line-dictionary.md`.

If there is no stamp, infer from captions and **write that you inferred it**. If nothing distinguishes it, the vintage is `not in source` and every line is mapped on its printed caption alone.

The vintage never overrides a printed caption. It only tells a reader which dictionary column to read.

## 3. Transcribe before you map

Copy captions, names and payees **exactly as they appear**, including missing spaces, odd capitalisation and abbreviations.

Where an extraction artifact makes a value hard to read, the verbatim value comes first and the reading follows in parentheses, labelled:

    NorthgateHoldings, LLC (spacing as extracted; reads "Northgate Holdings, LLC")

Never silently correct a name. Never replace an abbreviation with its expansion. Never apply the spelling a name usually has.

This is the rule the whole contract rests on, so it is worth stating the failure it prevents: a translator that writes `Northgate Holdings, LLC` because that is how the company is normally styled has put a string in the output that is not in the input.

## 4. Map the statement to the schema

Work the schema in order, section 1 through section 6. For each field:

1. Find the line or lettered block the schema names.
2. If it carries a value, copy it and cite the line.
3. If it is blank, write `not in source`.

**Blank is not zero.** `[1024-A 5]` and the form's own note in `[Sec. C]` both treat an absent amount as absent. A blank line 504 does not mean the payoff was zero; it means the statement does not say.

**A caption governs its line.** If line 803 is captioned `Appraisal Fee`, it is an appraisal fee, whatever the current appendix says line 803 is for. Record the conflict in section 9 if the caption disagrees with the identified vintage.

**Outside-the-column amounts stay outside.** Lines 1109 and 1110 carry policy coverage, not charges. The itemizations beside 1201-1203 are disclosure. They go in the `Outside columns` cell and enter no total.

**P.O.C. items are reported and excluded from every sum** `[1024-A 5]`.

**Statement status is derived, and the rule is this one.** `final` if `[Sec. I]` prints a settlement date; `preliminary` if it does not. Write which test fired, e.g. `final -- a settlement date is present`. A date found only elsewhere (a page-3 block, a filename, a file number) does not count.

## 5. When a field has no source

Write exactly `not in source`.

Not "N/A." Not "none." Not "0.00." Not an empty cell. Not a dash.

`not in source` means: *the schema asked, the statement did not answer.* Anything else asserts something the statement did not say. "None" is a claim that there were none. `0.00` is a claim that the amount was zero. The statement made neither claim.

Every `not in source` is then listed again in section 8, so a reader sees the shape of what is missing without reading the whole sheet.

## 6. What to never add

A close-out sheet fails the moment it contains something the statement did not.

Never add:

- **A date** the statement did not print -- not from the file number, not from a nearby date, not from a filename, not from today
- **A payee** for a line whose payee field was blank
- **A zero** for a blank amount
- **A party's role** the statement did not assign
- **A county, municipality or ZIP** not printed in `[Sec. G]`
- **A spelling** other than the one that appeared
- **A total** the statement did not print -- unless it sits in the `Recomputed` column of section 7, with every operand cited in the `Expression` column
- **A characterisation**: "high," "customary," "standard," "unusual," "should be"
- **A fact from another statement**, including an earlier version of this same deal

If you know something about this property or these parties from outside the statement, it does not go in the sheet. Not in a note, not in parentheses, not in section 9.

## 7. Computing is allowed; inventing is not

Section 7 re-adds the form's own totals. That is derivation from cited operands, not invention, and it is the one place the output may contain a number that is not printed on the statement.

The rules for it:

- Every computed value goes in the `Recomputed` column of section 7 and nowhere else. That column is the marker; no `computed:` prefix is written. The `Expression` column beside it shows the operands.
- Every operand in the expression carries its line citation.
- An operand that is `not in source` makes the whole check `cannot check`. It is never treated as zero to make a sum work.
- P.O.C. amounts and outside-the-column amounts are excluded.
- Round nothing. Copy the digits as printed and add them as printed.

When a recomputed total differs from the stated total, write `differs by <amount>` and move on. Do not adjust, do not hunt for the missing line, do not suggest which figure is right. The difference is the finding.

## 8. Ambiguity goes to section 9, not into a cell

Send a row to **Could not map** when any of these is true:

- An amount has no caption, or a caption does not fix its meaning
- A disbursement points at an exhibit or attachment that is not in the input
- A caption conflicts with the identified vintage
- A payoff-looking item sits outside the 500 series `[3500-A 35]`
- The same figure appears twice with different values -- report both, cite both, pick neither
- A mark, a checkbox or a handwritten entry cannot be read
- An attachment is referenced but not supplied

Quote the item verbatim, cite its line, and give the reason in one clause. Do not resolve it.

## 9. Before you output, check your own work

Run the shape test in `reference/output-schema.md` and confirm each point:

1. Nine sections, correct headings, correct order
2. Every field in sections 1-3 present, each with a citation or `not in source`
3. Tables in sections 4-6 present, even if empty-bodied
4. Section 7 shows a result for every check
5. Section 8 ends with the four counts
6. Section 9 lists rows or says `Nothing unmapped.`
7. **Every number in the output is either cited or sits in the `Recomputed` column of section 7**

8. **Every name, date, cash direction and line placement matches the input.** A name or date must be the printed characters. A figure must sit on the line it is cited to. A cash direction is the box that carries the X. `python3 tools/trace_check.py` runs these checks.

Point 7 is the test that catches invention. Walk the finished sheet, take each number in turn, and find the line it came from. If one cannot be traced, delete it or move it to section 9. Do not ship it with a plausible citation attached.

## 10. What a reader gets

One close-out sheet. No cover note, no summary paragraph, no recommendation.

If the caller asked a question about the deal, answer it separately, after the sheet, clearly marked -- and answer it only from the sheet.
