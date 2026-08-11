import sys
import subprocess

def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"[+] Installing {package}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package
        ])

install_package("instagrapi")

import time
import random
import threading
import os
import json
import re
from instagrapi import Client
# ================= ACCOUNT SETTINGS =================
USERNAME = "igqve"
PASSWORD = "273209Ansh"
OWNER    = "ig1vx"   # Main Owner Username

cl = Client()
SESSION_FILE = "session.json"
ADMINS_FILE  = "admins.json"
ECONOMY_FILE = "economy.json"

# Persistent Login
print("⚙️ Initializing Instagram Login...")
try:
    if os.path.exists(SESSION_FILE):
        cl.load_settings(SESSION_FILE)
        cl.login(USERNAME, PASSWORD)
    else:
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
except Exception as e:
    print("⚠️ Login Error / 2FA Required:", e)
    code = input("Enter 2FA Code: ")
    cl.login(USERNAME, PASSWORD, verification_code=code)
    cl.dump_settings(SESSION_FILE)

BOT_ID = str(cl.user_id)
try:
    OWNER_ID = str(cl.user_id_from_username(OWNER))
except Exception:
    OWNER_ID = BOT_ID

START_TIME = time.time()

# ================= ADMIN & PERSISTENCE DATA =================
ADMINS = set([OWNER_ID])
slide_targets = set()

# State Management
processed     = set()
spam_flag     = {}
gc_flag       = {}
economy_data  = {}  # { user_id: { "bal": 1000, "last_daily": 0, "last_kill": 0, "protected_until": 0, "dead_until": 0 } }

def load_json_file(file_path, default):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Error loading {file_path}]:", e)
    return default

def save_json_file(file_path, data):
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"[Error saving {file_path}]:", e)

def load_admins():
    global ADMINS
    data = load_json_file(ADMINS_FILE, [])
    ADMINS.update(data)

def save_admins():
    save_json_file(ADMINS_FILE, list(ADMINS))

def load_economy():
    global economy_data
    economy_data = load_json_file(ECONOMY_FILE, {})

def save_economy():
    save_json_file(ECONOMY_FILE, economy_data)

load_admins()
load_economy()

# ================= ECONOMY HELPER FUNCTIONS =================
def get_user_acc(uid):
    uid = str(uid)
    if uid not in economy_data:
        economy_data[uid] = {
            "bal": 1000,  # Starting balance
            "last_daily": 0,
            "last_kill": 0,
            "protected_until": 0,
            "dead_until": 0
        }
        save_economy()
    return economy_data[uid]

def add_bal(uid, amount):
    acc = get_user_acc(uid)
    acc["bal"] = max(0, acc["bal"] + amount)
    save_economy()

# ================= INSTAGRAM FIRE EFFECT HELPER =================
def send_fire(tid, text):
    """Sends native Instagram Fire Effect message using raw API Payload"""
    try:
        cl.private_request(
            f"direct_v2/threads/broadcast/text/",
            data={
                "thread_ids": f"[{tid}]",
                "text": text,
                "power_up_type": "1",  # 1 = FIRE EFFECT
                "item_type": "power_up",
                "client_context": cl.generate_client_context()
            }
        )
    except Exception:
        try:
            cl.direct_send(text, thread_ids=[str(tid)])
        except Exception as ex:
            print("[Send Error]:", ex)

