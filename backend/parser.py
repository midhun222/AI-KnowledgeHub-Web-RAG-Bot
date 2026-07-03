from bs4 import BeautifulSoup
import re


def extract_text(html: str) -> str:
    """
    Extract clean, readable text from raw HTML.

    Args:
        html (str): Raw HTML of the webpage.

    Returns:
        str: Cleaned text.
    """

    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted elements
    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "header",
        "footer",
        "nav",
        "aside",
        "form",
        "iframe",
        "canvas",
        "button",
        "input",
        "select",
        "textarea"
    ]):
        tag.decompose()

    # Remove comments
    for comment in soup.find_all(string=lambda text: isinstance(text, str) and "<!--" in text):
        comment.extract()

    # Extract visible text
    text = soup.get_text(separator="\n")

    # Normalize line breaks
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove repeated blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove empty lines
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    text = "\n".join(lines)

    return text.strip()