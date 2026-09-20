"""Turn a HUD-1 PDF into the text format the translator expects.

The translator reads text, not PDFs. This produces exactly the layout the
files in inputs/ use, so your own statement can be run the same way.

Usage:
    python tools/extract_hud.py "C:\\path\\to\\statement.pdf"
    python tools/extract_hud.py statement.pdf -o inputs/05-my-deal.txt

Requires pdfplumber (pip install pdfplumber).

Deliberately does NOT clean up the extracted text. Run-together words like
"CountyTaxes" are what the extractor produced, and rules.md requires them to
reach the translator unchanged -- correcting them here would hide exactly the
thing the verbatim rule exists to test.

ASCII output only. No prompts.
"""

import os
import sys


def ascii_only(s):
    return s.encode("ascii", "replace").decode("ascii")


def extract(pdf_path):
    try:
        import pdfplumber
    except ImportError:
        print("ERROR: pdfplumber is not installed. Run: pip install pdfplumber")
        return None

    lines = []
    lines.append("=" * 70)
    lines.append("FILE: %s" % ascii_only(os.path.basename(pdf_path)))
    lines.append("=" * 70)

    with pdfplumber.open(pdf_path) as pdf:
        lines.append("PAGES: %d" % len(pdf.pages))
        for i, page in enumerate(pdf.pages):
            lines.append("----- page %d -----" % (i + 1))
            lines.append(ascii_only(page.extract_text() or ""))

    return "\n".join(lines) + "\n"


def main():
    args = [a for a in sys.argv[1:]]
    if not args:
        print(__doc__)
        return 2

    pdf_path = args[0]
    out_path = None
    if "-o" in args:
        idx = args.index("-o")
        if idx + 1 < len(args):
            out_path = args[idx + 1]

    if not os.path.exists(pdf_path):
        print("ERROR: no such file: %s" % ascii_only(pdf_path))
        return 2

    text = extract(pdf_path)
    if text is None:
        return 2

    if out_path:
        with open(out_path, "w", encoding="ascii", errors="replace", newline="\n") as fh:
            fh.write(text)
        print("wrote %s (%d characters)" % (ascii_only(out_path), len(text)))
        print("")
        print("Now run:  Read identity.md and rules.md, then translate %s"
              % ascii_only(out_path))
    else:
        print(text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
