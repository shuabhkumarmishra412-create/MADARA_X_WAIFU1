from TEAMZYRO import *
import importlib
import logging
from pyrogram import Client
from pyrogram.errors import SessionRevoked
from TEAMZYRO.modules import ALL_MODULES


def main() -> None:
    for module_name in ALL_MODULES:
        imported_module = importlib.import_module("TEAMZYRO.modules." + module_name)
    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞s 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

    global ZYRO
    try:
        ZYRO.start()
    except SessionRevoked:
        LOGGER("TEAMZYRO").warning(
            "Telegram session revoked. Recreating bot client with an in-memory session and retrying startup."
        )
        ZYRO = Client(
            ":memory:", api_id=api_id, api_hash=api_hash, bot_token=TOKEN
        )
        ZYRO.start()

    application.run_polling(drop_pending_updates=True)
    send_start_message()
    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY GOJOXNETWORK☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

if __name__ == "__main__":
    main()
    
