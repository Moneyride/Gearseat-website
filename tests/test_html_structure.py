from collections import Counter
from pathlib import Path
import re

from bs4 import BeautifulSoup

# HTML void elements that do not require closing tags
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr"
}


def test_html_tags_are_balanced():
    base_dir = Path(__file__).resolve().parent.parent
    html_path = base_dir / "index.html"
    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    # Ensure BeautifulSoup can parse the HTML
    soup = BeautifulSoup(html, "html.parser")
    assert soup is not None

    # Count start and end tags using a simple regex parser
    tag_pattern = re.compile(r"<(/?)([a-zA-Z0-9]+)[^>]*>")
    counts = Counter()
    for match in tag_pattern.finditer(html):
        closing, tag = match.groups()
        tag = tag.lower()
        if tag in VOID_ELEMENTS:
            continue
        counts[tag] += -1 if closing else 1

    unbalanced = {tag: count for tag, count in counts.items() if count != 0}
    assert not unbalanced, f"Unbalanced tags found: {unbalanced}"