# ================= AUTOMATIC SLIDE MESSAGES LIST (25+ TEXTS) =================
SLIDE_RESPONSES = [
     "NAME 𝙆𝙊 𝙋𝙀𝙇𝙏𝙀 𝙃𝙐𝙀 𝙀𝙉𝙏𝙍𝙔 ???? 🤣😎❤️‍🔥",
    "NAME 𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐊𝐈 ̷C̷H̷U̷T̷ 𝙈𝙀 𝐋𝐎𝐔𝐃𝐀 ̷M̷A̷D̷A̷R̷C̷H̷O̷D̷ ???? 😂🩷🤚🏼",
    "NAME 𝙍𝙀𝙋𝙇𝙔 𝐊𝐀𝐑 𝙂𝘼𝙍𝙄𝘽 𝐃𝐀𝐑 𝙆𝙔𝙐 𝐑𝐀𝐇𝐀 𝐇 ???? 😁🤙🏼🤍",
    "NAME 𝐂𝐇𝐀𝐋 𝙏𝙀𝙍𝐈 𝐌𝐀 ̷C̷H̷O̷D̷U̷ 𝙋𝘼𝙏𝘼𝐊 𝐏𝐀𝐓𝐀𝐊 𝙆𝐄 ???? 🤪👻🩶",
    "NAME ̷C̷H̷U̷D̷K̷E̷ 𝙎𝙋𝘼𝙈 𝐘𝐀𝐇𝐈 𝘼𝙐𝙆𝘼𝙏 𝐇 𝙏𝙀𝙍𝐈 𝐆𝐀𝐑𝐈𝘽 ???? 😹🩵🙌🏼",
    "𝐂𝐏 𝐊𝐀𝐑 NAME 𝙂𝘼𝙍𝙄𝘽 𝐁𝐇𝐀𝐀𝐆 𝙈𝘼𝙏 𝐂𝐇𝐎𝐓𝐄𝐘 ???? 😂🩶🤚🏼",
    "NAME 𝐊𝐈 𝙈𝙐𝙈𝙈𝙔 𝐊𝐎 ̷R̷A̷N̷D̷I̷ 𝘽𝘼𝙉𝘼 𝘿𝙐𝙉𝙂𝘼 𝙃𝙀𝙃𝙀𝙃𝙀 ???? 🤣💖✌🏼",
    "NAME 𝐊𝐄 𝐁𝐀𝐀𝐏 𝙈𝘼𝙁𝙄𝘼 𝐘𝐄𝐇 𝐇𝐀𝐈 𝐈𝐍𝐊𝐈 𝐌𝐀𝐀 𝐊𝐄 𝐘𝐀𝐀𝐑 ???? 😆🩶🤚🏼",
    "𝐊𝐀𝐁𝐀𝐃𝐈 𝙒𝘼𝙇𝙀 NAME 𝐊𝐈 𝙈𝙆𝘽 ???? 🤣👻💗",
    "𝐀𝐑𝐄𝐘 NAME 𝐊𝐈 𝙈𝙆𝘽 𝙔𝘼𝘼𝐑 𝐁𝐇𝐀𝐆 𝙆𝘼𝙄𝙎𝙀 𝐑𝐇𝐄 𝐇𝐎 𝙂𝘼𝙍𝙄𝘽𝙊 ???? 😤👻💞",
    "𝘼𝙍𝙀𝙔 NAME 𝙈𝘼𝘾𝘾𝙃𝙃𝘼𝙍 𝙏𝙈𝙆𝘾 ???? 😂🩷✌🏾",
    "NAME 𝙏𝙐 𝙇𝘼𝘿𝙃𝙀𝙂𝘼 𝙃𝙐𝙈𝙎𝙀 𝙏𝙀𝙍𝙄 𝙈𝘼 𝘾𝙊𝘿𝙆𝙀 𝙈𝙄𝙏𝙏𝙄 𝙈𝙀 𝙈𝙄𝙇𝘼𝘿𝙀𝙉𝙂𝙀 𝙃𝙐𝙈 ???? 😂🔥🤸🏻",
    "NAME 𝙇𝙀𝘼𝙑𝙀 𝙇𝙀 𝙏𝙐 𝙍𝙉𝘿𝙔𝙆𝙀 𝙋𝘼𝙎𝘼𝙉𝘿 𝙉𝘼𝙄 𝘼𝙔𝘼 𝙈𝙍𝙆𝙊 ???? 😏👋🏼",
    "NAME 𝙂𝙍𝙄𝘽 𝙈𝘼 𝙆 𝘽𝘼𝘾𝙃𝙔 𝙂𝙃𝘼𝙍 𝙈𝙀 𝘼𝙏𝙏𝘼 𝙇𝙀 𝘼𝘼 ???? 😂🥲",
    "NAME 𝘼𝙐𝙍𝘼𝙏𝙊 𝙆𝘼 𝙆𝘼𝙈 𝙍𝙊𝙏𝙄 𝘽𝙉𝘼𝙉𝘼 𝙃𝙊𝙏𝘼 𝙃 𝙏𝙊 NAME 𝙆𝙄 𝙈𝘼 𝙔𝘼𝙃𝘼 𝙆𝙔𝙐 𝘾𝙃𝙐𝘿𝙍𝙃𝙄 ???? 🤬🤣😭",
    "NAME 𝙏𝙀𝙍𝙄 𝙈𝘼 𝙆𝙊 𝙎𝙀𝙉𝘼𝙋𝘼𝙏𝙄 𝙎𝙀 𝘾𝙃𝙐𝘿𝙒𝘼𝘿𝙀𝙉𝙂𝙀 ???? 🪖🖲️🔥",
    "NAME 𝙏𝙍𝙔 𝙂𝙉𝘿 𝙈𝙀 𝘼𝙀𝙎𝘼 𝘽𝙃𝘼𝙇𝘼 𝙈𝘼𝙍𝙐𝙂𝘼 𝙎𝙄𝘿𝙃𝘼 𝙈𝙊𝙐𝙉𝙏 𝙀𝙑𝙀𝙍𝙀𝙎𝙏 𝙋𝙀 𝙍𝙐𝙆𝙀𝙂𝘼 ???? 💯🚀💔",
    "NAME 𝑻𝑬𝑹𝑰 𝑴𝑨𝑨 ᵀᴬᴷᴸᴵ 𝑯𝑬𝑽𝑬𝑽𝑬 ???? 💖💛💚",
    "NAME 𝙈𝙐𝙅𝙃𝙀 𝙉𝙐𝙈𝘽𝙀𝙍 𝙆𝙄 𝙆𝙔𝘼 𝙕𝘼𝙍𝙐𝙍𝘼𝙏\n𝙈𝘼𝙄 𝙃𝙐 𝙀𝙆 𝙋𝙇𝙐𝙈𝘽𝙀𝙍 👨‍🔧\n𝙅𝘼𝘽 𝘾𝙃𝙊𝘿𝙉𝙀 𝙆𝘼 𝙈𝘼𝙉𝙉 𝙆𝙍𝙀𝙂𝘼 NAME 𝙆𝙄 𝙈𝘼𝘼 𝘾𝙊𝘿 𝘿𝙐𝙉𝙂𝘼 𝙂𝙃𝘼𝙍 ???? 😂🔧",
    "NAME 𝙏𝙀𝙍𝙔 𝙈𝘼𝘼 𝙆𝙊 𝙌𝘼𝘽𝘼𝙍 𝙉𝘼𝙎𝙀𝙀𝘽 𝙉𝘼 𝙃𝙊 𝙍𝙉𝘿𝙔𝙆𝙀 ???? 😑🖕🏽💔",
    "NAME ꪶ 𝗟𝗨𝗡 𝗧𝗘 𝗩𝗔𝗝 ꪻ♡︎ ???? 😂👏🏻✨",
    "NAME 𝙏𝙀𝙍𝙔 𝙉𝘼𝙉𝙄 𝘾𝙃𝙐𝘿 𝙂𝙔𝙄 𝘿𝙃𝘼𝙈 𝘿𝙃𝘼𝙈 𝘿𝙃𝘼𝙈 ???? 🥁🔊😍"
     "⭅╡𝗧𝗠𝗞𝗖╞⭆",
    "⭅╡𝗧𝗕𝗞𝗖╞⭆",
    "⭅╡𝗖𝗛𝗨𝗗╞⭆",
    "⭅╡𝗧𝗕𝗥╞⭆",
    "⭅╡𝗞𝗜𝗗𝗘╞⭆",
    "⭅╡𝗛𝗜𝗝𝗗𝗘╞⭆",
    "⭅╡𝗖𝗛𝗔𝗞𝗞𝗘╞⭆",
    "⭅╡𝗠𝗢𝗧𝗛𝗘𝗥𝗙𝗨𝗖𝗞𝗘𝗥╞⭆",
    "⭅╡𝗕𝗜𝗧𝗖𝗛╞⭆",
    "⭅╡𝗠𝗢𝗠𝗟𝗘𝗦𝗦╞⭆",
    "⭅╡𝗛𝗢𝗠𝗘𝗟𝗘𝗦𝗦╞⭆",
    "⭅╡𝗞𝗔𝗟𝗪𝗘╞⭆",
    "⭅╡𝗪𝗛𝗢𝗥𝗘╞⭆",
    "⭅╡𝗞𝗨𝗧𝗜𝗬𝗔╞⭆",
    "⭅╡𝗦𝗔𝗦𝗨𝗞𝗘 𝗕𝗔𝗔𝗣 𝗛𝗔𝗜╞⭆"
]

