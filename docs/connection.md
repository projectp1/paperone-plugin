# 连接 PaperOne

插件通过远程 MCP 使用 PaperOne 服务。插件包位于 `plugins/paperone`；可直接修改本地副本的 `.mcp.json` 选择已部署环境。

| 环境 | MCP URL | 验证状态 |
|---|---|---|
| 默认生产目标 | `https://app.paperone.ai/mcp` | 尚待生产连接验收 |
| Test | `https://app.testp1.testdomain.stream/mcp` | REST DOI/arXiv 搜索已验收；新仓库安装后的宿主连接需单独验证 |

`mcpServers.paperone.url` 必须与所选服务端的 MCP resource 一致。
公开客户端 ID 为 `paperone-codex`，固定回调地址为 `http://127.0.0.1:8766/callback`，`callbackPort` 为 `8766`。
服务端必须预注册相同客户端 ID 和完整回调地址；切换环境时不要只修改 issuer 或混用两套服务的令牌。

搜索和公共语料详情支持匿名工具调用。库内详情、文献库操作及 PDF 下载信息需要登录授权，具体以服务端工具描述和授权页面为准。
账号密码、Cookie、访问令牌和签名私钥不应写入插件文件。客户端 ID 是公开配置。

调试本地副本时，先将仓库注册为本地 marketplace，再安装 `paperone@projectp1`：

```sh
codex plugin marketplace add /absolute/path/to/paperone-plugin
codex plugin add paperone@projectp1
```

已注册同名 Git marketplace 时，应先通过宿主的 marketplace 管理流程切换来源，避免同时维护同名来源。
已有 `PaperOne Test` 个人插件是独立安装；添加本仓库不会自动替换它。
