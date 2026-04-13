# ------------------------------ IMPORTS ---------------------------------
import logging
import os
from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client, filters as f
from pyrogram.types import x

# ====================================================
#                LOGGING SETUP
# ====================================================

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
)

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("telegram").setLevel(logging.ERROR)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


# ====================================================
#                ENV CONFIG (Your Style)
# ====================================================

api_id = int(os.getenv("API_ID", "23343216"))
api_hash = os.getenv("API_HASH", "1d66f21cd828dc22b80e3750719bd94a")
TOKEN = os.getenv("TOKEN", "").strip() or "8264339422:AAGwdHNtrBH8lp0rdHb74eUIcwqFeAAYW5I"

GLOG = os.getenv("GLOG", "abrakatabragiligilichu")
CHARA_CHANNEL_ID = os.getenv("CHARA_CHANNEL_ID", "abrakatabragiligilichu")
SUPPORT_CHAT_ID = int(os.getenv("SUPPORT_CHAT_ID", "-1003984956252"))

mongo_url = os.getenv(
    "MONGO_URL",
    "mongodb+srv://rj5706603:O95nvJYxapyDHfkw@cluster0.fzmckei.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

MUSJ_JOIN = os.getenv("MUSJ_JOIN", "https://t.me/+8KU5ZDxvZyw0N2U1")

START_MEDIA = os.getenv(
    "START_MEDIA",
    "https://files.catbox.moe/aw6zui.jpg"
).split(',')

PHOTO_URL = [
    os.getenv("PHOTO_URL_1", "https://files.catbox.moe/f5njbm.jpg"),
    os.getenv("PHOTO_URL_2", "https://files.catbox.moe/3saw6n.jpg")
]

STATS_IMG = ["https://files.catbox.moe/0zvwpt.jpg"]

SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/thedrxnet")
UPDATE_CHAT = os.getenv("UPDATE_CHAT", "https://t.me/thedrxnet")

SUDO = list(map(int, os.getenv("SUDO", "8441236350").split(',')))
OWNER_ID = int(os.getenv("OWNER_ID", "8441236350"))




# --------------------- TELEGRAM BOT CONFIGURATION -----------------------
command_filter = f.create(lambda _, __, message: message.text and message.text.startswith("/"))
application = Application.builder().token(TOKEN).build()
ZYRO = Client(
    ":memory:", api_id=api_id, api_hash=api_hash, bot_token=TOKEN
)

# -------------------------- DATABASE SETUP ------------------------------
ddw = AsyncIOMotorClient(mongo_url)
db = ddw['hinata_waifu']

# Collections
user_totals_collection = db['gaming_totals']
group_user_totals_collection = db['gaming_group_total']
top_global_groups_collection = db['gaming_global_groups']
pm_users = db['gaming_pm_users']
destination_collection = db['gamimg_user_collection']
destination_char = db['gaming_anime_characters']
questions_collection = db["questions"]
group_collection = db["groups"]
waifu_collection = db["waifus"]
mines_collection = db["mines_games"]
multi_collection = db["multi_mines"]
txn_collection = db["transactions"]

# -------------------------- GLOBAL VARIABLES ----------------------------
app = ZYRO
sudo_users = SUDO
collection = destination_char
user_collection = destination_collection

# --------------------------- STRIN ---------------------------------------
locks = {}
message_counters = {}
spam_counters = {}
last_characters = {}
sent_characters = {}
first_correct_guesses = {}
message_counts = {}
last_user = {}
warned_users = {}
user_cooldowns = {}
user_nguess_progress = {}
user_guess_progress = {}
normal_message_counts = {}  

# -------------------------- POWER SETUP --------------------------------
from TEAMZYRO.unit.zyro_ban import *
from TEAMZYRO.unit.zyro_sudo import *
from TEAMZYRO.unit.zyro_react import *
from TEAMZYRO.unit.zyro_log import *
from TEAMZYRO.unit.zyro_send_img import *
from TEAMZYRO.unit.zyro_rarity import *
# ------------------------------------------------------------------------

async def PLOG(text: str):
    await app.send_message(
       chat_id=GLOG,
       text=text
   )

# ---------------------------- END OF CODE ------------------------------
