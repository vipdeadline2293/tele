import os
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle

# خادم ويب لإبقاء البوت يعمل 24/7 على Render
app = Flask(__name__)

@app.route('/')
def home(): 
    return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# جلب البيانات من إعدادات الموقع (Environment Variables)
API_ID = int(os.environ.get("33844027"))
API_HASH = os.environ.get("67f0b1f44e20beee3a94169998bfa00b")
BOT_TOKEN = os.environ.get("8866205672:AAF98UCdTQMysf9i85xHDKaJ6ZBbJm1jiQ0")
SESSION_STRING = os.environ.get("BQDFycsAZXcAfn9TznHOp70qUTMeBp6wjFZGFWSwO1bRQ9mKpBVh3wiOuKqE_ZD8scOhCOpeLaNi9bIQ4KYMD4FNoQqzeJCFf3AeVr4fbi0_NoCa6vnZ2ARqq2kLjr9Sm_pPHAQGQLP4pwcqfK9VlGS92Hu685fFPsIs_cCINoDEYw_sI4iznY4iKlOm_Jdlg1MF9exEEl9EEE6Y6TXa5VE88gUEk15pWT_mO5Mfqngoo-lpxlvSF886Tga_c8fnveDAyKk98PBqoEY4r8As-PbyM6tPuyPiZH482jIF3DKi8PWAJxGtcNdrFjbqKnSI2szHU_LwuuEnMqeSHqxbI-54OC1eZAAAAAGXQc5kAA")

# تهيئة البوت والحساب
app_bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_acc = Client("user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# --- إضافة الأوامر ---

@app_bot.on_message(filters.command("ping"))
async def ping_handler(client, message):
    await message.reply("البوت يعمل بكفاءة! 🚀")

@app_bot.on_message(filters.command("join") & filters.private)
async def join_chat(client, message):
    # الصيغة: /join رابط_القناة_أو_المعرف
    if len(message.command) < 2:
        await message.reply("يرجى إرسال الرابط بعد الأمر. مثال: /join @username")
        return
    
    chat_link = message.command[1]
    try:
        await user_acc.join_chat(chat_link)
        await message.reply(f"تم الانضمام بنجاح إلى: {chat_link}")
    except Exception as e:
        await message.reply(f"حدث خطأ: {e}")

# --- التشغيل ---

async def main():
    Thread(target=run_web).start()
    await app_bot.start()
    await user_acc.start()
    print("البوت يعمل الآن!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