AI_RESPONSES = [
    "Haanji bolo! Main Alexa AI hu, kaise help karu? 🤖",
    "Mujhe bulaaya aur main aa gaya! ✨",
    "Main active hu, sab par nazar hai meri 👀",
    "Group me aur bhi log hai unke sath gandmasti kro yaar 😭"
]

# WORKERS
def spam_worker(tid, text):
    while spam_flag.get(tid, False):
        send_fire(tid, text)
        time.sleep(2.5)

def gc_worker(tid, name):
    emojis = ["🔥", "✨", "🚀", "💎", "👑", "⚡"]
    i = 0
    while gc_flag.get(tid, False):
        new_name = f"{name} {emojis[i % len(emojis)]}"
        try:
            cl.direct_thread_update_title(tid, new_name)
        except Exception:
            pass
        i += 1
        time.sleep(6.0)

# ================= COMMAND HANDLERS =================
def cmd_roll(tid): send_fire(tid, f"🎲 Dice Roll Result: {random.randint(1, 6)}")
def cmd_flip_simple(tid): send_fire(tid, f"🪙 Coin Toss: {random.choice(['Heads 🪙', 'Tails 🪙'])}")

def cmd_addadmin(tid, arg, sender):
    if sender != OWNER_ID:
        send_fire(tid, f"🚫 Permission Denied! Only Main Owner (@{OWNER}) can add admins.")
        return
    u = arg.strip().lstrip("@")
    if not u: send_fire(tid, "❌ Use: .addadmin @username"); return
    try:
        uid = str(cl.user_id_from_username(u))
        ADMINS.add(uid)
        save_admins()
        send_fire(tid, f"👑 Added @{u} as Bot Admin!")
    except Exception as e: send_fire(tid, f"❌ Add Admin Failed: {e}")

