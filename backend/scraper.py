import requests

def scrape_page(url):
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.text

        return None

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None