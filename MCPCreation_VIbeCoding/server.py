"""
Demo MCP Server - A FastMCP-based MCP server with Playwright-style tools,
resources, data resources, and prompts.
"""

from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Demo MCP Server")


# =============================================================================
# TOOLS SECTION - 20+ Dummy Playwright-Style Tools
# =============================================================================


@mcp.tool()
def browser_launch(headless: bool = True) -> dict:
    """Launch a new browser instance."""
    return {"status": "success", "browser": "chromium", "headless": headless}


@mcp.tool()
def browser_close() -> dict:
    """Close the browser instance."""
    return {"status": "success", "message": "Browser closed"}


@mcp.tool()
def page_goto(url: str) -> dict:
    """Navigate to a URL."""
    return {"status": "success", "url": url, "title": "Demo Page"}


@mcp.tool()
def page_click(selector: str) -> dict:
    """Click an element on the page."""
    return {"status": "success", "selector": selector, "action": "clicked"}


@mcp.tool()
def page_fill(selector: str, value: str) -> dict:
    """Fill an input field with text."""
    return {"status": "success", "selector": selector, "value": value}


@mcp.tool()
def page_screenshot(path: str = "screenshot.png") -> dict:
    """Take a screenshot of the current page."""
    return {"status": "success", "path": path, "format": "png"}


@mcp.tool()
def page_get_text(selector: str) -> dict:
    """Get the text content of an element."""
    return {"status": "success", "selector": selector, "text": "Demo text content"}


@mcp.tool()
def page_get_attribute(selector: str, attribute: str) -> dict:
    """Get an attribute value from an element."""
    return {"status": "success", "selector": selector, "attribute": attribute, "value": "demo-value"}


@mcp.tool()
def page_wait_for_selector(selector: str, timeout: int = 30000) -> dict:
    """Wait for an element to appear on the page."""
    return {"status": "success", "selector": selector, "timeout": timeout}


@mcp.tool()
def page_select_option(selector: str, value: str) -> dict:
    """Select an option from a dropdown."""
    return {"status": "success", "selector": selector, "selected": value}


@mcp.tool()
def page_hover(selector: str) -> dict:
    """Hover over an element."""
    return {"status": "success", "selector": selector, "action": "hovered"}


@mcp.tool()
def page_press_key(key: str) -> dict:
    """Press a keyboard key."""
    return {"status": "success", "key": key}


@mcp.tool()
def page_evaluate(expression: str) -> dict:
    """Evaluate JavaScript in the page context."""
    return {"status": "success", "expression": expression, "result": None}


@mcp.tool()
def page_get_url() -> dict:
    """Get the current page URL."""
    return {"status": "success", "url": "https://example.com"}


@mcp.tool()
def page_get_title() -> dict:
    """Get the current page title."""
    return {"status": "success", "title": "Demo Page Title"}


@mcp.tool()
def page_is_visible(selector: str) -> dict:
    """Check if an element is visible."""
    return {"status": "success", "selector": selector, "visible": True}


@mcp.tool()
def page_is_enabled(selector: str) -> dict:
    """Check if an element is enabled."""
    return {"status": "success", "selector": selector, "enabled": True}


@mcp.tool()
def page_check(selector: str) -> dict:
    """Check a checkbox or radio button."""
    return {"status": "success", "selector": selector, "checked": True}


@mcp.tool()
def page_uncheck(selector: str) -> dict:
    """Uncheck a checkbox."""
    return {"status": "success", "selector": selector, "checked": False}


@mcp.tool()
def page_set_viewport(width: int = 1280, height: int = 720) -> dict:
    """Set the page viewport size."""
    return {"status": "success", "width": width, "height": height}


@mcp.tool()
def page_go_back() -> dict:
    """Navigate back in browser history."""
    return {"status": "success", "action": "navigated back"}


@mcp.tool()
def page_go_forward() -> dict:
    """Navigate forward in browser history."""
    return {"status": "success", "action": "navigated forward"}