def cmd_rmvadmin(tid, arg, sender):
    if sender != OWNER_ID:
        send_fire(tid, f"🚫 Permission Denied! Only Main Owner (@{OWNER}) can remove admins.")
        return
    u = arg.strip().lstrip("@")
    if not u: send_fire(tid, "❌ Use: .rmvadmin @username"); return
    try:
        uid = str(cl.user_id_from_username(u))
        if uid in ADMINS:
            ADMINS.remove(uid)
            save_admins()
            send_fire(tid, f"🗑️ Removed @{u} from Admins!")
        else: send_fire(tid, f"❌ @{u} is not an admin!")
    except Exception as e: send_fire(tid, f"❌ Remove Admin Failed: {e}")

def cmd_adminlist(tid):
    msg = "👑 **BOT ADMINS LIST** 👑\n\n"
    msg += f"👑 Owner: @{OWNER}\n"
    for uid in ADMINS:
        if uid != OWNER_ID:
            msg += f"🔹 Admin ID: {uid}\n"
    send_fire(tid, msg)

def cmd_slide(tid, arg):
    u = arg.strip().lstrip("@")
    if not u: send_fire(tid, "❌ Use: .slide @username"); return
    try:
        uid = str(cl.user_id_from_username(u))
        slide_targets.add(uid)
        send_fire(tid, f"🔥 **SLIDE STARTED ON @{u}!** Ab ye jab bhi msg karega auto reply aayega.")
    except Exception as e: send_fire(tid, f"❌ Target Error: {e}")

def cmd_stopslide(tid, arg):
    u = arg.strip().lstrip("@")
    if not u: send_fire(tid, "❌ Use: .stopslide @username"); return
    try:
        uid = str(cl.user_id_from_username(u))
        slide_targets.discard(uid)
        send_fire(tid, f"⏹️ **SLIDE STOPPED FOR @{u}!**")
    except Exception as e: send_fire(tid, f"❌ Target Error: {e}")

def cmd_broadcast(tid, arg, sender):
    if sender not in ADMINS:
        send_fire(tid, "🚫 Permission Denied! Only Admins/Owner can broadcast.")
        return
    if not arg:
        send_fire(tid, "❌ Use: .broadcast <your message>")
        return
    
    send_fire(tid, "📢 Starting Broadcast to all group chats...")
    count = 0
    try:
        threads = cl.direct_threads(amount=20)
        for thread in threads:
            send_fire(thread.id, f"📢 **GLOBAL BROADCAST** 📢\n\n{arg}\n\n~ By Admin")
            count += 1
            time.sleep(1.5)
        send_fire(tid, f"✅ Broadcast sent successfully to {count} chats!")
    except Exception as e:
        send_fire(tid, f"❌ Broadcast Error: {e}")

# ================= ECONOMY & SOCIAL COMMANDS =================
def cmd_bal(tid, sender, reply_to_uid=None):
    target_id = reply_to_uid if reply_to_uid else sender
    acc = get_user_acc(target_id)
    send_fire(tid, f"💰 **WALLET BALANCE**\nUser: `{target_id}`\nCash: **${acc['bal']}**")

def cmd_claim(tid, sender):
    acc = get_user_acc(sender)
    now = time.time()
    if now - acc["last_daily"] < 86400: # 24 Hours
        remaining = int((86400 - (now - acc["last_daily"])) / 3600)
        send_fire(tid, f"⏳ You already claimed today! Try again in {remaining} hours.")
        return
    acc["last_daily"] = now
    add_bal(sender, 500)
    send_fire(tid, f"🎉 **DAILY REWARD CLAIMED!** Received **$500**. New Balance: **${acc['bal']}**")

