import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# =====================================================
# EXTRACT CLEAN TEXT
# =====================================================
def extract_text(html):

    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted tags
    for tag in soup([
        "script",
        "style",
        "noscript",
        "header",
        "footer",
        "nav",
        "aside"
    ]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)

    cleaned = []

    for sentence in text.split("."):

        sentence = sentence.strip()

        if len(sentence) < 20:
            continue

        cleaned.append(sentence)

    return ". ".join(cleaned)


# =====================================================
# WEBSITE CRAWLER
# =====================================================
def crawl_website(start_url, max_pages=8):

    visited = set()
    queued = {start_url}

    queue = [start_url]
    pages = []

    domain = urlparse(start_url).netloc

    print(f"\n🚀 Crawling website: {start_url}")

    while queue and len(visited) < max_pages:

        url = queue.pop(0)

        if url in visited:
            continue

        visited.add(url)

        print(f"🌐 Crawling: {url}")

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=10
            )

            if response.status_code != 200:
                continue

            html = response.text

            text = extract_text(html)

            if len(text) > 50:
                pages.append(text)

            soup = BeautifulSoup(html, "html.parser")

            for tag in soup.find_all("a", href=True):

                link = urljoin(url, tag["href"])

                parsed = urlparse(link)

                if parsed.netloc != domain:
                    continue

                clean_link = parsed._replace(fragment="").geturl()

                if any(x in clean_link.lower() for x in [
                    "login",
                    "signup",
                    "logout",
                    "mailto:",
                    "javascript:"
                ]):
                    continue

                # Prevent duplicate queue entries
                if clean_link not in visited and clean_link not in queued:
                    queue.append(clean_link)
                    queued.add(clean_link)

        except Exception as e:
            print(f"❌ Failed: {url} -> {e}")

    print(f"\n✅ Total pages crawled: {len(pages)}")

    return pages