"""CLI module for textbrowser - fetches web pages and converts to Markdown."""

import argparse
import sys

from markdownify import markdownify as md
from playwright.sync_api import sync_playwright


def fetch_html(url: str) -> str:
    """Fetch HTML content from a URL using Playwright headless browser.

    :param url: The URL to fetch
    :type url: str
    :return: The HTML content of the page
    :rtype: str
    :raises RuntimeError: If the page fails to load
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
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

    args = parser.parse_args()

    try:
        if args.url:
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
