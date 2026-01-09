import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait, ChatAdminRequired

from TEAMZYRO import app
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

# ===============================
# Helpers
# ===============================

def is_sudo(user_id: int) -> bool:
    return user_id in SUDO_USERS or user_id == OWNER_ID


async def send_waifu(chat_id: int):
    waifu = get_random_waifu()
    if not waifu:
        return

    await app.send_photo(
        chat_id=chat_id,
        photo=waifu["image"],
        caption=(
            f"💖 **A Wild Waifu Appeared!**\n\n"
            f"👤 **{waifu['name']}**\n"
            f"🎌 {waifu['anime']}\n"
            f"⭐ **Rarity:** {waifu['rarity']}\n\n"
            f"⚔️ Use /claim to claim her!"
        )
    )


# ===============================
# MANUAL DROP COMMAND
# ===============================

@app.on_message(filters.command(["drop", "waifu"]) & filters.group)
async def manual_waifu_drop(client, message):
    try:
        me = await client.get_chat_member(message.chat.id, "me")
        if not me.privileges or not me.privileges.can_send_messages:
            return await message.reply_text("❌ I need admin permission.")
    except ChatAdminRequired:
        return await message.reply_text("❌ Make me admin first.")

    await send_waifu(message.chat.id)


# ===============================
# AUTO UPLOAD LOGIC
# ===============================

auto_upload_task = None


async def auto_upload_loop(interval: int):
    while True:
        groups = get_all_groups()

        for chat_id in groups:
            try:
                await send_waifu(chat_id)
                await asyncio.sleep(2)  # flood safety

            except FloodWait as e:
                await asyncio.sleep(e.value)

            except Exception:
                continue

        await asyncio.sleep(interval)


# ===============================
# START AUTO UPLOAD
# ===============================

@app.on_message(filters.command("autoupload") & filters.group)
async def start_auto_upload(_, message):
    global auto_upload_task

    if not is_sudo(message.from_user.id):
        return await message.reply_text("❌ Only **sudo / owner** can use this.")

    if len(message.command) != 2:
        return await message.reply_text(
            "❌ Usage:\n`/autoupload <time_in_seconds>`"
        )

    try:
        interval = int(message.command[1])
        if interval < 60:
            return await message.reply_text(
                "⚠️ Interval must be **at least 60 seconds**."
            )
    except ValueError:
        return await message.reply_text("❌ Time must be a number.")

    if auto_upload_task and not auto_upload_task.done():
        return await message.reply_text("⚠️ Auto upload is already running.")

    auto_upload_task = app.loop.create_task(auto_upload_loop(interval))

    await message.reply_text(
        f"✅ **Auto Waifu Upload Started**\n"
        f"⏱ Interval: `{interval}` seconds"
    )


# ===============================
# STOP AUTO UPLOAD
# ===============================

@app.on_message(filters.command("stopupload") & filters.group)
async def stop_auto_upload(_, message):
    global auto_upload_task

    if not is_sudo(message.from_user.id):
        return await message.reply_text("❌ Only **sudo / owner** can use this.")

    if not auto_upload_task:
        return await message.reply_text("⚠️ Auto upload is not running.")

    auto_upload_task.cancel()
    auto_upload_task = None

    await message.reply_text("🛑 **Auto Waifu Upload Stopped**")
