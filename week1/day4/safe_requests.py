import json
from pathlib import Path

import requests


def fetch_json(url: str) -> dict | None:
    """Get JSON from a URL. Returns None instead of crashing if something fails."""
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()  # turns 4xx/5xx status codes into an HTTPError
        return r.json()
    except requests.exceptions.Timeout:
        print("Error: the request timed out.")
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP {e.response.status_code} for {url}")
    except requests.exceptions.ConnectionError:
        print("Error: could not connect. Check the URL or your internet.")
    return None


def load_json_safe(path: str) -> list:
    """Load a JSON file. Returns [] if it's missing or broken."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"No file at {path}, starting fresh.")
        return []
    except json.JSONDecodeError:
        print(f"{path} is not valid JSON, starting fresh.")
        return []


if __name__ == "__main__":
    print("--- 1. A request that works ---")
    user = fetch_json("https://api.github.com/users/tahasuu")
    if user:
        print(f"Name: {user.get('name') or 'not set'}")
        print(f"Public repos: {user.get('public_repos')}")
        print(f"Followers: {user.get('followers')}")

    print("\n--- 2. A user that doesn't exist ---")
    fetch_json("https://api.github.com/users/no-such-user-xyz-98765")

    print("\n--- 3. A website that doesn't exist ---")
    fetch_json("https://no-such-site.invalid")

    print("\n--- 4. A missing file ---")
    print(load_json_safe("missing.json"))

    print("\n--- 5. A broken JSON file ---")
    Path("broken.json").write_text("{ oops, not json", encoding="utf-8")
    print(load_json_safe("broken.json"))
    Path("broken.json").unlink()  # delete the test file

    print("\nDone! The program survived every error.")