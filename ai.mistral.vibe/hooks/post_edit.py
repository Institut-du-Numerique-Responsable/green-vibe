#!/usr/bin/env python3
"""Green Vibe post_tool hook: audit what a write added, fail-open.

Vibe calls this after write_file/edit with a JSON payload on stdin. The hook
audits only the content introduced by the write (not the whole file) and, when
it finds candidates, appends them to the tool output via
hook_specific_output.additional_context so the model can fix them in the same
turn. Silence when there is nothing to report.

Fail-open by construction: any error exits 0 with no output, so the hook can
never block the work.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # .../green-vibe
sys.path.insert(0, str(ROOT / "validators"))

from green_vibe import audit as audit_mod  # noqa: E402
from green_vibe import rules as rules_mod  # noqa: E402


def added_text(tool_input: dict) -> tuple[str, str] | None:
    """Return (text_added, filename) for write_file/edit tool inputs."""
    filename = tool_input.get("file_path") or tool_input.get("path") or ""
    if not filename:
        return None
    if "content" in tool_input:
        return str(tool_input["content"]), filename
    if tool_input.get("new_string"):
        return str(tool_input["new_string"]), filename
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    tool_name = payload.get("tool_name", "")
    if tool_name not in ("write_file", "edit"):
        return 0
    added = added_text(payload.get("tool_input") or {})
    if not added:
        return 0
    text, filename = added
    try:
        rule_list = rules_mod.load_rules(ROOT)
        findings = audit_mod.audit_text(text, filename, rule_list)
    except Exception:
        return 0  # fail-open: never block the write
    if not findings:
        return 0
    lines = ["[green-vibe] NR candidates in what was written:"]
    for f in findings[:10]:
        lines.append(
            f"  {f['status']} {f['rule']} {f['title']} — {f['note']} | how: {f['how']}"
        )
    if len(findings) > 10:
        lines.append(f"  ... {len(findings) - 10} more")
    lines.append(
        "  Interpret each candidate in context before acting; full rule view: "
        "python3 validators/green-vibe rules <family>"
    )
    response = {
        "decision": "allow",
        "hook_specific_output": {"additional_context": "\n".join(lines)},
    }
    print(json.dumps(response))
    return 0


if __name__ == "__main__":
    sys.exit(main())
