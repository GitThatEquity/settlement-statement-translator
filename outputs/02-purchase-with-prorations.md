# Close-Out Sheet -- 25-0613

Source: `inputs/02-purchase-with-prorations.txt`

---

## 1. Statement identity

| Field | Value | Source |
|---|---|---|
| Form vintage | pre-2010 | form stamps |
| Form stamp | `1.0 3/98` (page 1 header) and `HUD-1 (3-86) RESPA, HB4305.2` (foot of page 1) | page 1 |
| File number | 25-0613 | `[Sec. B]` |
| Loan number | not in source | `[Sec. B]` |
| Mortgage insurance case number | not in source | `[Sec. B]` |
| Type of loan | not in source | `[Sec. B]` -- the five options print, none is marked |
| Settlement date | `December3, 2025` (spacing as extracted; reads "December 3, 2025") | `[Sec. I]` |
| Statement status | final | a settlement date is present |
| Settlement agent | `Cornerstone Settlement & Abstract, Inc.` | `[Sec. H]` |
| Settlement agent TIN | 99-1234567 | `[Sec. H]` |
| Place of settlement | `220 Ellison Court Suite 310 / Brookvale,PA 15012` (spacing as extracted) | `[Sec. H]` |
| Pages in source | 3 | |

## 2. Parties and property

| Field | Value | Source |
|---|---|---|
| Borrower | `Martin K. Ellsworth` | `[Sec. D]` |
| Borrower address | `1420 Crescent Street, 2nd Floor / Riverton, PA 19044` | `[Sec. D]` |
| Seller | `Eileen R. Prosser` | `[Sec. E]` |
| Seller address | `62 North Laurel Ave / Westbrook, PA 19023` | `[Sec. E]` |
| Lender | not in source | `[Sec. F]` empty |
| Property location | `62 North Laurel Ave / Westbrook, PA 19023` | `[Sec. G]` |
| County | `Hartley County, Pennsylvania` | `[Sec. G]` |

## 3. Price and cash movement

| Field | Value | Line |
|---|---|---|
| Contract sales price, borrower side | 95,095.36 | `[L101]` |
| Contract sales price, seller side | not in source | `[L401]` |
| Settlement charges to borrower | 17,239.55 | `[L103]` |
| Settlement charges to seller | not in source | `[L502]` |
| Gross amount due from borrower | 114,173.33 | `[L120]` |
| Total paid by or for borrower | 3,000.00 | `[L220]` |
| Cash at settlement, borrower | 111,173.33 | `[L303]` |
| Cash direction, borrower | FROM borrower | `[L303]`, X in the FROM box |
| Gross amount due to seller | not in source | `[L420]` |
| Total reductions in amount due seller | not in source | `[L520]` |
| Cash at settlement, seller | not in source | `[L603]` |
| Cash direction, seller | TO seller | `[L603]`, X in the TO box, with no amount beside it |

## 4. Payoffs, liens and seller obligations

| Line | Caption as printed | Payee | Amount | Note |
|---|---|---|---|---|
| `[L501]` | `Excess Deposit(See Instructions)` | not in source | not in source | caption present, no amount |
| `[L502]` | `Settlement Chargesto Seller(Line 1400)` | not in source | not in source | caption present, no amount |
| `[L503]` | `Existing loan(s) taken subject to` | not in source | not in source | caption present, no amount |

Lines 504 through 509 print with neither caption nor amount.

## 5. Settlement charges

