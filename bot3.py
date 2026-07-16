import sqlite3
import threading
from flask import Flask
from pyrogram import Client, filters
from tgcalls import GroupCallFactory

# --- الإعدادات ---
API_ID = 33844027
API_HASH = "67f0b1f44e20beee3a94169998bfa00b"
BOT_TOKEN = "8886784654:AAHzwFJkWgIJhFsWhpWgHJt-mwSzzbYiHeQ"

# --- خادم الويب ---
app_web = Flask(__name__)
@app_web.route('/')
def home(): return "Bot is alive!"
threading.Thread(target=lambda: app_web.run(host="0.0.0.0", port=8080)).start()

# --- قاعدة البيانات ---
conn = sqlite3.connect("accounts.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, session_string TEXT)")
conn.commit()

# --- إعداد البوت ---
app = Client("manager_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("join_vc"))
async def join_vc(client, message):
    if len(message.command) < 2:
        await message.reply("استخدم: /join_vc [رابط المجموعة]")
        return
    
    chat_link = message.command[1]
    accounts = cursor.execute("SELECT session_string FROM accounts").fetchall()
    
    if not accounts:
        await message.reply("لا توجد حسابات!")
        return

    for acc in accounts:
        try:
            # استخدام Session String في Pyrogram
            user = Client(f"session_{acc[0][:5]}", session_string=acc[0], api_id=API_ID, api_hash=API_HASH)
            await user.start()
            
            # تهيئة tgcalls القديمة
            factory = GroupCallFactory(user)
            group_call = factory.get_group_call()
            await group_call.join(chat_link)
            
            await message.reply(f"✅ تم الانضمام بالحساب {acc[0][:5]}...")
        except Exception as e:
            await message.reply(f"❌ خطأ: {str(e)}")

app.run()
