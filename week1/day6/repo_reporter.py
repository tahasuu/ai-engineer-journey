import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")  # optional, from your Day 5 .env


class RepoReport:
    def __init__(self, username, repos):
        self.username = username
        self.repos = repos  # list of dicts from the GitHub API

    def top_repos(self, n=5):
        """Return the n repos with the most stars."""
        return sorted(self.repos, key=lambda r: r["stargazers_count"], reverse=True)[:n]

    def languages(self):
        """Count how many repos use each language, skipping repos with no language."""
        counts = {}
        for repo in self.repos:
            lang = repo.get("language")
            if lang:
                counts[lang] = counts.get(lang, 0) + 1
        return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    def summary(self):
        """Build a clean dict with just the info we care about."""
        return {
            "username": self.username,
            "repo_count": len(self.repos),
            "top_repos": [
                {
                    "name": r["name"],
                    "stars": r["stargazers_count"],
                    "language": r.get("language"),
                    "url": r["html_url"],
                }
                for r in self.top_repos()
            ],
            "languages": self.languages(),
        }

    def save(self, path):
        """Write the summary to a JSON file."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.summary(), f, indent=2)


def fetch_repos(username):
    """Get a user's public repos. Returns a list, or None if something went wrong."""
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    try:
        response = requests.get(url, headers=headers, params={"per_page": 100}, timeout=10)
    except requests.exceptions.Timeout:
        print("GitHub took too long to respond. Try again in a moment.")
        return None
    except requests.exceptions.ConnectionError:
        print("Couldn't connect. Check your internet connection.")
        return None

    if response.status_code == 404:
        print(f"User '{username}' not found on GitHub.")
        return None
    if response.status_code == 401:
        print("Your GITHUB_TOKEN looks invalid. Check your .env file.")
        return None
    if response.status_code == 403:
        print("Rate limit hit. Wait a bit, or add a GITHUB_TOKEN to your .env.")
        return None
    if not response.ok:
        print(f"Unexpected error: {response.status_code}")
        return None

    return response.json()


def main():
    username = input("GitHub username: ").strip()
    if not username:
        print("Please enter a username.")
        return

    repos = fetch_repos(username)
    if repos is None:
        return

    report = RepoReport(username, repos)

    print(f"\n{username} - {len(repos)} public repos")

    if not repos:
        print("No public repos to show.")
        return

    top = ", ".join(f"{r['name']} ({r['stargazers_count']:,})" for r in report.top_repos())
    print(f"Top repos: {top}")

    langs = ", ".join(f"{lang}: {count}" for lang, count in report.languages().items())
    print(f"Languages: {langs or 'none listed'}")

    path = f"week1/day6/report_{username}.json"
    report.save(path)
    print(f"Saved to {path}")


if __name__ == "__main__":
    main()