| Line | Caption as printed | Payee | Borrower column | Seller column | Outside columns |
|---|---|---|---|---|---|
| `[L703]` | `Commission Paid at Settlement` | not in source | not in source | not in source | |
| `[L1101]` | `Settlement orClosing Fee` | `Cornerstone Settlement & Abstract, Inc.` | 395.00 | not in source | |
| `[L1102]` | `Notary/Overnight/WireFees` | `Cornerstone Settlement & Abstract, Inc.` | 210.00 | not in source | |
| `[L1103]` | `Lien LetterReimbursement` | `Cornerstone Settlement & Abstract, Inc.` | 165.00 | not in source | |
| `[L1104]` | `Deed Prep Fee` | `Cornerstone Settlement & Abstract, Inc.` | 250.00 | not in source | |
| `[L1108]` | `Title Insurance` ... `Sale Rate` | `Meridian National Title Insurance Co.` | 999.92 | not in source | |
| `[L1109]` | `Lender'sCoverage $` | not in source | not in source | not in source | |
| `[L1110]` | `Owner'sCoverage $` | not in source | not in source | not in source | 95,095.36 and 999.92 -- see section 9 |
| `[L1201]` | `Recording Fees: Deed $ 117.25; Mortgage $ ; Releases $` | not in source | 117.25 | not in source | Deed 117.25 |
| `[L1202]` | `City/CountyTax/Stamps: Deed $ 1,426.43;Mortgage` | not in source | 1,426.43 | not in source | Deed 1,426.43 |
| `[L1203]` | `State Tax/Stamps: Deed $ 950.95;Mortgage` | not in source | 950.95 | not in source | Deed 950.95 |
| `[L1303]` | `Release/Reimbursement Fees` | `Brightwater LLC` | 3,300.00 | not in source | |
| `[L1304]` | `Release/Reimbursement Fees` | `Cornerstone Property Partners` | 3,425.00 | not in source | |
| `[L1305]` | `See addit'l disb. exhibit` | not in source | 6,000.00 | not in source | see section 9 |
| `[L1400]` | `TOTAL SETTLEMENTCHARGES (Enter on Lines 103, Section Jand 502, Section K)` | | 17,239.55 | not in source | |

## 6. Prorations and adjustments

| Line | Caption as printed | Period from | Period to | Amount | Side |
|---|---|---|---|---|---|
| `[L106]` | `City/Town Taxes` | 12/03/25 | 01/01/26 | 148.04 | borrower |
| `[L107]` | `CountyTaxes` | 12/03/25 | 01/01/26 | 33.41 | borrower |
| `[L108]` | `School Taxes` | 12/03/25 | 07/01/26 | 1,656.97 | borrower |
| `[L210]` | `City/Town Taxes` | not in source | not in source | not in source | borrower |
| `[L211]` | `CountyTaxes` | not in source | not in source | not in source | borrower |
| `[L212]` | `School Taxes` | not in source | not in source | not in source | borrower |
| `[L406]` | `City/Town Taxes` | not in source | not in source | not in source | seller |
| `[L407]` | `CountyTaxes` | not in source | not in source | not in source | seller |
| `[L408]` | `School Taxes` | not in source | not in source | not in source | seller |
| `[L510]` | `City/Town Taxes` | not in source | not in source | not in source | seller |
| `[L511]` | `CountyTaxes` | not in source | not in source | not in source | seller |
| `[L512]` | `School Taxes` | not in source | not in source | not in source | seller |

The three prorations on 106-108 are captioned `Adjustments ForItemsPaid By Sellerin advance` (spacing as extracted). No per-diem or day count is stated, and none is derived.

## 7. Arithmetic checks

