from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ParseMode
from TEAMZYRO import group_user_totals_collection, OWNER_ID, app, x

async def is_admin(client: Client, chat_id: int, user_id: int) -> bool:
    if user_id == x:
        return True
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception as e:
        print(f"Error: {e}")
        return False

@app.on_message(filters.command("ctime") & filters.group)
async def set_ctime(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    is_admin_user = await is_admin(client, chat_id, user_id)
    is_owner = user_id == OWNER_ID

    if not (is_admin_user or is_owner):
        await message.reply("<blockquote>⚠️ ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ!</blockquote>", parse_mode=ParseMode.HTML)
        return

    try:
        ctime = int(message.command[1])
    except (IndexError, ValueError):
        await message.reply("<blockquote>⚠️ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ɴᴜᴍʙᴇʀ (ᴇ.ɢ., /ctime 80).</blockquote>", parse_mode=ParseMode.HTML)
        return

    if is_owner:
        if not 1 <= ctime <= 200:
            await message.reply("<blockquote>⚠️ ʙᴏᴛ ᴏᴡɴᴇʀ ᴄᴀɴ sᴇᴛ ᴄᴛɪᴍᴇ ʙᴇᴛᴡᴇᴇɴ 1 ᴀɴᴅ 200.</blockquote>", parse_mode=ParseMode.HTML)
            return
    else:
        if not 80 <= ctime <= 200:
            await message.reply("<blockquote>⚠️ ᴀᴅᴍɪɴs ᴄᴀɴ sᴇᴛ ᴄᴛɪᴍᴇ ʙᴇᴛᴡᴇᴇɴ 80 ᴀɴᴅ 200.</blockquote>", parse_mode=ParseMode.HTML)
            return

    await group_user_totals_collection.update_one(
        {"group_id": str(chat_id)},
        {"$set": {"ctime": ctime}},
        upsert=True
    )

    await message.reply(f"<blockquote>✅ ᴍᴇssᴀɢᴇ ᴄᴏᴜɴᴛ ᴛʜʀᴇsʜᴏʟᴅ sᴇᴛ ᴛᴏ {ctime} ғᴏʀ ᴛʜɪs ɢʀᴏᴜᴘ.</blockquote>", parse_mode=ParseMode.HTML)

