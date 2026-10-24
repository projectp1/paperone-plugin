# Researchzy source acquisition for Nature Skills

Use this reference before reading a paper or making a Paper Card from a DOI,
arXiv identifier, title, `corpusId`, or library `paperId`. Resolve paths relative
to the loaded skill directory. This reference only retrieves the source; return
to the requesting Nature skill afterward. Do not invoke skills recursively.

## Choose the source

- If the user supplied a local PDF, full text, or a reader `source_map.json`, use
  it directly. A Paper Card can consume the PDF itself; a bilingual reader is
  not a prerequisite. Reuse an existing verified download within the task.
- If the user only wants search results or bibliographic metadata, use
  `paperone-literature` and stop after returning metadata. Do not create a reader
  or card. A request to read, translate, or analyse an identified paper includes
  retrieving its available full text, but does not request adding it to a library.
- If no full text is available yet and Researchzy tools are connected, use the
  actual tool schema. Pass exactly one of `doi`, `arxiv`, or `query` to
  `search_papers`. DOI resolver URLs go into `doi`; arXiv URLs go into `arxiv`;
  titles go into `query`. Do not attach keyword filters to identifier searches.
  For an already known ID, use `get_paper` with exactly one of `corpusId` or
  `paperId` when details are needed. Reuse existing metadata when sufficient.
- For title searches, inspect candidates before selecting a paper. Ask the user
  to choose if the title/author/year do not identify one clearly. An empty exact
  query means Researchzy did not find a record; it is not proof the paper does not
  exist. Never substitute a similarly titled paper for an unmatched DOI.

## Obtain and verify the PDF

1. Retain the actual title, authors, DOI/arXiv, year, venue and
   `hasReadablePdf`. This flag is a hint; a failed download must still be reported.
2. For a full-text reading request, call `get_pdf_download` once for the selected
   paper to get its current availability, including when the earlier hint was
   false. Use `{corpusId: ...}` for a corpus result or `{paperId: ...}` for a
   library result; never both. A library authorization failure must not be
   bypassed by retrying the same request as a corpus lookup.
3. Use the returned `url` before `expiresAt` to download into the task workspace.
   The signed GET request must not include Researchzy Authorization or Cookies.
   A URL alone is not a downloaded PDF. Follow the existing PDF verification
   rules in `paperone-literature`: check HTTP success and actual PDF content,
   and compare `sizeBytes` and `fileHashSha256` when returned.
4. On expiry or HTTP 403, refresh with `get_pdf_download` once and retry once.
   Report a repeated failure using the actual `code`/`userMessage`. For an
   authorization failure, point to the host's Researchzy connection flow when one
   exists; never request a password, token or Cookie.
5. Hand back the verified local path plus bibliographic metadata and source
   provenance. Do not store signed URLs or credentials in reader/card artifacts.
   Record which document version was actually available; an arXiv `vN` request
   does not guarantee Researchzy supplies that PDF version.

## Continue the requested analysis

- `nature-reader`: classify the downloaded file as `pdf-text` or `scanned-pdf`
  and load that source fragment; apply its extraction and output contracts.
- `nature-paper-card`: prepare the local PDF or existing source map with its
  bundled `prepare_paper.py`; preserve its locator modes and run its auditor.
- Researchzy is optional for local inputs. When disconnected, or when a public
  corpus search has no record/PDF, explain the limitation and use the Nature
  workflow's lawfully accessible publisher/arXiv source, or a user-provided file.
  Label any partial result as partial. An authorization error does not authorize
  alternative access to private library content.
- PDF availability is not a reuse license. Follow the source's license and the
  host's content rules; when full reproduction/translation is not permitted,
  provide an original, source-grounded explanation with limited quotations.
