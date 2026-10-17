"""Static audit: deterministic pattern detection over masked source text."""

from __future__ import annotations

import re
from pathlib import Path

from .context import SKIP_DIRS, file_scopes, iter_files

# A finding is a candidate until a human or the model confirms it in context.
STATUS_FAIL = "FAIL"  # deterministic detector, violation confirmed by the pattern
STATUS_REVIEW = "REVIEW"  # candidate: context must settle it


# ---------------------------------------------------------------------------
# Masking: blank out strings/comments (positions preserved) so patterns do not
# match inside literals or comments. Ported from the Green Codex approach.
# ---------------------------------------------------------------------------

def _blank(m: re.Match) -> str:
    return re.sub(r"[^\n]", " ", m.group())


def mask_c_like(text: str) -> str:
    text = re.sub(r"//[^\n]*", _blank, text)
    text = re.sub(r"/\*.*?\*/", _blank, text, flags=re.S)
    return re.sub(r"'(?:\\.|[^'\\\n])*'|\"(?:\\.|[^\"\\\n])*\"|`(?:\\.|[^`\\])*`", _blank, text)


def mask_python(text: str) -> str:
    text = re.sub(r"#[^\n]*", _blank, text)
    text = re.sub(r"([rbfu]?\"\"\"|''')(?:(?!\1).)*?\1", _blank, text, flags=re.S)
    return re.sub(r"[rbfu]?'(?:\\.|[^'\\\n])*'|[rbfu]?\"(?:\\.|[^\"\\\n])*\"", _blank, text)


def mask_sql(text: str) -> str:
    text = re.sub(r"--[^\n]*", _blank, text)
    text = re.sub(r"/\*.*?\*/", _blank, text, flags=re.S)
    return re.sub(r"'(?:''|[^'])*'", _blank, text)


def mask_html(text: str) -> str:
    return re.sub(r"<!--.*?-->", _blank, text, flags=re.S)