def cmd_kill(tid, sender, reply_to_uid):
    if not reply_to_uid:
        send_fire(tid, "❌ Reply to a user's message to kill them!")
        return
    if reply_to_uid == sender:
        send_fire(tid, "❌ You cannot kill yourself!")
        return

    s_acc = get_user_acc(sender)
    t_acc = get_user_acc(reply_to_uid)
    now = time.time()

    if now - s_acc["last_kill"] < 1200: # 20 min cooldown
        rem = int((1200 - (now - s_acc["last_kill"])) / 60)
        send_fire(tid, f"⏳ Kill attack on cooldown! Wait {rem} minutes.")
        return

    if t_acc["protected_until"] > now:
        send_fire(tid, f"🛡️ Target is protected by Shield! Kill attack failed.")
        return

    s_acc["last_kill"] = now
    t_acc["dead_until"] = now + 900 # Dead for 15 min
    reward = random.randint(100, 500)
    add_bal(sender, reward)

    send_fire(tid, f"💥 **HEADSHOT!** User `{reply_to_uid}` was killed by `{sender}`! 🩸\nLoot earned: **${reward}**")

def cmd_rob(tid, sender, reply_to_uid):
    if not reply_to_uid:
        send_fire(tid, "❌ Reply to a user's message to rob them!")
        return
    if reply_to_uid == sender:
        send_fire(tid, "❌ You cannot rob yourself!")
        return

    s_acc = get_user_acc(sender)
    t_acc = get_user_acc(reply_to_uid)
    now = time.time()

    if t_acc["protected_until"] > now:
        send_fire(tid, "🛡️ Rob failed! Target has active protection shield.")
        return

    if t_acc["bal"] < 100:
        send_fire(tid, "❌ Target is too poor to be robbed!")
        return

    success = random.choice([True, False])
    if success:
        stolen = int(t_acc["bal"] * random.uniform(0.1, 0.4)) # 10% to 40%
        add_bal(reply_to_uid, -stolen)
        add_bal(sender, stolen)
        send_fire(tid, f"🥷 **SUCCESSFUL ROBBERY!** Stole **${stolen}** from `{reply_to_uid}`!")
    else:
        fine = 150
        add_bal(sender, -fine)
        send_fire(tid, f"🚔 **ROBBERY FAILED!** Police caught you and fined you **${fine}**!")

def cmd_protect(tid, sender):
    acc = get_user_acc(sender)
    if acc["bal"] < 300:
        send_fire(tid, "❌ Protection Shield costs **$300**. You don't have enough balance!")
        return
    
    add_bal(sender, -300)
    acc["protected_until"] = time.time() + 3600 # 1 Hour
    save_economy()
    send_fire(tid, "🛡️ **SHIELD ACTIVATED!** You are immune to Kill & Rob for **1 Hour**.")

def cmd_checkprotect(tid, sender):
    acc = get_user_acc(sender)
    now = time.time()
    if acc["protected_until"] > now:
        rem = int((acc["protected_until"] - now) / 60)
        send_fire(tid, f"🛡️ Your Protection Shield is ACTIVE for another {rem} minutes.")
    else:
        send_fire(tid, "❌ You currently have no active protection shield. Use `.protect` to buy one.")

def cmd_revive(tid, sender, reply_to_uid):
    if not reply_to_uid:
        send_fire(tid, "❌ Reply to a dead user to revive them!")
        return
    s_acc = get_user_acc(sender)
    t_acc = get_user_acc(reply_to_uid)
    now = time.time()

    if t_acc["dead_until"] <= now:
        send_fire(tid, "✨ Target user is already alive!")
        return

    if s_acc["bal"] < 200:
        send_fire(tid, "❌ Revive costs **$200**. You don't have enough balance!")
        return

    add_bal(sender, -200)
    t_acc["dead_until"] = 0
    save_economy()
    send_fire(tid, f"✨ **REVIVED!** User `{reply_to_uid}` was brought back to life by `{sender}`!")

def cmd_leaderboard(tid):
    sorted_users = sorted(economy_data.items(), key=lambda x: x[1].get("bal", 0), reverse=True)[:5]
    msg = "🏆 **ECONOMY LEADERBOARD (TOP 5)** 🏆\n\n"
    for idx, (uid, data) in enumerate(sorted_users, 1):
        msg += f"{idx}. ID `{uid}` — **${data.get('bal', 0)}**\n"
    send_fire(tid, msg)

def cmd_social(tid, sender, reply_to_uid, action):
    if not reply_to_uid:
        send_fire(tid, f"❌ Reply to a user to {action} them!")
        return
    emojis = {"slap": "👋💥", "kiss": "💋✨", "hug": "🤗❤️"}
    send_fire(tid, f"{emojis.get(action, '')} User `{sender}` gave a **{action.upper()}** to `{reply_to_uid}`!")

