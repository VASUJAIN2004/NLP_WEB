import json
from pathlib import Path


USER_FILE = Path(__file__).resolve().with_name("user.json")

class Database:
    def _load_users(self):
        try:
            with USER_FILE.open("r", encoding="utf-8") as rf:
                return json.load(rf)
        except FileNotFoundError:
            return {}

    def insert(self, name, email,password):
        users = self._load_users()

        if email in users:
            return 0

        users[email] = [name, password]

        with USER_FILE.open("w", encoding="utf-8") as wf:
            json.dump(users, wf, indent=4)
        return 1

    def search(self, email, password):
        users = self._load_users()

        if email in users:
            if users[email][1] == password:
                return 1
            else:
                return 0
        else:
            return 0

