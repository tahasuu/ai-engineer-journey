import os

import requests
from dotenv import load_dotenv

load_dotenv()  # reads .env into environment variables

TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"


def get_headers() -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return headers


def check_rate_limit() -> None:
    try:
        r = requests.get(f"{BASE_URL}/rate_limit", headers=get_headers(), timeout=10)
        r.raise_for_status()
        core = r.json()["resources"]["core"]
        print(f"Rate limit: {core['remaining']} of {core['limit']} requests left this hour")
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP {e.response.status_code} (401 means a bad token)")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def search_repos(query: str, count: int = 5) -> list[dict]:
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": count}
    try:
        r = requests.get(
            f"{BASE_URL}/search/repositories",
            headers=get_headers(),
            params=params,
            timeout=10,
        )
        r.raise_for_status()
        return r.json()["items"]
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return []


if __name__ == "__main__":
    print(f"Token loaded: {TOKEN is not None}")
    if TOKEN:
        print(f"Token starts with: {TOKEN[:10]}...")  # never print the full key!
    check_rate_limit()

    query = "rag language:python"
    print(f"\nTop repos for '{query}':")
    for i, repo in enumerate(search_repos(query), start=1):
        print(f"{i}. {repo['full_name']} - {repo['stargazers_count']:,} stars")