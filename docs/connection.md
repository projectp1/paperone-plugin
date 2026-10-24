# Connect Researchzy

The plugin uses Researchzy through a remote MCP server. The installable package is under `plugins/paperone`; edit its `.mcp.json` only when selecting a deployed environment for local testing.

| Environment | MCP URL | Status |
|---|---|---|
| Default production target | `https://app.researchzy.com/mcp` | End-to-end connection validation pending |
| Test | `https://app.testp1.testdomain.stream/mcp` | DOI/arXiv REST search accepted; repository-installed host connection still pending |

`mcpServers.paperone.url` must match the selected server's MCP resource. The public OAuth client ID is `paperone-codex`; its callback is `http://127.0.0.1:8766/callback`, with `callbackPort` set to `8766`. The server must register the exact client ID and callback. Do not mix issuers or tokens between environments.

Public search and corpus details can be anonymous. Library details, library operations, and PDF download metadata require sign-in and the scopes declared by the live tools. Never put passwords, cookies, access tokens, or signing keys in plugin files. The client ID is public configuration.

To test a local checkout, register its repository marketplace and install `paperone@projectp1`:

```sh
codex plugin marketplace add /absolute/path/to/paperone-plugin
codex plugin add paperone@projectp1
```

If a Git marketplace with the same name is already configured, switch sources through the host's marketplace workflow instead of keeping two sources with the same name. An existing personal `Researchzy Test` plugin is a separate installation; this repository does not replace it automatically.