@mcp.tool()
def page_reload() -> dict:
    """Reload the current page."""
    return {"status": "success", "action": "reloaded"}


@mcp.tool()
def context_new_page() -> dict:
    """Create a new page in the browser context."""
    return {"status": "success", "page_id": "page-1"}


@mcp.tool()
def context_cookies(url: str = "") -> dict:
    """Get cookies for the current context."""
    return {"status": "success", "cookies": [{"name": "session", "value": "demo-token"}]}


# =============================================================================
# RESOURCES SECTION - 3 Resources
# =============================================================================


@mcp.resource("config://server")
def server_config() -> str:
    """Return the server configuration."""
    return """
{
    "server_name": "Demo MCP Server",
    "version": "1.0.0",
    "framework": "FastMCP",
    "transport": "stdio"
}
"""


@mcp.resource("docs://tools")
def tools_documentation() -> str:
    """Return documentation for available tools."""
    return """
# Available Tools

This server provides 25 Playwright-style tools:
- browser_launch: Launch a browser
- browser_close: Close the browser
- page_goto: Navigate to URL
- page_click: Click elements
- page_fill: Fill input fields
- page_screenshot: Take screenshots
- And 20 more tools for page interaction
"""


@mcp.resource("docs://getting-started")
def getting_started() -> str:
    """Return getting started guide."""
    return """
# Getting Started

1. Install dependencies: pip install -r requirements.txt
2. Run the server: python server.py
3. Connect via MCP Inspector: mcp-inspector
4. Use STDIO transport with command: python server.py
"""


# =============================================================================
# DATA SECTION - 2 Data Resources
# =============================================================================


@mcp.resource("data://sample-users")
def sample_users() -> str:
    """Return sample user data."""
    return """
[
    {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "user"},
    {"id": 4, "name": "Diana", "email": "diana@example.com", "role": "moderator"},
    {"id": 5, "name": "Eve", "email": "eve@example.com", "role": "user"}
]
"""


@mcp.resource("data://sample-products")
def sample_products() -> str:
    """Return sample product data."""
    return """
[
    {"id": 101, "name": "Laptop", "price": 999.99, "category": "electronics"},
    {"id": 102, "name": "Mouse", "price": 29.99, "category": "accessories"},
    {"id": 103, "name": "Keyboard", "price": 79.99, "category": "accessories"},
    {"id": 104, "name": "Monitor", "price": 349.99, "category": "electronics"},
    {"id": 105, "name": "Headphones", "price": 149.99, "category": "audio"}
]
"""


# =============================================================================
# PROMPTS SECTION - 5 Prompts
# =============================================================================


@mcp.prompt()
def test_login_flow() -> str:
    """Generate a prompt for testing a login flow."""
    return """
Please test the login flow:
1. Navigate to the login page
2. Fill in the username field
3. Fill in the password field
4. Click the login button
5. Verify successful login
"""


@mcp.prompt()
def test_form_submission() -> str:
    """Generate a prompt for testing form submission."""
    return """
Please test the form submission:
1. Navigate to the form page
2. Fill all required fields
3. Select options from dropdowns
4. Check required checkboxes
5. Submit the form
6. Verify success message
"""


@mcp.prompt()
def test_navigation() -> str:
    """Generate a prompt for testing page navigation."""
    return """
Please test page navigation:
1. Navigate to the homepage
2. Click on each navigation link
3. Verify each page loads correctly
4. Test browser back and forward buttons
5. Verify URL changes are correct
"""


@mcp.prompt()
def test_screenshot_comparison() -> str:
    """Generate a prompt for visual regression testing."""
    return """
Please perform visual regression testing:
1. Navigate to the target page
2. Take a full-page screenshot
3. Compare with baseline image
4. Report any visual differences
5. Save the comparison report
"""


@mcp.prompt()
def test_api_integration() -> str:
    """Generate a prompt for testing API integration."""
    return """
Please test API integration:
1. Navigate to the API test page
2. Trigger API calls via UI
3. Verify response data displays correctly
4. Check error handling for failed requests
5. Validate response times
"""


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    mcp.run()
