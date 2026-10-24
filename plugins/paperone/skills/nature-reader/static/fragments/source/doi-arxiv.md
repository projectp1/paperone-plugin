# Source: DOI or arXiv identifier

> Modified by Researchzy (2026-09-13): prefer the plugin's connected MCP source.

First follow the Researchzy source-acquisition reference linked from this skill's
`SKILL.md`. If it already returned a verified local PDF, load the PDF source
fragment directly. If Researchzy is unavailable or a public record/PDF is absent,
use the lawful public-source steps below, preserving the authorization boundary.

The user gave a bare DOI or arXiv id/link that must be resolved before reading.

- Resolve the identifier to the actual article first:
  - arXiv → the abstract page, then the PDF (and HTML/LaTeX source when available).
  - DOI → the publisher landing page, then the open-access PDF or HTML if lawfully available.
- After resolving, this becomes a `pdf-text`, `scanned-pdf`, or `html` job — load that fragment and follow it for extraction. This fragment only covers retrieval.
- Capture bibliographic metadata (title, authors, venue, year, DOI/arXiv id) for the `paper.md` metadata header.
- Prefer the open-access version (arXiv, author copy, PMC) when the version of record is paywalled. Note which version was read in `translation_notes.md`, since arXiv and published versions can differ.
- When lawful arXiv HTML or TeX source is available, prefer its equation source over PDF text extraction, but still verify numbering and symbols against the rendered paper.
- If the identifier cannot be resolved or only the abstract is reachable, build a draft reader from what is available and clearly mark the rest as not retrieved. Do not fabricate body text.
- Apply the copyright caution to the resolved artifact.
