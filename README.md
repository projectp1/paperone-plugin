# Researchzy Plugin

[简体中文](README.zh-CN.md)

Researchzy for Codex: search scholarly papers, work with your library, retrieve PDFs, read papers with source anchors, and create evidence-grounded research cards.

## Capabilities

| Capability | Tool or skill |
|---|---|
| Search by title, keywords, DOI, or arXiv ID | `search_papers` |
| Retrieve metadata for a known paper ID | `get_paper` |
| Browse personal collections and personal/shared papers | `list_collections`, `list_library_papers` |
| Create a personal collection (shared collections cannot be created) | `create_collection` |
| Save a paper to the library or a writable collection | `add_paper_to_library` |
| Get PDF metadata and download URLs | `get_pdf_download` |
| Build a source-grounded bilingual reader | `nature-reader` |
| Create an evidence-grounded research card | `nature-paper-card` |

## Install in Codex

With a Codex version that supports plugins:

```sh
codex plugin marketplace add projectp1/paperone-plugin --ref main
codex plugin add paperone@projectp1
```

Connect Researchzy in the host, complete sign-in and authorization, then start a new task so Codex loads the plugin. A GitHub marketplace source is user-installed and is separate from publication in the universal plugin directory.

The bundled MCP configuration targets `https://app.researchzy.com/mcp`. Production MCP and OAuth still require end-to-end connection validation. The test environment's DOI, DOI URL, and arXiv REST searches were verified on 2026-09-18. See [connection setup](docs/connection.md) for environment details.

## Examples

- Find DOI `10.1051/0004-6361/202556799` and show its metadata and PDF availability.
- Find arXiv paper `2508.10985`.
- Read this paper closely and create a Chinese-English reader with source anchors.
- Create a Paper Card for this PDF and distinguish author claims from analysis.

See the [plugin guide](plugins/paperone/README.md) and [tool reference](plugins/paperone/docs/tools.md). PDF preparation scripts require Python 3.10+ and the optional dependencies in the plugin's `requirements.txt`.

## Repository layout

```text
.agents/plugins/marketplace.json   Repository marketplace
plugins/paperone/                  Installable plugin package
docs/                              Connection and maintenance notes
```

This repository owns the plugin package. The Researchzy backend owns the API, MCP service, OAuth implementation, and search indexes. See [maintenance notes](docs/maintenance.md) for provenance and validation.

## Licensing

Bundled Nature Skills retain their Apache-2.0 license and attribution; see [third-party notices](plugins/paperone/THIRD_PARTY_NOTICES.md). Researchzy-owned files do not yet declare a separate open-source license.