# ================= 10 GAMBLING & BET GAMES =================
def cmd_bet_game(tid, sender, game_type, args):
    if not args:
        send_fire(tid, f"❌ Usage: .{game_type} <amount> <choice>")
        return
    
    parts = args.split()
    try:
        bet = int(parts[0])
    except ValueError:
        send_fire(tid, "❌ Invalid bet amount!")
        return

    acc = get_user_acc(sender)
    if bet <= 0 or acc["bal"] < bet:
        send_fire(tid, "❌ Invalid bet amount or insufficient balance!")
        return

    # 1. FLIP (Coin Toss)
    if game_type == "flip":
        choice = parts[1].lower() if len(parts) > 1 else "heads"
        result = random.choice(["heads", "tails"])
        if choice in result:
            add_bal(sender, bet)
            send_fire(tid, f"🪙 Coin landed on **{result.upper()}**! You WON **${bet}**! 🎉")
        else:
            add_bal(sender, -bet)
            send_fire(tid, f"🪙 Coin landed on **{result.upper()}**! You Lost **${bet}**! 💸")

    # 2. ROLLBET (Dice Guess)
    elif game_type == "rollbet":
        try:
            guess = int(parts[1])
        except (IndexError, ValueError):
            send_fire(tid, "❌ Specify dice prediction (1-6)!")
            return
        roll = random.randint(1, 6)
        if guess == roll:
            win = bet * 5
            add_bal(sender, win)
            send_fire(tid, f"🎲 Rolled **{roll}**! PERFECT GUESS! Won **${win}**! 🚀")
        else:
            add_bal(sender, -bet)
            send_fire(tid, f"🎲 Rolled **{roll}**! Better luck next time! Lost **${bet}**.")

    # 3. SLOTS
    elif game_type == "slots":
        icons = ["🍎", "🍋", "🍒", "💎", "7️⃣"]
        r = [random.choice(icons) for _ in range(3)]
        slot_str = " | ".join(r)
        if r[0] == r[1] == r[2]:
            win = bet * 4
            add_bal(sender, win)
            send_fire(tid, f"🎰 [{slot_str}] 🎰\nJACKPOT! You WON **${win}**! 🔥")
        elif r[0] == r[1] or r[1] == r[2] or r[0] == r[2]:
            win = bet
            add_bal(sender, win)
            send_fire(tid, f"🎰 [{slot_str}] 🎰\nMATCHED TWO! You WON **${win}**! ✨")
        else:
            add_bal(sender, -bet)
            send_fire(tid, f"🎰 [{slot_str}] 🎰\nNo match! You Lost **${bet}**.")

    # 4. ROULETTE
    elif game_type == "roulette":
        choice = parts[1].lower() if len(parts) > 1 else "red"
        num = random.randint(0, 36)
        color = "red" if num % 2 == 0 else "black"
        if choice == color:
            add_bal(sender, bet)
            send_fire(tid, f"🎡 Ball landed on **{num} ({color.upper()})**! You WON **${bet}**!")
        else:
            add_bal(sender, -bet)
            send_fire(tid, f"🎡 Ball landed on **{num} ({color.upper()})**! You Lost **${bet}**.")

    # 5. RPS (Rock Paper Scissors)
    elif game_type == "rps":
        user_choice = parts[1].lower() if len(parts) > 1 else "rock"
        bot_choice = random.choice(["rock", "paper", "scissors"])
        if user_choice == bot_choice:
            send_fire(tid, f"✂️ Both chose **{bot_choice.upper()}**! It's a TIE!")
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "paper" and bot_choice == "rock") or \
             (user_choice == "scissors" and bot_choice == "paper"):
            add_bal(sender, bet)
            send_fire(tid, f"✂️ Bot chose **{bot_choice.upper()}**! You WON **${bet}**!")
        else:
            add_bal(sender, -bet)
            send_fire(tid, f"✂️ Bot chose **{bot_choice.upper()}**! You Lost **${bet}**.")

    # 6. GUESS (1 to 10)
    elif game_type == "guess":
        try:
            num = int(parts[1])
        except (IndexError, ValueError):
            send_fire(tid, "❌ Guess a number from 1-10!")
            return
        secret = random.randint(1, 10)
        if num == secret:
            win = bet * 3
            add_bal(sender, win)
            send_fire(tid, f"🔮 Secret number was **{secret}**! You WON **${win}**!")
        else:
            add_bal(sender, -bet)
            send_fire(tid, f"🔮 Secret number was **{secret}**! You Lost **${bet}**.")

    # 7. HIGHLOW
    elif game_type == "highlow":
        predict = parts[1].lower() if len(parts) > 1 else "high"
        num = random.randint(1, 6)
        res = "high" if num > 3 else "low"
        if predict == res:
            add_bal(sender, bet)
            send_fire(tid, f"🎲 Rolled **{num} ({res.upper()})**! Correct! Won **${bet}**!")
        else:
            add_bal(sender, -bet)
            send_fire(tid, f"🎲 Rolled **{num} ({res.upper()})**! Wrong! Lost **${bet}**.")

    # 8. CRASH
    elif game_type == "crash":
        multi = round(random.uniform(1.0, 3.5), 2)
        if multi >= 2.0:
            win = int(bet * multi)
            add_bal(sender, win)
            send_fire(tid, f"🚀 Multiplier reached **{multi}x**! Cashed out **${win}**!")
        else:
            add_bal(sender, -bet)
            send_fire(tid, f"💥 Crashed at **{multi}x**! You Lost **${bet}**.")

    # 9. JACKPOT
    elif game_type == "jackpot":
        if random.randint(1, 10) == 7: # 10% chance
            win = bet * 10
            add_bal(sender, win)
            send_fire(tid, f"💎 **MEGA JACKPOT!** You won **10x** earnings: **${win}**!")
        else:
            add_bal(sender, -bet)
            send_fire(tid, f"❌ Missed the Jackpot! Lost **${bet}**.")

    # 10. WHEEL
    elif game_type == "wheel":
        outcomes = [0, 0.5, 1.5, 3]
        mult = random.choice(outcomes)
        res_amt = int(bet * mult) - bet
        add_bal(sender, res_amt)
        if mult >= 1.0:
            send_fire(tid, f"🎡 Wheel stopped at **{mult}x**! Won **${int(bet*mult)}**!")
        else:
            send_fire(tid, f"🎡 Wheel stopped at **{mult}x**! Lost balance!")

