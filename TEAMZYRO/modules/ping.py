import time
import random

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from TEAMZYRO import application, sudo_users, START_MEDIA

async def ping(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        update.message.reply_text("Nouu.. its Sudo user's Command..")
        return
    start_time = time.time()
    media = random.choice(START_MEDIA)
    
    try:
        if media.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            message = await update.message.reply_photo(
                photo=media,
                caption='❛ ᴘɪɴɢ ᴘᴏɴɢ .... 💗'
            )
        else:
            message = await update.message.reply_video(
                video=media,
                caption='❛ ᴘɪɴɢ ᴘᴏɴɢ .... 💗'
            )
    except:
        message = await update.message.reply_text('❛ ᴘɪɴɢ ᴘᴏɴɢ .... 💗')
    
    end_time = time.time()
    elapsed_time = round((end_time - start_time) * 1000, 3)
    
    try:
        await message.edit_caption(caption=f'❛ ᴘɪɴɢ ᴘᴏɴɢ .... 💗\n\n⚡ Pong! {elapsed_time}ms')
    except:
        await message.edit_text(f'❛ ᴘɪɴɢ ᴘᴏɴɢ .... 💗\n\n⚡ Pong! {elapsed_time}ms')

application.add_handler(CommandHandler("ping", ping))
