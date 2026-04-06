import json
from datetime import date

USERS_FILE = "data/users.json"


def load_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def can_get_wish(user_id):
    users = load_users()
    today = str(date.today())

    user = users.get(str(user_id))
    if user and user.get("date") == today:
        return False, user.get("wish")

    return True, None


def save_wish(user_id, wish):
    users = load_users()
    today = str(date.today())

    users[str(user_id)] = {
        "date": today,
        "wish": wish
    }

    save_users(users)