| Check | Expression | Recomputed | Stated | Result |
|---|---|---|---|---|
| `[L120]` = sum 101-112 | `[L101]` 95,095.36 + `[L103]` 17,239.55 + `[L106]` 148.04 + `[L107]` 33.41 + `[L108]` 1,656.97 | 114,173.33 | 114,173.33 | agrees |
| `[L220]` = sum 201-219 | `[L201]` 3,000.00 | 3,000.00 | 3,000.00 | agrees |
| `[L303]` = `[L301]` - `[L302]` | 114,173.33 - 3,000.00 | 111,173.33 | 111,173.33 | agrees |
| `[L420]` = sum 401-412 | no operand carries an amount | -- | not in source | cannot check |
| `[L520]` = sum 501-519 | no operand carries an amount | -- | not in source | cannot check |
| `[L603]` = `[L601]` - `[L602]` | both operands not in source | -- | not in source | cannot check |
| `[L103]` = `[L1400]` borrower column | 17,239.55 vs 17,239.55 | 17,239.55 | 17,239.55 | agrees |
| `[L502]` = `[L1400]` seller column | both not in source | -- | -- | cannot check |
| `[L1400]` borrower col = sum of borrower column | `[L1101]` 395.00 + `[L1102]` 210.00 + `[L1103]` 165.00 + `[L1104]` 250.00 + `[L1108]` 999.92 + `[L1201]` 117.25 + `[L1202]` 1,426.43 + `[L1203]` 950.95 + `[L1303]` 3,300.00 + `[L1304]` 3,425.00 + `[L1305]` 6,000.00 | 17,239.55 | 17,239.55 | agrees |
| `[L1400]` seller col = sum of seller column | no seller-column amount on the statement | -- | not in source | cannot check |
| `[L301]` = `[L120]` | 114,173.33 vs 114,173.33 | -- | -- | agrees |
| `[L302]` = `[L220]` | 3,000.00 vs 3,000.00 | -- | -- | agrees |
| `[L601]` = `[L420]` | both not in source | -- | -- | cannot check |
| `[L602]` = `[L520]` | both not in source | -- | -- | cannot check |

The seller side of this statement -- the 400, 500 and 600 series -- carries no amounts anywhere. That is why seven checks resolve to `cannot check`. The 999.92 printed on `[L1110]` is excluded from the column sum, which closes at 17,239.55 without it.

## 8. Not in source

**Section 1** -- loan number; mortgage insurance case number; type of loan

**Section 2** -- lender

**Section 3** -- contract sales price, seller side `[L401]`; settlement charges to seller `[L502]`; gross amount due to seller `[L420]`; total reductions `[L520]`; cash at settlement, seller `[L603]`

Counts:

- Fields requested by the schema: 31
- Fields answered from the statement: 22
- Fields `not in source`: 9
- Blank form lines omitted from section 5: 38 of the 53 Section L line numbers printed

## 9. Could not map

| Item | Citation | Reason |
|---|---|---|
| `1305. See addit'l disb. exhibit to 6,000.00` | `[L1305]` | The line names an additional disbursement exhibit and the exhibit is not in the input. 6,000.00 of the 17,239.55 total has no stated payee and no stated purpose. The amount is included in the column sum because the statement puts it in the column. |
| `1303. Release/Reimbursement Fees to Brightwater LLC 3,300.00` and `1304. ... Cornerstone Property Partners 3,425.00` | `[L1303]`, `[L1304]` | The caption does not fix whether these are fees for obtaining releases or reimbursements of amounts paid to release something. `[3500-A 35]` says payoffs of seller obligations belong on lines 506-509 and not on 1303-1305; both amounts here sit in the borrower column. Reported as printed, not reclassified. |
| `1110. Owner'sCoverage $ 95,095.36 999.92` | `[L1110]` | Two figures on one line. 1109 and 1110 hold policy coverage amounts outside the columns, and 999.92 is also the amount on `[L1108]`. Whether this is the coverage line repeating the premium or a second charge is not fixed by the statement. |
| `Settlement Date:December 3, 2025` | page 3 | The page 3 block prints the settlement date with the spacing intact, where `[Sec. I]` prints `December3, 2025`. Same date, two extractions; neither was normalized. |
| `Settlement Agent:CornerstoneSettlement &Abstract, Inc.` and `(412)555-0142` | page 3 | The page 3 block prints the settlement agent name with different spacing from `[Sec. H]` (`Cornerstone Settlement & Abstract, Inc.`) and adds a telephone number that `[Sec. H]` does not carry. Neither is mapped to a section 1 field; the schema has no telephone field. Neither was normalized. |
