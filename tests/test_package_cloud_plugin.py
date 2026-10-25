from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path, PurePosixPath


SCRIPT = Path(__file__).parents[1] / "scripts" / "package_cloud_plugin.py"
SPEC = importlib.util.spec_from_file_location("package_cloud_plugin", SCRIPT)
PACKAGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGER)


class CloudPluginPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        (self.source / ".codex-plugin").mkdir(parents=True)
        self.default_prompt = ["Find papers", "Read the selected PDF"]
        metadata = {"name": "paperone", "version": "0.2.1", "description": "Researchzy literature tools.",
                    "author": {"name": "Researchzy"},
                    "interface": {"developerName": "Researchzy", "longDescription": "Find and read papers.",
                                  "defaultPrompt": self.default_prompt}}
        (self.source / ".codex-plugin" / "plugin.json").write_text(json.dumps(metadata), encoding="utf-8")
        for name in ("paperone-literature", "nature-reader", "nature-paper-card", "nature-shared"):
            directory = self.source / "skills" / name
            directory.mkdir(parents=True)
            (directory / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Test workflow.\n---\nUse this workflow.\n", encoding="utf-8")
        (self.source / "licenses").mkdir()
        (self.source / "licenses" / "upstream.txt").write_text("Upstream license", encoding="utf-8")
        (self.source / "THIRD_PARTY_NOTICES.md").write_text("Notices", encoding="utf-8")
        (self.source / "requirements.txt").write_text("PyMuPDF>=1.24,<2\n", encoding="utf-8")
        (self.source / ".mcp.json").write_text('{"production":"https://app.researchzy.com/mcp"}', encoding="utf-8")

    def build(self, target="private", version="0.3.0"):
        return PACKAGER.build_archive(self.source, self.root / f"{target}.zip", target, version)

    def test_cloud_package_preserves_nested_skill_resources(self):
        script = self.source / "skills" / "nature-reader" / "scripts" / "read.py"
        script.parent.mkdir()
        payload = b"print('preserve exact bytes')\r\n"
        script.write_bytes(payload)
        reference = script.parent.parent / "references" / "source.json"
        reference.parent.mkdir()
        reference.write_bytes(b'{"source":"example"}')
        with zipfile.ZipFile(self.build()) as archive:
            self.assertEqual(archive.read("paperone-test/skills/nature-reader/scripts/read.py"), payload)
            self.assertEqual(archive.read("paperone-test/skills/nature-reader/references/source.json"), reference.read_bytes())
            self.assertEqual(sum(n.endswith("/SKILL.md") for n in archive.namelist()), 4)
            self.assertIn("paperone-test/licenses/upstream.txt", archive.namelist())
            self.assertIn("paperone-test/requirements.txt", archive.namelist())

    def test_target_selects_exact_test_oauth_client(self):
        for target, client in (("private", "paperone-chatgpt-test"), ("submission-draft", "paperone-openai-draft-test")):
            with self.subTest(target=target), zipfile.ZipFile(self.build(target)) as archive:
                server = json.loads(archive.read("paperone-test/mcp.json"))["mcpServers"]["researchzy"]
                auth = server["extensions"]["com.openai"]["auth"]
                self.assertEqual(server["type"], "streamable-http")
                self.assertEqual(server["url"], "https://app.testp1.testdomain.stream/mcp")
                self.assertEqual(auth["type"], "oauth")
                self.assertEqual(auth["client"], {"mode": "provided", "clientId": client, "tokenEndpointAuthMethod": "none"})
                self.assertEqual(auth["baseScopes"], ["library.read", "pdf.read"])
                self.assertNotIn("clientSecret", auth["client"])
                self.assertNotIn("headers", server)

    def test_manifest_and_archive_paths_are_portable(self):
        with zipfile.ZipFile(self.build()) as archive:
            names = archive.namelist()
            manifest = json.loads(archive.read("paperone-test/plugin.json"))
            interface = manifest["extensions"]["com.openai"]["interface"]
            self.assertEqual(manifest["name"], "paperone-test")
            self.assertEqual(manifest["version"], "0.3.0")
            self.assertEqual(interface["displayName"], "Researchzy Test")
            self.assertLessEqual(len(interface["shortDescription"]), 30)
            self.assertEqual(interface["defaultPrompt"], self.default_prompt)
            self.assertIn("paperone-test/" + interface["logo"][2:], names)
            for name in names:
                self.assertTrue(name.startswith("paperone-test/"))
                self.assertFalse(PurePosixPath(name).is_absolute())
                self.assertNotIn("..", PurePosixPath(name).parts)
                self.assertNotIn("\\", name)
            self.assertFalse(any(n.endswith((".app.json", ".mcp.json")) for n in names))
            self.assertFalse({"skills", "mcpServers", "apps", "interface"} & manifest.keys())

    def test_archive_rejects_symlinks_and_unsafe_resources(self):
        secret = self.source / "skills" / "nature-reader" / ".env"
        secret.write_text("SECRET=do-not-upload", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unsafe|credential|secret"):
            self.build()
        secret.unlink()
        outside = self.root / "outside.txt"
        outside.write_text("outside", encoding="utf-8")
        link = self.source / "skills" / "nature-reader" / "linked.txt"
        try:
            os.symlink(outside, link)
        except OSError:
            if os.name != "nt":
                raise
            outside_directory = self.root / "outside-directory"
            outside_directory.mkdir()
            subprocess.run(["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(outside_directory)],
                           check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        with self.assertRaisesRegex(ValueError, "symlink|link|outside"):
            self.build()

    def test_generated_caches_are_excluded(self):
        cache = self.source / "skills" / "nature-reader" / "__pycache__"
        cache.mkdir()
        (cache / "read.pyc").write_bytes(b"cache")
        with zipfile.ZipFile(self.build()) as archive:
            self.assertFalse(any("__pycache__" in n or n.endswith(".pyc") for n in archive.namelist()))

    def test_private_registered_app_binding_replaces_raw_mcp(self):
        output = PACKAGER.build_archive(self.source, self.root / "app-bound.zip", "private", "0.3.1",
                                        app_id="fixture-registered-app")
        with zipfile.ZipFile(output) as archive:
            manifest = json.loads(archive.read("paperone-test/plugin.json"))
            app = json.loads(archive.read("paperone-test/.app.json"))
            compatibility = json.loads(archive.read("paperone-test/.codex-plugin/plugin.json"))
            self.assertEqual(manifest["extensions"]["com.openai"]["apps"], "./.app.json")
            self.assertEqual(app, {"apps": {"paperone": {"id": "fixture-registered-app", "required": True}}})
            self.assertEqual(compatibility["apps"], "./.app.json")
            self.assertEqual(compatibility["version"], "0.3.1")
            self.assertNotIn("mcpServers", compatibility)
            self.assertNotIn("paperone-test/mcp.json", archive.namelist())
            self.assertNotIn("paperone-test/.mcp.json", archive.namelist())
            self.assertEqual(sum(n.endswith("/SKILL.md") for n in archive.namelist()), 4)

    def test_app_binding_is_private_only_and_requires_nonempty_id(self):
        for target, app_id in (("submission-draft", "fixture-registered-app"), ("private", ""), ("private", " ")):
            with self.subTest(target=target, app_id=app_id), self.assertRaises(ValueError):
                PACKAGER.build_archive(self.source, self.root / "invalid-app.zip", target, "0.3.1", app_id=app_id)

    def test_invalid_targets_versions_and_nested_outputs_are_rejected(self):
        for target, version in (("production", "0.3.0"), ("private", "latest"), ("private", "v0.3.0")):
            with self.subTest(target=target, version=version), self.assertRaises(ValueError):
                self.build(target, version)
        with self.assertRaisesRegex(ValueError, "output|source"):
            PACKAGER.build_archive(self.source, self.source / "out.zip", "private", "0.3.0")


if __name__ == "__main__":
    unittest.main()
