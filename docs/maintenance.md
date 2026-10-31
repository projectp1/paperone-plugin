# Maintenance and provenance

This plugin was extracted from `projectp1/paperone_server/plugins/paperone` on 2026-09-18. The source commit was `186d1e4944a8698d83e040bdf61d8a5042fd1732`; the initial import copied 70 tracked plugin files. This repository starts with the plugin files only and contains no backend history, runtime configuration, or data.

The extraction added a repository marketplace, installation guidance, and tool documentation; repaired links to content outside the package; and retained the plugin name, MCP configuration, skills, and behavior. Version 0.2.1 makes English the default for Researchzy-owned skill and repository documentation. Nature Skills provenance and Researchzy-specific modifications are listed in `THIRD_PARTY_NOTICES.md`.

## Releases

Each skills change ships as a semantic version in `.codex-plugin/plugin.json` and a matching annotated Git tag `v<version>` on `main`. Version 0.3.0 makes the skill wording independent of the host's connection flow, so the same skills serve ChatGPT, Codex and the Researchzy research agent. Version 0.4.0 renames the product from PaperOne to Researchzy in the skills, the plugin's display metadata and its MCP target `https://app.researchzy.com/mcp`; the plugin id `paperone` and the skill names stay the same. Version 1.0.1 renames the MCP server from `paperone` to `researchzy`, so hosts list the tools under Researchzy (for example `mcp__researchzy__search_papers` in the research agent); hosts that stored a sign-in under the old server name ask to connect again. Version 1.1.0 adds the `create_collection` tool to the documentation and skills: it creates personal collections only, never shared ones, and needs the `library.write` scope. Version 1.1.1 corrects the connection documentation for the server's OAuth changes: every tool needs an account, tokens are refreshed (one-hour access tokens, 90-day rotating refresh tokens), apps can be disconnected on the Account page, and Claude, Claude Code, VS Code and Codex can connect without the plugin. The skill also describes the keyword search filters. Version 1.2.0 renames the literature skill from `paperone-literature` to `researchzy-literature`, and its source acquisition reference to `references/researchzy-source.md`; hosts and prompts that name the skill must use the new name. Version 1.3.0 documents `readerUrl`: papers whose PDF Researchzy can show link to the Researchzy reader, read-only for index papers and with the user's annotations for library papers, and `add_paper_to_library` reports `hasReadablePdf`. The skill gives the link to the user and never fetches it. Version 1.3.1 changes no skill or tool: it ships the new Researchzy logo (the fore-edge R on a pale blue tile) as the cloud package's logo and composer icon. Version 1.4.0 adds the `create_pdf_upload` tool to the documentation and skills: it returns a short-lived signed URL that the host PUTs a local PDF file to, for a library paper that has no PDF yet. A paper's PDF is never replaced, the paper's metadata stays as it is, and the tool needs the `library.write` scope. Hosts without file access or HTTP requests cannot use it.

The research agent image (`paperone_server/agent-runtime/Dockerfile`) pins a tag and the SHA-256 of its GitHub source archive (`https://github.com/projectp1/paperone-plugin/archive/refs/tags/<tag>.tar.gz`). The server's plugin catalog (`paperone.agent.plugins` in `paperone_server/src/main/resources/application.yml`: version, archive URL, archive SHA-256 and notes URL) offers a release to existing agents as an upgrade. Update them when releasing a tag. ChatGPT receives the same skills through `scripts/package_cloud_plugin.py` and an App-backed skill update of the existing plugin.

## Validation

Run the bundled tests from the repository root:

```sh
python3 -m unittest discover -s plugins/paperone/skills/nature-paper-card/tests
python3 -m unittest discover -s plugins/paperone/skills/nature-shared/tests
```

Validate `plugins/paperone` with the `validate_plugin.py` script bundled with Codex's `plugin-creator` skill. Before publishing, verify that the marketplace source resolves, relative documentation links work, and the target environment passes MCP authorization and tool-call acceptance.

The backend uses an independent identifier index to map DOI and arXiv identifiers to `corpusId`, then retrieves full metadata. This repository does not operate that index or deploy the backend.
