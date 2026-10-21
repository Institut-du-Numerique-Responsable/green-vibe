"""Green Vibe CLI: select, rules, audit, report, index, stats."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import audit as audit_mod
from . import context, report, rules as rules_mod


def _load(root: Path | None = None):
    rule_list = rules_mod.load_rules(root)
    by_id = {r["id"]: r for r in rule_list}
    return rule_list, by_id


def cmd_select(args):
    rule_list, _ = _load(args.root)
    ctx = context.analyze(args.paths)
    selected = context.select_rule_ids(ctx, rule_list, getattr(args, "family", None))
    out = {
        "context": ctx,
        "families": context.relevant_families(ctx, getattr(args, "family", None)),
        "selected_rules": selected,
        "count": len(selected),
    }
    print(json.dumps(out, indent=1, ensure_ascii=False))
    if not selected:
        print(
            "Aucune règle sélectionnée : le contexte n'expose aucun langage connu. "
            "Les règles de service et de mesure (NR-SERVICE-*, NR-MEASURE-*) restent applicables.",
            file=sys.stderr,
        )


def cmd_rules(args):
    rule_list, _ = _load(args.root)
    wanted = [w.lower() for w in args.what]
    for r in rule_list:
        fam = r["_family"].lower()
        rid = r["id"].lower()
        if wanted and not any(w in fam or w in rid for w in wanted):
            continue
        detect = r.get("detect") or {}
        automation = detect.get("automation", "none")
        rgesn = r.get("rgesn")
        level = f", {r['level']}" if r.get("level") else ""
        print(f"{r['id']} [{r['priority']}{level}] {r['title']}")
        print(f"  WHAT : {r['what']}")
        print(f"  WHY  : {r['why']}")
        print(f"  HOW  : {r['how']}")
        print(f"  VERIFY: {r['verify']['method']} — {r['verify']['how']}")
        print(f"  AUTO : {automation} | RGESN: {rgesn or '—'} | ORIGIN: {', '.join(r['origin'])}")


def cmd_audit(args):
    rule_list, _ = _load(args.root)
    findings = audit_mod.audit_files(args.paths, rule_list)
    payload = {"findings": findings, "count": len(findings)}
    print(json.dumps(payload, indent=1, ensure_ascii=False))
    for f in findings:
        print(
            f"{f['status']:<7} {f['rule']:<18} {f['path']}:{f['line']}  {f['note']}",
            file=sys.stderr,
        )


def cmd_report(args):
    rule_list, by_id = _load(args.root)
    payload = json.loads(Path(args.audit).read_text(encoding="utf-8"))
    findings = payload.get("findings", [])
    selected = args.selected or sorted({f["rule"] for f in findings})
    if not selected:
        selected = args.selected or []
    results = report.results_from_audit(findings, selected, by_id)
    verified = {}
    if args.verified:
        for item in args.verified:
            rid, _, ev = item.partition("=")
            verified[rid.strip()] = ev.strip()
    results = report.mark_verified(results, verified)
    out = report.render_report(
        results, args.intervention, args.mode, findings=findings
    )
    if args.json:
        print(json.dumps(out, indent=1, ensure_ascii=False))
    else:
        print(out["bilan"])


def cmd_index(args):
    rule_list, _ = _load(args.root)
    scopes = {}
    for r in rule_list:
        scopes[r["_family"]] = scopes.get(r["_family"], 0) + 1
    out = rules_mod.write_index(args.out, args.root)
    print(f"index written: {out} ({len(rule_list)} rules: {scopes})")


def cmd_stats(_args):
    rule_list, _ = _load(None)
    fam = {}
    auto = {"full": 0, "partial": 0, "special": 0, "none": 0}
    for r in rule_list:
        fam[r["_family"]] = fam.get(r["_family"], 0) + 1
        auto[(r.get("detect") or {}).get("automation", "none")] += 1
    print(json.dumps({"total": len(rule_list), "families": fam, "automation": auto}, indent=1))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="green-vibe", description="Green Vibe NR validators")
    ap.add_argument("--root", type=Path, default=None, help="Green Vibe root (default: autodetect)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("select", help="Context analysis + rule selection")
    p.add_argument("paths", nargs="+")
    p.add_argument("--family", action="append", help="force a family on (e.g. --family ai)")
    p.set_defaults(func=cmd_select)

    p = sub.add_parser("rules", help="Compact rule view (filter by family/id)")
    p.add_argument("what", nargs="*", default=[])
    p.set_defaults(func=cmd_rules)

    p = sub.add_parser("audit", help="Static audit of paths (deterministic findings)")
    p.add_argument("paths", nargs="+")
    p.set_defaults(func=cmd_audit)

    p = sub.add_parser("report", help="Normalized results + pedagogical bilan")
    p.add_argument("--audit", required=True, help="audit JSON file (or '-' for stdin)")
    p.add_argument("--selected", nargs="*", help="selected rule ids (default: rules with findings)")
    p.add_argument("--verified", nargs="*", metavar="RULE=EVIDENCE",
                   help="rules actually verified: NR-XXX=tests/foo.py::test_bar")
    p.add_argument("--intervention", default="")
    p.add_argument("--mode", choices=["discret", "pedagogique", "audit"], default="pedagogique")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("index", help="Regenerate rules/index.json")
    p.add_argument("--out", type=Path, default=None)
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("stats", help="Catalog statistics")
    p.set_defaults(func=cmd_stats)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
