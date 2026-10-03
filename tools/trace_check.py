"""Trace every claim in a close-out sheet back to the statement it came from.

This is the competition's own test, automated. It does four things:

  A. INVENTED FIGURES   Every dollar figure in the output must appear, character
                        for character, in the input. Exception: the "Recomputed"
                        column of section 7, which holds derived values.
  B. DANGLING CITATIONS Every [L###] cited must be a line the input actually prints.
  C. ARITHMETIC         Every expression in section 7 is re-evaluated and compared
                        to the Recomputed value the sheet claims.
  D. SHAPE              The nine section headings must be present, in order.
  E. TEXT               Every backticked name, caption and payee in sections 1, 2,
                        4, 5, 6 and 9 must be printed in the input, character for
                        character (whitespace aside).
  F. DATES              Every date in the output must be a date the input prints.
  G. PLACEMENT          A figure or date in a row cited to [Lnnn] must sit on line
                        nnn of the input, not merely somewhere in it. Section 7
                        operands are held to the same test.
  H. DIRECTION          Cash direction must be the box that carries the X.
  I. STATUS / COUNTS    Statement status must follow the settlement-date rule, and a
                        prose count of `cannot check` must match the table.

A line cited only from a section 7 row that resolves to `cannot check` may be absent
from the input (a cut or degraded statement). Any other dangling citation fails.

Usage:
    python tools/trace_check.py                        check every pair in outputs/
    python tools/trace_check.py outputs/01-....md inputs/01-....txt

Exit code 0 if every check passes, 1 if anything failed.
ASCII output only. No network, no prompts.
"""

import os
import re
import sys
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MONEY = re.compile(r"\d{1,3}(?:,\d{3})*\.\d{2}")
CITE_LINE = re.compile(r"\[L(\d{3,4})\]")
CITE_SEC = re.compile(r"\[Sec\. ([A-Z])\]")

SECTIONS = [
    "1. Statement identity",
    "2. Parties and property",
    "3. Price and cash movement",
    "4. Payoffs, liens and seller obligations",
    "5. Settlement charges",
    "6. Prorations and adjustments",
    "7. Arithmetic checks",
    "8. Not in source",
    "9. Could not map",
]


def to_num(s):
    return float(s.replace(",", ""))


def split_sections(md):
    """Return {section number: text}."""
    out = {}
    current = None
    buf = []
    for line in md.splitlines():
        m = re.match(r"^##\s+(\d)\.\s", line)
        if m:
            if current is not None:
                out[current] = "\n".join(buf)
            current = int(m.group(1))
            buf = [line]
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf)
    return out


def check_shape(md, fails):
    order = []
    for line in md.splitlines():
        m = re.match(r"^##\s+(\d\..*)$", line.strip())
        if m:
            order.append(m.group(1).strip())
    if order != SECTIONS:
        fails.append("SHAPE: section headings do not match the schema")
        for i, want in enumerate(SECTIONS):
            got = order[i] if i < len(order) else "<missing>"
            if got != want:
                fails.append("  position %d: expected %r, found %r" % (i + 1, want, got))
    return len(order)


def _strip_computed(cell):
    """Tolerate a legacy `computed:` prefix; the Recomputed column is the marker."""
    return re.sub(r"^computed:\s*", "", cell or "").strip()


def derived_allowed(sections):
    """Values section 7 may legitimately hold that the input does not print.

    Only two kinds qualify: the result of re-adding a stated total, and the
    difference between that result and the stated figure. Both are derived from
    cited operands, so both are allowed -- anywhere in section 7, including the
    prose under the table.
    """
    allowed = set()
    for raw in sections.get(7, "").splitlines():
        if not raw.strip().startswith("|"):
            continue
        cells = [c.strip() for c in raw.split("|")]
        if len(cells) < 6:
            continue
        recomputed, stated = _strip_computed(cells[3]), cells[4]
        if MONEY.fullmatch(recomputed or ""):
            allowed.add(to_num(recomputed))
            if MONEY.fullmatch(stated or ""):
                allowed.add(round(abs(to_num(recomputed) - to_num(stated)), 2))
    return allowed


def check_figures(sections, src, fails):
    """Every money figure in the output must be a figure the input prints.

    Matching is on whole tokens, not substrings: 2.00 must not pass merely
    because the input contains 1,412.00.
    """
    source_figures = set(to_num(f) for f in MONEY.findall(src))
    allowed = derived_allowed(sections)
    checked = 0

    for num, text in sorted(sections.items()):
        for fig in MONEY.findall(text):
            checked += 1
            value = to_num(fig)
            if value in source_figures:
                continue
            if num == 7 and value in allowed:
                continue
            fails.append(
                "INVENTED FIGURE: %s (section %d) is not a figure the input prints"
                % (fig, num))
    return checked


