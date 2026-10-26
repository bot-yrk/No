import random
import string
import time
import os
import asyncio
from flask import Flask
from telethon import TelegramClient, events
from telethon.tl.functions.account import CheckUsernameRequest
from telethon.errors import FloodWaitError, UsernameOccupiedError, UsernameInvalidError

# ==================== التهيئات والأساسيات ====================
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER", "")
CHAT_ID = int(os.environ.get("CHAT_ID", "0"))

client = TelegramClient('shadow_session', API_ID, API_HASH)
is_hunting = False

# ==================== سيرفر الويب لـ Render ====================
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Shadow Userbot System: Online & Active", 200

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, use_reloader=False)

# ==================== توليد الأنماط (رباعي وخماسي مع شرطة) ====================
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

# ==================== محرك الصيد المباشر ====================
async def check_and_hunt():
    global is_hunting
    print("⚔️ تم تفعيل محرك الصيد المباشر...")
    
    while is_hunting:
        username = generate_username()
        try:
            result = await client(CheckUsernameRequest(username=username))
            if result:
                msg = f"🎯 **صيد مؤكد ومتاح رسمياً!**\n\n🔹 **اليوزر:** `@{username}`\n📏 **الطول:** {len(username)}\n⚡ **الحالة:** جاهز للحجز الفوري"
                await client.send_message(CHAT_ID, msg)
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
            
        await asyncio.sleep(random.uniform(4.0, 7.0))

# ==================== تشغيل البوت ====================
async def main_loop():
    if not client.is_connected():
        await client.start(phone=PHONE_NUMBER)
    
    print("Userbot is running successfully!")

    @client.on(events.NewMessage(pattern='/hunt'))
    async def start_handler(event):
        global is_hunting
        if event.sender_id == CHAT_ID:
            if not is_hunting:
                is_hunting = True
                asyncio.create_task(check_and_hunt())
                await event.respond("🚀 تم إطلاق محرك الصيد بنجاح.")
            else:
                await event.respond("⚠️ المحرك يعمل بالفعل.")

    @client.on(events.NewMessage(pattern='/stop'))
    async def stop_handler(event):
        global is_hunting
        is_hunting = False
        await event.respond("🛑 تم إيقاف عملية الصيد.")

    await client.run_until_disconnected()

if __name__ == "__main__":
    import threading
    # تشغيل سيرفر الويب في خلفية مستقلة تماماً
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # تشغيل اليوزربوت في الحلقة الرئيسية
    with client:
        client.loop.run_until_complete(main_loop())
