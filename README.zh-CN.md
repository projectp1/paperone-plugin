# Researchzy Plugin

[English](README.md)

Researchzy 的 Codex 插件：查找论文、管理文献库、获取 PDF，并使用 Nature Skills 精读论文或制作研究卡片。

## 功能

| 能力 | 工具或 Skill |
|---|---|
| 标题、关键词、DOI、arXiv 检索 | `search_papers` |
| 已知论文 ID 的 metadata | `get_paper` |
| 个人 Collection 及个人/共享文献 | `list_collections`、`list_library_papers` |
| 保存论文到文献库或可写 Collection | `add_paper_to_library` |
| PDF metadata 与下载地址 | `get_pdf_download` |
| 中英文对照精读 | `nature-reader` |
| 论文卡片、方法与证据分析 | `nature-paper-card` |

## 在 Codex 中安装

```sh
codex plugin marketplace add projectp1/paperone-plugin --ref main
codex plugin add paperone@projectp1
```

安装后在宿主中连接 Researchzy，按授权页面完成登录，并在新任务中使用插件。GitHub 仓库是用户主动添加的插件来源，不代表已经进入公共插件目录。

随包 MCP 配置默认指向 `https://app.researchzy.com/mcp`。生产 MCP 和 OAuth 仍需完成端到端连接验收；test 环境的 DOI、DOI URL 和 arXiv REST 搜索已于 2026-09-18 验证。环境配置见[连接说明](docs/connection.md)。

## 示例

- 用 Researchzy 查找 DOI `10.1051/0004-6361/202556799`，显示 metadata 和 PDF 是否可用。
- 查找 arXiv `2508.10985`。
- 精读论文，生成保留来源定位的中英文对照内容。
- 为 PDF 制作论文卡片，区分作者结论和分析推断。

更多说明：[插件使用](plugins/paperone/README.md)、[工具说明](plugins/paperone/docs/tools.md)。

本仓库维护插件包；API、MCP 服务、OAuth 和检索索引由 Researchzy 后端维护。Nature Skills 的许可证与来源见[第三方声明](plugins/paperone/THIRD_PARTY_NOTICES.md)。
