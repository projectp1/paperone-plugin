# Maintenance and provenance

This plugin was extracted from `projectp1/paperone_server/plugins/paperone` on 2026-09-18. The source commit was `186d1e4944a8698d83e040bdf61d8a5042fd1732`; the initial import copied 70 tracked plugin files. This repository starts with the plugin files only and contains no backend history, runtime configuration, or data.

The extraction added a repository marketplace, installation guidance, and tool documentation; repaired links to content outside the package; and retained the plugin name, MCP configuration, skills, and behavior. Version 0.2.1 makes English the default for PaperOne-owned skill and repository documentation. Nature Skills provenance and PaperOne-specific modifications are listed in `THIRD_PARTY_NOTICES.md`.

## Releases

Each skills change ships as a semantic version in `.codex-plugin/plugin.json` and a matching annotated Git tag `v<version>` on `main`. Version 0.3.0 makes the skill wording independent of the host's connection flow, so the same skills serve ChatGPT, Codex and the PaperOne research agent.

The research agent image (`paperone_server/agent-runtime/Dockerfile`) pins a tag and the SHA-256 of its GitHub source archive (`https://github.com/projectp1/paperone-plugin/archive/refs/tags/<tag>.tar.gz`). Update both there when releasing a tag. ChatGPT receives the same skills through `scripts/package_cloud_plugin.py` and an App-backed skill update of the existing plugin.

## Validation

Run the bundled tests from the repository root:

```sh
python3 -m unittest discover -s plugins/paperone/skills/nature-paper-card/tests
python3 -m unittest discover -s plugins/paperone/skills/nature-shared/tests
```

Validate `plugins/paperone` with the `validate_plugin.py` script bundled with Codex's `plugin-creator` skill. Before publishing, verify that the marketplace source resolves, relative documentation links work, and the target environment passes MCP authorization and tool-call acceptance.

The backend uses an independent identifier index to map DOI and arXiv identifiers to `corpusId`, then retrieves full metadata. This repository does not operate that index or deploy the backend.
