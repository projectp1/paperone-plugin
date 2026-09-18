# PaperOne Plugin

PaperOne 的独立插件仓库：查找论文、管理文献库、获取 PDF，并使用 Nature Skills 精读论文或制作研究卡片。

## 功能

| 能力 | 工具 / Skill |
|---|---|
| 标题、关键词、DOI、arXiv 检索 | `search_papers` |
| 已知论文 ID 的 metadata | `get_paper` |
| 个人及共享文件夹、文献 | `list_folders`、`list_library_papers` |
| 保存论文到文献库或可写文件夹 | `add_paper_to_library` |
| PDF metadata 与下载地址 | `get_pdf_download` |
| 中英文对照精读 | `nature-reader` |
| 论文卡片、方法与证据分析 | `nature-paper-card` |

## 在 Codex 中添加

使用支持插件的 Codex 版本：

```sh
codex plugin marketplace add projectp1/paperone-plugin --ref main
codex plugin add paperone@projectp1
```

安装后在宿主中连接 PaperOne，按授权页面完成登录；在新任务中使用插件。
GitHub 仓库是主动添加的插件来源，不代表已进入官方公共插件目录。

**连接状态：** 随包默认 MCP 地址为 `https://app.paperone.ai/mcp`。
2026-09-18 已验证 test 环境的 DOI、DOI URL 和 arXiv REST 搜索；生产 MCP 和从本仓库安装后的 OAuth 完整流程尚待验证。
如连接失败，请先确认所用环境已启用 MCP，参见[连接说明](docs/connection.md)。

## 示例

- 用 PaperOne 查找 DOI `10.1051/0004-6361/202556799`，显示 metadata 和 PDF 是否可用。
- 查找 arXiv `2508.10985`。
- 精读这篇论文，生成中英文对照内容并保留来源定位。
- 为这份 PDF 制作论文卡片，区分作者结论和分析推断。

更多说明：[插件使用](plugins/paperone/README.md)、[工具说明](plugins/paperone/docs/tools.md)。
PDF 处理脚本需要 Python 3.10+ 和插件目录中 `requirements.txt` 指定的可选依赖。

## 维护

```text
.agents/plugins/marketplace.json   仓库插件目录
plugins/paperone/                  可安装的插件包
docs/                             连接及迁移说明
```

插件源码在本仓库维护；API、MCP 服务、OAuth 和检索索引由 PaperOne 后端维护。
迁移来源和验证方法见[维护说明](docs/maintenance.md)。

## 版权与许可证

随包 Nature Skills 保留 Apache-2.0 许可证及来源声明，见[第三方声明](plugins/paperone/THIRD_PARTY_NOTICES.md)。
本次迁移不改变已有授权；PaperOne 自有文件尚未另行声明开源许可证。
