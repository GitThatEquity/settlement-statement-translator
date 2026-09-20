# Close-Out Sheet -- 26-0118

Source: `inputs/04-seller-side-payoffs.txt`

---

## 1. Statement identity

| Field | Value | Source |
|---|---|---|
| Form vintage | pre-2010 | form stamps |
| Form stamp | `1.0 3/98` (page 1 header) and `HUD-1 (3-86) RESPA, HB4305.2` (foot of page 1) | page 1 |
| File number | 26-0118 | `[Sec. B]` |
| Loan number | not in source | `[Sec. B]` |
| Mortgage insurance case number | not in source | `[Sec. B]` |
| Type of loan | not in source | `[Sec. B]` -- the five options print, none is marked |
| Settlement date | `March 14, 2026` | `[Sec. I]` |
| Statement status | final | a settlement date is present |
| Settlement agent | `Cornerstone Settlement & Abstract, Inc.` | `[Sec. H]` |
| Settlement agent TIN | 99-1234567 | `[Sec. H]` |
| Place of settlement | `220 Ellison Court Suite 310 / Brookvale,PA 15012` (spacing as extracted) | `[Sec. H]` |
| Pages in source | 2 | |

## 2. Parties and property

| Field | Value | Source |
|---|---|---|
| Borrower | `Fallbrook Property Group, LLC` | `[Sec. D]` |
| Borrower address | not in source | see section 9 |
| Seller | `Dennis R. Ashby` | `[Sec. E]` |
| Seller address | not in source | see section 9 |
| Lender | not in source | `[Sec. F]` empty |
| Property location | `84 Tanner Mill Road / Westbrook, PA 19023` | `[Sec. G]` |
| County | `Hartley County, Pennsylvania` | `[Sec. G]` |

## 3. Price and cash movement

| Field | Value | Line |
|---|---|---|
| Contract sales price, borrower side | 185,000.00 | `[L101]` |
| Contract sales price, seller side | 185,000.00 | `[L401]` |
| Settlement charges to borrower | 3,379.25 | `[L103]` |
| Settlement charges to seller | 14,310.00 | `[L502]` |
| Gross amount due from borrower | 188,379.25 | `[L120]` |
| Total paid by or for borrower | 5,000.00 | `[L220]` |
| Cash at settlement, borrower | 183,379.25 | `[L303]` |
| Cash direction, borrower | FROM borrower | `[L303]`, X in the FROM box |
| Gross amount due to seller | 185,000.00 | `[L420]` |
| Total reductions in amount due seller | 142,272.30 | `[L520]` |
| Cash at settlement, seller | 42,727.70 | `[L603]` |
| Cash direction, seller | TO seller | `[L603]`, X in the TO box |

## 4. Payoffs, liens and seller obligations

| Line | Caption as printed | Payee | Amount | Note |
|---|---|---|---|---|
| `[L501]` | `Excess Deposit(See Instructions)` | not in source | not in source | caption present, no amount |
| `[L502]` | `Settlement Chargesto Seller(Line 1400)` | not in source | 14,310.00 | |
| `[L503]` | `Existing loan(s) taken subject to` | not in source | not in source | caption present, no amount |
| `[L504]` | `Payoff FirstMortgage` | not in source | 112,480.36 | |
| `[L505]` | `Payoff Second Mortgage` | not in source | not in source | caption present, no amount |
| `[L506]` | `Payoff Municipal Lien - Westbrook Boro Water` | not in source | 3,218.44 | |
| `[L507]` | `Payoff Judgment - Docket 2023-04417` | not in source | 9,650.00 | |

Lines 508 and 509 print with neither caption nor amount.

No payee is named on any 500-series line. The captions on `[L506]` and `[L507]` name a lienholder and a docket number inside the caption text; they are reproduced above as printed and are not split into a payee field, because the form's payee position is empty.

## 5. Settlement charges