def cmd_ping(tid):
    t0 = time.time()
    send_fire(tid, f"🏓 PONG!\nLatency: {int((time.time() - t0) * 1000)}ms\nStatus: Active ⚡")

def cmd_alive(tid):
    up = int(time.time() - START_TIME)
    send_fire(tid, f"🔥 ALEXA BOT ONLINE 🔥\nUptime: {up//60}m {up%60}s\nOwner: @{OWNER}\nMade By: @IG1VX")

def cmd_help(tid):
    msg = (
        "👑 **ALEXA BOT COMMANDS** 👑\n\n"
        "🎮 **PUBLIC & UTILS:**\n"
        ".roll | .flip | .ping | .alive | .adminlist\n\n"
        "💰 **ECONOMY & BATTLE (REPLY BASED):**\n"
        ".bal | .claim | .kill | .rob | .protect | .checkprotect | .revive | .leaderboard\n\n"
        "🎭 **SOCIAL ACTIONS (REPLY):**\n"
        ".slap | .kiss | .hug\n\n"
        "🎰 **CASINO & BET GAMES:**\n"
        ".flip <amt> <h/t> | .rollbet <amt> <1-6> | .slots <amt>\n"
        ".roulette <amt> <r/b> | .rps <amt> <choice> | .guess <amt> <1-10>\n"
        ".highlow <amt> <h/l> | .crash <amt> | .jackpot <amt> | .wheel <amt>\n\n"
        "⚙️ **ADMIN & OWNER:**\n"
        ".slide @user | .stopslide @user | .broadcast <msg>\n"
        ".addadmin @user | .rmvadmin @user | .spam <txt> | .gc <name>"
    )
    send_fire(tid, msg)

