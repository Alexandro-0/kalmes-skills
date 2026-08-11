#!/usr/bin/env python3
"""Validate the complete Kalmes Skills repository without third-party packages."""

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path


CANONICAL_REMOTE = "https://github.com/Alexandro-0/kalmes-skills"
TEXT_SUFFIXES = {
    ".cfg",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".ps1",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
TEXT_NAMES = {
    ".gitattributes",
    ".gitignore",
    "LICENSE",
    "SKILL.md",
}
FORBIDDEN_BRAND = re.compile(
    "|".join(
        (
            "Kal" + "MES",
            "Kal" + "Mes",
            "kal" + "Mes",
            "Kal" + "-Mes",
            "kal" + "-Mes",
            "Kal" + "-MES",
            "kal" + "-MES",
        )
    )
)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PLACEHOLDER_TOKENS = ("[" + "TODO", "TODO" + ":")


def run_git(root, *args):
    return subprocess.check_output(
        ["git", "-C", str(root), *args],
        stderr=subprocess.STDOUT,
    ).decode("utf-8", errors="strict").strip()


def normalize_remote(value):
    remote = value.strip().replace("\\", "/").rstrip("/")
    if remote.endswith(".git"):
        remote = remote[:-4]
    if remote.startswith("git@github.com:"):
        remote = "https://github.com/" + remote[len("git@github.com:") :]
    return remote.lower()


def repository_files(root):
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(root), "ls-files", "-co", "--exclude-standard", "-z"],
            stderr=subprocess.STDOUT,
        )
        names = [os.fsdecode(item) for item in raw.split(b"\0") if item]
        return sorted(root / name for name in names if (root / name).is_file())
    except (OSError, subprocess.CalledProcessError):
        return sorted(
            path
            for path in root.rglob("*")
            if path.is_file() and ".git" not in path.parts
        )


def is_text_file(path):
    return path.name in TEXT_NAMES or path.suffix.lower() in TEXT_SUFFIXES


def parse_frontmatter(path, errors):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        errors.append(f"{path}: missing opening frontmatter delimiter")
        return {}, text
    try:
        end = lines.index("---", 1)
    except ValueError:
        errors.append(f"{path}: missing closing frontmatter delimiter")
        return {}, text

    fields = {}
    keys = []
    for line in lines[1:end]:
        if not line.strip() or line[:1].isspace():
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            errors.append(f"{path}: unsupported frontmatter line: {line!r}")
            continue
        key, value = match.groups()
        keys.append(key)
        fields[key] = value.strip().strip('"').strip("'")
    if keys != ["name", "description"]:
        errors.append(
            f"{path}: frontmatter must contain only name then description; found {keys}"
        )
    if not fields.get("name"):
        errors.append(f"{path}: empty name")
    if not fields.get("description") or "TODO" in fields.get("description", ""):
        errors.append(f"{path}: empty or placeholder description")
    return fields, text


def quoted_yaml_value(text, key):
    match = re.search(rf"^\s+{re.escape(key)}:\s*([\"']).*\1\s*$", text, re.MULTILINE)
    return bool(match)


