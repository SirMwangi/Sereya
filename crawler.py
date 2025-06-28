import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def extract_page_content(url):
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch page: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Title
    title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

    # Meta Description
    meta_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = meta_tag["content"].strip() if meta_tag and meta_tag.get("content") else "No meta description"

    # Headings
    headings = {
        "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
        "h2": [h.get_text(strip=True) for h in soup.find_all("h2")],
        "h3": [h.get_text(strip=True) for h in soup.find_all("h3")]
    }

    # Images + Alt Attributes
    images = [{"src": img.get("src"), "alt": img.get("alt", "").strip()} for img in soup.find_all("img")]

    # Links
    internal_links = []
    external_links = []
    domain = urlparse(url).netloc

    for a_tag in soup.find_all("a", href=True):
        full_url = urljoin(url, a_tag["href"])
        if domain in urlparse(full_url).netloc:
            internal_links.append(full_url)
        else:
            external_links.append(full_url)

    # Main Text Content (limited)
    text = soup.get_text(separator=' ', strip=True)
    main_text_snippet = text[:1000] + "..." if len(text) > 1000 else text

    return {
        "url": url,
        "title": title,
        "meta_description": meta_description,
        "headings": headings,
        "images": images,
        "internal_links": internal_links,
        "external_links": external_links,
        "main_text_snippet": main_text_snippet
    }

# CLI test runner
if __name__ == "__main__":
    test_url = input("🔗 Enter a URL to crawl: ").strip()
    data = extract_page_content(test_url)

    if data:
        from pprint import pprint
        pprint(data)
    else:
        print("❌ Failed to extract data.")
