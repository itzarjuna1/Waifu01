import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait, ChatAdminRequired

from TEAMZYRO import app, OWNER_ID, SUDO
from TEAMZYRO.modules.upload import get_random_waifu
from TEAMZYRO.modules.joinlog import get_all_groups  # adjust if needed

# ===============================
# PERMISSION CHECK
# ===============================

def is_authorized(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in SUDO


# ===============================
# WAIFU SENDER
# ===============================

async def send_waifu(chat_id: int):
    waifu = get_random_waifu()
    if not waifu:
        return

    await app.send_photo(
        chat_id,
        photo=waifu["image"],
        caption=(
            f"💖 **A Wild Waifu Appeared!**\n\n"
            f"👤 **{waifu['name']}**\n"
            f"🎌 {waifu['anime']}\n"
            f"⭐ **Rarity:** {waifu['rarity']}\n\n"
            f"⚔️ Use /claim to claim!"
        )
    )


# ===============================
# MANUAL DROP
# ===============================

@app.on_message(filters.command(["drop", "waifu"]) & filters.group)
async def manual_drop(client, message):
    try:
        me = await client.get_chat_member(message.chat.id, "me")
        if not me.privileges or not me.privileges.can_send_messages:
            return await message.reply_text("❌ I need admin permission.")
    except ChatAdminRequired:
        return await message.reply_text("❌ Make me admin first.")

    await send_waifu(message.chat.id)


# ===============================
# AUTO UPLOAD LOOP
# ===============================

auto_upload_task = None


async def auto_upload_loop(interval: int):
    while True:
        for chat_id in get_all_groups():
            try:
                await send_waifu(chat_id)
                await asyncio.sleep(2)
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

    # 🔥 THIS WAS MISSING
    if not message.from_user:
        return await message.reply_text(
            "❌ Disable anonymous admin mode."
        )

    if not is_authorized(message.from_user.id):
        return await message.reply_text("❌ Only owner / sudo can use this.")

    if len(message.command) != 2:
        return await message.reply_text(
            "❌ Usage:\n`/autoupload <seconds>`"
        )

    try:
        interval = int(message.command[1])
        if interval < 60:
            return await message.reply_text(
                "⚠️ Interval must be at least 60 seconds."
            )
    except ValueError:
        return await message.reply_text("❌ Invalid number.")

    if auto_upload_task and not auto_upload_task.done():
        return await message.reply_text("⚠️ Auto upload already running.")

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

    if not message.from_user:
        return await message.reply_text(
            "❌ Disable anonymous admin mode."
        )

    if not is_authorized(message.from_user.id):
        return await message.reply_text("❌ Only owner / sudo can use this.")

    if not auto_upload_task:
        return await message.reply_text("⚠️ Auto upload is not running.")

    auto_upload_task.cancel()
    auto_upload_task = None

    await message.reply_text("🛑 **Auto Waifu Upload Stopped**")
