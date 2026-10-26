import random
import string
import time
import os
import asyncio
from flask import Flask
from telethon import TelegramClient, events
from telethon.functions.account import CheckUsernameRequest
from telethon.errors import FloodWaitError, UsernameOccupiedError, UsernameInvalidError

# ==================== التهيئات والأساسيات ====================
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = int(os.environ.get("CHAT_ID", "0"))

# استخدام جلسة للـ Userbot
client = TelegramClient('shadow_session', API_ID, API_HASH)

is_hunting = False

# سيرفر خفيف للبقاء نشطاً على Render
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Shadow Userbot System: Online & Active", 200

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

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

# ==================== محرك الصيد الدقيق والمحكم ====================
async def check_and_hunt():
    global is_hunting
    print("⚔️ تم تفعيل محرك الفحص الحقيقي والمطور...")
    
    while is_hunting:
        username = generate_username()
        try:
            # فحص إضافي للتأكد من طول النمط والشروط
            if len(username) < 4:
                continue

            # استعلام الفحص الرسمي المباشر من سيرفرات تيليجرام
            result = await client(CheckUsernameRequest(username=username))
            
            # إذا أرجع النظام True، فهذا يعني أن اليوزر غير مأخوذ ومتاح تماماً 100%
            if result:
                msg = f"🎯 **صيد مؤكد ومتاح رسمياً!**\n\n🔹 **اليوزر:** `@{username}`\n📏 **الطول:** {len(username)}\n⚡ **الحالة:** جاهز للحجز الفوري"
                await client.send_message(CHAT_ID, msg)
                print(f"[SUCCESS] Found 100% available username: @{username}")
                
        except UsernameOccupiedError:
            # اليوزر مأخوذ بالفعل (نتجاهله بصمت)
            pass
        except UsernameInvalidError:
            # يوزر مخالف للقواعد أو غير صالح
            pass
        except FloodWaitError as e:
            # نظام الحماية من السبام، سننتظر الفترة المطلوبة بدقة
            print(f"⚠️ حظر مؤقت من تيليجرام. جاري الانتظار لمدة {e.seconds} ثانية...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"خطأ أثناء فحص اليوزر {username}: {e}")
            
        # فاصل زمني مدروس بين كل محاولة وأخرى لضمان الأمان وعدم كشف السكربت
        await asyncio.sleep(random.uniform(4.0, 7.0))

# ==================== استقبال الأوامر والتشغيل ====================
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
                await event.respond("🚀 تم إطلاق محرك الصيد المطور بنجاح.")
            else:
                await event.respond("⚠️ المحرك يعمل بالفعل في الخلفية.")

    @client.on(events.NewMessage(pattern='/stop'))
    async def stop_handler(event):
        global is_hunting
        if event.sender_id == CHAT_ID:
            is_hunting = False
            await event.respond("🛑 تم إيقاف عملية الصيد.")

    await client.run_until_disconnected()

if __name__ == "__main__":
    import threading
    # تشغيل سيرفر الويب لضمان استمرار عمل Render
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # تشغيل اليوزربوت
    with client:
        client.loop.run_until_complete(main_loop())
