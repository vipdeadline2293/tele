from pyrogram import Client, filters
import sqlite3

# إعداد البيانات الخاصة بك
API_ID = 33844027
API_HASH = "67f0b1f44e20beee3a94169998bfa00b"
BOT_TOKEN = "8866205672:AAF98UCdTQMysf9i85xHDKaJ6ZBbJm1jiQ0"

# تهيئة البوت
app = Client("manager_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# إعداد قاعدة البيانات لحفظ الحسابات
conn = sqlite3.connect("accounts.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS accounts (session_string TEXT)")
conn.commit()

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("مرحباً بك في لوحة تحكم الحسابات.\nأرسل الـ Session String لإضافة حساب جديد.")

@app.on_message(filters.text & ~filters.command(["start"]))
async def handle_input(client, message):
    # افتراض أن الرسالة هي الـ Session String
    if len(message.text) > 50: # التحقق من طول الـ Session
        cursor.execute("INSERT INTO accounts VALUES (?)", (message.text,))
        conn.commit()
        await message.reply("✅ تم حفظ الحساب بنجاح.")
    else:
        await message.reply("⚠️ يرجى التأكد من إرسال Session String صحيح.")

app.run()
