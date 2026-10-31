# Connect Researchzy

The plugin uses Researchzy through a remote MCP server. The installable package is under `plugins/paperone`; edit its `.mcp.json` only when selecting a deployed environment for local testing.

| Environment | MCP URL | Status |
|---|---|---|
| Default production target | `https://app.researchzy.com/mcp` | End-to-end connection validation pending |
| Test | `https://app.testp1.testdomain.stream/mcp` | Sign-in, refresh and disconnect verified on 2026-10-25 (release 1.0.202610250432) with the Codex CLI (`paperone-codex`) and Claude Code (metadata document); DOI/arXiv search accepted |

`mcpServers.researchzy.url` must match the selected server's MCP resource. The public OAuth client ID is `paperone-codex`; its callback is `http://127.0.0.1:8766/callback`, with `callbackPort` set to `8766`. The server must register the client ID; a loopback callback (`127.0.0.1`, `[::1]` or `localhost`) matches on any port, every other callback exactly. Do not mix issuers or tokens between environments.

Every tool requires sign-in and the scopes declared by the live tools: `library.read` for search, details, library and profile, `library.write` for saving papers, creating collections and adding PDFs to library papers, `pdf.read` for PDF download metadata. Never put passwords, cookies, access tokens, or signing keys in plugin files. The client ID is public configuration.

## Sign-in and tokens

- A host that calls a tool without a token receives HTTP 401 with a `WWW-Authenticate` challenge that points to `/.well-known/oauth-protected-resource` and names all three scopes. `initialize` and `tools/list` work without a token, so a host can list the tools before connecting.
- Authorization uses the code flow with PKCE (S256) and the `resource` parameter. The access token lasts one hour. The refresh token is replaced on every refresh and lasts 90 days, so a connection stays signed in while it is used at least once in 90 days. A refresh request may omit `resource`; if it sends one, it must be the MCP URL.
- The user can disconnect an app on the Researchzy **Account** page (**Connected apps**). Disconnecting ends that connection's access and refresh tokens at once, on every server instance.

## Connect a host without the plugin

The server identifies a host in one of two ways:

- **Pre-registered client ID**: `paperone-codex` for Codex, and the ChatGPT app's client.
- **Client ID Metadata Document**: the host sends the HTTPS URL of a JSON document that names it and lists its callbacks. Researchzy accepts documents hosted on `claude.ai`, `claude.com`, `chatgpt.com` and `vscode.dev`, so Claude, Claude Code, ChatGPT and VS Code connect without registration. The consent page shows the host that published the document. Callbacks on another site are ignored; loopback callbacks are allowed, and the consent page then warns that a local app receives the authorization.

Replace the URL below with the environment's MCP URL.

| Host | Setup |
|---|---|
| Claude Code | `claude mcp add --transport http researchzy https://app.researchzy.com/mcp`, then `claude mcp login researchzy` (add `--no-browser` on a remote machine) |
| Claude (web or desktop) | **Settings → Connectors → Add custom connector**, with the MCP URL; then connect it |
| VS Code | Add `{"servers": {"researchzy": {"type": "http", "url": "https://app.researchzy.com/mcp"}}}` to the user `mcp.json`, then start the server and approve the sign-in |
| Codex without the plugin | `codex mcp add researchzy --url https://app.researchzy.com/mcp --oauth-client-id paperone-codex`, then `codex mcp login researchzy` |
| ChatGPT | Use the Researchzy app |

Other hosts work when they support a metadata document from a trusted site or have a client ID registered on the server. Ask the Researchzy team to register a client with its exact callback URLs.

To test a local checkout, register its repository marketplace and install `paperone@projectp1`:

```sh
codex plugin marketplace add /absolute/path/to/paperone-plugin
codex plugin add paperone@projectp1
```

If a Git marketplace with the same name is already configured, switch sources through the host's marketplace workflow instead of keeping two sources with the same name. An existing personal `Researchzy Test` plugin is a separate installation; this repository does not replace it automatically.
