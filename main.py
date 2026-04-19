import json
import requests

from config import MAX_TOKEN, BASE_URL, ADDRESSES_TEXT, CHILDREN_CHANNEL_URL, LINGERIE_CHANNEL_URL

HEADERS = {
    "Authorization": MAX_TOKEN,
    "Content-Type": "application/json; charset=utf-8"
}


def handle_catalog(chat_id):
    text = (
        "🛍 Каталог\n\n"
        "Выбери категорию:"
    )
    send_message(chat_id, text, buttons=build_catalog_buttons())


def build_main_buttons():
    return [
        [
            {
                "type": "link",
                "text": "👶 Детская одежда",
                "url": CHILDREN_CHANNEL_URL
            }
        ],
        [
            {
                "type": "link",
                "text": "👙 Нижнее бельё",
                "url": LINGERIE_CHANNEL_URL
            }
        ],
        [
            {
                "type": "message",
                "text": "🛍 Каталог",
                "payload": "каталог"
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


def build_catalog_buttons():
    return [
        [{"type": "message", "text": "👗 Платья", "payload": "платье"}],
        [{"type": "message", "text": "👖 Джинсы", "payload": "джинсы"}],
        [{"type": "message", "text": "🧥 Верхняя одежда", "payload": "верхняя"}],
        [{"type": "message", "text": "👕 Футболки", "payload": "футболка"}],
        [{"type": "message", "text": "👚 Блузы", "payload": "блуза"}],
        [{"type": "message", "text": "👗 Юбки", "payload": "юбка"}],
        [{"type": "message", "text": "👜 Аксессуары", "payload": "аксессуары"}],
        [{"type": "message", "text": "✨ Новинки", "payload": "новинка"}],
        [{"type": "message", "text": "🔥 Распродажа", "payload": "распродажа"}],
        [{"type": "message", "text": "🔙 Назад", "payload": "назад"}]
    ]


def send_catalog_tag(chat_id, title, tag):
    text = (
        f"{title}\n\n"
        f"Мы уже всё подобрали за тебя 🤍\n"
        f"Открой канал и ищи по тегу: #{tag}"
    )
    send_message(chat_id, text, buttons=build_catalog_buttons())


def send_message(chat_id, text, buttons=None):
    payload = {"text": text}

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
        timeout=15
    )

    print("SEND:", response.status_code, response.text)
    response.raise_for_status()


def handle_start(chat_id):
    text = (
        "Добро пожаловать 🤍\n\n"
        "Посмотри, что есть:"
    )
    send_message(chat_id, text, buttons=build_main_buttons())


def handle_message(chat_id, text):
    text = (text or "").strip().lower()
    print("ПОЛУЧЕН ТЕКСТ:", text)

    if text in ["/start", "start", "меню", "назад"]:
        handle_start(chat_id)
        return

    if "каталог" in text:
        handle_catalog(chat_id)
        return

    if "адрес" in text:
        send_message(chat_id, ADDRESSES_TEXT, buttons=build_main_buttons())
        return

    if "платье" in text:
        send_catalog_tag(chat_id, "👗 Платья", "платье")
        return

    if "джинсы" in text:
        send_catalog_tag(chat_id, "👖 Джинсы", "джинсы")
        return

    if "верхняя" in text:
        send_catalog_tag(chat_id, "🧥 Верхняя одежда", "верхняя")
        return

    if "футболка" in text:
        send_catalog_tag(chat_id, "👕 Футболки", "футболка")
        return

    if "блуза" in text:
        send_catalog_tag(chat_id, "👚 Блузы", "блуза")
        return

    if "юбка" in text:
        send_catalog_tag(chat_id, "👗 Юбки", "юбка")
        return

    if "аксессуары" in text:
        send_catalog_tag(chat_id, "👜 Аксессуары", "аксессуары")
        return

    if "новинка" in text:
        send_catalog_tag(chat_id, "✨ Новинки", "новинка")
        return

    if "распродажа" in text:
        send_catalog_tag(chat_id, "🔥 Распродажа", "распродажа")
        return

    handle_start(chat_id)


def handle_callback(update):
    callback = update.get("callback", {})
    payload = (callback.get("payload") or "").strip().lower()

    chat_id = update.get("chat_id")
    if not chat_id:
        chat_id = update.get("message", {}).get("recipient", {}).get("chat_id")

    if not chat_id:
        return

    if payload == "каталог":
        handle_catalog(chat_id)
        return

    if payload == "адрес":
        send_message(chat_id, ADDRESSES_TEXT, buttons=build_main_buttons())
        return

    if payload == "назад":
        handle_start(chat_id)
        return

    if payload == "платье":
        send_catalog_tag(chat_id, "👗 Платья", "платье")
        return

    if payload == "джинсы":
        send_catalog_tag(chat_id, "👖 Джинсы", "джинсы")
        return

    if payload == "верхняя":
        send_catalog_tag(chat_id, "🧥 Верхняя одежда", "верхняя")
        return

    if payload == "футболка":
        send_catalog_tag(chat_id, "👕 Футболки", "футболка")
        return

    if payload == "блуза":
        send_catalog_tag(chat_id, "👚 Блузы", "блуза")
        return

    if payload == "юбка":
        send_catalog_tag(chat_id, "👗 Юбки", "юбка")
        return

    if payload == "аксессуары":
        send_catalog_tag(chat_id, "👜 Аксессуары", "аксессуары")
        return

    if payload == "новинка":
        send_catalog_tag(chat_id, "✨ Новинки", "новинка")
        return

    if payload == "распродажа":
        send_catalog_tag(chat_id, "🔥 Распродажа", "распродажа")
        return

    handle_start(chat_id)


def process_update(update):
    update_type = update.get("update_type")

    if update_type == "bot_started":
        chat_id = update.get("chat_id")
        if chat_id:
            handle_start(chat_id)
        return

    if update_type == "message_callback":
        handle_callback(update)
        return

    if update_type == "message_created":
        message = update.get("message", {})
        recipient = message.get("recipient", {})
        chat_id = recipient.get("chat_id")
        text = message.get("body", {}).get("text", "")

        if chat_id:
            handle_message(chat_id, text)