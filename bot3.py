import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytgcalls import PyTgCalls

# بياناتك (يجب وضعها هنا)
API_ID = 33844027
API_HASH = "67f0b1f44e20beee3a94169998bfa00b"
BOT_TOKEN = "8866205672:AAF98UCdTQMysf9i85xHDKaJ6ZBbJm1jiQ0"

app_bot = Client("my_controller_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# قائمة الأزرار
@app_bot.on_message(filters.command("start"))
async def start(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📞 انضمام لاتصال", callback_data="join_call")],
        [InlineKeyboardButton("🚪 خروج من الاتصال", callback_data="leave_call")]
    ])
    await message.reply("مرحباً! استخدم الأزرار للتحكم بالحسابات:", reply_markup=buttons)

# معالجة الضغط على الأزرار
@app_bot.on_callback_query()
async def callback_handler(client, query):
    if query.data == "join_call":
        await query.message.reply("أرسل رابط المكالمة أو الكروب الآن:")
        # البوت ينتظر الرسالة القادمة من المستخدم
        
    elif query.data == "leave_call":
        await query.message.reply("جاري الخروج من الاتصال في جميع الحسابات...")
        # هنا يتم تنفيذ كود الخروج

# دالة الانضمام (عندما ترسل الرابط)
@app_bot.on_message(filters.text & ~filters.command("start"))
async def handle_link(client, message):
    link = message.text
    sessions = [f.replace(".session", "") for f in os.listdir() if f.endswith(".session")]
    
    await message.reply(f"جاري الانضمام للرابط عبر {len(sessions)} حساباً...")
    
    for session_name in sessions:
        if session_name == "my_controller_bot": continue
        try:
            acc = Client(session_name, api_id=API_ID, api_hash=API_HASH)
            await acc.start()
            # الانضمام للمجموعة ثم الاتصال
            await acc.join_chat(link)
            # دمج PyTgCalls للانضمام للاتصال الفعلي
            call = PyTgCalls(acc)
            await call.start()
            await call.join_group_call(link)
            await message.reply(f"الحساب {session_name} انضم بنجاح!")
        except Exception as e:
            await message.reply(f"فشل {session_name}: {e}")

app_bot.run()
