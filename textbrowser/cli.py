"""CLI module for textbrowser - fetches web pages and converts to Markdown."""

import argparse
import subprocess
import sys
from pathlib import Path

from markdownify import markdownify as md
from playwright.sync_api import sync_playwright


def ensure_playwright_browsers() -> None:
    """Ensure Playwright browsers are installed, installing them if missing.

    :raises RuntimeError: If browser installation fails
    """
    try:
        # Quick check: try to launch Firefox headlessly
        with sync_playwright() as p:
            p.firefox.launch(headless=True).close()
    except Exception as e:
        error_msg = str(e)
        if "Executable doesn't exist" in error_msg or "playwright install" in error_msg.lower():
            print("Playwright browsers not found. Installing Firefox...", file=sys.stderr)
            try:
                # Get the playwright executable from the same environment
                playwright_path = Path(sys.executable).parent / "playwright"
                subprocess.run(
                    [str(playwright_path), "install", "firefox"],
                    check=True,
                    capture_output=False,
                )
                print("Firefox browser installed successfully.", file=sys.stderr)
            except subprocess.CalledProcessError as install_err:
                raise RuntimeError(
                    f"Failed to install Playwright browsers. "
                    f"Run: playwright install firefox\n{install_err.stderr}"
                ) from install_err
        else:
            raise


def fetch_html(url: str) -> str:
    """Fetch HTML content from a URL using Playwright headless browser.

    :param url: The URL to fetch
    :type url: str
    :return: The HTML content of the page
    :rtype: str
    :raises RuntimeError: If the page fails to load
    """
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        response = page.goto(url)

        if response is None or not response.ok:
            status = response.status if response else "unknown"
            raise RuntimeError(f"Failed to load {url}: HTTP {status}")

        html = page.content()
        browser.close()
        return html


def html_to_markdown(html: str) -> str:
    """Convert HTML content to Markdown.

    :param html: The HTML content to convert
    :type html: str
    :return: The Markdown representation
    :rtype: str
    """
    return md(html)


def main() -> None:
    """Main entry point for the textbrowser CLI."""
    parser = argparse.ArgumentParser(
        description="Fetch a web page and convert it to Markdown",
        prog="textbrowser",
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="URL of the web page to fetch (if not provided, reads HTML from stdin)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--install-browsers",
        action="store_true",
        help="Install Playwright browsers and exit",
    )

    args = parser.parse_args()

    if args.install_browsers:
        print("Installing Playwright browsers...", file=sys.stderr)
        ensure_playwright_browsers()
        print("Done. You can now use textbrowser.", file=sys.stderr)
        return

    try:
        if args.url:
            ensure_playwright_browsers()
            html = fetch_html(args.url)
        else:
            html = sys.stdin.read()

        markdown = html_to_markdown(html)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(markdown)
        else:
            print(markdown)

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