# ================= MAIN DISPATCHER =================
def handle(tid, text, sender, reply_to_uid=None):
    parts = text.split(" ", 1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    admin_cmds = {
        ".gc", ".stopgc", ".spam", ".stopspam", ".slide", ".stopslide",
        ".addadmin", ".rmvadmin", ".broadcast"
    }

    # ADMIN COMMANDS CHECK
    if cmd in admin_cmds:
        if sender not in ADMINS:
            send_fire(tid, "🚫 Permission Denied! Only Bot Admins/Owner can execute this.")
            return

        if cmd == ".addadmin":     cmd_addadmin(tid, arg, sender)
        elif cmd == ".rmvadmin":   cmd_rmvadmin(tid, arg, sender)
        elif cmd == ".slide":      cmd_slide(tid, arg)
        elif cmd == ".stopslide":  cmd_stopslide(tid, arg)
        elif cmd == ".broadcast":  cmd_broadcast(tid, arg, sender)
        elif cmd == ".gc":
            if not arg: send_fire(tid, "❌ Use: .gc <name>"); return
            gc_flag[tid] = arg
            threading.Thread(target=gc_worker, args=(tid, arg), daemon=True).start()
            send_fire(tid, f"🔥 GC Name Changer Active: {arg}")
        elif cmd == ".stopgc":
            send_fire(tid, "⏹️ GC Changer Stopped!") if gc_flag.pop(tid, None) else send_fire(tid, "No active GC changer.")
        elif cmd == ".spam":
            if not arg: send_fire(tid, "❌ Use: .spam <text>"); return
            if spam_flag.get(tid): send_fire(tid, "📢 Spam is already running!"); return
            spam_flag[tid] = True
            threading.Thread(target=spam_worker, args=(tid, arg), daemon=True).start()
            send_fire(tid, f"📢 Spam Started: {arg}")
        elif cmd == ".stopspam":
            send_fire(tid, "⏹️ Spam Stopped!") if spam_flag.pop(tid, None) else send_fire(tid, "No active spam.")
        return

    # ECONOMY & GAMES
    if cmd in [".bal", ".wallet"]:        cmd_bal(tid, sender, reply_to_uid)
    elif cmd in [".claim", ".daily"]:     cmd_claim(tid, sender)
    elif cmd == ".kill":                  cmd_kill(tid, sender, reply_to_uid)
    elif cmd in [".rob", ".steal"]:       cmd_rob(tid, sender, reply_to_uid)
    elif cmd == ".protect":               cmd_protect(tid, sender)
    elif cmd == ".checkprotect":          cmd_checkprotect(tid, sender)
    elif cmd == ".revive":                cmd_revive(tid, sender, reply_to_uid)
    elif cmd in [".leaderboard", ".top"]: cmd_leaderboard(tid)
    
    # SOCIAL ACTIONS
    elif cmd in [".slap", ".kiss", ".hug"]:
        cmd_social(tid, sender, reply_to_uid, cmd.lstrip("."))

    # BET GAMES
    elif cmd in [".flip", ".rollbet", ".slots", ".roulette", ".rps", ".guess", ".highlow", ".crash", ".jackpot", ".wheel"]:
        cmd_bet_game(tid, sender, cmd.lstrip("."), arg)

    # PUBLIC COMMANDS
    elif cmd == ".roll":        cmd_roll(tid)
    elif cmd == ".ping":        cmd_ping(tid)
    elif cmd == ".alive":       cmd_alive(tid)
    elif cmd == ".adminlist":   cmd_adminlist(tid)
    elif cmd in [".help", ".start"]:
        send_fire(tid, "✨ THIS BOT IS MADE BY @IG1VX ✨")
        cmd_help(tid)

# ================= BACKGROUND MESSAGE MONITOR =================
def process_auto_triggers(th, msg):
    sid = str(msg.user_id)
    txt = (msg.text or "").strip().lower()

    # 1. AUTO SLIDE TRIGGER
    if sid in slide_targets and not txt.startswith("."):
        reply_msg = random.choice(SLIDE_RESPONSES)
        send_fire(th.id, reply_msg)
        return

    # 2. OWNER DETECTION
    if any(q in txt for q in ["owner kon hai", "who is owner", "owner name", "owner कौन है"]):
        send_fire(th.id, "👑 My Owner is Alexa (@ig1vx) 🔥")
        return

    # 3. AI MENTION / CHAT
    if "alexa" in txt or f"@{USERNAME.lower()}" in txt:
        if not txt.startswith("."):
            send_fire(th.id, random.choice(AI_RESPONSES))
            return

    # 4. SYSTEM EVENT: NEW MEMBER WELCOME
    if msg.item_type == "action_log":
        send_fire(th.id, "🎉 **WELCOME TO THE GROUP!** 🔥\nRule follow karna aur maza karna ✨")

# ================= MAIN LOOP =================
print("⚙️ Catching up with existing messages...")
try:
    threads = cl.direct_threads(amount=3)
    for th in threads:
        for msg in th.messages:
            processed.add(str(msg.id))
    print("✅ Initialization done! Listening for commands & events...")
except Exception as e:
    print("⚠️ Init Warning:", e)

while True:
    try:
        threads = cl.direct_threads(amount=3)
        for th in threads:
            for msg in th.messages:
                msg_id = str(msg.id)
                if msg_id in processed:
                    continue
                processed.add(msg_id)

                sid = str(msg.user_id)
                if sid == BOT_ID:
                    continue

                # Reply Detection for .kill, .rob, .slap, etc.
                reply_to_uid = None
                if msg.reply_to_message:
                    reply_to_uid = str(msg.reply_to_message.user_id)

                txt = (msg.text or "").strip()
                if txt.startswith("."):
                    print(f"📩 Command Received: {txt}")
                    threading.Thread(target=handle, args=(th.id, txt, sid, reply_to_uid), daemon=True).start()
                else:
                    threading.Thread(target=process_auto_triggers, args=(th, msg), daemon=True).start()

    except Exception as e:
        print("[Main Loop Error]:", e)

    time.sleep(3)