DATE_NUM = re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b")
DATE_TXT = re.compile(r"\b(?:January|February|March|April|May|June|July|August|"
                      r"September|October|November|December)\s*\d{1,2},\s*\d{4}\b")
NEXT_LINE_TOKEN = re.compile(r"(?<![\d,.$])\d{3,4}\.(?=\s|$)")
BACKTICKED = re.compile(r"`([^`]+)`")
ROW_LINE = re.compile(r"\[L(\d{3,4})\]")
NUMWORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
            "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
            "fourteen": 14}


def squash(t):
    return re.sub(r"\s+", "", t)


def source_segment(src, num):
    """The text the input prints for numbered line `num`, and no neighbour.

    The input often prints a borrower line and a seller line side by side
    ("106. ... 148.04 406. ..."), so the segment runs from this line's own
    number to the next line number on the same physical line.
    """
    segs = []
    for raw in src.splitlines():
        for m in re.finditer(r"(?<![\d,.$])%s\.(?=\s|$)" % re.escape(num), raw):
            rest = raw[m.end():]
            nxt = NEXT_LINE_TOKEN.search(rest)
            segs.append(raw[m.start():m.end() + (nxt.start() if nxt else len(rest))])
    return " ".join(segs)


def table_rows(text):
    for raw in text.splitlines():
        if raw.strip().startswith("|"):
            yield [c.strip() for c in raw.strip().strip("|").split("|")]


def check_text(sections, src, fails):
    """Backticked names, captions and payees must be printed in the input."""
    flat = squash(src)
    checked = 0
    for num in (1, 2, 4, 5, 6, 9):
        for cells in table_rows(sections.get(num, "")):
            for cell in cells:
                # the labelled reading is allowed to differ from the source
                cell = re.sub(r"\(spacing as extracted[^)]*\)", "", cell)
                for span in BACKTICKED.findall(cell):
                    if span.startswith("[") or span == "not in source":
                        continue
                    if "P.O.C." in span or "caption present" in span:
                        continue
                    for frag in re.split(r"\s/\s|\.\.\.", span):
                        frag = re.sub(r"^\d{3,4}\.\s*", "", frag.strip())
                        frag = re.sub(r"\s+to\s+\d[\d,]*\.\d{2}$", "", frag)
                        if len(squash(frag)) < 3:
                            continue
                        checked += 1
                        if squash(frag) not in flat:
                            fails.append(
                                "TEXT: %r (section %d) is not printed in the input" % (frag, num))
    return checked


def check_dates(md, src, fails):
    flat = squash(src)
    found = set(DATE_NUM.findall(md)) | set(DATE_TXT.findall(md))
    for d in sorted(found):
        if squash(d) not in flat:
            fails.append("DATE: %s is not a date the input prints" % d)
    return len(found)


def check_placement(sections, src, fails):
    """A cited figure or date must sit on the cited line."""
    checked = 0
    for num in (3, 4, 5, 6):
        for cells in table_rows(sections.get(num, "")):
            row = " | ".join(cells)
            cites = set(ROW_LINE.findall(row))
            if len(cites) != 1:
                continue
            ln = next(iter(cites))
            seg = source_segment(src, ln)
            if not seg:
                continue
            body = ROW_LINE.sub(" ", row)
            seg_flat = squash(seg)
            for fig in MONEY.findall(body):
                checked += 1
                if fig not in seg:
                    fails.append("PLACEMENT: %s is cited to [L%s] but line %s does not print it"
                                 % (fig, ln, ln))
            for d in set(DATE_NUM.findall(body)) | set(DATE_TXT.findall(body)):
                checked += 1
                if squash(d) not in seg_flat:
                    fails.append("PLACEMENT: %s is cited to [L%s] but line %s does not print it"
                                 % (d, ln, ln))
    for cells in table_rows(sections.get(7, "")):
        if len(cells) < 3:
            continue
        pairs = re.findall(r"`\[L(\d{3,4})\]`\s*(\d{1,3}(?:,\d{3})*\.\d{2})", cells[2])
        for ln, amt in pairs:
            seg = source_segment(src, ln)
            if seg:
                checked += 1
                if amt not in seg:
                    fails.append("PLACEMENT: section 7 gives %s for [L%s] but line %s does not print it"
                                 % (amt, ln, ln))
    return checked


