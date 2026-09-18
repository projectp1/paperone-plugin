# 基础工具

| 工具 | 输入 | 用途 |
|---|---|---|
| `search_papers` | `query`、`doi`、`arxiv` 恰好一个；可带 `page`、`pageSize` | 检索论文 metadata |
| `get_paper` | `corpusId` 或 `paperId`，恰好一个 | 单篇详情 |
| `list_folders` | `includeShared` | 可见文件夹及 `canAddPapers` 权限提示 |
| `list_library_papers` | `scope: personal/shared/folder`；folder 需 `folderId` | 分页读取可见文献 |
| `add_paper_to_library` | `corpusId`，可选 `folderId` | 用户明确要求时保存论文 |
| `get_pdf_download` | `corpusId` 或 `paperId`，恰好一个 | 最新 PDF metadata 与短期下载地址 |

以所连服务的实际 MCP schema 为准。编号检索只接受编号及分页，不附加关键词筛选或排序。
DOI 支持裸编号、`doi:` 前缀和 DOI 链接；arXiv 支持裸编号、前缀及 abs/pdf 链接。
arXiv 版本后缀识别为同篇论文，不保证返回指定版本的 PDF。

返回 metadata 包含实际可用的标题、作者、摘要、年份、`corpusId`、`doi`、`arxiv` 和 `hasReadablePdf`。
成功且零命中只说明当前索引未收录匹配编号，后端异常不能解释为论文不存在。

`hasReadablePdf` 是可读性提示；需要 PDF 时使用 `get_pdf_download` 获取最新 `url`、`expiresAt` 和可用的 `sizeBytes`、`fileHashSha256`。
下载签名 URL 时不附加 PaperOne Authorization 或 Cookie；只拿到 URL 不算完成文件下载。
具体操作见 [PaperOne Skill](../skills/paperone-literature/SKILL.md)。
