import os
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls

# خادم ويب لإبقاء البوت يعمل 24/7 على Render
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# جلب البيانات من إعدادات الموقع (Environment Variables)
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SESSION_STRING = os.environ.get("SESSION_STRING")

# تهيئة البوت
app_bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_acc = Client("user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

async def main():
    Thread(target=run_web).start()
    await app_bot.start()
    await user_acc.start()
    print("البوت يعمل الآن!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())