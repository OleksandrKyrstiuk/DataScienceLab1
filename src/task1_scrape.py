from typing import Dict
import requests
from bs4 import BeautifulSoup

try:
    from .utils import save_to_json
except ImportError:
    from utils import save_to_json


def fetch_wikipedia_page(url: str) -> str:
    """Fetch the HTML content of the given Wikipedia page.

    Args:
        url (str): The URL of the Wikipedia page to fetch.

    Returns:
        str: The raw HTML content of the page.

    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch page from {url}: {e}") from e


def extract_title(soup: BeautifulSoup) -> str:
    """Extract the title of the Wikipedia page.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the page.

    Returns:
        str: The extracted page title, or an empty string if not found.
    """
    title_element = soup.find("h1", id="firstHeading")
    if title_element:
        return title_element.text.strip()
    return ""


def extract_first_sentence(soup: BeautifulSoup) -> str:
    """Extract the first sentence of the first paragraph on the Wikipedia page.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the page.

    Returns:
        str: The first sentence of the main content paragraph.
    """
    for p in soup.find_all("p"):
        text = p.get_text().strip()
        if text:
            first_sentence = text.split(".")[0].strip() + "."
            return first_sentence
    return ""


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    try:
        page_content = fetch_wikipedia_page(url)
        soup = BeautifulSoup(page_content, "html.parser")

        title = extract_title(soup)
        first_sentence = extract_first_sentence(soup)

        extracted_data = {
            "title": title,
            "first_sentence": first_sentence
        }

        print("Extracted Data:", extracted_data)
        save_to_json(extracted_data, "extracted_wikipedia_data.json")
        print("Data successfully saved to extracted_wikipedia_data.json")
    except Exception as e:
        print(f"An error occurred: {e}")