import os
import requests
import asyncio
import hashlib
from pyrogram import filters, enums
from pyrogram.errors import RPCError

# ✅ FIX 1: 'ZYRO' ki jagah 'app' import kiya
from TEAMZYRO import (
    app, 
    CHARA_CHANNEL_ID,
    SUPPORT_CHAT,
    OWNER_ID,
    collection,
    user_collection,
    db,
    SUDO,
    rarity_map
)

# 🛑 YAHAN APNA IMGBB API KEY DAALNA HAI 🛑
IMGBB_API_KEY = "95c5713baa2adf32c45f91191939d7ad"

upload_lock = None

WRONG_FORMAT_TEXT = """<blockquote>❌ ᴡʀᴏɴɢ ғᴏʀᴍᴀᴛ...  
ᴇɢ. /upload ʀᴇᴘʟʏ ᴛᴏ ᴘʜᴏᴛᴏ muzan-kibutsuji Demon-slayer 3

ғᴏʀᴍᴀᴛ:- /upload reply character-name anime-name rarity-number
</blockquote>"""

async def find_available_id():
    cursor = collection.find().sort("id", 1)
    ids = []

    async for doc in cursor:
        if "id" in doc:
            try:
                ids.append(int(doc["id"]))
            except:
                continue

    ids.sort()

    for i in range(1, len(ids) + 2):
        if i not in ids:
            return str(i).zfill(2)

    return str(len(ids) + 1).zfill(2)

def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# 🔄 UPDATED: Multi-Fallback Upload System
def upload_file_with_fallback(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found")

    # 1️⃣ FIRST TRY: IMGBB 
    if IMGBB_API_KEY and IMGBB_API_KEY != "YOUR_IMGBB_API_KEY_HERE":
        try:
            with open(file_path, "rb") as file:
                r = requests.post(
                    "https://api.imgbb.com/1/upload",
                    data={"key": IMGBB_API_KEY},
                    files={"image": file},
                    timeout=60
                )
            if r.status_code == 200:
                data = r.json()
                if "data" in data and "url" in data["data"]:
                    return data["data"]["url"]
        except Exception:
            pass # Agar ImgBB fail hua toh aage badhega

    # 2️⃣ SECOND TRY: CATBOX.MOE
    try:
        with open(file_path, "rb") as file:
            r = requests.post(
                "https://catbox.moe/user/api.php",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": file},
                timeout=60
            )
        if r.status_code == 200 and r.text.startswith("https"):
            return r.text.strip()
    except Exception:
        pass # Agar Catbox fail hua toh Graph par jayega

    # 3️⃣ THIRD TRY: GRAPH.ORG
    try:
        with open(file_path, "rb") as file:
            r = requests.post(
                "https://graph.org/upload",
                files={"file": file},
                timeout=60
            )
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and "src" in data[0]:
                return "https://graph.org" + data[0]["src"]
    except Exception:
        pass

    raise Exception("Upload failed on all servers (ImgBB, Catbox, Graph)")

async def animate_upload(msg):
    frames = [
        "⏳ Initializing...",
        "📥 Downloading...",
        "🔄 Processing...",
        "☁️ Uploading..."
    ]
    try:
        while True:
            for f in frames:
                await msg.edit_text(f)
                await asyncio.sleep(1)
    except:
        pass

# ✅ FIX 2: @ZYRO.on_message ko @app.on_message kar diya
@app.on_message(filters.command("upload"))
async def ul(client, message):
    global upload_lock

    if upload_lock is None:
        upload_lock = asyncio.Lock()

    if upload_lock.locked():
        return await message.reply_text("⏳ Another upload in progress...")

    async with upload_lock:
        reply = message.reply_to_message
        if not reply:
            return await message.reply_text("❌ Reply to media")

        args = message.text.split()
        if len(args) != 4:
            return await message.reply_text(WRONG_FORMAT_TEXT)

        try:
            name = args[1].replace("-", " ").title()
            anime = args[2].replace("-", " ").title()
            rarity = int(args[3])
        except:
            return await message.reply_text("❌ Invalid format")

        if rarity not in rarity_map:
            return await message.reply_text("❌ Invalid rarity")

        msg = await message.reply_text("⏳ Processing...")
        task = asyncio.create_task(animate_upload(msg))

        path = None

        try:
            path = await reply.download()

            file_hash = get_file_hash(path)
            existing = await collection.find_one({"file_hash": file_hash})

            if existing:
                task.cancel()
                return await msg.edit_text("⚠️ Duplicate detected")

            url = await asyncio.to_thread(upload_file_with_fallback, path)

            char = {
                "name": name,
                "anime": anime,
                "rarity": rarity_map[rarity],
                "rarity_number": rarity,
                "id": await find_available_id(),
                "file_hash": file_hash
            }

            if reply.photo or reply.document:
                char["img_url"] = url
                await client.send_photo(CHARA_CHANNEL_ID, path)
            elif reply.video:
                char["vid_url"] = url
                await client.send_video(CHARA_CHANNEL_ID, path)

            await collection.insert_one(char)

            task.cancel()
            await msg.edit_text(f"✅ Uploaded {name}")

        except RPCError as e:
            task.cancel()
            await msg.edit_text(f"❌ Telegram Error: {e}")

        except Exception as e:
            task.cancel()
            await msg.edit_text(f"❌ Error: {e}")

        finally:
            if path and os.path.exists(path):
                os.remove(path)
                
