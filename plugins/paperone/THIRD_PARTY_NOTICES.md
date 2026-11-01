# Third-party components

## researchzy-paper-card

`skills/researchzy-paper-card` is derived from `nature-paper-card` in
[Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills),
commit `c4e4c99fbeaf0168cda090f8739e1508017a610e` (2026-09-10), together with
`nature-shared/core/terminology-ledger.md` from the same commit.

The skill retains its upstream references, templates, scripts, tests and
attribution. It is distributed under the
[Apache License 2.0](licenses/nature-skills-Apache-2.0.txt). Upstream did not
contain a NOTICE file at this revision. Nature Skills is a third-party project;
bundling it does not imply endorsement by its authors or the journal Nature.

Researchzy modifications:

- 2026-09-13: `SKILL.md` gained optional Researchzy retrieval, a limited-source
  classification fallback, and optional references to workflows outside this
  bundle. Researchzy's own source-acquisition reference resides in
  `skills/researchzy-literature/references/researchzy-source.md`.
- 2026-09-18: README tutorial links point to the pinned upstream repository
  because those tutorials are not bundled.
- 2026-11-01 (version 1.5.0): renamed from `nature-paper-card` to
  `researchzy-paper-card` (`SKILL.md`, `manifest.yaml`, `agents/openai.yaml`,
  `evals/evals.json`, the READMEs, the docstring of `scripts/prepare_paper.py`
  and a module name in `tests/test_prepare_paper.py`). The Terminology Ledger,
  the only `nature-shared` file the skill loads, is bundled unchanged as
  `static/core/terminology-ledger.md`; `manifest.yaml` and
  `static/core/principles.md` point to it, and `nature-shared` is no longer
  bundled. `nature-reader` is no longer bundled either: `SKILL.md` lists it among
  the workflows that are not bundled and points to `researchzy-download` for full
  text.

The upstream content and the bundled Python scripts are otherwise unchanged.

## researchzy-download

`skills/researchzy-download` is derived from `nature-downloader` in
[Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills),
commit `c1a8e7bbcf86d82a268dc4a9980d36082b31fb2f` (2026-10-31; the skill last
changed in `3981da9877237d36a21705f314b2b66e41ca59e5`, 2026-10-20). That skill is
distributed under its own [MIT License](licenses/nature-downloader-MIT.txt),
Copyright (c) 2026 baihe26, which the skill directory keeps as `LICENSE`.

Researchzy modifications (2026-11-01):

- Renamed to `researchzy-download`, and every file is English only.
- Kept only the open-access and publisher-API routes. Removed the CNKI route and
  every Chinese-language source, the Web of Science, institutional-browser,
  Chrome DevTools and supporting-information routes, the automatic verification
  module (`anti-bot.mjs`), the school configuration (`configure_school.py`,
  `src/`, `data/school*`), the browser helper scripts, the examples, the upstream
  READMEs, banner and development notes.
- `scripts/batch_download.mjs`: rewritten for those routes (DOI list, exact title,
  known URL); a title shared by several Crossref works is reported as
  `metadata_ambiguous` with its candidates instead of taking the first match.
- `scripts/lib/open-access.mjs`: PMC copies come from NCBI's PMC Article Datasets
  on AWS, because the PMC OA web service (`oa.fcgi`) no longer answers.
- `scripts/lib/routing.mjs`, `status-codes.mjs`, `provider-utils.mjs`,
  `publisher-providers.mjs`, `metadata.mjs`: reduced to the remaining routes and
  statuses; English-only content checks.
- `SKILL.md`, `manifest.yaml`, `agents/openai.yaml` and the tests rewritten
  accordingly; Researchzy's own PDFs are tried first.
