# Core tools

| Tool | Input | Purpose |
|---|---|---|
| `search_papers` | Exactly one of `query`, `doi`, or `arxiv`; optional `page` and `pageSize`. Keyword (`query`) searches also take `sort` (`relevance`, `citationCount`, `year` newest first, `influency`), `yearFrom`, `yearTo`, `fieldOfStudy`, `venue` and `hasPdfInS3` | Search bibliographic metadata |
| `get_paper` | Exactly one of `corpusId` or `paperId` | Retrieve one paper |
| `list_collections` | No arguments (`{}`) | List visible personal collections only and `canAddPapers` hints; a paper may belong to multiple collections |
| `list_library_papers` | `scope: personal/shared/collection`; collection scope requires `collectionId`; optional `query`, `page`, `pageSize` | Browse visible papers; `collection` scope selects a collection; `query` narrows the list |
| `create_collection` | `name` (1–100 characters); optional `parentCollectionId` of a personal collection | Create a personal collection when explicitly requested; shared collections cannot be created or used as the parent. An existing personal collection with the same name in the same place is returned with `status: already_present` |
| `add_paper_to_library` | `corpusId`; optional `collectionId` | Save a paper when explicitly requested |
| `get_pdf_download` | Exactly one of `corpusId` or `paperId` | Get current PDF metadata and a short-lived URL |
| `get_profile` | No arguments (`{}`) | Read the connected account's opaque ID, name and email; hosts such as ChatGPT use it to tell linked accounts apart |

Follow the connected MCP server's live schemas. Every tool requires a connected Researchzy account. Input schemas carry no `oneOf`; the exactly-one rules above are enforced by the server, which answers a wrong combination with `INVALID_REQUEST`. Identifier searches accept only the identifier and pagination; do not add keyword sorting or filters. For keyword searches, `sort: citationCount` finds influential work, `sort: year` recent work, and `fieldOfStudy` must match the index's field name, such as `Computer Science` or `Medicine`. DOI input may be a bare value, a `doi:` prefix, or a resolver URL. arXiv input may be a bare value, a prefix, or an abs/pdf URL. A version suffix resolves the paper identity but does not guarantee that PDF version.

Metadata may include title, authors, abstract, year, `corpusId`, `doi`, `arxiv`, and `hasReadablePdf`. A successful empty search means only that the current index found no match. Do not interpret a backend error as evidence that the paper does not exist.

`hasReadablePdf` is a hint. Use `get_pdf_download` for current `url`, `expiresAt`, and any available `sizeBytes` or `fileHashSha256`. Do not attach Researchzy authorization or cookies to the signed URL. Receiving a URL alone does not complete the download. See the [Researchzy Literature skill](../skills/paperone-literature/SKILL.md) for the full workflow.
