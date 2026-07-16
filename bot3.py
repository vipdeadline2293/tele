import sqlite3
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from pytgcalls import PyTgCalls
from pytgcalls.types import GroupCall

# --- 1. الإعدادات ---
API_ID = 33844027
API_HASH = "67f0b1f44e20beee3a94169998bfa00b"
BOT_TOKEN = "8866205672:AAF98UCdTQMysf9i85xHDKaJ6ZBbJm1jiQ0"

# --- 2. خادم الويب (للحفاظ على البوت يعمل) ---
app_web = Flask(__name__)
@app_web.route('/')
def home(): return "Bot is running!"

def run_web():
    app_web.run(host="0.0.0.0", port=8080)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect("accounts.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, session_string TEXT)")
conn.commit()

# --- 4. البوت ---
app = Client("manager_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("أهلاً بك! أرسل الـ Session String لإضافة حساب جديد.")

@app.on_message(filters.text & ~filters.command(["start", "list", "join_vc", "leave_vc", "del"]))
async def add_acc(client, message):
    if len(message.text) > 50:
        cursor.execute("INSERT INTO accounts (session_string) VALUES (?)", (message.text,))
        conn.commit()
        await message.reply("✅ تم حفظ الحساب بنجاح.")
    else:
        await message.reply("⚠️ يرجى إرسال Session String صحيح.")

@app.on_message(filters.command("list"))
async def list_acc(client, message):
    rows = cursor.execute("SELECT id, session_string FROM accounts").fetchall()
    if not rows:
        await message.reply("القائمة فارغة.")
        return
    text = "\n".join([f"{r[0]}: {r[1][:15]}..." for r in rows])
    await message.reply(f"الحسابات المسجلة:\n{text}")

@app.on_message(filters.command("del"))
async def del_acc(client, message):
    if len(message.command) > 1:
        cursor.execute("DELETE FROM accounts WHERE id=?", (message.command[1],))
        conn.commit()
        await message.reply("✅ تم الحذف.")

@app.on_message(filters.command("join_vc"))
async def join_vc(client, message):
    if len(message.command) < 2:
        await message.reply("استخدم: /join_vc [الرابط]")
        return
    
    chat_link = message.command[1]
    accounts = cursor.execute("SELECT session_string FROM accounts").fetchall()
    await message.reply(f"جاري محاولة الانضمام لـ {len(accounts)} حساب...")
    
    for acc in accounts:
        try:
            user = Client("temp", session_string=acc[0], api_id=API_ID, api_hash=API_HASH)
            await user.start()
            vc = PyTgCalls(user)
            await vc.start()
            await vc.join_group_call(chat_link, GroupCall())
            await user.stop()
        except Exception as e:
            await message.reply(f"خطأ: {e}")
    await message.reply("✅ انتهت العملية.")

@app.on_message(filters.command("leave_vc"))
async def leave_vc(client, message):
    await message.reply("تم استلام أمر المغادرة.")

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    app.run()
