import asyncio
import random
from pyrogram import filters
from TEAMZYRO import app, OWNER_ID, SUDO, collection

print("🔥 gupload module loaded")

AUTO_TASK = None


def is_admin(user_id: int):
    return user_id == OWNER_ID or user_id in SUDO


def get_random_waifu():
    waifus = list(collection.find())
    if not waifus:
        return None
    return random.choice(waifus)


@app.on_message(filters.command("drop") & filters.group)
async def manual_drop(_, message):
    if not is_admin(message.from_user.id):
        return await message.reply_text("❌ Only owner / sudo can drop waifus")

    waifu = get_random_waifu()
    if not waifu:
        return await message.reply_text("❌ No waifus found in database")

    await message.reply_photo(
        waifu["photo"],
        caption=f"💖 **{waifu['name']}**\n🎬 {waifu['anime']}\n⭐ Rarity: {waifu['rarity']}"
    )


@app.on_message(filters.command("autoupload") & filters.group)
async def start_autoupload(_, message):
    global AUTO_TASK

    if not is_admin(message.from_user.id):
        return await message.reply_text("❌ Only owner / sudo can use this")

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
            waifu = get_random_waifu()
            if waifu:
                await app.send_photo(
                    message.chat.id,
                    waifu["photo"],
                    caption=f"💖 **{waifu['name']}**\n🎬 {waifu['anime']}\n⭐ Rarity: {waifu['rarity']}"
                )
            await asyncio.sleep(interval)

    AUTO_TASK = asyncio.create_task(uploader())
    await message.reply_text(f"✅ Auto upload started every `{interval}` seconds")


@app.on_message(filters.command("stopupload") & filters.group)
async def stop_autoupload(_, message):
    global AUTO_TASK

    if not is_admin(message.from_user.id):
        return await message.reply_text("❌ Only owner / sudo can stop this")

    if AUTO_TASK:
        AUTO_TASK.cancel()
        AUTO_TASK = None
        await message.reply_text("🛑 Auto upload stopped")
    else:
        await message.reply_text("⚠ No active auto upload running")
