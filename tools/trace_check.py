"""Trace every claim in a close-out sheet back to the statement it came from.

This is the competition's own test, automated. It does four things:

  A. INVENTED FIGURES   Every dollar figure in the output must appear, character
                        for character, in the input. Exception: the "Recomputed"
                        column of section 7, which holds derived values.
  B. DANGLING CITATIONS Every [L###] cited must be a line the input actually prints.
  C. ARITHMETIC         Every expression in section 7 is re-evaluated and compared
                        to the Recomputed value the sheet claims.
  D. SHAPE              The nine section headings must be present, in order.

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
        recomputed, stated = cells[3], cells[4]
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


def check_citations(md, src, fails):
    lines_cited = sorted(set(CITE_LINE.findall(md)), key=lambda x: (len(x), x))
    for num in lines_cited:
        # the input prints line numbers as "101." -- guard against 110 matching 1110
        if not re.search(r"(?<!\d)%s\." % re.escape(num), src):
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
        name, expr, recomputed = cells[1], cells[2], cells[3]
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

    name = os.path.basename(out_path)
    print("-" * 68)
    print("PAIR: %s" % name)
    print("  against: %s" % os.path.basename(src_path))
    print("  sections found      : %d" % n_sec)
    print("  figures traced      : %d" % n_fig)
    print("  citations resolved  : %d" % n_cite)
    print("  expressions re-added: %d" % n_math)
    if fails:
        print("  RESULT: FAIL (%d)" % len(fails))
        for f in fails:
            print("    - %s" % f)
    else:
        print("  RESULT: PASS")
    return len(fails)


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

    print("-" * 68)
    if missed:
        print("SELFTEST: FAIL -- %d case(s) not caught" % missed)
        return 1
    print("SELFTEST: PASS -- all 4 injected failures were caught")
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
