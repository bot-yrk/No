import os
import random
import string
import asyncio
from flask import Flask

# ==================== إعدادات سيرفر الويب الأساسي ====================
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Shadow System: Online & Active 🟢", 200

# تشغيل خادم الويب مباشرة في الخيط الرئيسي لترضي منصة Render وتبقى الخدمة Live دائماً
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
