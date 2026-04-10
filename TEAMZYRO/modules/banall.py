import asyncio

from pyrogram import filters
from pyrogram.errors import BadRequest, ChatAdminRequired

from TEAMZYRO import OWNER_ID, SUDO, app

ALLOWED_USERS = SUDO + [OWNER_ID]


@app.on_message(filters.command("banall") & filters.private & filters.user(ALLOWED_USERS))
async def ban_all_members(client, message):
    args = message.text.strip().split(maxsplit=1)
    if len(args) < 2:
        return await message.reply_text(
            "Usage: /banall <group_id_or_username>\nExample: /banall -1001234567890"
        )

    chat_identifier = args[1].strip()
    try:
        chat = await client.get_chat(chat_identifier)
    except BadRequest as exc:
        return await message.reply_text(f"Unable to resolve chat: {exc.message}")
    except Exception as exc:
        return await message.reply_text(f"Failed to get chat: {exc}")

    if chat.type not in ["group", "supergroup"]:
        return await message.reply_text("Please provide a valid group or supergroup chat ID.")

    status_message = await message.reply_text(
        f"Starting banall in {chat.title or chat.id} ({chat.id})...\nGathering members..."
    )

    members_to_ban = []
    bot_id = (await client.get_me()).id

    async for member in client.iter_chat_members(chat.id):
        user = member.user
        if user.id == bot_id:
            continue
        members_to_ban.append(user.id)

    if not members_to_ban:
        return await status_message.edit_text("No members found to ban in that group.")

    total = len(members_to_ban)
    success = 0
    failed = 0

    for start in range(0, total, 100):
        batch = members_to_ban[start : start + 100]
        tasks = [client.ban_chat_member(chat.id, user_id) for user_id in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                failed += 1
            else:
                success += 1

        if start + 100 < total:
            await status_message.edit_text(
                f"Banned {success} of {total} members so far...\nFailed: {failed}"
            )
            await asyncio.sleep(1)

    await status_message.edit_text(
        f"Banall complete.\nTotal processed: {total}\nSuccessfully banned: {success}\nFailed: {failed}"
    )