| Line | Caption as printed | Payee | Borrower column | Seller column | Outside columns |
|---|---|---|---|---|---|
| `[L700]` | `TOTAL COMMISSION Basedon Price $ 185,000.00 @ 6 %` | not in source | not in source | not in source | 185,000.00 and 6 % |
| `[L701]` | `$ 5,550.00 to` | `Harbor Point Realty` | not in source | not in source | 5,550.00 |
| `[L702]` | `$ 5,550.00 to` | `Lakeside RealtyGroup` | not in source | not in source | 5,550.00 |
| `[L703]` | `Commission Paid at Settlement` | not in source | not in source | 11,100.00 | |
| `[L1101]` | `Settlement orClosing Fee` | `Cornerstone Settlement & Abstract, Inc.` | not in source | 425.00 | |
| `[L1102]` | `Notary/WireFees` | `Cornerstone Settlement & Abstract, Inc.` | not in source | 175.00 | |
| `[L1103]` | `Lien LetterReimbursement` | `Cornerstone Settlement & Abstract, Inc.` | not in source | 185.00 | |
| `[L1104]` | `Deed Prep Fee` | `Cornerstone Settlement & Abstract, Inc.` | not in source | 250.00 | |
| `[L1108]` | `Title Insurance` ... `Sale Rate` | `Meridian National Title Insurance Co.` | 1,412.00 | not in source | |
| `[L1109]` | `Lender'sCoverage $` | not in source | not in source | not in source | |
| `[L1110]` | `Owner'sCoverage $` | not in source | not in source | not in source | 185,000.00 and 1,412.00 -- see section 9 |
| `[L1201]` | `Recording Fees: Deed $ 117.25; Mortgage $ ; Releases $ 98.00` | not in source | 117.25 | 98.00 | Deed 117.25; Releases 98.00 |
| `[L1202]` | `City/CountyTax/Stamps: Deed 1,850.00;Mortgage` | not in source | 1,850.00 | not in source | Deed 1,850.00 |
| `[L1203]` | `State Tax/Stamps: Deed 1,850.00;Mortgage` | not in source | not in source | 1,850.00 | Deed 1,850.00 |
| `[L1302]` | `Pest Inspection` `[POC (seller)]` | `ApexPest Control` | not in source | not in source | 175.00, P.O.C. |
| `[L1303]` | `Release/Reimbursement Fee` | `Brightwater LLC` | not in source | 225.00 | |
| `[L1305]` | `See addit'l disb. exhibit` | not in source | not in source | not in source | caption present, no amount -- see section 9 |
| `[L1400]` | `TOTAL SETTLEMENTCHARGES (Enter on Lines 103, Section Jand 502, Section K)` | | 3,379.25 | 14,310.00 | |

## 6. Prorations and adjustments

| Line | Caption as printed | Period from | Period to | Amount | Side |
|---|---|---|---|---|---|
| `[L106]` | `City/Town Taxes` | not in source | not in source | not in source | borrower |
| `[L107]` | `CountyTaxes` | not in source | not in source | not in source | borrower |
| `[L108]` | `School Taxes` | not in source | not in source | not in source | borrower |
| `[L210]` | `City/Town Taxes` | not in source | not in source | not in source | borrower |
| `[L211]` | `CountyTaxes` | not in source | not in source | not in source | borrower |
| `[L212]` | `School Taxes` | not in source | not in source | not in source | borrower |
| `[L406]` | `City/Town Taxes` | not in source | not in source | not in source | seller |
| `[L407]` | `CountyTaxes` | not in source | not in source | not in source | seller |
| `[L408]` | `School Taxes` | not in source | not in source | not in source | seller |
| `[L510]` | `City/Town Taxes` | 01/01/26 | 03/14/26 | 412.18 | seller |
| `[L511]` | `CountyTaxes` | 01/01/26 | 03/14/26 | 96.55 | seller |
| `[L512]` | `School Taxes` | 07/01/25 | 03/14/26 | 2,104.77 | seller |

The three seller prorations sit under the printed heading "Adjustments For Items Unpaid By Seller." No per-diem or day count is stated, and none is derived.

## 7. Arithmetic checks

