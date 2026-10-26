import random
import string
import time
import os
import asyncio
import threading
import telebot
from flask import Flask
from telethon import TelegramClient
from telethon.tl.functions.account import CheckUsernameRequest
from telethon.errors import FloodWaitError, UsernameOccupiedError, UsernameInvalidError

# ==================== التهيئات والأساسيات ====================
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = int(os.environ.get("CHAT_ID", "0"))

client = TelegramClient('shadow_session', API_ID, API_HASH)
bot = telebot.TeleBot(BOT_TOKEN)

is_hunting = False

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Shadow System: Online & Active", 200

def generate_username():
    length = random.choice([4, 5])
    chars = string.ascii_lowercase + string.digits
    dash_position = random.randint(1, length - 2)
    
    result = []
    for i in range(length):
        if i == dash_position:
            result.append('-')
        else:
            result.append(random.choice(chars))
            
    return "".join(result)

async def check_and_hunt():
    global is_hunting
    bot.send_message(CHAT_ID, "⚔️ **تم تفعيل محرك الصيد!**\nجارٍ فحص اليوزرات الآن...")
    
    while is_hunting:
        username = generate_username()
        try:
            # طباعة اليوزر في السجلات لترى أنه يبحث بدون توقف
            print(f"[CHECKING] Testing username: @{username}")
            
            result = await client(CheckUsernameRequest(username=username))
            if result:
                msg = f"🎯 **صيد مؤكد ومتاح رسمياً!**\n\n🔹 **اليوزر:** `@{username}`\n📏 **الطول:** {len(username)}\n⚡ **الحالة:** جاهز للحجز الفوري"
                bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                print(f"[SUCCESS] Available username found: @{username}")
                
        except UsernameOccupiedError:
            pass
        except UsernameInvalidError:
            pass
        except FloodWaitError as e:
            print(f"⚠️ حظر مؤقت، الانتظار لمدة {e.seconds} ثانية...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"خطأ: {e}")
            
        # تقليل الفاصل الزمني قليلاً لزيادة سرعة الصيد
        await asyncio.sleep(random.uniform(2.0, 4.0))

def run_async_hunter():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def main():
        if not client.is_connected():
            await client.start(phone=PHONE_NUMBER)
        print("Userbot connected successfully!")
        
        while True:
            if is_hunting:
                await check_and_hunt()
            await asyncio.sleep(1)
            
    loop.run_until_complete(main())

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "👋 أهلاً بك يا سيد الظل.\nأرسل /hunt لبدء الصيد، أو /stop للإيقاف.")

@bot.message_handler(commands=['hunt'])
def hunt_cmd(message):
    global is_hunting
    if not is_hunting:
        is_hunting = True
        bot.reply_to(message, "🚀 تم إعطاء أمر البدء، جارٍ تشغيل المحرك...")
    else:
        bot.reply_to(message, "⚠️ المحرك يعمل بالفعل.")

@bot.message_handler(commands=['stop'])
def stop_cmd(message):
    global is_hunting
    is_hunting = False
    bot.reply_to(message, "🛑 تم إيقاف عملية الصيد.")

if __name__ == "__main__":
    threading.Thread(target=run_async_hunter, daemon=True).start()
    threading.Thread(target=lambda: bot.infinity_polling(timeout=10, long_polling_timeout=5), daemon=True).start()
    
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