def check_direction(sections, src, fails):
    done = 0
    for cells in table_rows(sections.get(3, "")):
        if len(cells) < 3 or not cells[0].startswith("Cash direction"):
            continue
        m = ROW_LINE.search(cells[2])
        if not m:
            continue
        seg = source_segment(src, m.group(1))
        marks = re.findall(r"\(\s*X\s*(FROM|TO)\s*\)", seg)
        said = cells[1].replace("`", "").strip()
        if said == "not in source":
            if marks:
                fails.append("DIRECTION: [L%s] says not in source but the input marks %s"
                             % (m.group(1), marks[0]))
            continue
        done += 1
        if not marks:
            fails.append("DIRECTION: [L%s] says %r but the input carries no X" % (m.group(1), said))
        elif said.split()[0] != marks[0]:
            fails.append("DIRECTION: [L%s] says %r but the X is in the %s box"
                         % (m.group(1), said, marks[0]))
    return done


def check_status_and_counts(sections, fails):
    done = 0
    sec1 = {c[0]: c for c in table_rows(sections.get(1, "")) if len(c) >= 2}
    st, dt = sec1.get("Statement status"), sec1.get("Settlement date")
    if st and dt:
        done += 1
        has_date = dt[1].replace("`", "").strip() != "not in source"
        want = "final" if has_date else "preliminary"
        if st[1].replace("`", "").strip().split()[0] != want:
            fails.append("STATUS: settlement date %s, so status must be %s, sheet says %r"
                         % ("present" if has_date else "absent", want, st[1]))
    text = sections.get(7, "")
    table_n = sum(1 for c in table_rows(text)
                  if c and c[-1].replace("*", "").strip() == "cannot check")
    for m in re.finditer(r"\b(\w+)\s+(?:checks?\s+)?resolves?\s+to\s+`cannot check`", text):
        n = NUMWORDS.get(m.group(1).lower())
        if n is not None:
            done += 1
            if n != table_n:
                fails.append("COUNT: prose says %d `cannot check`, table shows %d" % (n, table_n))
    return done



def exempt_citations(md):
    """Lines cited ONLY from section 7 rows that resolve to `cannot check`."""
    in7 = False
    exempt, other = set(), set()
    for line in md.splitlines():
        m = re.match(r"^##\s+(\d)\.\s", line)
        if m:
            in7 = m.group(1) == "7"
        cited = set(CITE_LINE.findall(line))
        if in7 and line.strip().startswith("|") and line.rstrip().rstrip("|").rstrip().endswith("cannot check"):
            exempt |= cited
        else:
            other |= cited
    return exempt - other


def check_citations(md, src, fails):
    exempt = exempt_citations(md)
    lines_cited = sorted(set(CITE_LINE.findall(md)), key=lambda x: (len(x), x))
    for num in lines_cited:
        # the input prints line numbers as "101." -- guard against 110 matching 1110
        if not re.search(r"(?<!\d)%s\." % re.escape(num), src):
            if num in exempt:
                continue
            fails.append("DANGLING CITATION: [L%s] is not a line the input prints" % num)
    secs = sorted(set(CITE_SEC.findall(md)))
    for s in secs:
        if not re.search(r"(?<![A-Za-z])%s\." % s, src):
            fails.append("DANGLING CITATION: [Sec. %s] is not a block the input prints" % s)
    return len(lines_cited) + len(secs)


def check_arithmetic(sections, fails):
    """Re-evaluate every expression in section 7."""
    text = sections.get(7, "")
    done = 0
    for raw in text.splitlines():
        if not raw.strip().startswith("|"):
            continue
        cells = [c.strip() for c in raw.split("|")]
        if len(cells) < 6:
            continue
        name, expr, recomputed = cells[1], cells[2], _strip_computed(cells[3])
        if name.lower().startswith("check") or set(name) <= set("-: "):
            continue

        plain = re.sub(r"`\[L\d{3,4}\]`", " ", expr)
        plain = re.sub(r"`|\*\*", "", plain)

        if " vs " in plain:
            nums = MONEY.findall(plain)
            if len(nums) == 2:
                done += 1
                same = to_num(nums[0]) == to_num(nums[1])
                stated = cells[5].replace("*", "").strip().lower()
                if same and not stated.startswith("agrees"):
                    fails.append("ARITHMETIC: %s -- values match but result says %r"
                                 % (name, cells[5]))
                if (not same) and stated.startswith("agrees"):
                    fails.append("ARITHMETIC: %s -- values differ but result says agrees" % name)
            continue

        tokens = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}|[+\-]", plain)
        nums = [t for t in tokens if t not in "+-"]
        if len(nums) < 2 or not MONEY.fullmatch(recomputed or ""):
            continue

        total = to_num(tokens[0])
        i = 1
        while i < len(tokens) - 1:
            op, val = tokens[i], tokens[i + 1]
            if op == "+":
                total += to_num(val)
            elif op == "-":
                total -= to_num(val)
            i += 2

        done += 1
        claimed = to_num(recomputed)
        if abs(total - claimed) > 0.005:
            fails.append("ARITHMETIC: %s -- expression evaluates to %.2f, sheet says %s"
                         % (name, total, recomputed))
    return done


