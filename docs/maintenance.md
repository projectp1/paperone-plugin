# 维护与迁移记录

2026-09-18 从 `projectp1/paperone_server` 的 `plugins/paperone` 迁出。
来源提交：`186d1e4944a8698d83e040bdf61d8a5042fd1732`，初始复制 70 个已跟踪插件文件。
本仓库以插件文件的新提交开始，不包含后端仓库历史、配置或数据。

迁移调整：新增仓库 marketplace、安装说明和工具文档；修复包外文档链接；保留插件名 `paperone`、版本 `0.2.0`、MCP 配置和技能行为。
Nature 上游来源和修改记录见包内 `THIRD_PARTY_NOTICES.md`。

## 验证

从仓库根目录执行已有脚本测试：

```sh
python3 -m unittest discover -s plugins/paperone/skills/nature-paper-card/tests
python3 -m unittest discover -s plugins/paperone/skills/nature-shared/tests
```

使用 Codex `plugin-creator` 技能附带的 `validate_plugin.py` 验证 `plugins/paperone`。
发布前检查 marketplace 指向有效插件包、文档相对链接有效，并按连接说明验证对应环境的 MCP 授权与工具调用。

编号检索的服务端采用独立编号索引，将 DOI/arXiv 映射到 corpusId，再读取完整 metadata。
该索引与后端部署不由本仓库管理。
