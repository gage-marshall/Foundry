"""Markdown processing utilities for Foundry Engine."""

from typing import Any

import markdown
from markdown.extensions import codehilite, fenced_code, tables, toc
from pymdownx import superfences, tasklist


def setup_markdown_processor() -> markdown.Markdown:
    """Create and configure a Markdown processor with extensions."""
    md = markdown.Markdown(
        extensions=[
            "extra",  # Includes tables, footnotes, attr_list, etc.
            "codehilite",  # Syntax highlighting
            "fenced_code",  # Fenced code blocks
            "tables",  # Tables support
            "toc",  # Table of contents
            "nl2br",  # Newline to <br>
            "sane_lists",  # Better list handling
            "pymdownx.superfences",  # Enhanced fenced code blocks
            "pymdownx.tasklist",  # Task lists
            "pymdownx.emoji",  # Emoji support
            "pymdownx.magiclink",  # Auto-link URLs
            "pymdownx.tilde",  # Strikethrough
            "pymdownx.mark",  # Highlighting
        ],
        extension_configs={
            "codehilite": {
                "css_class": "highlight",
                "linenums": False,
            },
            "pymdownx.superfences": {
                "custom_fences": [
                    {
                        "name": "mermaid",
                        "class": "mermaid",
                        "format": lambda src, lang, **kwargs: f'<div class="mermaid">{src}</div>',
                    }
                ]
            },
            "pymdownx.tasklist": {
                "custom_checkbox": True,
            },
        },
    )
    return md


def render_markdown(md_processor: markdown.Markdown, content: str) -> str:
    """Render markdown content to HTML."""
    return md_processor.convert(content)


def render_markdown_file(md_processor: markdown.Markdown, file_path: str) -> str:
    """Render markdown file to HTML."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return render_markdown(md_processor, content)