def run_pair(out_path, src_path):
    md = open(out_path, encoding="utf-8", errors="replace").read()
    src = open(src_path, encoding="utf-8", errors="replace").read()

    fails = []
    n_sec = check_shape(md, fails)
    n_fig = check_figures(split_sections(md), src, fails)
    n_cite = check_citations(md, src, fails)
    n_math = check_arithmetic(split_sections(md), fails)
    secs = split_sections(md)
    n_text = check_text(secs, src, fails)
    n_date = check_dates(md, src, fails)
    n_place = check_placement(secs, src, fails)
    n_dir = check_direction(secs, src, fails)
    n_stat = check_status_and_counts(secs, fails)

    name = os.path.basename(out_path)
    print("-" * 68)
    print("PAIR: %s" % name)
    print("  against: %s" % os.path.basename(src_path))
    print("  sections found      : %d" % n_sec)
    print("  figures traced      : %d" % n_fig)
    print("  citations resolved  : %d" % n_cite)
    print("  expressions re-added: %d" % n_math)
    print("  names/captions      : %d" % n_text)
    print("  dates traced        : %d" % n_date)
    print("  placements checked  : %d" % n_place)
    print("  directions checked  : %d" % n_dir)
    print("  status/count checks : %d" % n_stat)
    if fails:
        print("  RESULT: FAIL (%d)" % len(fails))
        for f in fails:
            print("    - %s" % f)
    else:
        print("  RESULT: PASS")
    return len(fails)


def run_all(md, src):
    fails = []
    secs = split_sections(md)
    check_shape(md, fails)
    check_figures(secs, src, fails)
    check_citations(md, src, fails)
    check_arithmetic(secs, fails)
    check_text(secs, src, fails)
    check_dates(md, src, fails)
    check_placement(secs, src, fails)
    check_direction(secs, src, fails)
    check_status_and_counts(secs, fails)
    return fails


