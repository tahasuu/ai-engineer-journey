import sys
import requests

def main() -> None:
    print(f"Python: {sys.version.split()[0]}")
    print(f"In venv: {sys.prefix != sys.base_prefix}")
    r = requests.get("https://api.github.com")
    print(f"GitHub API status: {r.status_code}")

if __name__ == "__main__":
    main()