import os
import requests
import asyncio
import hashlib
from pyrogram import filters, enums
from TEAMZYRO import (
    application,
    CHARA_CHANNEL_ID,
    SUPPORT_CHAT,
    OWNER_ID,
    collection,
    user_collection,
    db,
    SUDO,
    rarity_map,
    ZYRO,
    require_power
)


WRONG_FORMAT_TEXT = """<blockquote>❌ ᴡʀᴏɴɢ ғᴏʀᴍᴀᴛ...  
ᴇɢ. /upload ʀᴇᴘʟʏ ᴛᴏ ᴘʜᴏᴛᴏ muzan-kibutsuji Demon-slayer 3

ғᴏʀᴍᴀᴛ:- /upload reply character-name anime-name rarity-number

ᴜsᴇ ʀᴀʀɪᴛʏ ɴᴜᴍʙᴇʀ ᴀᴄᴄᴏʀᴅɪɴɢʟʏ ʀᴀʀɪᴛʏ ᴍᴀᴘ:

1: "⚪️ Low", 2: "🟠 Medium", 3: "🔴 High", 4: "🎩 Special Edition",
5: "🪽 Elite Edition", 6: "🪐 Exclusive", 7: "💞 Valentine",
8: "🎃 Halloween", 9: "❄️ Winter", 10: "🏖 Summer", 
11: "🎗 Royal", 12: "💸 Luxury Edition", 13: "🍃 echhi", 
14: "🌧️ Rainy Edition", 15: "🎍 Festival"</blockquote>"""


async def find_available_id():
    cursor = collection.find().sort("id", 1)
    ids = []
    async for doc in cursor:
        if "id" in doc:
            try:
                ids.append(int(doc["id"]))
            except Exception:
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


def upload_to_catbox(file_path):
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError("file_path is missing or file does not exist")

    url = "https://catbox.moe/user/api.php"
    with open(file_path, "rb") as file:
        response = requests.post(
            url,
            data={"reqtype": "fileupload"},
            files={"fileToUpload": file},
            timeout=120
        )
    if response.status_code == 200 and response.text.startswith("https"):
        return response.text.strip()
    else:
        raise Exception(f"Error uploading to Catbox: {response.status_code} {response.text}")

upload_lock = asyncio.Lock()


async def animate_upload(message):
    frames = [
        "<blockquote>⏳ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ... [□□□□□□□□□□] 0%</blockquote>",
        "<blockquote>📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴍᴇᴅɪᴀ... [■■■□□□□□□□] 30%</blockquote>",
        "<blockquote>🔄 ᴘʀᴏᴄᴇssɪɴɢ ᴅᴀᴛᴀ... [■■■■■■□□□□] 60%</blockquote>",
        "<blockquote>☁️ ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴄᴀᴛʙᴏx... [■■■■■■■■■□] 90%</blockquote>"
    ]
    try:
        while True:
            for frame in frames:
                await message.edit_text(frame, parse_mode=enums.ParseMode.HTML)
                await asyncio.sleep(1.2) 
    except asyncio.CancelledError:
        pass
    except Exception:
        pass

