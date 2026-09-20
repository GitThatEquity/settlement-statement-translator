# Output schema: the Close-Out Sheet

This is the contract. A close-out sheet has **nine sections, always, in this order**, whatever the input looked like.

If the input was three pages or one. If the deal was a cash purchase or a financed sale. If half the form was blank. Nine sections, same order, same field names.

---

## Notation used in every section

| Token | Meaning |
|---|---|
| `[L303]` | A numbered line on the statement. The citation anchor. |
| `[Sec. G]` | A lettered block in the header. |
| `not in source` | The schema asks for this; the statement does not answer it. **Required value. Never leave a field blank, never guess.** |
| `computed:` | A value this translator derived. Must be followed by the expression, with every operand cited. |
| `P.O.C.` | Paid outside closing. Reported, never added into a total `[1024-A 5]`. |
| `verbatim` | Reproduce the characters as printed, including odd spacing and abbreviations. |

**Every value in sections 1 through 6 carries a citation or says `not in source`.** There is no third option.

A number that appears in the output and is neither cited nor marked `computed:` is a defect.

---

## Section 1. Statement identity

| Field | Source | Notes |
|---|---|---|
| Form vintage | see `hud1-line-dictionary.md` | `pre-2010`, `2010-and-later`, or `not in source`. If inferred from captions rather than a stamp, write `pre-2010 (inferred from captions)`. |
| Form stamp | verbatim | e.g. `1.0 3/98`, `HUD-1 (3-86) RESPA, HB4305.2` |
| File number | `[Sec. B]` | |
| Loan number | `[Sec. B]` | |
| Mortgage insurance case number | `[Sec. B]` | |
| Type of loan | `[Sec. B]` | Only if a box is marked. An unmarked row of options is `not in source`. |
| Settlement date | `[Sec. I]` | |
| Statement status | derived, stated rule | `final` if a settlement date is present; `preliminary` if not. Say which test fired. |
| Settlement agent | `[Sec. H]` verbatim | |
| Settlement agent TIN | `[Sec. H]` | |
| Place of settlement | `[Sec. H]` verbatim | |
| Pages in source | count | |

## Section 2. Parties and property

| Field | Source |
|---|---|
| Borrower | `[Sec. D]` verbatim |
| Borrower address | `[Sec. D]` verbatim |
| Seller | `[Sec. E]` verbatim |
| Seller address | `[Sec. E]` verbatim |
| Lender | `[Sec. F]` verbatim |
| Property location | `[Sec. G]` verbatim |
| County | `[Sec. G]` |

Names are transcribed as printed. If extraction produced `DoulosConsulting, LLC` with the space missing, that is what the field says. A normalized reading may be added in parentheses **after** the verbatim value, labelled: `DoulosConsulting, LLC (spacing as extracted; reads "Doulos Consulting, LLC")`.

## Section 3. Price and cash movement

| Field | Line |
|---|---|
| Contract sales price, borrower side | `[L101]` |
| Contract sales price, seller side | `[L401]` |
| Settlement charges to borrower | `[L103]` |
| Settlement charges to seller | `[L502]` |
| Gross amount due from borrower | `[L120]` |
| Total paid by or for borrower | `[L220]` |
| Cash at settlement, borrower | `[L303]` |
| Cash direction, borrower | `[L303]` checkbox: `FROM borrower`, `TO borrower`, or `not in source` |
| Gross amount due to seller | `[L420]` |
| Total reductions in amount due seller | `[L520]` |
| Cash at settlement, seller | `[L603]` |
| Cash direction, seller | `[L603]` checkbox: `TO seller`, `FROM seller`, or `not in source` |

Direction is read from the mark. It is never inferred from whether a number is positive.

## Section 4. Payoffs, liens and seller obligations

A table of **lines 501 through 509**. One row per line that carries a caption, an amount, or both.

Lines 510-519 are prorations and belong to section 6, not here. Line 502 appears both here and in section 3; that is intended, and both carry the same citation.

| Column | Rule |
|---|---|
| Line | `[L504]` etc. |
| Caption as printed | verbatim |
| Payee | verbatim, or `not in source` |
| Amount | as printed, or `not in source` |
| Note | `P.O.C.`, `caption present, no amount`, or empty |

**A caption with no amount still gets a row.** `504. Payoff First Mortgage` printed with an empty amount means the form contemplated a payoff and none was entered. That is a fact about the statement and it belongs in the output.

If no 500-series line carries a caption or an amount, the section reads: `No 500-series entries in source.`

## Section 5. Settlement charges

A table of section L, 700 through 1400. One row per line that carries a caption, a payee or an amount.

