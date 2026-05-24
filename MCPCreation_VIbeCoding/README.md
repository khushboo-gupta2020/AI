# Demo MCP Server

A complete Python MCP server built with FastMCP, featuring 25 Playwright-style tools, 3 resources, 2 data resources, and 5 prompts.

## Installation

### 1. Install FastMCP

```bash
pip install -r requirements.txt
```

Or directly:

```bash
pip install fastmcp
```

### 2. Install Playwright (Optional - for real browser automation)

This server uses dummy implementations, but if you want real Playwright:

```bash
pip install playwright
playwright install chromium
```

### 3. Install MCP Inspector

```bash
npm install -g @modelcontextprotocol/inspector
```

## Running the Server

### Start the server using STDIO:

```bash
python server.py
```

The server will start and listen for MCP protocol messages over STDIO.

## Connecting with MCP Inspector

### 1. Launch MCP Inspector:

```bash
mcp-inspector
```

### 2. Connect via STDIO:

- Open MCP Inspector in your browser (usually http://localhost:6274)
- Select **STDIO** as the transport type
- Enter the command: `python server.py`
- Click **Connect**

## Expected Output

After connecting in MCP Inspector, you should see:

- **25 Tools** visible in the Tools tab:
  - browser_launch, browser_close
  - page_goto, page_click, page_fill, page_screenshot
  - page_get_text, page_get_attribute, page_wait_for_selector
  - page_select_option, page_hover, page_press_key
  - page_evaluate, page_get_url, page_get_title
  - page_is_visible, page_is_enabled, page_check, page_uncheck
  - page_set_viewport, page_go_back, page_go_forward, page_reload
  - context_new_page, context_cookies

- **3 Resources** visible in the Resources tab:
  - config://server
  - docs://tools
  - docs://getting-started

- **2 Data Resources** visible in the Resources tab:
  - data://sample-users
  - data://sample-products

- **5 Prompts** visible in the Prompts tab:
  - test_login_flow
  - test_form_submission
  - test_navigation
  - test_screenshot_comparison
  - test_api_integration

## Taking Screenshot Proof

1. Start MCP Inspector: `mcp-inspector`
2. Connect with STDIO using command: `python server.py`
3. Navigate to each tab (Tools, Resources, Prompts)
4. Take screenshots showing:
   - Tools tab with 25 tools listed
   - Resources tab with 5 resources (3 + 2 data)
   - Prompts tab with 5 prompts listed

Use your OS screenshot tool:
- **Windows**: `Win + Shift + S`
- **macOS**: `Cmd + Shift + 4`
- **Linux**: `gnome-screenshot` or `flameshot`

## Project Structure

```
MCPCreation_VIbeCoding/
├── server.py          # Main MCP server file
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## License

MIT
