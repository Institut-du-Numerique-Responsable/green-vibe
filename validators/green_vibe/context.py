"""Context detection: files in a change set -> scopes, project markers, families."""

from __future__ import annotations

import json
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "dist", "build", "__pycache__", ".mypy_cache"}

EXT_SCOPES = {
    ".py": {"py"},
    ".js": {"js"},
    ".mjs": {"js"},
    ".cjs": {"js"},
    ".ts": {"ts", "js"},
    ".jsx": {"jsx", "js"},
    ".tsx": {"tsx", "ts", "jsx"},
    ".vue": {"vue", "js", "html", "css"},
    ".java": {"java"},
    ".go": {"go"},
    ".rs": {"rs"},
    ".php": {"php"},
    ".rb": {"rb"},
    ".cs": {"cs"},
    ".kt": {"kt"},
    ".kts": {"kt"},
    ".swift": {"swift"},
    ".c": {"c"},
    ".h": {"c"},
    ".cc": {"cpp"},
    ".cpp": {"cpp"},
    ".cxx": {"cpp"},
    ".hpp": {"cpp"},
    ".hh": {"cpp"},
    ".svelte": {"svelte", "js", "html", "css"},
    ".astro": {"astro", "html", "js", "css"},
    ".scala": {"scala"},
    ".sc": {"scala"},
    ".jl": {"jl"},
    ".nim": {"nim"},
    ".zig": {"zig"},
    ".sql": {"sql"},
    ".html": {"html"},
    ".htm": {"html"},
    ".css": {"css"},
    ".scss": {"scss", "css"},
    ".sh": {"sh", "bash"},
    ".bash": {"sh", "bash"},
    ".zsh": {"sh", "bash"},
    ".json": {"json"},
    ".yaml": {"yaml", "conf"},
    ".yml": {"yaml", "conf"},
    ".toml": {"conf"},
    ".ini": {"conf"},
    ".conf": {"conf"},
    ".cfg": {"conf"},
    ".md": {"docs"},
}

# Extensions audited as code/text; everything else is skipped by the scanner.
TEXT_SUFFIXES = set(EXT_SCOPES) | {".pl", ".pls", ".pkb"}


def iter_files(paths: list[str | Path]) -> list[Path]:
    """Expand the given paths into files, skipping vendored/build dirs."""
    files: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            for child in sorted(p.rglob("*")):
                if any(part in SKIP_DIRS for part in child.parts):
                    continue
                if child.is_file() and child.suffix.lower() in TEXT_SUFFIXES:
                    files.append(child)
        # Non-existent paths are ignored: the caller decides whether that is an error.
    return files


def file_scopes(path: Path) -> set[str]:
    name = path.name.lower()
    if name == "dockerfile" or name.startswith("dockerfile."):
        return {"dockerfile"}
    if name == "package.json":
        return {"json", "package.json"}
    scopes = set(EXT_SCOPES.get(path.suffix.lower(), set()))
    if name == "docker-compose.yml" or name == "docker-compose.yaml":
        scopes.add("dockerfile")
    if ".github" in path.parts and "workflows" in path.parts:
        scopes.add("workflow-yaml")
    scopes.add("any")
    return scopes


def detect_project_markers(root: Path) -> dict:
    """Light project fingerprint from manifest files, for context analysis."""
    markers = {}
    checks = {
        "python": ["requirements.txt", "pyproject.toml", "setup.py"],
        "node": ["package.json"],
        "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
        "go": ["go.mod"],
        "rust": ["Cargo.toml"],
        "php": ["composer.json"],
        "ruby": ["Gemfile"],
        "swift": ["Package.swift"],
        "docker": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
        "ci_github": [".github/workflows"],
    }
    for label, names in checks.items():
        markers[label] = any((root / n).exists() for n in names)
    return markers


def _head(path: Path, size: int = 4096) -> str:
    """First bytes of a file, where imports live; empty on read errors."""
    try:
        with path.open(encoding="utf-8", errors="replace") as fh:
            return fh.read(size)
    except OSError:
        return ""


def detect_frameworks(files: list[Path]) -> list[str]:
    """Framework hints from file names and common import lines (cheap heuristics)."""
    hints = set()
    for f in files:
        suffix = f.suffix.lower()
        solid = suffix in {".jsx", ".tsx", ".js", ".ts"} and "solid-js" in _head(f)
        if solid:
            hints.add("solid")  # JSX shared by React and Solid: the import decides
        elif suffix in {".jsx", ".tsx"} or f.name.lower() in {"next.config.js", "next.config.mjs"}:
            hints.add("react")
        if f.name.lower() in {"nuxt.config.js", "nuxt.config.ts"}:
            hints.add("vue")
        if suffix == ".vue":
            hints.add("vue")
        if f.name.lower() in {"angular.json"} or f.name.lower().endswith((".component.ts", ".component.html")):
            hints.add("angular")
        if f.name.lower() in {"svelte.config.js"} or suffix == ".svelte":
            hints.add("svelte")
    return sorted(hints)


