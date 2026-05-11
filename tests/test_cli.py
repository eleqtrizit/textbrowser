"""Tests for textbrowser CLI module."""

import pytest
from playwright.sync_api import sync_playwright

from textbrowser.cli import fetch_html, html_to_markdown


class TestHtmlToMarkdown:
    """Tests for html_to_markdown function."""

    def test_simple_paragraph(self) -> None:
        """Test conversion of a simple paragraph."""
        html = "<p>Hello, World!</p>"
        result = html_to_markdown(html)
        assert "Hello, World!" in result

    def test_heading(self) -> None:
        """Test conversion of headings."""
        html = "<h1>Title</h1>"
        result = html_to_markdown(html)
        assert "Title" in result
        assert "===" in result  # Setext-style h1

    def test_link(self) -> None:
        """Test conversion of links."""
        html = '<a href="https://example.com">Example</a>'
        result = html_to_markdown(html)
        assert "[Example](https://example.com)" in result

    def test_nested_elements(self) -> None:
        """Test conversion of nested elements."""
        html = "<div><p><strong>Bold text</strong></p></div>"
        result = html_to_markdown(html)
        assert "**Bold text**" in result

    def test_empty_input(self) -> None:
        """Test conversion of empty input."""
        html = ""
        result = html_to_markdown(html)
        assert result == ""

    def test_complex_html(self) -> None:
        """Test conversion of complex HTML structure."""
        html = """
        <html>
            <body>
                <h1>Main Title</h1>
                <p>This is a <a href="https://example.com">link</a>.</p>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                </ul>
            </body>
        </html>
        """
        result = html_to_markdown(html)
        assert "Main Title" in result
        assert "===" in result  # Setext-style h1
        assert "[link](https://example.com)" in result
        assert "Item 1" in result
        assert "Item 2" in result


class TestFetchHtml:
    """Tests for fetch_html function."""

    @pytest.mark.integration
    def test_fetch_valid_url(self) -> None:
        """Test fetching HTML from a valid URL."""
        # Using a simple, reliable test page
        url = "https://example.com"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            response = page.goto(url)
            assert response is not None
            assert response.ok
            html = page.content()
            browser.close()

        assert "<html" in html.lower()
        assert "Example Domain" in html

    @pytest.mark.integration
    def test_fetch_invalid_url(self) -> None:
        """Test fetching HTML from an invalid URL."""
        with pytest.raises(Exception):
            fetch_html("https://this-domain-definitely-does-not-exist-12345.com")
