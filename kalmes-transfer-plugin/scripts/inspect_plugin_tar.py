#!/usr/bin/env python3
"""Inspect a plain Kalmes plugin tar without extracting it."""

import argparse
import hashlib
import json
import re
import sys
import tarfile
from pathlib import Path, PurePosixPath


DEFAULT_MAX_MEMBERS = 10000
DEFAULT_MAX_BYTES = 1024 * 1024 * 1024
MAX_META_BYTES = 5 * 1024 * 1024
KNOWN_CODE_TYPES = {"API", "Html", "Others", "Initial"}


def digest_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_member_name(name):
    normalized = name.replace("\\", "/")
    if not normalized or normalized.startswith("/"):
        raise ValueError("empty or absolute member path")
    if re.match(r"^[A-Za-z]:", normalized):
        raise ValueError("drive-qualified member path")
    path = PurePosixPath(normalized)
    if ".." in path.parts:
        raise ValueError("parent traversal in member path")
    clean = path.as_posix().rstrip("/")
    if clean in {"", "."}:
        raise ValueError("empty member path")
    return clean


def plugin_root_candidates(member_map):
    names = set(member_map)
    candidates = []
    for name in sorted(names):
        if name != "meta.json" and not name.endswith("/meta.json"):
            continue
        root = name[: -len("/meta.json")] if name.endswith("/meta.json") else ""
        files_dir = f"{root}/files" if root else "files"
        files_prefix = files_dir + "/"
        if files_dir in names or any(item.startswith(files_prefix) for item in names):
            candidates.append((root, name, files_dir))
    return candidates


