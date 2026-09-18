# PaperOne 文献插件

0.2.0 保留六个基础工具：`search_papers`、`get_paper`、`list_folders`、`list_library_papers`、`add_paper_to_library`、`get_pdf_download`，增加本地论文精读和论文卡片工作流。不包装 AI Search、AI Survey 或自动综述。

搜索支持标题、关键词、DOI 和 arXiv；metadata 沿用 `hasReadablePdf`，无需新增 `haspdf`。PDF 工具返回短期下载地址、有效期和可用的文件哈希/大小，实际文件由宿主按 [Skill](skills/paperone-literature/SKILL.md) 下载。

DOI/arXiv 检索使用服务端独立编号索引。Test 环境已完成索引构建并通过 REST 查询验收；生产连接状态见[连接说明](https://github.com/projectp1/paperone-plugin/blob/main/docs/connection.md)。

## 阅读工作流

| 用户目标 | Skill | 结果 |
|---|---|---|
| 查 DOI、论文 metadata、文献库或 PDF | `paperone-literature` | 真实 metadata 或验证后的本地 PDF |
| 精读、双语阅读、论文翻译 | `nature-reader` | `paper.md`、`source_map.json`、图表/公式资产和阅读说明 |
| 论文卡片、证据链、方法与局限分析 | `nature-paper-card` | 带来源定位的 `paper-card.md` 与审计报告 |
| 上述 Nature 工作流的依赖 | `nature-shared` | 按需加载共享资料，无独立用户入口 |

Codex 按 [来源衔接规则](skills/paperone-literature/references/paperone-source.md) 调用 PaperOne MCP，下载验证 PDF 后运行 Nature 工作流。PaperOne 后端无需执行这些 Skill。已有本地 PDF 或阅读产物时直接分析；制作论文卡片不必先全文翻译。只有 metadata 时明确标注材料不足，不编造正文、页码或论文贡献。全文翻译遵循来源许可和宿主内容规则。

示例：

- `用 PaperOne 查询 DOI 10.1051/0004-6361/202556799，只返回 metadata。`
- `精读 https://doi.org/10.1051/0004-6361/202556799，并标注图表和证据来源。`
- `为这份本地 PDF 制作论文卡片，区分作者结论和你的分析。`

运行 Python 脚本需要宿主提供 Python；建议 Python 3.10+。PDF 准备需要 PyMuPDF，可在宿主的隔离环境安装 `requirements.txt`。扫描版 PDF 还需要可用的 OCR 工具；缺少工具时报告限制。`nature-reader` 和 `nature-paper-card` 的上游版本固定，来源、许可证及修改清单见 [第三方声明](THIRD_PARTY_NOTICES.md)。

## 连接前

此目录是可安装的插件包，由 [paperone-plugin](https://github.com/projectp1/paperone-plugin) 独立维护。`.mcp.json` 默认指向生产目标 `https://app.paperone.ai/mcp`，该目标仍需连接验收；环境选择、安装与授权步骤见[连接说明](https://github.com/projectp1/paperone-plugin/blob/main/docs/connection.md)。

随包 OAuth 配置使用公开客户端 ID `paperone-codex` 和固定本机回调 `http://127.0.0.1:8766/callback`（`callbackPort: 8766`）。服务端须预注册相同 ID 和完整回调地址；如果修改客户端或端口，同步更新两端配置。

搜索和公共语料详情可匿名调用；文献库需要 `library.read`，保存需要 `library.write`，PDF 下载信息需要 `pdf.read`。权限由宿主发起申请，并由用户在授权页确认。账号密码、Cookie、访问令牌和服务端签名私钥都不写入此目录。

## 基本流程

1. `search_papers({"doi":"10.1000/example"})`；或传 `query` / `arxiv`，三者只传一个。
2. 直接使用已有 metadata；需要补全详情时 `get_paper({"corpusId":123})`。
3. 用户要 PDF 时 `get_pdf_download({"corpusId":123})`，按返回地址下载并验证文件。
4. 用户要求保存时 `add_paper_to_library({"corpusId":123})`；选择文件夹时先查 `list_folders` 的 `canAddPapers`。

示例 ID 仅说明参数格式，不代表一定存在论文。完整边界见 [工具说明](docs/tools.md)。
