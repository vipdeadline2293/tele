import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from telethon import TelegramClient
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

# الإعدادات الأساسية
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = Flask(__name__)

# خادم ويب بسيط لإبقاء البوت قيد التشغيل على Render
@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# إدارة المهام
active_clients = {}

async def sender_task(client, group, message, interval):
    while True:
        try:
            await client.send_message(group, message)
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(interval * 60)

@dp.message(F.text.startswith("/add"))
async def add_account(message: types.Message):
    # استخدام كود الجلسة (StringSession) المضاف في المتغيرات
    # أو يمكنك تطويره ليطلب من المستخدم إدخال كود الجلسة عبر المحادثة
    await message.reply("تم تفعيل النظام. الحسابات تعمل عبر الجلسات المخزنة.")

@dp.message(F.text.startswith("/start"))
async def start_spam(message: types.Message):
    # مثال: /start group_username 5 message_text
    args = message.text.split(maxsplit=3)
    group, interval, text = args[1], int(args[2]), args[3]
    
    # هنا يتم استخدام الحساب الرئيسي أو الحسابات المضافة
    client = TelegramClient(StringSession(os.environ.get("SESSION_STRING")), API_ID, API_HASH)
    await client.start()
    asyncio.create_task(sender_task(client, group, text, interval))
    await message.reply("بدأت عملية النشر.")

async def main():
    Thread(target=run_web).start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
