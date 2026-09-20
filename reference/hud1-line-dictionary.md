# HUD-1 line dictionary

What each numbered line on a HUD-1 settlement statement means, and **which vintage of the form you are looking at**.

This file is the input side of the contract. `output-schema.md` is the output side.

---

## Why this file exists: there are two HUD-1s

Two different forms are both called "the HUD-1," both carry OMB number 2502-0265, and **they use the same line numbers for different things**.

| Line | Pre-2010 form says | 2010-and-later form says |
|---|---|---|
| 801 | Loan Origination Fee `[3500-A 55]` | "Our origination charge" `[1024-A 47]` |
| 803 | Appraisal Fee (printed caption) | "Your adjusted origination charges" `[1024-A 51]` |
| 1101 | the settlement agent's fee `[3500-A 63]` | "Title services and lender's title insurance" `[1024-A 67]` |
| 1103 | title examination `[3500-A 64]` | owner's title insurance `[1024-A 69]` |

The 2010 form came out of HUD's 2008 RESPA rule. The pre-2010 form is still in everyday use for **cash purchases, commercial deals and other transactions outside that rule** -- which is most of what an investor signs.

**Consequence for this translator:** a line number alone does not tell you what a line means. Line 803 is an appraisal fee on one form and a net origination charge on the other. Mapping by line number alone will confidently mislabel real money.

So:

- The **line number is the citation anchor.** It is how a reader finds the row again.
- The **caption printed next to it governs the meaning.** Transcribe it verbatim and let it decide which output field the row belongs to.
- The vintage is **evidence, not authority.** If a printed caption disagrees with the vintage you identified, report the caption and record the conflict. Do not relabel the row to match the dictionary.

## Identifying the vintage

Look for a form stamp, usually at the foot of page 1 or in the header block:

| Stamp seen on real statements | Vintage |
|---|---|
| `HUD-1 (3-86) RESPA, HB4305.2` | pre-2010 |
| `1.0 3/98` | pre-2010 (software version stamp on a 3-86 layout) |
| `HUD-1 (3-10)` | 2010-and-later |

If no stamp is present, infer from captions -- a statement whose line 1101 reads "Settlement or Closing Fee" is pre-2010 -- and **say that you inferred it**. If neither a stamp nor a distinguishing caption is present, the vintage is `not in source`.

---

## Section A-I: the header block

Lettered, not numbered. Cite these as `[Sec. A]` through `[Sec. I]`.

| Key | What it holds |
|---|---|
| `[Sec. B]` | Type of loan; file number, loan number, mortgage insurance case number |
| `[Sec. C]` | The form's own note, including the P.O.C. sentence |
| `[Sec. D]` | Name and address of borrower |
| `[Sec. E]` | Name and address of seller |
| `[Sec. F]` | Name and address of lender |
| `[Sec. G]` | Property location |
| `[Sec. H]` | Settlement agent, agent TIN, place of settlement |
| `[Sec. I]` | Settlement date |

A cash purchase usually leaves `[Sec. F]` empty. That is normal, and it is reported as `not in source` -- never as "none" or "cash deal."

---

## Section J: summary of borrower's transaction (100-303)

| Line | Meaning | Cite |
|---|---|---|
| 101 | Contract sales price, excluding separately priced personal property | `[3500-A 15]` |
| 102 | Personal property priced separately from 101 | `[3500-A 16]` |
| 103 | Total settlement charges to borrower, carried from line 1400 | `[3500-A 17]`, `[1024-A 20]` |
| 104-105 | Other amounts owed by the borrower | `[3500-A 18]` |
| 106-112 | Items the **seller paid in advance** that the borrower reimburses (taxes, assessments) | `[3500-A 19]` |
| 120 | Total of lines 101 through 112 | `[3500-A 20]` |
| 201 | Deposit or earnest money paid before settlement | `[3500-A 21]` |
| 202 | Principal of the new loan | `[3500-A 22]` |
| 203 | Existing loan the borrower takes title subject to | `[3500-A 23]` |
| 204-209 | Other items paid by or for the borrower, incl. seller credits and seller financing | `[3500-A 24]` |
| 210-219 | Items **unpaid by the seller** attributable to a pre-settlement period | `[3500-A 25]` |
| 220 | Total of lines 201 through 219 | `[3500-A 26]` |
| 301 | Carried from line 120 | `[3500-A 27]` |
| 302 | Carried from line 220 | `[3500-A 27]` |
| 303 | Cash at settlement. **Direction is a checkbox: FROM or TO the borrower** | `[3500-A 28]` |

On 303 the instruction is explicit: "Subtract Line 302 from Line 301 ... The appropriate box should be checked" `[3500-A 28]`. The direction is read from the mark, not assumed from the arithmetic.

## Section K: summary of seller's transaction (400-603)

