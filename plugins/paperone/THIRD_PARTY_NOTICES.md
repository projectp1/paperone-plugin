# Third-party components

This plugin includes `nature-reader`, `nature-paper-card` and `nature-shared`
from [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills),
commit `c4e4c99fbeaf0168cda090f8739e1508017a610e` (2026-09-10).

These directories retain their upstream references, templates, scripts, tests
and attribution. They are distributed under the
[Apache License 2.0](licenses/nature-skills-Apache-2.0.txt). Upstream did not
contain a NOTICE file at this revision. Nature Skills is a third-party project;
bundling it does not imply endorsement by its authors or the journal Nature.

Researchzy modifications (2026-09-13):

- `skills/nature-reader/SKILL.md`: optional Researchzy retrieval and reuse boundary.
- `skills/nature-reader/static/fragments/source/doi-arxiv.md`: Researchzy-first
  DOI/arXiv retrieval, returning to upstream source handling when appropriate.
- `skills/nature-reader/static/core/output-contract.md`: resolve the bundled
  validator from the installed skill directory; handle optional host PDF tooling.
- `skills/nature-reader/references/equation-handling.md`: use the same installed
  validator path as the output contract.
- `skills/nature-reader/static/fragments/source/{pdf-text,scanned-pdf}.md`:
  make the host PDF skill optional, consistent with the output contract.
- `skills/nature-paper-card/SKILL.md`: optional Researchzy retrieval, a limited-source
  classification fallback, and optional references to workflows outside this bundle.

Researchzy's own source-acquisition reference resides in
`skills/paperone-literature/references/paperone-source.md`. Shared upstream
content and the bundled Python scripts are otherwise unchanged.

Packaging changes (2026-09-18): paper-card README tutorial links now point to the pinned upstream repository because those tutorials are not bundled.
