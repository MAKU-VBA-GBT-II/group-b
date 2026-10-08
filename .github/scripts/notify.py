import os
import json
import requests

with open(os.environ["GITHUB_EVENT_PATH"]) as f:
    event = json.load(f)

issue = event["issue"]
number = issue["number"]
title = issue["title"]
body = issue.get("body") or "Açık yok."
labels = ", ".join([l["name"] for l in issue.get("labels", [])])

message = (
    f"📌 *Görev geldi!*\n"
    f"• Issue: #{number}\n"
    f"• Başlık: {title}\n"
    f"• İçerik: {body}\n"
    f"• Etiket: {labels}"
)

bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]
requests.post(
    f"https://api.telegram.org/bot{bot_token}/sendMessage",
    json={"chat_id": chat_id, "text": message}
)
print("✅ Bildirim gönderildi.")
