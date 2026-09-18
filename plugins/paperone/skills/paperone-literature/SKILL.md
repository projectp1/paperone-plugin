---
name: paperone-literature
description: Use when the user requests PaperOne paper lookup by DOI, arXiv, title or keywords, bibliographic metadata, library or shared-folder access, or PDF metadata and downloads.
---

# PaperOne 文献操作

使用 PaperOne 的基础 MCP 工具完成文献操作。先确认工具已连接并读取实际 schema；未连接时说明需要连接 PaperOne。按当前工具返回值工作。

## 工具

| 用户目标 | 工具 |
|---|---|
| 按标题、关键词、DOI 或 arXiv 检索 | `search_papers` |
| 按已知 corpusId 或 paperId 读取单篇详情 | `get_paper` |
| 查看个人和共享文件夹 | `list_folders` |
| 查看个人、文件夹或共享文献 | `list_library_papers` |
| 将论文加入文献库或可写文件夹 | `add_paper_to_library` |
| 获取 PDF metadata 和下载地址 | `get_pdf_download` |

## 使用规则

- 搜索结果复用返回的标题、作者、摘要、DOI、年份、`corpusId` 和 `hasReadablePdf`，不猜测缺失字段。
- DOI 或 DOI 链接传给 `search_papers` 的 `doi`；arXiv 编号、前缀或 abs/pdf 链接传 `arxiv`；关键词传 `query`，三者恰好一个，由服务端规范化。编号查询不附加排序、年份等关键词筛选；精确查询为空只表示 PaperOne 当前未找到。
- arXiv 首版按论文 ID 查询，版本后缀用于识别同篇论文。输入含版本时说明返回的是 PaperOne 收录记录，metadata/PDF 未保证指定版本，也不据此声称为最新版本。
- 已知 `corpusId` 或 `paperId` 且需要详情时用 `get_paper`，两个 ID 只传一个；结果已有所需字段时直接使用。读取返回的 `metadata` 和顶层 `hasReadablePdf`；库内详情需要授权，失败后不改走语料分支。详情查询不会自动下载或加入库。
- `list_folders` 使用 `includeShared`；`list_library_papers` 使用 `scope: personal | shared | folder`，folder 模式必须传 `folderId`。按 `hasMore` 按需翻页；文件夹查询只包含直接关联论文。
- 只有用户明确要求时才调用 `add_paper_to_library`。通过 `canAddPapers` 选择可写目录；省略 `folderId` 表示个人库，失败后不静默改存其他位置。按返回的 `created`、`linked`、`already_present` 状态说明结果。
- 使用 `userMessage` 和 `code` 说明工具错误；空搜索结果只表示未找到。需要账号授权时通过宿主连接流程处理，不索取 token、Cookie 或密码。

## PDF metadata 与下载

1. 先读取 `hasReadablePdf`。用户明确要求某篇 PDF metadata 或下载时，可调用一次 `get_pdf_download` 获取最新状态。
2. 搜索语料传 `{corpusId: ...}`；个人或共享库论文传 `{paperId: ...}`，两者只传一个。下载不会自动把论文加入文献库。
3. 读取成功结果的 `url`、`expiresAt`，以及有值时的 `fileHashSha256`、`sizeBytes`；缺少 `url` 时报告工具的实际结果。用户只要 PDF metadata 时直接返回这些信息，无需下载文件。
4. 需要文件时，在有效期内下载到任务工作区；签名地址请求不附加 PaperOne Authorization 或 Cookie。
5. 地址过期或返回 403 时，重新调用 `get_pdf_download` 刷新一次并重试一次。再次失败时报告实际错误。
6. 验证响应和文件内容确为 PDF；若返回 `sizeBytes` 或 `fileHashSha256`，一并核对。只取得 URL 不算下载完成。
7. 返回保存后的文件链接或附件。论文 metadata 与 PDF 文件 metadata 分开解释，未返回的字段不猜测。

## 精读和论文卡片

- 用户只要求检索或 metadata 时，在已有结果处结束。
- 用户要求精读、双语阅读或翻译时，使用同包的 `nature-reader`；要求结构化论文卡片、证据链或局限分析时，使用 `nature-paper-card`。
- 这两种分析请求允许获取所选论文的全文。读取 [PaperOne 来源衔接](references/paperone-source.md)，取得并验证 PDF 后，将本地路径和真实 metadata 交给对应技能继续；不自动加入文献库。
- 已提供本地 PDF 或阅读产物时直接分析；论文卡片不必先生成全文翻译。
