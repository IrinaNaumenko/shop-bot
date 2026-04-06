import time
import requests
import json
from requests.exceptions import ReadTimeout


from config import BOT_TOKEN, BASE_URL, ADDRESSES_TEXT, CHILDREN_CHANNEL_URL, LINGERIE_CHANNEL_URL
from wishes import get_random_wish
from storage import can_get_wish, save_wish

HEADERS = {
    "Authorization": "f9LHodD0cOJ7x6p1nhw6fuNYUxPFuHRXuE-csabyOzLvbNaBuwTc0DN1BjEIlCLKjC1s07k8y98RbKBQhhQE",
    "Content-Type": "application/json; charset=utf-8"
}
print("main.py запущен")

def build_main_buttons():
    return [
        [
            {
                "type": "link",
                "text": "👶 Детская одежда",
                "url": "https://max.ru/join/KnDN_ZjI64bc2WkA5T-bcycgse4OITs2LvD5tV57I1I"
            }
        ],
        [
            {
                "type": "link",
                "text": "👙 Нижнее бельё",
                "url": "https://max.ru/join/oL7jV0AUuo8bfjQK62gpr46eSk6RvZjOzbnHB2B4Q70"
            }
        ],
        [
            {
                "type": "message",
                "text": "🔮 Гадалка",
                "payload": "гадалка"
            }
        ],
        [
            {
                "type": "message",
                "text": "📍 Адрес",
                "payload": "адрес"
            }
        ]
    ]


def send_message(chat_id, text, buttons=None):
    payload = {
        "text": text
    }

    if buttons:
        payload["attachments"] = [
            {
                "type": "inline_keyboard",
                "payload": {
                    "buttons": buttons
                }
            }
        ]

    response = requests.post(
        f"{BASE_URL}/messages",
        params={"chat_id": chat_id},
        headers=HEADERS,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=30
    )
    print("SEND:", response.status_code, response.text)


def get_updates(marker=None):
    params = {}
    if marker is not None:
        params["marker"] = marker

    response = requests.get(
        f"{BASE_URL}/updates",
        headers=HEADERS,
        params=params,
        timeout=(5, 60)
    )
    print("UPDATES:", response.status_code, response.text)
    response.raise_for_status()
    return response.json()


def handle_start(chat_id):
    text = (
        "Добро пожаловать 🤍\n\n"
        "Посмотри, что есть:"
    )

    send_message(chat_id, text, buttons=build_main_buttons())


def handle_message(chat_id, user_id, text):
    text = (text or "").strip().lower()

    print("ПОЛУЧЕН ТЕКСТ:", text)  # чтобы видеть

    if text in ["/start", "start", "меню"]:
        handle_start(chat_id)
        return

    if "гадалка" in text:
        allowed, old_wish = can_get_wish(user_id)

        if not allowed:
            send_message(chat_id, f"🔮 Сегодня тебе уже выпало:\n\n{old_wish}", buttons=build_main_buttons())
            return

        wish = get_random_wish()
        save_wish(user_id, wish)

        send_message(chat_id, f"🔮 Твоё сообщение на сегодня:\n\n{wish}", buttons=build_main_buttons())
        return

    if "адрес" in text:
        send_message(chat_id, ADDRESSES_TEXT, buttons=build_main_buttons())
        return

    handle_start(chat_id)


def handle_callback(update):
    callback = update.get("callback", {})
    payload = (callback.get("payload") or "").strip().lower()
    chat_id = update.get("chat_id")
    user = update.get("user", {})
    user_id = user.get("user_id")

    if not chat_id:
        return

    if payload == "гадалка":
        allowed, old_wish = can_get_wish(user_id)

        if not allowed:
            send_message(chat_id, f"🔮 Сегодня тебе уже выпало:\n\n{old_wish}", buttons=build_main_buttons())
            return

        wish = get_random_wish()
        save_wish(user_id, wish)
        send_message(chat_id, f"🔮 Твоё сообщение на сегодня:\n\n{wish}", buttons=build_main_buttons())
        return

    if payload == "адрес":
        send_message(chat_id, ADDRESSES_TEXT, buttons=build_main_buttons())
        return

    handle_start(chat_id)


def run():
    print("run() стартовал")
    marker = None

    while True:
        try:
            data = get_updates(marker)
            updates = data.get("updates", [])
            marker = data.get("marker", marker)

            for update in updates:
                update_type = update.get("update_type")

                if update_type == "bot_started":
                    chat_id = update.get("chat_id")
                    if chat_id:
                        handle_start(chat_id)
                    continue

                if update_type == "message_callback":
                    handle_callback(update)
                    continue

                if update_type == "message_created":
                    message = update.get("message", {})
                    recipient = message.get("recipient", {})
                    sender = message.get("sender", {})

                    chat_id = recipient.get("chat_id")
                    user_id = sender.get("user_id")
                    text = message.get("body", {}).get("text", "")

                    if chat_id:
                        handle_message(chat_id, user_id, text)
                    continue

            time.sleep(1)

        except Exception as e:
            print("Ошибка:", e)
            time.sleep(3)


if __name__ == "__main__":
    print("__main__ сработал")
    run()


if __name__ == "__main__":
    print("__main__ сработал")
    run()