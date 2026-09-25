import json
from pathlib import Path


class Conversation:
    def __init__(self, path: str):
        self.path = path
        self.messages = self.load()

    def load(self) -> list[dict]:
        # TODO 1: same as yesterday's load_history, but use self.path
        if not Path(self.path).exists():
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def add(self, role: str, content: str) -> None:
        # TODO 2: append {"role": role, "content": content} to self.messages
        self.messages.append({"role": role, "content": content})

    def save(self) -> None:
        # TODO 3: same as yesterday's save_history, using self.path and self.messages
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=2)

    def export_txt(self, txt_path: str) -> None:
        # TODO 4: write one line per message, like "[user] Hi!", to a .txt file
        # hint: open(txt_path, "w", encoding="utf-8") as f, then
        #       loop over self.messages and f.write(f"[{m['role']}] {m['content']}\n")
        with open(txt_path, "w", encoding="utf-8") as f:
            for m in self.messages:
                f.write(f"[{m['role']}] {m['content']}\n")


if __name__ == "__main__":
    chat = Conversation("chat_day3.json")
    chat.add("user", "What is a class?")
    chat.add("assistant", "A blueprint that bundles data and methods.")
    chat.save()
    chat.export_txt("chat_day3.txt")

    print(f"Messages: {len(chat.messages)}")
    for m in chat.messages:
        print(f"[{m['role']}] {m['content']}")
    print("Exported to chat_day3.txt")