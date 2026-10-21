"""Rule catalog loading and index generation."""

from __future__ import annotations

import json
from pathlib import Path


def find_root(start: Path | None = None) -> Path:
    """Locate the Green Vibe root (the directory containing rules/)."""
    candidates = []
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / "rules" / "usage.json").is_file():
            return parent
    candidates.append(Path.home() / ".vibe" / "plugins" / "green-vibe")
    for extra in candidates:
        if (extra / "rules" / "usage.json").is_file():
            return extra
    raise FileNotFoundError(
        "Green Vibe rule catalog not found (no rules/usage.json above this file)"
    )


REQUIRED_FIELDS = (
    "id",
    "title",
    "what",
    "why",
    "how",
    "verify",
    "priority",
    "applies",
    "origin",
)


def _rule_files(root: Path) -> list[Path]:
    files = sorted((root / "rules" / "core").glob("*.json"))
    files += sorted((root / "rules" / "lang").glob("*.json"))
    files += [root / "rules" / "usage.json", root / "rules" / "tokens.json"]
    return [f for f in files if f.is_file()]


def load_rules(root: Path | None = None) -> list[dict]:
    """Load every rule sheet; validate the required schema fields."""
    root = root or find_root()
    rules = []
    seen = set()
    for path in _rule_files(root):
        catalog = json.loads(path.read_text(encoding="utf-8"))
        for rule in catalog["rules"]:
            missing = [f for f in REQUIRED_FIELDS if f not in rule]
            if missing:
                raise ValueError(f"{path.name}:{rule.get('id')} missing fields {missing}")
            if rule["id"] in seen:
                raise ValueError(f"duplicate rule id {rule['id']} in {path.name}")
            seen.add(rule["id"])
            rule["_family"] = catalog["family"]
            rule["_file"] = path.name
            rules.append(rule)
    return rules


def rule_index(rules: list[dict]) -> list[dict]:
    """Compact one-line index entries (this is what gets committed as index.json)."""
    entries = []
    for r in rules:
        detect = r.get("detect") or {}
        entries.append(
            {
                "id": r["id"],
                "title": r["title"],
                "family": r["_family"],
                "priority": r["priority"],
                "applies": r["applies"],
                "automation": detect.get("automation", "none"),
                "scopes": sorted(
                    {s for p in detect.get("patterns", []) for s in p.get("scope", [])}
                ),
                "rgesn": r.get("rgesn"),
                "origin": r["origin"],
            }
        )
    return entries


def build_index(root: Path | None = None) -> list[dict]:
    return rule_index(load_rules(root))


def write_index(out: Path | None = None, root: Path | None = None) -> Path:
    root = root or find_root()
    out = out or root / "rules" / "index.json"
    index = build_index(root)
    out.write_text(
        json.dumps({"version": "1.0", "rules": index}, indent=1, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    return out
