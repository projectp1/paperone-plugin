# Core tools

| Tool | Input | Purpose |
|---|---|---|
| `search_papers` | Exactly one of `query`, `doi`, or `arxiv`; optional `page` and `pageSize` | Search bibliographic metadata |
| `get_paper` | Exactly one of `corpusId` or `paperId` | Retrieve one paper |
| `list_collections` | No arguments (`{}`) | List visible personal collections only and `canAddPapers` hints; a paper may belong to multiple collections |
| `list_library_papers` | `scope: personal/shared/collection`; collection scope requires `collectionId` | Browse visible papers; `collection` scope selects a collection |
| `create_collection` | `name` (1–100 characters); optional `parentCollectionId` of a personal collection | Create a personal collection when explicitly requested; shared collections cannot be created or used as the parent. An existing personal collection with the same name in the same place is returned with `status: already_present` |
| `add_paper_to_library` | `corpusId`; optional `collectionId` | Save a paper when explicitly requested |
| `get_pdf_download` | Exactly one of `corpusId` or `paperId` | Get current PDF metadata and a short-lived URL |

Follow the connected MCP server's live schemas. Identifier searches accept only the identifier and pagination; do not add keyword sorting or filters. DOI input may be a bare value, a `doi:` prefix, or a resolver URL. arXiv input may be a bare value, a prefix, or an abs/pdf URL. A version suffix resolves the paper identity but does not guarantee that PDF version.

Metadata may include title, authors, abstract, year, `corpusId`, `doi`, `arxiv`, and `hasReadablePdf`. A successful empty search means only that the current index found no match. Do not interpret a backend error as evidence that the paper does not exist.

`hasReadablePdf` is a hint. Use `get_pdf_download` for current `url`, `expiresAt`, and any available `sizeBytes` or `fileHashSha256`. Do not attach Researchzy authorization or cookies to the signed URL. Receiving a URL alone does not complete the download. See the [Researchzy Literature skill](../skills/paperone-literature/SKILL.md) for the full workflow.