def validate(root, require_canonical_origin=False):
    errors = []
    warnings = []
    report = {
        "root": str(root),
        "canonical_remote": CANONICAL_REMOTE,
        "errors": errors,
        "warnings": warnings,
    }

    try:
        actual_root = Path(run_git(root, "rev-parse", "--show-toplevel")).resolve()
        if actual_root != root:
            errors.append(f"path is not repository root; Git root is {actual_root}")
        try:
            origin = run_git(root, "remote", "get-url", "origin")
            report["origin"] = origin
            if normalize_remote(origin) != normalize_remote(CANONICAL_REMOTE):
                message = f"origin is not canonical: {origin}"
                if require_canonical_origin:
                    errors.append(message)
                else:
                    warnings.append(message)
        except subprocess.CalledProcessError:
            message = "origin remote is missing"
            if require_canonical_origin:
                errors.append(message)
            else:
                warnings.append(message)
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError) as exc:
        errors.append(f"cannot inspect Git repository: {exc}")

    files = repository_files(root)
    report["files_checked"] = len(files)
    report["text_files_checked"] = 0
    for path in files:
        if not is_text_file(path):
            continue
        report["text_files_checked"] += 1
        try:
            data = path.read_bytes()
            if b"\x00" in data:
                errors.append(f"{path.relative_to(root)}: NUL byte in text file")
                continue
            if data.startswith(b"\xef\xbb\xbf"):
                warnings.append(f"{path.relative_to(root)}: UTF-8 BOM present")
            text = data.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            errors.append(f"{path.relative_to(root)}: invalid UTF-8: {exc}")
            continue
        if FORBIDDEN_BRAND.search(text):
            errors.append(f"{path.relative_to(root)}: invalid Kalmes display spelling")
        if any(token in text for token in PLACEHOLDER_TOKENS):
            errors.append(f"{path.relative_to(root)}: placeholder TODO remains")
        if path.suffix.lower() == ".py":
            try:
                ast.parse(text, filename=str(path))
            except SyntaxError as exc:
                errors.append(f"{path.relative_to(root)}: Python syntax error: {exc}")

    skill_dirs = sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and path.name.startswith("kalmes-") and (path / "SKILL.md").is_file()
    )
    report["skill_count"] = len(skill_dirs)
    if not skill_dirs:
        errors.append("no top-level kalmes-* skills found")

    seen_names = set()
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        fields, text = parse_frontmatter(skill_md, errors)
        name = fields.get("name")
        if name != skill_dir.name:
            errors.append(
                f"{skill_md.relative_to(root)}: name {name!r} does not match folder {skill_dir.name!r}"
            )
        if name in seen_names:
            errors.append(f"duplicate skill name: {name}")
        seen_names.add(name)
        if not re.fullmatch(r"[a-z0-9-]{1,63}", skill_dir.name):
            errors.append(f"invalid skill folder name: {skill_dir.name}")
        if len(text.splitlines()) > 500:
            warnings.append(f"{skill_md.relative_to(root)}: exceeds 500 lines")

        agent_path = skill_dir / "agents" / "openai.yaml"
        if not agent_path.is_file():
            errors.append(f"{skill_dir.name}: missing agents/openai.yaml")
        else:
            agent_text = agent_path.read_text(encoding="utf-8")
            for key in ("display_name", "short_description", "default_prompt"):
                if not quoted_yaml_value(agent_text, key):
                    errors.append(f"{agent_path.relative_to(root)}: {key} must be quoted")
            prompt = re.search(
                r"^\s+default_prompt:\s*[\"'](.*)[\"']\s*$",
                agent_text,
                re.MULTILINE,
            )
            if not prompt or f"${skill_dir.name}" not in prompt.group(1):
                errors.append(
                    f"{agent_path.relative_to(root)}: default_prompt must invoke ${skill_dir.name}"
                )

        for link in MARKDOWN_LINK.findall(text):
            if "://" in link or link.startswith("#"):
                continue
            target = (skill_dir / link.split("#", 1)[0]).resolve()
            try:
                target.relative_to(skill_dir.resolve())
            except ValueError:
                errors.append(f"{skill_md.relative_to(root)}: link escapes skill: {link}")
                continue
            if not target.exists():
                errors.append(f"{skill_md.relative_to(root)}: missing linked path: {link}")

    for readme_name in ("README.md", "README.zh-TW.md"):
        readme_path = root / readme_name
        if not readme_path.is_file():
            errors.append(f"missing {readme_name}")
            continue
        readme = readme_path.read_text(encoding="utf-8")
        for skill_dir in skill_dirs:
            if f"./{skill_dir.name}" not in readme:
                errors.append(f"{readme_name}: missing catalog link for {skill_dir.name}")

    report["valid"] = not errors
    return report


def print_human(report):
    print("VALID" if report["valid"] else "INVALID")
    for key in (
        "root",
        "canonical_remote",
        "origin",
        "files_checked",
        "text_files_checked",
        "skill_count",
    ):
        if key in report:
            print(f"{key}: {report[key]}")
    for warning in report["warnings"]:
        print(f"WARNING: {warning}")
    for error in report["errors"]:
        print(f"ERROR: {error}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".", type=Path)
    parser.add_argument("--require-canonical-origin", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = args.repository.resolve()
    if not root.is_dir():
        parser.error(f"repository directory does not exist: {root}")
    report = validate(root, args.require_canonical_origin)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
