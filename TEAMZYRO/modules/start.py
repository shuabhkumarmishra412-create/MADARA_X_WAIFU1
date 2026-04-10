import os
import importlib.util
import random
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import ChatWriteForbidden
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from TEAMZYRO import LOGGER
from TEAMZYRO import *
from TEAMZYRO.unit.zyro_help import HELP_DATA  

LOG = LOGGER(__name__) 

# 🔹 Startup Animation Function
async def show_startup_animation(message):
    """Shows startup animation messages that appear word by word then delete"""
    animation_texts = [
        "🔥 ʜʟᴏ ʙᴀʙʏ ... 🝐",
        "❛ ᴘɪɴɢ ᴘᴏɴɢ .... 💗",
        "𓂃❛ ⟶ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴡᴀɪғᴜ x sʟᴀᴠᴇ ❜ 🌙⤹🌸"
    ]
    
    for text in animation_texts:
        try:
            # Split text into words and animate word by word
            words = text.split()
            animated_msg = ""
            
            sent_msg = None
            for word in words:
                animated_msg += word + " "
                if sent_msg is None:
                    sent_msg = await message.reply_text(animated_msg)
                else:
                    await sent_msg.edit_text(animated_msg)
                await asyncio.sleep(0.2)  # Speed of animation
            
            # Keep the message for a moment then delete
            await asyncio.sleep(0.5)
            await sent_msg.delete()
            await asyncio.sleep(0.3)
        except Exception as e:
            LOG.warning("Startup animation error: %s", e)

# 🔹 Function to Calculate Uptime
START_TIME = time.time()

def get_uptime():
    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# 🔹 Function to Generate Private Start Message & Buttons
async def generate_start_message(client, message):
    bot_user = await client.get_me()
    bot_name = bot_user.first_name
    ping = round(time.time() - message.date.timestamp(), 2)
    uptime = get_uptime()

    
    caption = f"""🍃 ɢʀᴇᴇᴛɪɴɢs, ɪ'ᴍ {bot_name} 🫧, ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ!
╭━━━━━━━╾❁✦❁╼━━━━━━━╮
"⟡ ɪ ᴀᴍ ʏᴏᴜʀ ᴡᴀɪғᴜ ɢᴇɴɪᴇ!  
    sᴜᴍᴍᴏɴ ᴄᴜᴛᴇ ᴡᴀɪғᴜs  
    ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ ✧"

"⟡ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ  
    & ᴛᴀᴘ /help ғᴏʀ ᴄᴏᴍᴍᴀɴᴅs"
╰━━━━━━━╾❁✦❁╼━━━━━━━╯
➺ ᴘɪɴɢ: {ping} ms
➺ ᴜᴘᴛɪᴍᴇ: {uptime}"""

    buttons = [
        [InlineKeyboardButton("🟢 ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ", url=f"https://t.me/{bot_user.username}?startgroup=true")],
        [InlineKeyboardButton("🔴 ɖᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/II_YOUR_VILLAIN_II"), 
         InlineKeyboardButton("🔵 sᴜᴘᴘᴏʀᴛ", url="https://t.me/+dv_rcq5uIXhmMWM1")],
        [InlineKeyboardButton("🟡 ᴄʜᴀɴɴᴇʟ", url="https://t.me/+Imyf3M9TO5k1ODRl")],
        [InlineKeyboardButton("🟣 ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅ", callback_data="open_help")]
    ]
    
    return caption, buttons

# 🔹 Function to Generate Group Start Message & Buttons
async def generate_group_start_message(client):
    bot_user = await client.get_me()
    caption = f"🍃 ɪ'ᴍ {bot_user.first_name} 🫧\nɪ sᴘᴀᴡɴ ᴡᴀɪғᴜs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ғᴏʀ ᴜsᴇʀs ᴛᴏ ɢʀᴀʙ.\nᴜsᴇ /help ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏ."
    buttons = [
        [
            InlineKeyboardButton("◦ᴀᴅᴅ ᴍᴇ◦", url=f"https://t.me/{bot_user.username}?startgroup=true"),
            InlineKeyboardButton("◦sᴜᴘᴘᴏʀᴛ◦", url="https://t.me/+dv_rcq5uIXhmMWM1"),
        ]
    ]
    return caption, buttons