def selftest():
    """Poison a passing sheet four ways and confirm each one is caught.

    A checker that only ever reports PASS is evidence of nothing. This injects
    the four failures the schema exists to prevent and fails loudly if any of
    them slips through.
    """
    out = os.path.join(ROOT, "outputs", "01-cash-purchase-prelim.md")
    src = os.path.join(ROOT, "inputs", "01-cash-purchase-prelim.txt")
    if not (os.path.exists(out) and os.path.exists(src)):
        print("selftest: outputs/01 pair not found")
        return 2

    clean = open(out, encoding="utf-8", errors="replace").read()
    source = open(src, encoding="utf-8", errors="replace").read()

    cases = [
        ("invented figure",
         lambda t: t.replace("| 569.00 | not in source | |",
                             "| 1,250.00 | not in source | |", 1),
         "INVENTED FIGURE"),
        ("dangling citation",
         lambda t: t.replace("`[L1108]`", "`[L9997]`", 1),
         "DANGLING CITATION"),
        ("bad arithmetic",
         lambda t: t.replace("| 27,032.75 | 27,032.75 | agrees |",
                             "| 25,000.00 | 27,032.75 | agrees |", 1),
         "ARITHMETIC"),
        ("dropped section",
         lambda t: t.replace("## 9. Could not map", "## Extra notes", 1),
         "SHAPE"),
    ]

    out2 = os.path.join(ROOT, "outputs", "02-purchase-with-prorations.md")
    src2 = os.path.join(ROOT, "inputs", "02-purchase-with-prorations.txt")
    clean2 = open(out2, encoding="utf-8", errors="replace").read()
    source2 = open(src2, encoding="utf-8", errors="replace").read()
    cases2 = [
        ("changed name",
         lambda t: t.replace("Eileen R. Prosser", "Eileen R. Prossor", 1), "TEXT"),
        ("moved date",
         lambda t: t.replace("| 12/03/25 | 07/01/26 |", "| 12/03/25 | 07/02/26 |", 1), "DATE"),
        ("moved date, real date wrong line",
         lambda t: t.replace("| `School Taxes` | 12/03/25 | 07/01/26 |",
                             "| `School Taxes` | 12/03/25 | 01/01/26 |", 1), "PLACEMENT"),
        ("flipped direction",
         lambda t: t.replace("| FROM borrower |", "| TO borrower |", 1), "DIRECTION"),
        ("figure on wrong line",
         lambda t: t.replace("| `Notary/Overnight/WireFees` | `Cornerstone Settlement & Abstract, Inc.` | 210.00 |",
                             "| `Notary/Overnight/WireFees` | `Cornerstone Settlement & Abstract, Inc.` | 395.00 |", 1),
         "PLACEMENT"),
        ("wrong status",
         lambda t: t.replace("| Statement status | final |", "| Statement status | preliminary |", 1),
         "STATUS"),
        ("wrong cannot-check count",
         lambda t: re.sub(r"\b(six|seven) checks", "five checks", t, count=1), "COUNT"),
    ]

    print("=" * 68)
    print("SELFTEST -- each case must be caught")
    print("=" * 68)

    missed = 0
    for label, poison, expect in cases:
        bad = poison(clean)
        if bad == clean:
            print("  %-20s SETUP FAILED (nothing was changed)" % label)
            missed += 1
            continue
        fails = []
        check_shape(bad, fails)
        secs = split_sections(bad)
        check_figures(secs, source, fails)
        check_citations(bad, source, fails)
        check_arithmetic(secs, fails)
        caught = any(f.startswith(expect) or ("  " in f and expect in f) for f in fails)
        print("  %-20s %s" % (label, "caught" if caught else "MISSED"))
        if caught:
            for f in fails:
                if f.startswith(expect):
                    print("      %s" % f)
                    break
        else:
            missed += 1

    for label, poison, expect in cases2:
        bad = poison(clean2)
        if bad == clean2:
            print("  %-20s SETUP FAILED (nothing was changed)" % label)
            missed += 1
            continue
        fails = run_all(bad, source2)
        caught = any(f.startswith(expect) for f in fails)
        print("  %-20s %s" % (label, "caught" if caught else "MISSED"))
        if not caught:
            missed += 1

    # degraded input: a line the input no longer prints is fine when only a
    # `cannot check` row cites it, and still a failure anywhere else.
    cut = "\n".join(l for l in source2.splitlines() if not l.startswith("1400."))
    row7 = "| `[L103]` = `[L1400]` borrower column | both not in source | -- | -- | cannot check |"
    row5 = "| `[L1400]` | `TOTAL` | | 17,239.55 | not in source | |"
    ok_md = "## 7. Arithmetic checks\n\n" + row7 + "\n"
    bad_md = ok_md + "\n## 5. Settlement charges\n\n" + row5 + "\n"
    a, b = [], []
    check_citations(ok_md, cut, a)
    check_citations(bad_md, cut, b)
    degraded_ok = not a and any("[L1400]" in f for f in b)
    print("  %-20s %s" % ("degraded citation", "caught" if degraded_ok else "MISSED"))
    if not degraded_ok:
        missed += 1

    print("-" * 68)
    if missed:
        print("SELFTEST: FAIL -- %d case(s) not caught" % missed)
        return 1
    print("SELFTEST: PASS -- all %d injected failures were caught" % (len(cases) + len(cases2) + 1))
    return 0


def main():
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        return selftest()

    pairs = []
    if len(args) == 2:
        pairs.append((args[0], args[1]))
    elif not args:
        for out in sorted(glob.glob(os.path.join(ROOT, "outputs", "*.md"))):
            stem = os.path.splitext(os.path.basename(out))[0]
            src = os.path.join(ROOT, "inputs", stem + ".txt")
            if os.path.exists(src):
                pairs.append((out, src))
    else:
        print("usage: python tools/trace_check.py [output.md input.txt]")
        return 2

    if not pairs:
        print("no output/input pairs found")
        return 2

    total = 0
    for out, src in pairs:
        total += run_pair(out, src)

    print("-" * 68)
    if total:
        print("OVERALL: FAIL -- %d problem(s) across %d pair(s)" % (total, len(pairs)))
        return 1
    print("OVERALL: PASS -- %d pair(s), every figure traced to source" % len(pairs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