@ZYRO.on_message(filters.command(["upload"]))
@require_power("add_character")
async def ul(client, message):
    global upload_lock

    if upload_lock.locked():
        return await message.reply_text("<blockquote>⏳ ᴀɴᴏᴛʜᴇʀ ᴜᴘʟᴏᴀᴅ ɪs ɪɴ ᴘʀᴏɢʀᴇss. ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ.</blockquote>", parse_mode=enums.ParseMode.HTML)

    async with upload_lock:
        reply = message.reply_to_message
        if not reply:
            return await message.reply_text("<blockquote>❌ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ, ᴅᴏᴄᴜᴍᴇɴᴛ, ᴏʀ ᴠɪᴅᴇᴏ.</blockquote>", parse_mode=enums.ParseMode.HTML)

        args = message.text.strip().split()
        if len(args) != 4:
            return await client.send_message(chat_id=message.chat.id, text=WRONG_FORMAT_TEXT, parse_mode=enums.ParseMode.HTML)

        try:
            character_name = args[1].replace('-', ' ').title()
            anime = args[2].replace('-', ' ').title()
            rarity = int(args[3])
        except Exception:
            return await message.reply_text("<blockquote>❌ ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ғᴏʀᴍᴀᴛ.</blockquote>", parse_mode=enums.ParseMode.HTML)

        if rarity not in rarity_map:
            return await message.reply_text("<blockquote>❌ ɪɴᴠᴀʟɪᴅ ʀᴀʀɪᴛʏ ᴠᴀʟᴜᴇ.</blockquote>", parse_mode=enums.ParseMode.HTML)

        
        processing_message = await message.reply_text("<blockquote>⏳ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ... [□□□□□□□□□□] 0%</blockquote>", parse_mode=enums.ParseMode.HTML)
        anim_task = asyncio.create_task(animate_upload(processing_message))
        
        path = None
        thumb_path = None
        try:
            
            path = await reply.download()
            if not path or not os.path.exists(path):
                raise Exception("Failed to download media.")

            
            file_hash = get_file_hash(path)
            existing_char = await collection.find_one({"file_hash": file_hash})
            
            if existing_char:
                anim_task.cancel() 
                return await processing_message.edit_text(
                    f"<blockquote>⚠️ ᴅᴜᴘʟɪᴄᴀᴛᴇ ᴜᴘʟᴏᴀᴅ ᴅᴇᴛᴇᴄᴛᴇᴅ!\n\n"
                    f"ᴍᴇᴅɪᴀ ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛs ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.\n"
                    f"ɪᴅ: <code>{existing_char.get('id')}</code>\n"
                    f"ɴᴀᴍᴇ: <code>{existing_char.get('name')}</code></blockquote>",
                    parse_mode=enums.ParseMode.HTML
                )

            
            catbox_url = await asyncio.to_thread(upload_to_catbox, path)

            rarity_text = rarity_map[rarity]
            available_id = await find_available_id()

            character = {
                'name': character_name,
                'anime': anime,
                'rarity': rarity_text,
                'rarity_number': rarity,
                'id': available_id,
                'file_hash': file_hash 
            }

            if reply.photo or reply.document:
                character['img_url'] = catbox_url
            elif reply.video:
                character['vid_url'] = catbox_url
                try:
                    thumbs = getattr(reply.video, "thumbs", None)
                    if thumbs and len(thumbs) > 0:
                        thumb_path = await client.download_media(thumbs[0].file_id)
                        if thumb_path and os.path.exists(thumb_path):
                            thumbnail_url = await asyncio.to_thread(upload_to_catbox, thumb_path)
                            character['thum_url'] = thumbnail_url
                except Exception:
                    pass 

            caption_text = (
                f"<blockquote>✨ ᴄʜᴀʀᴀᴄᴛᴇʀ ɴᴀᴍᴇ: {character_name}\n"
                f"🎬 ᴀɴɪᴍᴇ ɴᴀᴍᴇ: {anime}\n"
                f"💎 ʀᴀʀɪᴛʏ: {rarity_text}\n"
                f"🆔 ɪᴅ: {available_id}\n"
                f"👤 ᴀᴅᴅᴇᴅ ʙʏ <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a></blockquote>"
            )

            if 'img_url' in character:
                await client.send_photo(chat_id=CHARA_CHANNEL_ID, photo=character['img_url'], caption=caption_text, parse_mode=enums.ParseMode.HTML)
            elif 'vid_url' in character:
                await client.send_video(chat_id=CHARA_CHANNEL_ID, video=character['vid_url'], caption=caption_text, parse_mode=enums.ParseMode.HTML)
            else:
                await client.send_document(chat_id=CHARA_CHANNEL_ID, document=path, caption=caption_text, parse_mode=enums.ParseMode.HTML)

            await collection.insert_one(character)

            
            anim_task.cancel()
            await processing_message.edit_text(
                f"<blockquote>✅ ᴡᴀɪғᴜ sᴜᴄᴄᴇssғᴜʟʟʏ ᴜᴘʟᴏᴀᴅᴇᴅ! [■■■■■■■■■■] 100%</blockquote>\n\n"
                f"<blockquote>➲ ᴀᴅᴅᴇᴅ ʙʏ » <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n"
                f"➥ ᴄʜᴀʀᴀᴄᴛᴇʀ ɪᴅ: <code>{available_id}</code>\n"
                f"➥ ʀᴀʀɪᴛʏ: {rarity_text}\n"
                f"➥ ᴄʜᴀʀᴀᴄᴛᴇʀ ɴᴀᴍᴇ: {character_name}</blockquote>",
                parse_mode=enums.ParseMode.HTML
            )

        except Exception as e:
            anim_task.cancel()
            await processing_message.edit_text(f"<blockquote>❌ ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ. ᴇʀʀᴏʀ: <code>{str(e)}</code></blockquote>", parse_mode=enums.ParseMode.HTML)
        
        finally:
            try:
                if path and os.path.exists(path):
                    os.remove(path)
                if thumb_path and os.path.exists(thumb_path):
                    os.remove(thumb_path)
            except Exception:
                pass
                