| Check | Expression | Recomputed | Stated | Result |
|---|---|---|---|---|
| `[L120]` = sum 101-112 | `[L101]` 185,000.00 + `[L103]` 3,379.25 | 188,379.25 | 188,379.25 | agrees |
| `[L220]` = sum 201-219 | `[L201]` 5,000.00 | 5,000.00 | 5,000.00 | agrees |
| `[L303]` = `[L301]` - `[L302]` | 188,379.25 - 5,000.00 | 183,379.25 | 183,379.25 | agrees |
| `[L420]` = sum 401-412 | `[L401]` 185,000.00 | 185,000.00 | 185,000.00 | agrees |
| `[L520]` = sum 501-519 | `[L502]` 14,310.00 + `[L504]` 112,480.36 + `[L506]` 3,218.44 + `[L507]` 9,650.00 + `[L510]` 412.18 + `[L511]` 96.55 + `[L512]` 2,104.77 | 142,272.30 | 142,272.30 | agrees |
| `[L603]` = `[L601]` - `[L602]` | 185,000.00 - 142,272.30 | 42,727.70 | 42,727.70 | agrees |
| `[L103]` = `[L1400]` borrower column | 3,379.25 vs 3,379.25 | 3,379.25 | 3,379.25 | agrees |
| `[L502]` = `[L1400]` seller column | 14,310.00 vs 14,310.00 | 14,310.00 | 14,310.00 | agrees |
| `[L1400]` borrower col = sum of borrower column | `[L1108]` 1,412.00 + `[L1201]` 117.25 + `[L1202]` 1,850.00 | 3,379.25 | 3,379.25 | agrees |
| `[L1400]` seller col = sum of seller column | `[L703]` 11,100.00 + `[L1101]` 425.00 + `[L1102]` 175.00 + `[L1103]` 185.00 + `[L1104]` 250.00 + `[L1201]` 98.00 + `[L1203]` 1,850.00 + `[L1303]` 225.00 | 14,308.00 | 14,310.00 | **differs by 2.00** |
| `[L301]` = `[L120]` | 188,379.25 vs 188,379.25 | -- | -- | agrees |
| `[L302]` = `[L220]` | 5,000.00 vs 5,000.00 | -- | -- | agrees |
| `[L601]` = `[L420]` | 185,000.00 vs 185,000.00 | -- | -- | agrees |
| `[L602]` = `[L520]` | 142,272.30 vs 142,272.30 | -- | -- | agrees |

The seller column of `[L1400]` is stated as 14,310.00 and the seller-column charges add to 14,308.00. **The difference is 2.00.** Which figure is correct is not something this statement settles, and no adjustment was made to either.

The 175.00 on `[L1302]` is marked P.O.C. and is excluded from the column sums `[1024-A 5]`. The 1,412.00 printed on `[L1110]` is excluded as an outside-the-column figure; see section 9.

Note that the stated 14,310.00 carries forward into `[L502]`, and from there into `[L520]` and `[L603]`. Every check that consumes the stated figure agrees, because they all consume the same stated figure. Only the check that re-adds the column disagrees.

## 8. Not in source

**Section 1** -- loan number; mortgage insurance case number; type of loan

**Section 2** -- borrower address; seller address; lender

**Section 3** -- none

Counts:

- Fields requested by the schema: 31
- Fields answered from the statement: 25
- Fields `not in source`: 6
- Blank form lines omitted from section 5: 35 of the 53 Section L line numbers printed

## 9. Could not map

| Item | Citation | Reason |
|---|---|---|
| `84 Tanner Mill Road / Westbrook, PA 19023` in the header block | `[Sec. D]` / `[Sec. E]` | One address is printed beneath two names. On the form, D and E are separate columns; the text extraction does not preserve which column it sat in, so it cannot be assigned to the borrower or the seller. A reader holding the PDF can settle this by eye. Both address fields are `not in source` rather than guessed. |
| `1305. See addit'l disb. exhibit to` | `[L1305]` | The line names an additional disbursement exhibit, the exhibit is not in the input, and no amount is printed. Whether the exhibit carries money is not determinable here. |
| `1303. Release/Reimbursement Fee to Brightwater LLC 225.00` | `[L1303]` | The caption does not fix whether this is a fee for obtaining a release or the reimbursement of a released obligation. `[3500-A 35]` says payoffs of seller obligations belong on lines 506-509 and not on 1303-1305. Reported as printed, not reclassified. |
| `1110. Owner'sCoverage $ 185,000.00 1,412.00` | `[L1110]` | Two figures on one line. 1109 and 1110 hold policy coverage amounts outside the columns, and 1,412.00 is also the amount on `[L1108]`. Whether this is the coverage line repeating the premium or a second charge is not fixed by the statement. |
