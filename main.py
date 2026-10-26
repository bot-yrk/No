import random
import string
import time
import os
import threading
import requests
import telebot
from flask import Flask

# ==================== التهيئات والتهيئات الأجهزة ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8611579779:AAEXVTGW7pIIwv5wA1FbLUzcWuD9smPWH80")
CHAT_ID = os.environ.get("CHAT_ID", "8487652113")  # معرف حسابك المستهدف لاستلام الصيد

bot = telebot.TeleBot(BOT_TOKEN)
is_hunting = False

# سيرفر خفيف للبقاء نشطاً على Render (Health check)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Shadow Engineer System: Online & Active", 200

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# ==================== خوارزمية التوليد الأنماط ====================
def generate_username():
    """
    توليد يوزر رباعي أو خماسي يحتوي على شرطة (-) في مكان عشوائي.
    أمثلة: a-8k, 9x-m, x-98q, 1b2-z
    """
    length = random.choice([4, 5]) # رباعي أو خماسي
    chars = string.ascii_lowercase + string.digits # أحرف وأرقام
    
    # اختيار مكان الشرطة بحيث لا تكون في البداية أو النهاية لتكون متوافقة
    dash_position = random.randint(1, length - 2)
    
    result = []
    for i in range(length):
        if i == dash_position:
            result.append('-')
        else:
            result.append(random.choice(chars))
            
    return "".join(result)

# ==================== آلية الفحص والصيد ====================
def check_username(username):
    """
    فحص توفر اسم المستخدم من خلال واجهة Telegram الرسمية
    """
    url = f"https://t.me/{username}"
    try:
        response = requests.get(url, timeout=5)
        # إذا كانت الصفحة لا تحتوي على زر الفتح فغالباً اليوزر متاح
        if "tgme_action_button_new" not in response.text and "Preview channel" not in response.text:
            return True
    except Exception as e:
        print(f"Error checking {username}: {e}")
    return False

def hunter_loop():
    global is_hunting
    bot.send_message(CHAT_ID, "⚔️ **بدأت عملية الصيد في الظل...**\nجارٍ فحص اليوزرات الرباعية والخماسية مع الشرطة (-)")
    
    while is_hunting:
        user = generate_username()
        is_available = check_username(user)
        
        if is_available:
            msg = f"🎯 **تم صيد يوزر متاح!**\n\n🔹 **اليوزر:** `@{user}`\n📏 **الطول:** {len(user)}\n⚡ **الحالة:** متاح للإنشاء"
            print(f"[SUCCESS] Found available username: @{user}")
            bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
        
        # فاصل أمني مدروس لحماية السيرفر والبوت من الحظر (بين 2 إلى 4 ثوانٍ)
        time.sleep(random.uniform(2.5, 4.0))

# ==================== أوامر البوت ====================
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "👋 **مرحباً بك يا سيد الظل**\n\nالأوامر المتاحة:\n/hunt - بدء عملية الصيد والتوليد\n/stop - إيقاف العملية مؤقتاً\n/status - فحص حالة النظام")

@bot.message_handler(commands=['hunt'])
def start_hunt(message):
    global is_hunting
    if not is_hunting:
        is_hunting = True
        threading.Thread(target=hunter_loop, daemon=True).start()
        bot.reply_to(message, "🚀 تم إطلاق محرك الصيد بنجاح.")
    else:
        bot.reply_to(message, "⚠️ محرك الصيد يعمل بالفعل في الخلفية!")

@bot.message_handler(commands=['stop'])
def stop_hunt(message):
    global is_hunting
    is_hunting = False
    bot.reply_to(message, "🛑 تم إيقاف عملية الصيد.")

@bot.message_handler(commands=['status'])
def status_cmd(message):
    state = "شغال 🟢" if is_hunting else "متوقف 🔴"
    bot.reply_to(message, f"📊 **حالة النظام:** {state}")

# ==================== التشغيل الرئيسي ====================
if __name__ == "__main__":
    # تشغيل سيرفر الويب في المسار الخفي
    threading.Thread(target=run_web_server, daemon=True).start()
    
    print("Bot is alive and listening for commands...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
