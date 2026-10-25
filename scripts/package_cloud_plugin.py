"""Package the existing Researchzy workflows for private cloud use or a submission draft."""
from __future__ import annotations

import argparse
import json
import re
import stat
import struct
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "paperone-test"
TEST_ORIGIN = "https://app.testp1.testdomain.stream"
CLIENTS = {"private": "paperone-chatgpt-test", "submission-draft": "paperone-openai-draft-test"}
SKILLS = {"researchzy-literature", "nature-reader", "nature-paper-card", "nature-shared"}
SKIP_DIRECTORIES = {"__pycache__", "node_modules", ".venv", ".git", ".pytest_cache"}
UNSAFE_NAMES = {".npmrc", ".pypirc", "credentials.json", "token.json", "tokens.json", "id_rsa", "id_ed25519"}


def _validate_version(version: str) -> None:
    match = re.fullmatch(
        r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
        r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?",
        version,
    )
    if not match or any(part.isdigit() and len(part) > 1 and part.startswith("0")
                        for part in (match.group(1) or "").split(".")):
        raise ValueError("version must be a strict semantic version")


def _check_resource(path: Path, source: Path) -> None:
    attributes = getattr(path.lstat(), "st_file_attributes", 0)
    if path.is_symlink() or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 1024):
        raise ValueError(f"symlink or reparse link is not allowed: {path.name}")
    if not path.resolve().is_relative_to(source):
        raise ValueError(f"resource is outside source: {path.name}")
    name = path.name.lower()
    if name.startswith(".env") or name in UNSAFE_NAMES or path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}:
        raise ValueError(f"unsafe credential resource: {path.name}")


def _resources(source: Path) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    skill_root = source / "skills"
    if not skill_root.is_dir() or {p.name for p in skill_root.iterdir() if p.is_dir()} != SKILLS:
        raise ValueError("source must contain the four expected Researchzy skills")
    for directory in (skill_root, source / "licenses"):
        _check_resource(directory, source)
        for path in sorted(directory.rglob("*")):
            _check_resource(path, source)
            relative = path.relative_to(source)
            if any(part in SKIP_DIRECTORIES for part in relative.parts) or path.suffix in {".pyc", ".pyo"}:
                continue
            if path.is_file():
                result[relative.as_posix()] = path.read_bytes()
    for skill in SKILLS:
        if f"skills/{skill}/SKILL.md" not in result:
            raise ValueError(f"missing SKILL.md: {skill}")
    for name in ("THIRD_PARTY_NOTICES.md", "requirements.txt"):
        path = source / name
        _check_resource(path, source)
        result[name] = path.read_bytes()
    return result


def _icon() -> bytes:
    path = ROOT / "assets" / "paperone-mark.png"
    if path.is_symlink():
        raise ValueError("icon must not be a symlink")
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("icon must be a PNG")
    width, height = struct.unpack(">II", data[16:24])
    if width != height or not 48 <= width <= 4096 or len(data) > 5 * 1024 * 1024:
        raise ValueError("icon must be square, 48-4096 pixels and at most 5 MiB")
    return data


def build_archive(source: Path, output: Path, target: str, version: str, *, app_id: str | None = None) -> Path:
    if target not in CLIENTS:
        raise ValueError("target must be private or submission-draft")
    if app_id is not None and (target != "private" or not app_id.strip() or app_id != app_id.strip()):
        raise ValueError("a nonempty registered App ID is supported only for private packages")
    _validate_version(version)
    if source.is_symlink():
        raise ValueError("source must not be a symlink")
    source, output = source.resolve(), output.resolve()
    if output.is_relative_to(source):
        raise ValueError("output archive must be outside source")
    metadata_path = source / ".codex-plugin" / "plugin.json"
    _check_resource(metadata_path, source)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    original_interface = metadata["interface"]
    interface = {key: original_interface[key] for key in ("longDescription", "developerName", "defaultPrompt")
                 if key in original_interface}
    interface.update(displayName="Researchzy Test", shortDescription="Search papers and read PDFs",
                     category="Productivity", capabilities=[], logo="./assets/paperone-mark.png",
                     composerIcon="./assets/paperone-mark.png")
    manifest = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": PACKAGE_NAME, "version": version, "description": metadata["description"],
        "author": metadata["author"], "extensions": {"com.openai": {"interface": interface}},
    }
    for key in ("homepage", "repository"):
        if key in metadata:
            manifest[key] = metadata[key]
    mcp = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
        "mcpServers": {"researchzy": {
            "type": "streamable-http", "url": TEST_ORIGIN + "/mcp",
            "extensions": {"com.openai": {"auth": {
                "type": "oauth", "client": {"mode": "provided", "clientId": CLIENTS[target],
                                               "tokenEndpointAuthMethod": "none"},
                "authorizationUrl": TEST_ORIGIN + "/oauth2/authorize",
                "tokenUrl": TEST_ORIGIN + "/oauth2/token", "baseScopes": ["library.read", "pdf.read"],
            }}},
        }},
    }
    resources = _resources(source)
    resources["assets/paperone-mark.png"] = _icon()
    if app_id is None:
        configurations = {"plugin.json": manifest, "mcp.json": mcp}
    else:
        manifest["extensions"]["com.openai"]["apps"] = "./.app.json"
        compatibility = {**metadata, "name": PACKAGE_NAME, "version": version,
                         "interface": interface, "apps": "./.app.json"}
        compatibility.pop("mcpServers", None)
        configurations = {
            "plugin.json": manifest,
            ".codex-plugin/plugin.json": compatibility,
            ".app.json": {"apps": {"paperone": {"id": app_id, "required": True}}},
        }
    for name, value in configurations.items():
        resources[name] = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, suffix=".zip", delete=False) as temp:
        temporary = Path(temp.name)
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, data in sorted(resources.items()):
                archive.writestr(f"{PACKAGE_NAME}/{name}", data)
        if temporary.stat().st_size > 100 * 1024 * 1024:
            raise ValueError("archive exceeds the platform's 100 MiB upload limit")
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "plugins" / "paperone")
    parser.add_argument("--target", choices=CLIENTS, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--app-id", help="Registered platform App ID (private target only)")
    args = parser.parse_args()
    print(build_archive(args.source, args.output, args.target, args.version, app_id=args.app_id))


if __name__ == "__main__":
    main()