| Column | Rule |
|---|---|
| Line | `[L1101]` etc. |
| Caption as printed | verbatim |
| Payee | verbatim, or `not in source` |
| Borrower column | amount, or `not in source` |
| Seller column | amount, or `not in source` |
| Outside columns | amount printed outside both columns, or empty |

Blank lines that the form prints but nobody filled in are **omitted** from this table -- with one exception: if a blank line's caption is itself informative about the deal (a printed `Payoff First Mortgage` on 504, a printed `Commission Paid at Settlement` on 703), it appears with `caption present, no amount`. Section 8 records the omission count so the reader knows how many lines were dropped as empty.

## Section 6. Prorations and adjustments

A table of lines 106-112, 210-219, 406-412 and 510-519.

| Column | Rule |
|---|---|
| Line | `[L106]` etc. |
| Caption as printed | verbatim |
| Period from | as printed, or `not in source` |
| Period to | as printed, or `not in source` |
| Amount | as printed, or `not in source` |
| Side | `borrower` or `seller`, from which section the line sits in |

Do not compute a daily rate, a per-diem, or a "days elapsed." Those are not on the form. If a period is printed as `12/03/25 to 01/01/26`, both endpoints are copied and nothing is calculated from them.

## Section 7. Arithmetic checks

The form states its own totals. This section re-adds them and reports whether the stated total matches.

Run every check that the input supports. Each row:

| Column | Rule |
|---|---|
| Check | Plain name, e.g. `Line 120 = sum of 101-112` |
| Expression | Operands with citations, e.g. `[L101] 25,000.00 + [L103] 2,032.75` |
| Recomputed | The result |
| Stated | The figure printed on the line |
| Result | `agrees`, `differs by <amount>`, or `cannot check` |

The standing checks:

1. `[L120]` equals the sum of `[L101]` through `[L112]`
2. `[L220]` equals the sum of `[L201]` through `[L219]`
3. `[L303]` equals `[L301]` minus `[L302]` `[3500-A 28]`
4. `[L420]` equals the sum of `[L401]` through `[L412]`
5. `[L520]` equals the sum of `[L501]` through `[L519]`
6. `[L603]` equals `[L601]` minus `[L602]`
7. `[L103]` equals the borrower column of `[L1400]` `[3500-A 17]`
8. `[L502]` equals the seller column of `[L1400]` `[3500-A 31]`
9. `[L1400]` borrower column equals the sum of the borrower column, 700-1305
10. `[L1400]` seller column equals the sum of the seller column, 700-1305
11. `[L301]` equals `[L120]`, and `[L302]` equals `[L220]` `[3500-A 27]`
12. `[L601]` equals `[L420]`, and `[L602]` equals `[L520]` `[3500-A 38]`

`cannot check` is the correct result whenever an operand is `not in source`. It is not a failure of the translator, and it is never resolved by supplying a plausible number.

P.O.C. amounts are excluded from every sum `[1024-A 5]`. Amounts printed outside the columns are excluded from column sums.

**A check that differs is reported, not fixed.** The statement is the source. If the form's own arithmetic does not close, that is the single most useful thing this sheet can tell a reader.

## Section 8. Not in source

A plain list of every schema field above that resolved to `not in source`, grouped by section.

Close with the counts:

- Fields requested by the schema: `<n>`
- Fields answered from the statement: `<n>`
- Fields `not in source`: `<n>`
- Blank form lines omitted from section 5: `<n>`

## Section 9. Could not map

Everything present in the input that the schema has no home for, or that the schema cannot resolve without a judgment call. One row each, quoted verbatim, with a citation and a reason.

This section exists because a close-out sheet that silently drops something is worse than one that admits it. Typical entries:

- An amount with no caption, or a caption whose meaning the form does not fix
- A blind disbursement, e.g. `1305. See addit'l disb. exhibit  6,000.00`, where the exhibit is not in the input
- A caption that conflicts with the identified form vintage
- A payoff-looking item outside the 500 series `[3500-A 35]`
- Handwriting, a stamp, a signature block, or an attachment referenced but not supplied
- Any figure that appears twice with different values

If there is nothing to report: `Nothing unmapped.`

---

## The shape test

A close-out sheet is well formed when all of the following hold:

1. Nine sections, these headings, this order.
2. Every field in sections 1-3 is present, with a citation or `not in source`.
3. Every table in sections 4-6 exists, even if its body reads `No 500-series entries in source.`
4. Section 7 lists every check with a result of `agrees`, `differs by`, or `cannot check`.
5. Section 8 ends with the four counts.
6. Section 9 lists rows or says `Nothing unmapped.`
7. No number appears anywhere without a citation or a `computed:` expression.

Point 7 is the one the whole thing rests on.