def inspect_archive(path, max_members, max_bytes):
    report = {
        "path": str(path.resolve()),
        "archive_size": path.stat().st_size,
        "sha256": digest_file(path),
        "valid": False,
        "errors": [],
        "warnings": [],
    }

    try:
        archive = tarfile.open(path, "r:*")
    except (tarfile.TarError, OSError) as exc:
        report["errors"].append(f"cannot open as tar: {exc}")
        return report

    with archive:
        members = archive.getmembers()
        report["member_count"] = len(members)
        report["unpacked_size"] = sum(max(0, member.size) for member in members)
        if len(members) > max_members:
            report["errors"].append(
                f"member count {len(members)} exceeds limit {max_members}"
            )
        if report["unpacked_size"] > max_bytes:
            report["errors"].append(
                f"unpacked size {report['unpacked_size']} exceeds limit {max_bytes}"
            )

        member_map = {}
        for member in members:
            try:
                name = normalize_member_name(member.name)
            except ValueError as exc:
                report["errors"].append(f"unsafe member {member.name!r}: {exc}")
                continue
            if name in member_map:
                report["errors"].append(f"duplicate member path: {name}")
                continue
            member_map[name] = member
            if member.issym() or member.islnk():
                report["errors"].append(f"link member is not allowed: {name}")
            elif not (member.isfile() or member.isdir()):
                report["errors"].append(f"special member is not allowed: {name}")

        candidates = plugin_root_candidates(member_map)
        if len(candidates) != 1:
            report["errors"].append(
                "expected exactly one plugin root containing meta.json and files/; "
                f"found {len(candidates)}"
            )
            return report

        root, meta_name, files_dir = candidates[0]
        report["plugin_root"] = root or "."
        meta_member = member_map[meta_name]
        if not meta_member.isfile():
            report["errors"].append("meta.json is not a regular file")
            return report
        if meta_member.size > MAX_META_BYTES:
            report["errors"].append(
                f"meta.json size {meta_member.size} exceeds limit {MAX_META_BYTES}"
            )
            return report

        try:
            stream = archive.extractfile(meta_member)
            if stream is None:
                raise ValueError("cannot read meta.json")
            meta = json.loads(stream.read().decode("utf-8-sig", errors="strict"))
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            report["errors"].append(f"invalid UTF-8 JSON metadata: {exc}")
            return report
        if not isinstance(meta, dict):
            report["errors"].append("meta.json root must be an object")
            return report

        plugin_name = meta.get("plugin_name")
        version = meta.get("version")
        descriptors = meta.get("files")
        if not isinstance(plugin_name, str) or not plugin_name.strip():
            report["errors"].append("plugin_name must be a non-empty string")
        if not isinstance(version, str) or not version.strip():
            report["errors"].append("version must be a non-empty string")
        for label, value in (("plugin_name", plugin_name), ("version", version)):
            if isinstance(value, str) and not re.fullmatch(r"[A-Za-z0-9._-]+", value):
                report["errors"].append(
                    f"{label} must contain only letters, digits, dots, underscores, or hyphens"
                )
        if not isinstance(descriptors, list):
            report["errors"].append("files must be an array")
            descriptors = []
        elif not descriptors:
            report["warnings"].append("files is empty")

        declared = []
        initial_files = []
        for index, descriptor in enumerate(descriptors):
            if not isinstance(descriptor, dict):
                report["errors"].append(f"files[{index}] must be an object")
                continue
            filename = descriptor.get("name")
            code_type = descriptor.get("type")
            if not isinstance(filename, str) or not filename:
                report["errors"].append(f"files[{index}].name must be a non-empty string")
                continue
            if Path(filename).name != filename or "/" in filename or "\\" in filename:
                report["errors"].append(f"declared file must be a basename: {filename!r}")
                continue
            declared.append(filename)
            expected = f"{files_dir}/{filename}"
            member = member_map.get(expected)
            if member is None or not member.isfile():
                report["errors"].append(f"declared file is missing: {expected}")
            if not isinstance(code_type, str) or not code_type:
                report["errors"].append(f"files[{index}].type must be a non-empty string")
            elif code_type not in KNOWN_CODE_TYPES:
                report["warnings"].append(
                    f"unknown code type {code_type!r} for {filename}"
                )
            if code_type == "Initial":
                initial_files.append(filename)

        files_prefix = files_dir + "/"
        packaged_files = sorted(
            name[len(files_prefix) :]
            for name, member in member_map.items()
            if name.startswith(files_prefix) and member.isfile()
        )
        top_level_packaged = sorted(name for name in packaged_files if "/" not in name)
        unlisted = sorted(set(top_level_packaged) - set(declared))
        if unlisted:
            report["warnings"].append(
                "unlisted top-level files under files/: " + ", ".join(unlisted)
            )

        env_names = []
        envs = meta.get("env") or []
        if not isinstance(envs, list):
            report["errors"].append("env must be an array when present")
        else:
            for index, env in enumerate(envs):
                if not isinstance(env, dict) or not isinstance(env.get("name"), str):
                    report["errors"].append(f"env[{index}] must contain a string name")
                else:
                    env_names.append(env["name"])

        fap_collections = []
        fap_ds = meta.get("fap_ds") or []
        if not isinstance(fap_ds, list):
            report["errors"].append("fap_ds must be an array when present")
        else:
            for item in fap_ds:
                if isinstance(item, dict) and isinstance(item.get("collectionName"), str):
                    fap_collections.append(item["collectionName"])

        if meta.get("flat") is True:
            report["warnings"].append(
                "flat=true installs into the shared extraCode directory"
            )
        if initial_files:
            report["warnings"].append(
                "Initial modules execute automatically during import: "
                + ", ".join(initial_files)
            )

        report.update(
            {
                "plugin_name": plugin_name,
                "version": version,
                "flat": meta.get("flat") is True,
                "expose": meta.get("expose") is not False,
                "declared_files": declared,
                "packaged_files": packaged_files,
                "initial_files": initial_files,
                "env_names": env_names,
                "fap_collections": fap_collections,
            }
        )
        report["valid"] = not report["errors"]
        return report


def print_human(report):
    print("VALID" if report["valid"] else "INVALID")
    for key in (
        "path",
        "archive_size",
        "sha256",
        "member_count",
        "unpacked_size",
        "plugin_root",
        "plugin_name",
        "version",
        "flat",
        "expose",
    ):
        if key in report:
            print(f"{key}: {report[key]}")
    for key in ("declared_files", "initial_files", "env_names", "fap_collections"):
        if key in report:
            values = report[key]
            print(f"{key}: {', '.join(values) if values else '-'}")
    for warning in report["warnings"]:
        print(f"WARNING: {warning}")
    for error in report["errors"]:
        print(f"ERROR: {error}")


def main():
    parser = argparse.ArgumentParser(
        description="Inspect a plain Kalmes plugin tar without extracting it."
    )
    parser.add_argument("archive", type=Path)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--max-members", type=int, default=DEFAULT_MAX_MEMBERS)
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    args = parser.parse_args()

    if args.max_members <= 0 or args.max_bytes <= 0:
        parser.error("limits must be positive")
    if not args.archive.is_file():
        parser.error(f"archive does not exist: {args.archive}")

    report = inspect_archive(args.archive, args.max_members, args.max_bytes)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
