#!/usr/bin/env python3
"""
Package lint for the ecosystem-digital-twin skill. Run after every change:

  python3 tests/check_package.py            # from the skill root
  python3 tests/check_package.py --strict   # also require folder name == skill name

Checks: SKILL.md frontmatter parses as YAML with valid name, description and
compatibility; SKILL.md stays under 500 lines; code fences open and close
cleanly (a closing fence followed by text silently swallows the rest of a
file); every referenced package path exists; version strings agree across
SKILL.md, READMEs, CHANGELOG, TESTS and the scripts; long reference files
carry a table of contents; every script answers --help; every test named
under "Automated by" in TESTS.md exists.
Exit 0 clean, 3 on any error. Warnings do not fail the run.
"""

import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def frontmatter(text):
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with a '---' frontmatter line")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("frontmatter is not closed with '---'")
    return text[4:end], text[end + 5:]


def parse_yaml(block):
    try:
        import yaml  # PyYAML, when available, is the strict check
    except ImportError:
        yaml = None
    if yaml is not None:
        return yaml.safe_load(block), "PyYAML"
    data = {}
    for line in block.splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"frontmatter line is not 'key: value': {line[:40]}")
        value = value.strip()
        if value[:1] in "\"'":
            if len(value) < 2 or value[-1] != value[0]:
                raise ValueError(f"unterminated quoted value for '{key}'")
            value = value[1:-1]
        elif ": " in value:
            raise ValueError(f"unquoted ': ' inside the value of '{key}' (invalid YAML)")
        data[key.strip()] = value
    return data, "minimal parser (install PyYAML for the strict check)"


def fence_problems(rel, text):
    problems, inside = [], False
    for n, line in enumerate(text.splitlines(), start=1):
        s = line.strip()
        if not s.startswith("```"):
            continue
        rest = s[3:]
        if not inside:
            if rest and not re.match(r"^[A-Za-z0-9_+-]+$", rest):
                problems.append(f"{rel}:{n}: opening fence has text after the info string")
            inside = True
        else:
            if rest:
                problems.append(f"{rel}:{n}: closing fence followed by text - the block never closes")
            else:
                inside = False
    if inside:
        problems.append(f"{rel}: a code block is never closed")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args(argv)
    errors, warnings, info = [], [], {}

    skill = read("SKILL.md")
    try:
        block, body = frontmatter(skill)
        meta, parser = parse_yaml(block)
        info["yaml_parser"] = parser
    except Exception as exc:  # any parse failure is the finding
        errors.append(f"SKILL.md frontmatter: {exc}")
        meta, body = {}, skill
    name = str(meta.get("name", ""))
    desc = str(meta.get("description", ""))
    if not NAME_RE.match(name) or len(name) > 64 or "claude" in name or "anthropic" in name:
        errors.append(f"name '{name}': lowercase letters, digits and hyphens, max 64, no reserved words")
    if not desc or len(desc) > 1024:
        errors.append(f"description must be 1-1024 characters (has {len(desc)})")
    if re.search(r"<[^>]+>", desc):
        errors.append("description must not contain XML/HTML tags")
    if "compatibility" in meta and len(str(meta["compatibility"])) > 500:
        errors.append("compatibility must be at most 500 characters")
    info["description_chars"] = len(desc)
    folder = os.path.basename(ROOT)
    if name and folder != name:
        msg = f"folder '{folder}' differs from skill name '{name}': install it as '{name}/'"
        (errors if a.strict else warnings).append(msg)

    lines = skill.count("\n") + 1
    info["skill_md_lines"] = lines
    if lines > 500:
        errors.append(f"SKILL.md has {lines} lines; keep it under 500 and move detail to references/")

    md_files = []
    for d, _, files in os.walk(ROOT):
        if "/.git" in d:
            continue
        md_files += [os.path.relpath(os.path.join(d, f), ROOT) for f in files if f.endswith(".md")]
    for rel in sorted(md_files):
        errors += fence_problems(rel, read(rel))

    for rel in sorted(md_files):
        for ref in set(re.findall(r"`((?:references|assets|examples|scripts|tests)/[\w./-]+?)`", read(rel))):
            if not os.path.exists(os.path.join(ROOT, ref)):
                errors.append(f"{rel}: referenced path '{ref}' does not exist")

    version = str((meta.get("metadata") or {}).get("version", "")) if isinstance(meta.get("metadata"), dict) else ""
    info["version"] = version
    checks = {
        "README.md": r"Current version: \*\*([\d.]+)\*\*",
        "README.ru.md": r"Текущая версия: \*\*([\d.]+)\*\*",
        "CHANGELOG.md": r"^## v([\d.]+)",
        "tests/TESTS.md": r"\(v([\d.]+)\)",
        "scripts/evidence_search.py": r"ecosystem-digital-twin/([\d.]+)",
    }
    for rel, pat in checks.items():
        if not os.path.exists(os.path.join(ROOT, rel)):
            continue
        m = re.search(pat, read(rel), re.M)
        if not m or m.group(1) != version:
            errors.append(f"{rel}: version {m.group(1) if m else 'missing'} != SKILL.md {version}")

    for rel in sorted(md_files):
        if rel.startswith("references/"):
            text = read(rel)
            if text.count("\n") > 100 and "## Contents" not in "\n".join(text.splitlines()[:15]):
                errors.append(f"{rel}: over 100 lines without a '## Contents' list near the top")

    tests_md = read("tests/TESTS.md")
    test_code = read("tests/test_scripts.py")
    for line in tests_md.splitlines():
        if line.startswith("**Automated by:**"):
            for name in re.findall(r"`(Test\w+|test_\w+)`", line):
                if not re.search(rf"(class|def) {name}\b", test_code):
                    errors.append(f"tests/TESTS.md names automated test '{name}', which does not exist")

    scripts = sorted(f for f in os.listdir(os.path.join(ROOT, "scripts")) if f.endswith(".py"))
    for f in scripts:
        res = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", f), "--help"],
                             capture_output=True, text=True, timeout=60)
        if res.returncode != 0:
            errors.append(f"scripts/{f} --help exited {res.returncode}: {res.stderr.strip()[:120]}")
        if not res.stdout.strip():
            errors.append(f"scripts/{f} --help printed nothing")
    info["scripts"] = scripts

    out = {"root": ROOT, "errors": errors, "warnings": warnings, "info": info,
           "result": "fail" if errors else "pass"}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 3 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