# 🔹 Private Start Command Handler
@app.on_message(filters.command("start") & filters.private)
async def start_private_command(client, message):
    # Check if user exists in user_collection
    existing_user = await user_collection.find_one({"id": message.from_user.id})
    
    # Save user data only if they don't exist in the collection
    if not existing_user:
        user_data = {
            "id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "start_time": time.time()
        }
        await user_collection.insert_one(user_data)

    caption, buttons = await generate_start_message(client, message)
    media = random.choice(START_MEDIA)
    
    # Show startup animation
    await show_startup_animation(message)
    
    username = f"@{message.from_user.username}" if message.from_user.username else "N/A"
    try:
        await app.send_message(
            chat_id=GLOG,
            text=(
                f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"
                f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> {username}"
            ),
        )
    except ChatWriteForbidden:
        # Ignore when bot cannot write in log chat, so /start still works for users.
        pass
    except Exception as exc:
        # Any logging failure should not block /start response in private chat.
        LOG.warning("Failed to send /start log to GLOG (%s): %s", GLOG, exc)
    
    try:
        if media.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            await message.reply_photo(
                photo=media,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(buttons)  # Pass InlineKeyboardMarkup directly
            )
        else:
            await message.reply_video(
                video=media,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(buttons)  # Pass InlineKeyboardMarkup directly
            )
    except Exception as exc:
        LOG.warning("Failed to send /start media '%s': %s. Falling back to text.", media, exc)
        await message.reply_text(
            caption,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# 🔹 Group Start Command Handler
@app.on_message(filters.command("start") & filters.group)
async def start_group_command(client, message):
    caption, buttons = await generate_group_start_message(client)
    media = random.choice(START_MEDIA)
    
    # Check if media is image or video based on extension
    if media.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        await message.reply_photo(
            photo=media,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons)  # Pass InlineKeyboardMarkup directly
        )
    else:
        await message.reply_video(
            video=media,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons)  # Pass InlineKeyboardMarkup directly
        )

# 🔹 Function to Find Help Modules
def find_help_modules():
    buttons = []
    
    for module_name, module_data in HELP_DATA.items():
        button_name = module_data.get("HELP_NAME", "Unknown")
        buttons.append(InlineKeyboardButton(button_name, callback_data=f"help_{module_name}"))

    return [buttons[i : i + 3] for i in range(0, len(buttons), 3)]

# 🔹 Help Button Click Handler
@app.on_callback_query(filters.regex("^open_help$"))
async def show_help_menu(client, query: CallbackQuery):
    await asyncio.sleep(1)
    buttons = find_help_modules()
    buttons.append([InlineKeyboardButton("⬅ Back", callback_data="back_to_home")])

    await query.message.edit_text(
        "*ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.\n\nᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /",
        reply_markup=InlineKeyboardMarkup(buttons)  # Pass InlineKeyboardMarkup directly
    )

# 🔹 Individual Module Help Handler
@app.on_callback_query(filters.regex(r"^help_(.+)"))
async def show_help(client, query: CallbackQuery):
    await asyncio.sleep(1)
    module_name = query.data.split("_", 1)[1]
    
    try:
        module_data = HELP_DATA.get(module_name, {})
        help_text = module_data.get("HELP", "Is module ka koi help nahi hai.")
        buttons = [[InlineKeyboardButton("⬅ Back", callback_data="open_help")]]
        
        await query.message.edit_text(
            f"**{module_name} Help:**\n\n{help_text}",
            reply_markup=InlineKeyboardMarkup(buttons)  # Pass InlineKeyboardMarkup directly
        )
    except Exception as e:
        await query.answer("Help load karne me error aayi!")

# 🔹 Back to Home
@app.on_callback_query(filters.regex("^back_to_home$"))
async def back_to_home(client, query: CallbackQuery):
    await asyncio.sleep(1)
    caption, buttons = await generate_start_message(client, query.message)
    await query.message.edit_text(
        caption,
        reply_markup=InlineKeyboardMarkup(buttons)  # Pass InlineKeyboardMarkup directly
        )



