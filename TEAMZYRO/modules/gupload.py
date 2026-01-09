import asyncio
import random
from pyrogram import filters
from TEAMZYRO import app, OWNER_ID, SUDO, db
from TEAMZZYRO.__init__ import CHARA_CHANNEL_ID

print("🔥 gupload module loaded")

AUTO_TASK = None

waifu_logs = db.waifu_logs   # collection name


def is_admin(uid: int):
    return uid == OWNER_ID or uid in SUDO


def get_random_waifu_msg():
    data = list(waifu_logs.find())
    if not data:
        return None
    return random.choice(data)


# 🔹 MANUAL DROP
@app.on_message(filters.command("drop") & filters.group)
async def manual_drop(_, message):
    if not is_admin(message.from_user.id):
        return

    waifu = get_random_waifu_msg()
    if not waifu:
        return await message.reply_text("❌ No waifus stored")

    await app.copy_message(
        chat_id=message.chat.id,
        from_chat_id=CHARA_CHANNEL_ID,
        message_id=waifu["msg_id"]
    )


# 🔹 AUTO UPLOAD
@app.on_message(filters.command("autoupload") & filters.group)
async def start_autoupload(_, message):
    global AUTO_TASK

    if not is_admin(message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text("Usage: `/autoupload <seconds>`")

    try:
        interval = int(message.command[1])
        if interval < 10:
            return await message.reply_text("⏱ Minimum 10 seconds")
    except ValueError:
        return await message.reply_text("❌ Invalid time")

    if AUTO_TASK:
        AUTO_TASK.cancel()

    async def uploader():
        while True:
            waifu = get_random_waifu_msg()
            if waifu:
                await app.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=CHARA_CHANNEL_ID,
                    message_id=waifu["msg_id"]
                )
            await asyncio.sleep(interval)

    AUTO_TASK = asyncio.create_task(uploader())
    await message.reply_text(f"✅ Auto upload started every `{interval}` seconds")


# 🔹 STOP AUTO UPLOAD
@app.on_message(filters.command("stopupload") & filters.group)
async def stop_autoupload(_, message):
    global AUTO_TASK

    if not is_admin(message.from_user.id):
        return

    if AUTO_TASK:
        AUTO_TASK.cancel()
        AUTO_TASK = None
        await message.reply_text("🛑 Auto upload stopped")
    else:
        await message.reply_text("⚠ No auto upload running")