def mask_css(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", _blank, text, flags=re.S)
    return re.sub(r"'[^'\n]*'|\"[^\"\n]*\"", _blank, text)


def mask_shell(text: str) -> str:
    # Mask comments and strings, but keep the shebang line (line 1) intact.
    first, nl, rest = text.partition("\n")
    if rest:
        rest = re.sub(r"(?<!\S)#(?!\[)[^\n]*", _blank, rest)
        rest = re.sub(r"'[^'\n]*'|\"[^\"\n]*\"", _blank, rest)
    return first + nl + rest


def mask_yaml(text: str) -> str:
    return re.sub(r"(?<!\S)#(?!\[)[^\n]*", _blank, text)


def mask_text(path: Path, text: str) -> str:
    suffix = path.suffix.lower()
    name = path.name.lower()
    if name.startswith("dockerfile"):
        return mask_shell(text)
    if suffix == ".py":
        return mask_python(text)
    if suffix in {".js", ".mjs", ".cjs", ".ts", ".jsx", ".tsx", ".java", ".go"}:
        return mask_c_like(text)
    if suffix == ".sql":
        return mask_sql(text)
    if suffix in {".html", ".htm", ".vue"}:
        return mask_html(text)
    if suffix in {".css", ".scss"}:
        return mask_css(text)
    if suffix in {".sh", ".bash", ".zsh"}:
        return mask_shell(text)
    if suffix in {".yml", ".yaml"}:
        return mask_yaml(text)
    return text


# ---------------------------------------------------------------------------
# Special detectors (rules whose check is cleaner in code than in regex)
# ---------------------------------------------------------------------------

def _det_shebang_strict(masked: str, raw: str, scopes: set[str]) -> list[int]:
    """NR-LANG-SH-002: script preamble missing set -euo pipefail."""
    if not ({"sh", "bash"} & scopes):
        return []
    first = raw.split("\n", 1)[0]
    if not first.startswith("#!"):
        return []
    head = raw[:2000]
    if re.search(r"(?m)^set\s+[euo].*$|^set\s+-euo\s+pipefail", head) or "set -euo pipefail" in head:
        return []
    return [1]


def _det_nested_loops(masked: str, raw: str, scopes: set[str]) -> list[int]:
    """NR-ALGO-002: a for/while loop whose body contains another loop, by indentation."""
    if not (scopes & {"py", "js", "ts", "jsx", "tsx", "java", "go"}):
        return []
    lines = raw.split("\n")
    hits = []
    for i, line in enumerate(lines):
        m = re.match(r"^([ \t]*)(?:for|while)\b", line)
        if not m:
            continue
        indent = len(m.group(1))
        for j in range(i + 1, min(i + 40, len(lines))):
            nxt = lines[j]
            if not nxt.strip():
                continue
            stripped = len(nxt) - len(nxt.lstrip(" \t"))
            if stripped <= indent:
                break  # block closed
            if re.match(r"^[ \t]*(?:for|while)\b", nxt):
                hits.append(i + 1)
                break
    return hits


SPECIAL_DETECTORS = {
    "shebang_strict": _det_shebang_strict,
    "nested_loops": _det_nested_loops,
}


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def _rule_patterns(rule: dict) -> list[dict]:
    detect = rule.get("detect") or {}
    return detect.get("patterns", [])


def audit_files(paths: list[str | Path], rules: list[dict]) -> list[dict]:
    """Scan the given files and return findings (candidates and confirmed)."""
    files = iter_files(paths)
    findings = []
    compiled = _compile_rules(rules)
    for path in files:
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scopes = file_scopes(path)
        masked = mask_text(path, raw)
        lines = None  # computed lazily

        for rule, patterns, flags, detector in compiled:
            hits: list[tuple[int, dict]] = []
            if detector:
                hit_lines = SPECIAL_DETECTORS[detector](masked, raw, scopes)
                hits = [(ln, {}) for ln in hit_lines]
            else:
                for pattern in patterns:
                    if not (set(pattern.get("scope", ["any"])) & scopes):
                        continue
                    try:
                        for m in re.finditer(pattern["re"], masked, flags):
                            start = m.start()
                            if lines is None:
                                lines = _line_offsets(masked)
                            ln = _line_of(lines, start)
                            hits.append((ln, pattern))
                    except re.error:
                        continue  # malformed pattern: skip, never crash the audit
            for ln, pattern in hits:
                findings.append(
                    {
                        "rule": rule["id"],
                        "title": rule["title"],
                        "path": str(path),
                        "line": ln,
                        "status": STATUS_FAIL
                        if (rule.get("detect") or {}).get("automation") == "full"
                        else STATUS_REVIEW,
                        "note": pattern.get("note", "") if isinstance(pattern, dict) else "",
                        "how": rule.get("how", ""),
                        "why": rule.get("why", ""),
                    }
                )
    # Deduplicate (rule, path, line)
    seen = set()
    unique = []
    for f in sorted(findings, key=lambda x: (x["rule"], x["path"], x["line"])):
        key = (f["rule"], f["path"], f["line"])
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


def _compile_rules(rules: list[dict]):
    out = []
    for rule in rules:
        detect = rule.get("detect") or {}
        detector = detect.get("detector")
        if detector and detector not in SPECIAL_DETECTORS:
            detector = None
        patterns = _rule_patterns(rule)
        if not patterns and not detector:
            continue
        # Compile once per rule; patterns are case-insensitive + multiline.
        compiled = [dict(p, _re=re.compile(p["re"], re.I | re.M)) for p in patterns]
        out.append((rule, compiled, re.I | re.M, detector))
    return out


def _line_offsets(text: str) -> list[int]:
    offsets = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            offsets.append(i + 1)
    return offsets


def _line_of(offsets: list[int], pos: int) -> int:
    lo, hi = 0, len(offsets) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if offsets[mid] <= pos:
            lo = mid
        else:
            hi = mid - 1
    return lo + 1


def audit_text(text: str, filename: str, rules: list[dict]) -> list[dict]:
    """Audit a text buffer (used by the post-edit hook on freshly written content)."""
    import tempfile, os

    with tempfile.NamedTemporaryFile(
        "w", suffix=_suffix_for(filename), delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(text)
        tmp_path = tmp.name
    try:
        findings = audit_files([tmp_path], rules)
        for f in findings:
            f["path"] = filename
        return findings
    finally:
        os.unlink(tmp_path)


def _suffix_for(filename: str) -> str:
    p = Path(filename)
    if p.name.lower().startswith("dockerfile"):
        return ".sh"  # dockerfile rules are handled by name; suffix only routes masking
    return p.suffix or ".txt"