def analyze(paths: list[str | Path], project_root: Path | None = None) -> dict:
    """Full context analysis used by `select`."""
    files = iter_files(paths)
    scopes: set[str] = set()
    by_lang: dict[str, int] = {}
    for f in files:
        fs = file_scopes(f) - {"any"}
        scopes |= fs
        for s in fs:
            by_lang[s] = by_lang.get(s, 0) + 1
    root = project_root or (Path(paths[0]).resolve() if paths else Path.cwd())
    return {
        "files": [str(f) for f in files],
        "scopes": sorted(scopes),
        "files_per_scope": by_lang,
        "project_markers": detect_project_markers(root) if root else {},
        "frameworks": detect_frameworks(files),
    }


# Families selected for any coding intervention (process-level core).
ALWAYS_FAMILIES = {"strategy", "service", "architecture", "measure", "algo"}

# Scope tokens that switch on each optional family.
FAMILY_TRIGGERS = {
    "frontend": {"html", "css", "scss", "js", "ts", "jsx", "tsx", "vue", "svelte", "astro"},
    "ux": {"html", "css", "scss", "js", "ts", "jsx", "tsx", "vue", "svelte", "astro", "swift", "kt"},
    "content": {"html", "css", "scss", "js", "ts", "jsx", "tsx", "vue", "svelte", "astro"},
    "backend": {"py", "java", "go", "js", "ts", "sql", "rs", "php", "rb", "cs", "kt", "c", "cpp",
                "scala", "jl", "nim", "zig"},
    "data": {"sql", "py", "java", "go", "js", "ts", "rs", "php", "rb", "cs", "kt"},
    "api": {"py", "java", "go", "js", "ts", "sql", "rs", "php", "rb", "cs", "kt", "swift"},
    "infra": {"dockerfile", "yaml", "conf", "workflow-yaml", "sh", "bash"},
}


def relevant_families(context: dict, extra: list[str] | None = None) -> list[str]:
    """Families worth loading for this context, deterministic and cheap."""
    scopes = set(context.get("scopes", []))
    markers = context.get("project_markers", {})
    families = set(ALWAYS_FAMILIES)
    for fam, triggers in FAMILY_TRIGGERS.items():
        if scopes & triggers:
            families.add(fam)
    if markers.get("docker") or markers.get("ci_github"):
        families.add("infra")
    if extra:
        for f in extra:
            families.add(f)
    return sorted(families)


def select_rule_ids(context: dict, rules: list[dict],
                    extra_families: list[str] | None = None) -> list[str]:
    """Rule ids relevant to this context: family-driven selection.

    Core families split into always-on (process) and scope-triggered; language
    families are gated by scope overlap, framework families by the detected
    framework; `usage` and `tokens` rules are conversation-scoped and never
    auto-selected.
    """
    scopes = set(context.get("scopes", []))
    frameworks = set(context.get("frameworks", []))
    families = set(relevant_families(context, extra_families))
    selected = []
    for r in rules:
        family = r["_family"]
        if family in ("usage", "tokens"):
            continue
        if family in FRAMEWORK_FAMILIES:
            if FRAMEWORK_FAMILIES[family] in frameworks:
                selected.append(r["id"])
        elif family.startswith("lang-"):
            if _lang_family_scopes(family) & scopes:
                selected.append(r["id"])
        elif family in families:
            selected.append(r["id"])
    return selected


# Framework catalogs share file extensions with plain JS/TS: gate them on the
# framework detected in the change set, not on the scope.
FRAMEWORK_FAMILIES = {
    "lang-react": "react",
    "lang-vue": "vue",
    "lang-angular": "angular",
    "lang-svelte": "svelte",
    "lang-solid": "solid",
}


def _lang_family_scopes(family: str) -> set[str]:
    mapping = {
        "lang-python": {"py"},
        "lang-javascript": {"js", "ts", "jsx", "tsx"},
        "lang-java": {"java"},
        "lang-sql": {"sql"},
        "lang-html-css": {"html", "css", "scss"},
        "lang-shell": {"sh", "bash"},
        "lang-go": {"go"},
        "lang-rust": {"rs"},
        "lang-php": {"php"},
        "lang-ruby": {"rb"},
        "lang-csharp": {"cs"},
        "lang-kotlin": {"kt"},
        "lang-swift": {"swift"},
        "lang-c": {"c"},
        "lang-cpp": {"cpp"},
        "lang-scala": {"scala"},
        "lang-julia": {"jl"},
        "lang-nim": {"nim"},
        "lang-zig": {"zig"},
        "lang-astro": {"astro"},
    }
    return mapping.get(family, set())
