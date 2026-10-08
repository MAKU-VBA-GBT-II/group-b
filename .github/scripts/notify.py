import os
import json
import requests

event_path = os.environ.get("GITHUB_EVENT_PATH")
with open(event_path, "r", encoding="utf-8") as f:
    event = json.load(f)

issue = event.get("issue", {})
number = issue.get("number", "0")
title = issue.get("title", "Başlıksız")
body = issue.get("body") or "Açıklama yok."
html_url = issue.get("html_url", "")
labels = ", ".join([l["name"] for l in issue.get("labels", [])]) or "Etiket yok"

message = (
    f"📌 Yeni Görev / Issue Geldi!\n\n"
    f"• Numara: #{number}\n"
    f"• Başlık: {title}\n"
    f"• Etiketler: {labels}\n"
    f"• Link: {html_url}\n\n"
    f"📝 Açıklama:\n{body}"
)

bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

if not bot_token or not chat_id:
    raise ValueError(f"HATA: Secret'lar okunamadı! TOKEN: {bool(bot_token)}, CHAT_ID: {bool(chat_id)}")

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
response = requests.post(url, json={"chat_id": chat_id, "text": message})

print(f"Telegram Durum Kodu: {response.status_code}")
print(f"Telegram Cevabı: {response.text}")

if response.status_code != 200:
    raise Exception(f"Mesaj iletilemedi: {response.text}")

print("✅ Bildirim başarıyla iletildi.")
