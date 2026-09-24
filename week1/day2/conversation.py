import json
from pathlib import Path


def make_message(role: str, content: str) -> dict:
    # TODO 1: return a dict with "role" and "content"
    return {"role": role, "content": content}


def add_message(history: list[dict], role: str, content: str) -> list[dict]:
    # TODO 2: use make_message(), append it to history, then return history
    msg = make_message(role, content)
    history.append(msg)
    return history


def save_history(history: list[dict], path: str) -> None:
    # TODO 3: open the file in "w" mode and json.dump() history into it (indent=2)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def load_history(path: str) -> list[dict]:
    # TODO 4: if the file doesn't exist, return []
    #         otherwise open it in "r" mode and return json.load(f)
    if not Path(path).exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    history = load_history("chat.json")
    history = add_message(history, "user", "Hi! What's RAG?")
    history = add_message(history, "assistant", "RAG = Retrieval-Augmented Generation.")
    save_history(history, "chat.json")

    print(f"Messages saved: {len(history)}")
    for m in history:
        print(f"[{m['role']}] {m['content']}")