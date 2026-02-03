import requests
from bs4 import BeautifulSoup


def web_search(query: str, max_results: int = 5):
    params = {
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1,
    }

    response = requests.get("https://api.duckduckgo.com/", params=params)
    data = response.json()

    results = []

    for item in data.get("RelatedTopics", []):
        if isinstance(item, dict) and "FirstURL" in item:
            results.append(item["FirstURL"])
        if len(results) >= max_results:
            break

    return results

def web_fetch(url: str):

    response = requests.get(url, timeout=10)

    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    text = " ".join(text.split())

    return text