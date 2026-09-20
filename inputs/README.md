# Inputs

Four statements you can run the translator against. Each is the text of a HUD-1 as a PDF text extractor produces it -- which is what a Claude project actually receives when you paste or attach a settlement statement.

| File | What it exercises |
|---|---|
| `01-cash-purchase-prelim.txt` | A sparse statement. Preliminary: no settlement date. Seller side almost entirely blank. Two captioned payoff lines with **no amounts**. |
| `02-purchase-with-prorations.txt` | Tax prorations with date ranges, three third-party disbursements, and a **blind disbursement** pointing at an exhibit that is not in the file. |
| `03-cash-purchase-alt-layout.txt` | **The same deal as 01**, run through a different PDF extractor. Different line breaks, different word spacing, four pages instead of three. Same facts. |
| `04-seller-side-payoffs.txt` | A populated seller side: mortgage payoff, municipal lien, judgment, commission split, a **P.O.C. item**, and a column total that **does not add up**. Also a single address printed under two names, which text extraction cannot assign to a party. |

## Where these came from

`01`, `02` and `03` are **real HUD-1 settlement statements from closed Pennsylvania transactions**, pseudonymized. `03` is genuinely the same document as `01` re-extracted -- the layout difference is real, not manufactured.

`04` is **constructed**. No real transaction in hand had a fully populated 500-series block, and that block is where the money a seller actually loses shows up, so it needed coverage.

## What was changed, and what was not

**Replaced** in `01`, `02` and `03`:

- every party name -- buyer, seller, settlement agent, title underwriter, third-party payees
- every street address, municipality, county and ZIP
- the settlement agent's phone number and taxpayer ID
- the file and document reference numbers

**Kept exactly as printed:**

- every dollar amount
- every date, including the proration periods
- the form stamps, the layout, the line captions
- the extraction artifacts -- `CountyTaxes`, `NorthgateHoldings, LLC`, `Lender'sCoverage`

The amounts and dates are untouched because they are what makes these worth testing against. The arithmetic in the checks section is real arithmetic from a real closing. Change the numbers and the test stops proving anything.

The municipality and county names are fictional -- there is no Hartley County, Pennsylvania. That is deliberate, so no reader mistakes a pseudonymized statement for a locatable one. The state is left as PA because the form's transfer-tax lines only make sense in a state that charges them that way.

The extraction artifacts were kept on purpose. `rules.md` requires captions and names to be transcribed exactly as they arrive, and a clean input cannot test that.

## Running one

Open the folder, or drop it into a Claude project, and say:

    Read identity.md and rules.md, then translate inputs/02-purchase-with-prorations.txt.

The finished sheets for all four are in `outputs/`.
