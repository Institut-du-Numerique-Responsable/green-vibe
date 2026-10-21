"""Normalized results and the pedagogical report (bilan).

Statuses (normalized):
  verified               the rule's own check was actually executed and passed
  failed                 a confirmed violation (deterministic finding, or a failed check)
  not_applicable         the rule does not apply to this intervention, with reason
  not_tested             applied but no check was executed
  manual_review_required a candidate finding that context must settle
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone

from .audit import STATUS_FAIL, STATUS_REVIEW

VALID_STATUSES = (
    "verified",
    "failed",
    "not_applicable",
    "not_tested",
    "manual_review_required",
)


def results_from_audit(findings: list[dict], selected: list[str], rules_by_id: dict,
                       applied: list[str] | None = None) -> list[dict]:
    """Build one normalized result per selected rule from audit findings.

    `applied` lists the rules the intervention actually applied (model-declared);
    a rule declared applied but without evidence is `not_tested` unless the
    audit found a violation.
    """
    findings_by_rule: dict[str, list[dict]] = {}
    for f in findings:
        findings_by_rule.setdefault(f["rule"], []).append(f)

    applied = set(applied or selected)  # default: selected and applied coincide
    results = []
    for rid in selected:
        rule = rules_by_id.get(rid)
        hits = findings_by_rule.get(rid, [])
        if hits:
            status = "failed" if any(h["status"] == STATUS_FAIL for h in hits) \
                else "manual_review_required"
            evidence = [
                f"{h.get('path', '?')}:{h.get('line', '?')}" for h in hits
            ]
        elif rid in applied:
            status = "not_tested"  # never `verified` from a declaration alone
            evidence = []
        else:
            status = "not_tested"
            evidence = []
        results.append(
            {
                "rule_id": rid,
                "title": (rule or {}).get("title", rid),
                "status": status,
                "verification_method": (rule or {}).get("verify", {}).get("method", "review"),
                "evidence": evidence,
                "limitations": (rule or {}).get("limits", []),
            }
        )
    return results


def mark_verified(results: list[dict], verified: dict[str, str]) -> list[dict]:
    """Mark rules as verified when real evidence exists (a test that ran, a
    measurement taken, a command executed). `verified` maps rule id -> evidence.
    A rule with findings stays failed; verified requires a clean state."""
    vmap = dict(verified)
    for r in results:
        if r["rule_id"] in vmap and r["status"] not in ("failed",):
            r["status"] = "verified"
            r["evidence"] = [vmap[r["rule_id"]]]
    return results


def bilan(results: list[dict], intervention: str, mode: str = "pedagogique") -> str:
    """Render the French pedagogical report (BILAN NUMERIQUE RESPONSABLE)."""
    counts = Counter(r["status"] for r in results)
    verified = [r for r in results if r["status"] == "verified"]
    failed = [r for r in results if r["status"] == "failed"]
    review = [r for r in results if r["status"] == "manual_review_required"]
    teachable = verified[:2] or review[:1]

    lines = []
    lines.append("🌱 BILAN NUMÉRIQUE RESPONSABLE")
    lines.append("")
    lines.append("INTERVENTION :")
    lines.append(intervention or "(décrire la modification)")
    lines.append("")
    if mode == "discret":
        applied = [r for r in results if r["status"] in ("verified", "not_tested")]
        lines.append("RÈGLES NR APPLIQUÉES :")
        for r in applied:
            lines.append(f"- {r['rule_id']} : {r['title']} [{r['status']}]")
        if teachable:
            lines.append("")
            lines.append("💡 À RETENIR : " + _teach_line(teachable[0]))
    else:
        lines.append("RÈGLES NR APPLIQUÉES :")
        shown = verified + failed + review if mode == "audit" else verified + failed
        for r in shown:
            lines.append("")
            lines.append(f"RÈGLE {r['rule_id']} : {r['title']}")
            lines.append(f"Statut : {r['status']}")
            if r["evidence"]:
                lines.append("Vérification/preuves : " + ", ".join(r["evidence"]))
            if r["limitations"]:
                lines.append("Limites : " + " ".join(r["limitations"]))
        lines.append("")
        lines.append("POINTS À EXAMINER :")
        for r in review if mode != "audit" else []:
            lines.append(f"- {r['rule_id']} : {r['limitations'][0] if r['limitations'] else 'contexte à trancher'}")
        lines.append("")
        lines.append("💡 CE QUE TU PEUX RETENIR")
        for r in teachable:
            lines.append("- " + _teach_line(r))
    lines.append("")
    lines.append("BILAN :")
    lines.append(f"- Règles évaluées : {len(results)}")
    lines.append(f"- Vérifiées : {counts.get('verified', 0)}")
    lines.append(f"- En échec : {counts.get('failed', 0)}")
    lines.append(f"- À examiner : {counts.get('manual_review_required', 0)}")
    lines.append(f"- Non testées : {counts.get('not_tested', 0)}")
    return "\n".join(lines)


def _teach_line(result: dict) -> str:
    # The `why` field is the pedagogical one-liner of each rule sheet.
    return result.get("limitations") and result["limitations"][0] or \
        f"{result['rule_id']} : appliquer la règle ne suffit pas, sa vérification fait la preuve."


def render_report(results: list[dict], intervention: str, mode: str,
                  findings: list[dict] | None = None) -> dict:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "intervention": intervention,
        "mode": mode,
        "results": results,
        "bilan": bilan(results, intervention, mode),
    }
    if findings is not None:
        payload["findings"] = findings
    return payload
