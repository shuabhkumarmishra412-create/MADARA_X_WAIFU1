from TEAMZYRO import *
import importlib
import logging
import os
from pyrogram.errors import SessionRevoked
from TEAMZYRO.modules import ALL_MODULES

SESSION_NAME = "Shivu"


def remove_session_files(session_name: str) -> None:
    paths = [
        session_name,
        f"{session_name}.session",
        f"{session_name}.session-journal",
        f"{session_name}.session.lock",
        f"{session_name}.session.bak",
    ]
    for path in paths:
        if os.path.exists(path):
            os.remove(path)


def main() -> None:
    for module_name in ALL_MODULES:
        imported_module = importlib.import_module("TEAMZYRO.modules." + module_name)
    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞s 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

    try:
        ZYRO.start()
    except SessionRevoked:
        LOGGER("TEAMZYRO").warning(
            "Telegram session revoked. Removing local Pyrogram session files and retrying startup."
        )
        remove_session_files(SESSION_NAME)
        ZYRO.start()

    application.run_polling(drop_pending_updates=True)
    send_start_message()
    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY GOJOXNETWORK☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

if __name__ == "__main__":
    main()
    
