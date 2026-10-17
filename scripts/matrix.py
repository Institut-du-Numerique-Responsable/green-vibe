#!/usr/bin/env python3
"""Correspondence matrix between Green Vibe and its sources.

Reads the origin fields of the Green Vibe rule catalog and inventories the two
source projects (Green Claude JSON catalogs, Green Codex rules.md) to produce
docs/matrice-correspondance.md: what each Green Vibe rule derives from, and
which source rules are not covered in this version.

Usage:
    python3 scripts/matrix.py [--sources DIR] [--out FILE] [--check]

--check exits non-zero if a declared origin id does not exist in the sources:
it is the drift/regression guard for the provenance fields.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "validators"))

from green_vibe import rules as rules_mod  # noqa: E402


def green_claude_inventory(sources: Path) -> dict[str, str]:
    """id -> title for every Green Claude rule (eco + langages + usage)."""
    inv: dict[str, str] = {}
    base = sources / "green-claude" / "skills" / "green-claude" / "rules"
    if not base.is_dir():
        base = sources / "green_claude" / "skills" / "green-claude" / "rules"
    files = [base / "ecoconception.json", base / "usage.json"]
    files += sorted((base / "langages").glob("*.json")) if (base / "langages").is_dir() else []
    for path in files:
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        cats = data.get("categories", {})
        for cat in cats.values():
            for rule in (cat if isinstance(cat, list) else cat.get("rules", [])):
                inv[rule["id"]] = rule.get("title", "")
    return inv


def green_codex_inventory(sources: Path) -> dict[str, str]:
    """id -> short title for every Green Codex rule in references/rules.md."""
    path = sources / "green_codex" / "green-codex" / "references" / "rules.md"
    if not path.is_file():
        path = sources / "green-codex" / "green-codex" / "references" / "rules.md"
    inv: dict[str, str] = {}
    if not path.is_file():
        return inv
    text = path.read_text(encoding="utf-8")
    for m in re.finditer(r"\*\*([A-Z]+(?:-[A-Z0-9]+)*-[0-9]{3})\b\**\s*(?:—|-)?\s*([^:*\n]*)", text):
        rid, title = m.group(1), m.group(2).strip(" —-")
        inv.setdefault(rid, title)
    # usage practices live in a separate reference file
    up = path.parent / "usage-practices.md"
    if up.is_file():
        for m in re.finditer(r"\b(USAGE-[A-Z]+-\d+)\b", up.read_text(encoding="utf-8")):
            inv.setdefault(m.group(1), "")
    return inv


def parse_origin(origin: list[str]) -> tuple[set[str], set[str]]:
    claude, codex = set(), set()
    for entry in origin:
        if entry.startswith("green-claude:"):
            for part in entry[len("green-claude:"):].split(","):
                if part.strip():
                    claude.add(part.strip())
        elif entry.startswith("green-codex:"):
            for part in entry[len("green-codex:"):].split(","):
                if part.strip():
                    codex.add(part.strip())
    return claude, codex


ID_SHAPE = re.compile(r"^[A-Z]+(?:-[A-Z0-9]+)*-[0-9]+$")


def id_shaped(ids: set[str]) -> set[str]:
    """Only strictly id-shaped origins are checked against the source catalogs;
    document-level provenance (usage-practices.md, hooks discipline, wildcards)
    is descriptive and trusted as written."""
    return {i for i in ids if ID_SHAPE.match(i)}


def build_matrix(sources: Path) -> dict:
    gv_rules = rules_mod.load_rules(REPO_ROOT)
    claude = green_claude_inventory(sources)
    codex = green_codex_inventory(sources)
    rows = []
    missing = []
    for r in gv_rules:
        gc, gx = parse_origin(r["origin"])
        for cid in id_shaped(gc):
            if claude and cid not in claude:
                missing.append((r["id"], "green-claude", cid))
        for cid in id_shaped(gx):
            if codex and cid not in codex:
                missing.append((r["id"], "green-codex", cid))
        rows.append(
            {
                "id": r["id"],
                "title": r["title"],
                "green_claude": ", ".join(sorted(gc)) or "—",
                "green_codex": ", ".join(sorted(gx)) or "—",
                "rgesn": r.get("rgesn") or "—",
            }
        )
    covered_claude = {c for row in rows for c in row["green_claude"].split(", ") if c != "—"}
    covered_codex = {c for row in rows for c in row["green_codex"].split(", ") if c != "—"}
    return {
        "rows": rows,
        "missing": missing,
        "claude_total": len(claude),
        "claude_covered": len(covered_claude & set(claude)),
        "codex_total": len(codex),
        "codex_covered": len(covered_codex & set(codex)),
        "claude_uncovered": sorted(set(claude) - covered_claude),
        "codex_uncovered": sorted(set(codex) - covered_codex),
    }


def render_markdown(m: dict) -> str:
    lines = [
        "# Matrice de correspondance des règles",
        "",
        "Générée par `scripts/matrix.py`. Une ligne = une règle Green Vibe, avec sa",
        "provenance dans Green Claude et Green Codex, et le critère RGESN associé quand",
        "il s'applique. Les identifiants NR-* sont des identifiants Green Vibe, pas des",
        "numéros de critères officiels.",
        "",
        f"- Règles Green Vibe : **{len(m['rows'])}**",
        f"- Green Claude : **{m['claude_covered']}/{m['claude_total']}** règles source couvertes",
        f"- Green Codex : **{m['codex_covered']}/{m['codex_total']}** règles source couvertes",
        "",
        "## Correspondance par règle Green Vibe",
        "",
        "| ID Green Vibe | Règle | Green Claude | Green Codex | RGESN |",
        "|---|---|---|---|---|",
    ]
    for row in m["rows"]:
        title = row["title"].replace("|", "/")
        lines.append(
            f"| `{row['id']}` | {title} | {row['green_claude']} | {row['green_codex']} | {row['rgesn']} |"
        )
    lines += [
        "",
        "## Règles sources non reprises en v1",
        "",
        "Ces règles ne sont pas portées telles quelles : elles sont couvertes par une",
        "règle Green Vibe existante (voir la matrice), jugées non applicables au",
        "périmètre Vibe, ou laissées pour une version ultérieure.",
        "",
        "### Green Claude",
        "",
    ]
    lines += [f"- `{cid}`" for cid in m["claude_uncovered"]] or ["- (aucune)"]
    lines += ["", "### Green Codex", ""]
    lines += [f"- `{cid}`" for cid in m["codex_uncovered"]] or ["- (aucune)"]
    if m["missing"]:
        lines += [
            "",
            "## Incohérences de provenance (à corriger)",
            "",
        ]
        lines += [
            f"- {rule}: origine `{src}:{cid}` introuvable dans les sources"
            for rule, src, cid in m["missing"]
        ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", type=Path,
                    default=Path("/Volumes/Ugreen/projects/inr"),
                    help="directory containing green-claude and green_codex")
    ap.add_argument("--out", type=Path, default=REPO_ROOT / "docs" / "matrice-correspondance.md")
    ap.add_argument("--check", action="store_true",
                    help="fail on unresolvable provenance ids (drift guard)")
    args = ap.parse_args()
    m = build_matrix(args.sources)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_markdown(m), encoding="utf-8")
    print(f"matrix written: {args.out}")
    print(f"green-vibe rules: {len(m['rows'])}")
    print(f"green-claude covered: {m['claude_covered']}/{m['claude_total']}")
    print(f"green-codex covered: {m['codex_covered']}/{m['codex_total']}")
    if m["missing"]:
        for item in m["missing"]:
            print(f"UNRESOLVED: {item}", file=sys.stderr)
        if args.check:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