| Line | Meaning | Cite |
|---|---|---|
| 401-412 | Mirror of 101-112 on the seller's side | `[3500-A 29]` |
| 420 | Total of lines 401 through 412 | `[3500-A 29]` |
| 501 | Excess deposit held by a broker who is not the settlement agent | `[3500-A 30]` |
| 502 | Total settlement charges to seller, carried from line 1400 | `[3500-A 31]`, `[1024-A 34]` |
| 503 | Existing loan taken subject to, deducted from the price | `[3500-A 32]` |
| 504-505 | **Payoff of first and second loans, including accrued interest** | `[3500-A 33]` |
| 506-509 | Deposits, **additional liens that must be paid off to clear title**, other seller obligations, utility holdbacks | `[3500-A 34]`, `[3500-A 35]`, `[1024-A 38]` |
| 510-519 | Items unpaid by the seller, same basis as 210-219 | `[3500-A 36]` |
| 520 | Total of lines 501 through 519 | `[3500-A 37]` |
| 601 | Carried from line 420 | `[3500-A 38]` |
| 602 | Carried from line 520 | `[3500-A 38]` |
| 603 | Cash at settlement. **Direction is a checkbox: TO or FROM the seller** | `[3500-A 38]` |

**Lines 504-509 are the lien block.** Mortgage payoffs, judgments, municipal liens and other title-clearing payments appear here. Both vintages say 506-509 "may be used to list additional liens which must be paid off through the settlement to clear title to the property" `[3500-A 35]`, `[1024-A 38]`.

The pre-2010 text adds a placement rule: "Other payoffs of Seller obligations should be shown on Lines 506-509 (but not on Lines 1303-1305)" `[3500-A 35]`. A payoff-looking item sitting in the 1300 series is therefore worth recording as printed and noting as ambiguous -- but the caption still governs, and this translator does not decide that a fee is really a payoff.

## Section L: settlement charges (700-1400)

Two columns: paid from borrower's funds, paid from seller's funds. An amount printed **outside** the columns is disclosure only and is not part of a column total.

| Series | Covers | Cite |
|---|---|---|
| 700 | Real estate commission and its division | `[3500-A 39]` |
| 800 | Items payable in connection with the loan. **Captions differ by vintage -- see the table at the top** | `[3500-A 55]` / `[1024-A 47]` |
| 900 | Items the lender requires paid in advance (prepaid interest, insurance premiums) | `[3500-A 58]` |
| 1000 | Reserves deposited with the lender (escrow) | `[3500-A 59]` |
| 1100 | Title charges, attorney fees, settlement agent fees, notary | `[3500-A 62]`, `[1024-A 66]` |
| 1200 | Government recording and transfer charges | `[3500-A 70]` |
| 1300 | Additional settlement charges (survey, pest inspection, blank lines) | `[3500-A 73]` |
| 1400 | **Total settlement charges, the sum of each column** | `[1024-A 84]` |

Line 1400 ties the form together: it feeds line 103 on the borrower's side and line 502 on the seller's side.

### The 1100 series on a pre-2010 form

Captions as printed on real pre-2010 statements, which do not match the current appendix:

| Line | Printed caption | Current appendix calls this line |
|---|---|---|
| 1101 | Settlement or Closing Fee | "Title services and lender's title insurance" |
| 1102 | Notary / Wire / Overnight Fees | abstract or title search |
| 1103 | Lien Letter Reimbursement | owner's title insurance |
| 1104 | Deed Prep Fee | title insurance binder |
| 1107 | Attorney's Fees | |
| 1108 | Title Insurance | amount retained by the title underwriter |
| 1109 | Lender's Coverage (amount, outside columns) | |
| 1110 | Owner's Coverage (amount, outside columns) | |

Lines 1109 and 1110 hold **policy coverage amounts, not charges.** They print outside the columns. Reading a coverage amount as a fee is a mapping error, and a large one -- an owner's coverage figure is usually the entire purchase price.

---

## Traps this dictionary exists to prevent

1. **Blank is not zero.** A caption with no amount means the amount is `not in source`. A HUD-1 prints every line whether or not it is used, so most lines on any real statement are blank.
2. **P.O.C. items are not in the totals.** The form's own note says items marked "[POC]" "were paid outside the closing ... and are not included in the totals," and the appendix agrees: P.O.C. items "must not be included in computing totals" `[1024-A 5]`. Report them, mark them, keep them out of every sum.
3. **Outside-the-column amounts are not charges.** Coverage amounts on 1109/1110, and the itemizations printed beside 1201-1203, sit outside the columns on purpose.
4. **Direction is a checkbox.** Lines 303 and 603 each have FROM and TO boxes. Read the mark.
5. **A prelim is not a final.** A statement with no settlement date filled in is a preliminary figure sheet. Say which one you were handed; never infer the date from a file number or a nearby date.
6. **The same line number means different things on different vintages.** This is the whole reason for this file.
