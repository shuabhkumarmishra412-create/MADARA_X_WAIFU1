import random
import asyncio
import time
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from TEAMZYRO import app, collection, group_user_totals_collection

log = "-1002792716047"

# Dictionaries to track progress
message_counters = {}
last_characters = {}
first_correct_guesses = {}

# Updated Rarity Chart with all 15 categories
RARITY_WEIGHTS = {
    "⚪️ Low": (40, True),              
    "🟠 Medium": (20, True),           
    "🔴 High": (12, True),             
    "🎩 Special Edition": (8, True),   
    "🪽 Elite Edition": (6, True),     
    "🪐 Exclusive": (4, True),         
    "💞 Valentine": (2, False),         
    "🎃 Halloween": (2, False),        
    "❄️ Winter": (1.5, False),          
    "🏖 Summer": (1.2, False),          
    "🎗 Royal": (0.5, False),           
    "💸 Luxury Edition": (0.5, False),  
    "🍃 echhi": (3, True),             # Added
    "🌧️ Rainy Edition": (1.5, False),   # Added
    "🎍 Festival": (1.5, False)         # Added
}

async def delete_message(chat_id, message_id, client):
    await asyncio.sleep(300)  # 5 minutes
    try:
        await client.delete_messages(chat_id, message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")

async def send_image(client, chat_id: int) -> None:
    # Fetch characters matching allowed rarities
    all_characters = list(await collection.find({"rarity": {"$in": [k for k, v in RARITY_WEIGHTS.items() if v[1]]}}).to_list(length=None))

    if not all_characters:
        return

    available_characters = [
        c for c in all_characters 
        if 'id' in c and c.get('rarity') is not None and RARITY_WEIGHTS.get(c['rarity'], (0, False))[1]
    ]

    if not available_characters:
        return

    # Weighted selection
    cumulative_weights = []
    cumulative_weight = 0
    for character in available_characters:
        cumulative_weight += RARITY_WEIGHTS.get(character.get('rarity'), (1, False))[0]
        cumulative_weights.append(cumulative_weight)

    rand = random.uniform(0, cumulative_weight)
    selected_character = None
    for i, character in enumerate(available_characters):
        if rand <= cumulative_weights[i]:
            selected_character = character
            break

    if not selected_character:
        selected_character = random.choice(available_characters)

    # State reset for guessing
    last_characters[chat_id] = selected_character
    last_characters[chat_id]['timestamp'] = time.time()
    if chat_id in first_correct_guesses:
        del first_correct_guesses[chat_id]

    # Spawn Caption in Tiny Caps & Blockquote
    caption_text = (
        f"<blockquote>✨ ᴀ {selected_character['rarity']} ᴄʜᴀʀᴀᴄᴛᴇʀ ᴀᴘᴘᴇᴀʀs! ✨\n\n"
        f"🔍 ᴜsᴇ /guess ᴛᴏ ᴄʟᴀɪᴍ ᴛʜɪs ᴍʏsᴛᴇʀɪᴏᴜs ᴄʜᴀʀᴀᴄᴛᴇʀ!\n"
        f"💫 ʜᴜʀʀʏ, ʙᴇғᴏʀᴇ sᴏᴍᴇᴏɴᴇ ᴇʟsᴇ sɴᴀᴛᴄʜᴇs ᴛʜᴇᴍ!</blockquote>"
    )

    try:
        if 'vid_url' in selected_character and selected_character['vid_url']:
            sent_message = await client.send_video(
                chat_id=chat_id,
                video=selected_character['vid_url'],
                caption=caption_text,
                parse_mode=ParseMode.HTML
            )
        else:
            sent_message = await client.send_photo(
                chat_id=chat_id,
                photo=selected_character['img_url'],
                caption=caption_text,
                parse_mode=ParseMode.HTML
            )
        # Schedule delete
        asyncio.create_task(delete_message(chat_id, sent_message.id, client))
    except Exception as e:
        print(f"Failed to send image: {e}")

# Fixed Auto Spawn Watcher
@app.on_message(filters.group, group=10)
async def auto_spawn_watcher(client, message):
    # Ignore bot messages
    if message.from_user and message.from_user.is_bot:
        return
        
    # Ignore commands
    if message.text and message.text.startswith('/'):
        return

    chat_id = message.chat.id

    if chat_id not in message_counters:
        message_counters[chat_id] = 0
    message_counters[chat_id] += 1

    group_data = await group_user_totals_collection.find_one({"group_id": str(chat_id)})
    ctime_limit = group_data.get("ctime", 80) if group_data else 80

    if message_counters[chat_id] >= ctime_limit:
        message_counters[chat_id] = 0  # Reset Counter
        await send_image(client, chat_id)
        
