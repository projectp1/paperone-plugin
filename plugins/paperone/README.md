# Researchzy Literature Plugin

Version 1.0.1 provides six focused MCP tools: `search_papers`, `get_paper`, `list_collections`, `list_library_papers`, `add_paper_to_library`, and `get_pdf_download`. It also bundles local workflows for close reading and research cards. It does not wrap AI Search, AI Survey, or automated literature reviews.

Search supports titles, keywords, DOI, and arXiv identifiers. Metadata uses `hasReadablePdf`. The PDF tool returns a short-lived URL, its expiry, and any available file hash and size; the host downloads and verifies the file according to the [Researchzy Literature skill](skills/paperone-literature/SKILL.md).

DOI and arXiv lookup uses the backend's independent identifier index. The test environment has passed REST acceptance for DOI, DOI URL, and arXiv lookup. Production connection status is documented in [connection setup](https://github.com/projectp1/paperone-plugin/blob/main/docs/connection.md).

## Workflows

| User goal | Skill | Result |
|---|---|---|
| Search, metadata, library, or PDF retrieval | `paperone-literature` | Real metadata or a verified local PDF |
| Close reading, bilingual reading, or translation | `nature-reader` | `paper.md`, `source_map.json`, figure/equation assets, and reading notes |
| Paper Card, evidence chain, methods, or limitations | `nature-paper-card` | Source-anchored `paper-card.md` and an audit report |
| Shared Nature workflow dependency | `nature-shared` | Loaded on demand; no standalone user entry point |

For Nature workflows, Codex follows the [source acquisition rules](skills/paperone-literature/references/paperone-source.md), retrieves and verifies the PDF, then runs the requested local skill. Researchzy's backend does not execute these skills. Existing local PDFs or reader artifacts can be used directly, and a Paper Card does not require a translation first. Metadata alone is not enough to invent full-text claims or page references.

Example prompts:

- `Use Researchzy to look up DOI 10.1051/0004-6361/202556799 and return metadata only.`
- `Read https://doi.org/10.1051/0004-6361/202556799 closely and preserve figure and evidence anchors.`
- `Create a Paper Card for this local PDF and separate author claims from your analysis.`

Python 3.10+ is recommended for bundled scripts. PDF preparation uses PyMuPDF from `requirements.txt`; scanned PDFs also require OCR support. Pinned upstream sources, licenses, and Researchzy modifications are recorded in [third-party notices](THIRD_PARTY_NOTICES.md).

## Connection

This installable package is maintained in [projectp1/paperone-plugin](https://github.com/projectp1/paperone-plugin). Its `.mcp.json` targets `https://app.researchzy.com/mcp`; that production connection still requires end-to-end validation. See [connection setup](https://github.com/projectp1/paperone-plugin/blob/main/docs/connection.md).

The OAuth client ID is `paperone-codex`. Its callback is `http://127.0.0.1:8766/callback`, with `callbackPort` set to `8766`. The server must register the exact client ID and callback. Update both sides together when changing either value.

Public corpus search and details can be anonymous. Library access requires `library.read`, saving requires `library.write`, and PDF download metadata requires `pdf.read`. The host requests these scopes and the user approves them. Do not store passwords, cookies, access tokens, or signing keys in this package.

## Basic flow

1. Call `search_papers` with exactly one of `doi`, `arxiv`, or `query`.
2. Reuse returned metadata; call `get_paper` only when additional details are needed.
3. When the user requests a PDF, call `get_pdf_download`, download the signed URL, and verify the file.
4. Save a paper only when requested. Use `list_collections` and `canAddPapers` before selecting a collection.

Example identifiers illustrate input formats and do not guarantee a match. See the [tool reference](docs/tools.md) for boundaries.
