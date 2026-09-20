# Examples

Three worked pairs. Each shows a fragment of the input and the fragment of the close-out sheet it produced, with a note on what a summarizer would have written instead.

The complete sheets for all four inputs are in `outputs/`.

---

## Example 1 -- the blank line that is not a zero

**From `inputs/01-cash-purchase-prelim.txt`:**

```
500. REDUCTIONSIN AMOUNTDUETOSELLER:
501. Excess Deposit(See Instructions)
502. Settlement Chargesto Seller(Line 1400)
503. Existing loan(s) taken subject to
504. Payoff FirstMortgage
505. Payoff Second Mortgage
506.
...
520. TOTAL REDUCTION AMOUNTDUESELLER
```

Every one of those lines is empty. The form printed the captions; the settlement agent filled in nothing.

**Section 4 of the sheet:**

| Line | Caption as printed | Payee | Amount | Note |
|---|---|---|---|---|
| `[L501]` | `Excess Deposit(See Instructions)` | not in source | not in source | caption present, no amount |
| `[L502]` | `Settlement Chargesto Seller(Line 1400)` | not in source | not in source | caption present, no amount |
| `[L503]` | `Existing loan(s) taken subject to` | not in source | not in source | caption present, no amount |
| `[L504]` | `Payoff FirstMortgage` | not in source | not in source | caption present, no amount |
| `[L505]` | `Payoff Second Mortgage` | not in source | not in source | caption present, no amount |

**What this pair is showing.** The captions are transcribed with their extraction damage intact -- `Chargesto`, `FirstMortgage` -- because `rules.md` rule 3 says the characters that arrived are the characters that get recorded.

Lines 506 through 509 print with neither caption nor amount, so they are named in a sentence rather than given empty rows. The schema keeps a row when the form said something; it drops one when the form said nothing at all.

**What a summarizer would have written:** `Payoffs: none` or `Payoffs: $0.00`. Both are claims. The statement made neither. It left five lines blank, and a blank line and a zero are different facts about a closing -- one says nothing was owed, the other says nobody filled it in.

And on this statement the distinction has consequences: `[L520]` is also blank, so six of the fourteen arithmetic checks resolve to `cannot check`. A sheet that had quietly written zeros would have "verified" a seller side that was never filled in.

---

## Example 2 -- same deal, two layouts, same shape

`inputs/01` and `inputs/03` are the **same settlement statement**, put through two different PDF text extractors. Compare the header block.

**From `inputs/01-cash-purchase-prelim.txt`:**

```
D. NAME AND ADDRESS OF BORROWER: E. NAME AND ADDRESS OF SELLER: ...
NorthgateHoldings, LLC Ruth E. Calloway
```

**From `inputs/03-cash-purchase-alt-layout.txt`:**

```
D. NAME AND ADDRESS OF BORROWER: E. NAME AND ADDRESS OF SELLER: F. NAME AND ADDRESS OF LENDER: Northgate Holdings,
LLC Ruth E. Calloway
```

Three pages in one, four in the other. Word spacing collapsed in one, preserved in the other. The name even breaks across a line.

**Section 2, from each sheet:**

| Field | From `01` | From `03` |
|---|---|---|
| Borrower | `NorthgateHoldings, LLC` (spacing as extracted; reads "Northgate Holdings, LLC") | `Northgate Holdings, LLC` |
| Seller | `Ruth E. Calloway` | `Ruth E. Calloway` |
| Property location | `118 Ridge Avenue / Fairview, PA 19041` | `118 Ridge Avenue / Fairview, PA 19041` |

**And the money, which does not move at all:**

| Field | From `01` | From `03` |
|---|---|---|
| Contract sales price `[L101]` | 25,000.00 | 25,000.00 |
| Gross due from borrower `[L120]` | 27,032.75 | 27,032.75 |
| Cash at settlement `[L303]` | 26,932.75, FROM borrower | 26,932.75, FROM borrower |
| Section L column total `[L1400]` | 2,032.75, agrees | 2,032.75, agrees |
| Fields answered / `not in source` | 22 / 9 | 22 / 9 |

**What this pair is showing.** The two sheets are identical except where the *input* genuinely differed: the page count, and the spacing of names. The verbatim rule means the transcription follows the input, and the field-level counts confirm the shape did not drift -- same 31 fields requested, same 22 answered, same 9 missing, same 41 blank Section L lines dropped.

Where `01` needed a parenthetical to record that the spacing was damaged, `03` did not, because `03`'s extractor did not damage it. Neither sheet corrected the other.

---

## Example 3 -- the total that does not add up

**From `inputs/04-seller-side-payoffs.txt`:**

```
703. Commission Paid at Settlement 11,100.00
1101. Settlement orClosing Fee to Cornerstone Settlement & Abstract, Inc. 425.00
1102. Notary/WireFees to Cornerstone Settlement & Abstract, Inc. 175.00
1103. Lien LetterReimbursement to Cornerstone Settlement & Abstract, Inc. 185.00
1104. Deed Prep Fee to Cornerstone Settlement & Abstract, Inc. 250.00
1201. Recording Fees: Deed $ 117.25; Mortgage $ ; Releases $ 98.00 117.25 98.00
1203. State Tax/Stamps: Deed 1,850.00;Mortgage 1,850.00
1302. Pest Inspection to ApexPest Control [POC (seller)] 175.00
1303. Release/Reimbursement Fee to Brightwater LLC 225.00
1400. TOTAL SETTLEMENTCHARGES ... 3,379.25 14,310.00
```

**Section 7 of the sheet, the row that matters:**

| Check | Expression | Recomputed | Stated | Result |
|---|---|---|---|---|
| `[L1400]` seller col = sum of seller column | `[L703]` 11,100.00 + `[L1101]` 425.00 + `[L1102]` 175.00 + `[L1103]` 185.00 + `[L1104]` 250.00 + `[L1201]` 98.00 + `[L1203]` 1,850.00 + `[L1303]` 225.00 | 14,308.00 | 14,310.00 | **differs by 2.00** |

**What this pair is showing.**

The P.O.C. item is excluded. `1302` carries 175.00 marked `[POC (seller)]`, and `[1024-A 5]` says P.O.C. items "must not be included in computing totals." It appears in section 5 with its own row and a `P.O.C.` marker, and it stays out of the sum.

The difference is reported, not repaired. Two dollars. Nobody catches that by eye, and the sheet does not decide which figure is right -- it says the column adds to 14,308.00 and the form says 14,310.00, and stops.

The sheet also says why the other checks passed anyway:

> Note that the stated 14,310.00 carries forward into `[L502]`, and from there into `[L520]` and `[L603]`. Every check that consumes the stated figure agrees, because they all consume the same stated figure. Only the check that re-adds the column disagrees.

**What a summarizer would have written:** `Total seller charges: $14,310.00`. True to the form, and it would have carried the discrepancy silently into the seller's net.

---

## The property all three share

Every figure above appears in the input it came from. The only exception is `14,308.00`, which is a sum of eight cited operands, and `2.00`, which is the difference between that sum and the stated figure -- both in section 7, both marked as derived.

`tools/trace_check.py` enforces exactly that, on whole-token matching, across all four pairs:

```
OVERALL: PASS -- 4 pair(s), every figure traced to source
```
