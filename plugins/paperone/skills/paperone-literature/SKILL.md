---
name: paperone-literature
description: Search PaperOne by DOI, arXiv ID, title, or keywords; retrieve bibliographic metadata, browse personal or shared libraries, and get verified PDF metadata or downloads. Use for paper discovery and library operations, not for deep reading or research-card analysis.
---

# PaperOne Literature

Use PaperOne's MCP tools for literature search, metadata, library access, and PDF retrieval. Confirm that the tools are connected and follow their live schemas. If they are unavailable, explain that PaperOne must be connected. Report only fields returned by the tools.

## Tool routing

| User goal | Tool |
|---|---|
| Search by title, keywords, DOI, or arXiv ID | `search_papers` |
| Retrieve one paper by known `corpusId` or `paperId` | `get_paper` |
| List personal and shared collections | `list_collections` |
| Browse personal, collection, or shared papers | `list_library_papers` |
| Add a paper to the library or a writable collection | `add_paper_to_library` |
| Get current PDF metadata and a download URL | `get_pdf_download` |

## Search and metadata

- Reuse returned titles, authors, abstracts, identifiers, years, `corpusId`, and `hasReadablePdf`. Do not infer missing values.
- Pass a DOI or DOI resolver URL as `doi`, an arXiv ID/prefix/abs URL/pdf URL as `arxiv`, and a title or keyword query as `query`. Pass exactly one. The service normalizes supported forms.
- Identifier searches accept pagination only. Do not attach keyword filters, sorting, venue, year, or PDF filters. An empty exact search means only that PaperOne found no indexed match.
- arXiv searches resolve a paper identity. A `vN` suffix identifies the same paper, but the returned metadata or PDF is not guaranteed to be that version or the latest version.
- Use `get_paper` only when a known `corpusId` or `paperId` needs more detail; pass exactly one. Reuse existing search metadata when it is sufficient.
- A `paperId` lookup requires library authorization. Do not bypass a failed library lookup by switching to a corpus lookup. Retrieving details does not download or save the paper.
- PaperOne organizes papers in Collections. A paper may belong to multiple Collections; adding it to one does not move it out of another. Collections may be nested.
- Use `includeShared` with `list_collections`. Collection IDs are exposed as `collectionId` and `parentCollectionId`. For `list_library_papers`, use `scope: personal | shared | collection`; `collection` selects a Collection and requires `collectionId`. Collection scope includes direct memberships only. Pagination starts at `page: 1`, never 0; follow `hasMore` when additional pages are needed.
- Call `add_paper_to_library` only when the user explicitly asks to save a paper. Use `canAddPapers` to select writable Collections. Use `collectionId` to link the paper to a Collection, preserving its existing Collection memberships. Omit `collectionId` for the personal library. Never silently save somewhere else after a failure. Report the returned `created`, `linked`, or `already_present` result.
- Report tool failures with the returned `code` and `userMessage`. Use the host connection flow for authorization; never request passwords, tokens, or cookies.

## PDF metadata and downloads

1. Treat `hasReadablePdf` as a hint. When the user explicitly requests PDF metadata or the file, call `get_pdf_download` once for the current state.
2. Use `{corpusId: ...}` for a corpus result or `{paperId: ...}` for a personal/shared library paper; never pass both. Downloading does not add a paper to the library.
3. For metadata-only requests, return `url`, `expiresAt`, and any available `fileHashSha256` and `sizeBytes`. If no URL is returned, report the actual tool result.
4. When the file is requested, download it into the task workspace before `expiresAt`. Do not send PaperOne authorization headers or cookies to the signed URL.
5. If the URL has expired or returns HTTP 403, call `get_pdf_download` once more and retry once. Report the actual error after a second failure.
6. Verify HTTP success and that the downloaded content is a PDF. Compare `sizeBytes` and `fileHashSha256` when supplied. Receiving a URL alone is not a completed download.
7. Return a link or attachment for the saved file. Keep bibliographic metadata distinct from PDF-file metadata, and do not invent absent fields.

## Deep reading and research cards

- Stop after search or metadata when that is all the user requested.
- For full-paper reading, bilingual translation, or close reading, continue with the bundled `nature-reader` skill.
- For a structured Paper Card, claim-to-evidence analysis, limitations, or research ideas, continue with `nature-paper-card`.
- These analysis requests allow retrieving the selected paper's available full text. Read [PaperOne source acquisition](references/paperone-source.md), obtain and verify the PDF, then pass its local path and real metadata to the selected skill. Do not add the paper to the library unless requested.
- If a local PDF or existing reader artifact is already available, use it directly. A Paper Card does not require a bilingual reader first.
