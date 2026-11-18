#!/usr/bin/env python3
"""Keep unpublished privacy stubs aligned with the one shared core.

The visitor-facing core lives only in:

    _includes/privacy-shared-core.md

Published pages pull that file in with a Liquid include, so they cannot
drift from each other. This script:

  * re-injects that file into _privacy/*-privacy.md (unpublished stubs)
  * fails if a published privacy page drops the include
  * fails if the core or a published page still contains an [OPEN] or
    warning marker that would render

Usage (from the repo root):

    python3 _privacy/sync-shared.py
    python3 _privacy/sync-shared.py --check
    python3 _privacy/sync-shared.py --diff
"""
import difflib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CORE = REPO / "_includes" / "privacy-shared-core.md"
STUB_DIR = REPO / "_privacy"
END = "<!-- END SHARED CORE -->"
BEGIN_RE = re.compile(r"<!-- (?:shared-core-version:|BEGIN SHARED CORE)")
INCLUDE = "{% include privacy-shared-core.md %}"
LIVE_INCLUDE = [
    REPO / "privacy.md",
    REPO / "herenotes" / "privacy.md",
]
LIVE_CLEAN = LIVE_INCLUDE + [
    REPO / "support.html",
    REPO / "support-thanks.html",
    REPO / "_includes" / "support-form.html",
    REPO / "_includes" / "capsule-web-form.html",
    CORE,
]
COMMENT_RE = re.compile(
    r"<!--.*?-->|\{%\s*comment\s*%\}.*?\{%\s*endcomment\s*%\}",
    re.S,
)


def load_block():
    text = CORE.read_text(encoding="utf-8")
    version = re.search(r"shared-core-version:\s*(.+?)\s*-->", text)
    date = re.search(r"shared-core-date:\s*(.+?)\s*-->", text)
    if not (version and date and END in text and "BEGIN SHARED CORE" in text):
        sys.exit("privacy-shared-core.md is missing its version, date, or markers")
    return text.strip("\n"), version.group(1), date.group(1)


def visible(text):
    return COMMENT_RE.sub("", text)


def placeholder_hits(text):
    shown = visible(text)
    return len(re.findall(r"\[OPEN", shown)) + shown.count("⚠")


def main():
    check = "--check" in sys.argv or "--diff" in sys.argv
    show_diff = "--diff" in sys.argv
    block, version, date = load_block()
    print(f"privacy-shared-core.md  version {version}  date {date}\n")

    failed = 0
    core_hits = placeholder_hits(block)
    if core_hits:
        print(f"[PLACEHOLDER] privacy-shared-core.md still has {core_hits} marker(s) that would render")
        failed += 1
    else:
        print("[clean]    privacy-shared-core.md")

    for page in LIVE_INCLUDE:
        text = page.read_text(encoding="utf-8") if page.exists() else ""
        rel = page.relative_to(REPO)
        if INCLUDE not in text:
            print(f"[MISSING INCLUDE] {rel}")
            failed += 1
        elif "## Bout Labs standard privacy terms" in text:
            print(f"[DUPLICATE CORE] {rel} pastes the core instead of including it")
            failed += 1
        else:
            print(f"[include]  {rel}")

    for page in LIVE_CLEAN:
        if not page.exists():
            print(f"[MISSING]  {page.relative_to(REPO)}")
            failed += 1
            continue
        hits = placeholder_hits(page.read_text(encoding="utf-8"))
        if hits:
            print(f"[PLACEHOLDER] {page.relative_to(REPO)} has {hits} marker(s) outside comments")
            failed += 1

    drifted = broken = 0
    stubs = sorted(STUB_DIR.glob("*-privacy.md"))
    if not stubs:
        print("\n[MISSING STUBS] expected unpublished *-privacy.md files in _privacy/")
        failed += 1
    for page in stubs:
        text = page.read_text(encoding="utf-8")
        shown = visible(text)
        inactive = len(re.findall(r"INACTIVE", text))
        open_items = len(re.findall(r"\[OPEN", shown)) + shown.count("⚠")
        status = "NOT READY (stub)" if "STATUS: NOT READY" in text else "draft"
        extra = f" (+{inactive} inactive block)" if inactive else ""
        begin = BEGIN_RE.search(text)
        end_at = text.find(END)
        if not begin or end_at == -1 or end_at < begin.start():
            print(f"[MISSING MARKERS] {page.name}")
            broken += 1
            continue
        current = text[begin.start(): end_at + len(END)].strip("\n")
        if current == block:
            print(f"[in sync]  {page.name:28} {status:18} open items: {open_items}{extra}")
            continue
        drifted += 1
        diff = list(difflib.unified_diff(
            current.splitlines(), block.splitlines(),
            "embedded", "privacy-shared-core.md", lineterm="", n=0,
        ))
        changed = sum(1 for line in diff if line[:1] in "+-" and not line.startswith(("+++", "---")))
        print(f"[DRIFTED]  {page.name:28} {status:18} open items: {open_items}{extra}  ({changed} differing lines)")
        if show_diff:
            print("\n".join("    " + line for line in diff[:80]))
        if not check:
            page.write_text(text[:begin.start()] + block + text[end_at + len(END):], encoding="utf-8")
            print("           -> re-injected from privacy-shared-core.md")

    print(f"\n{drifted} drifted, {broken} missing markers, {failed} live-page problems.")
    if broken:
        sys.exit(2)
    if check and (drifted or failed):
        sys.exit(1)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
