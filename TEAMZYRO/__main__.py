from TEAMZYRO import *
import importlib
import logging
import asyncio
from TEAMZYRO.modules import ALL_MODULES

# ---------------- SAFE START MESSAGE -----------------
async def send_start_message():
    """
    Safely send the bot start message/photo to GLOG chat.
    Prevents crashing if chat ID is invalid.
    """
    try:
        chat_id = int(GLOG)  # Ensure numeric ID
    except ValueError:
        print(f"GLOG is not numeric: {GLOG}. Skipping start message.")
        return

    try:
        await application.bot.send_photo(
            chat_id=chat_id,
            photo=PHOTO_URL[0],
            caption="🤖 Bot started successfully! ✅"
        )
        print("Start message sent ✅")
    except Exception as e:
        print(f"Failed to send start message: {e}")

# ---------------- SAFE POST INIT -----------------
async def post_init(application):
    # Start Pyrogram safely inside PTB loop
    await ZYRO.start()

    # Send start message after bot fully starts
    await send_start_message()


# ---------------- MAIN FUNCTION -----------------
def main() -> None:
    # Load all modules safely
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)
        
    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

    # Assign post_init function to the application
    application.post_init = post_init

    # Run the bot with polling
    application.run_polling(
        drop_pending_updates=True,
        close_loop=False
    )

    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY GOJOXNETWORK☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )


# ---------------- RUN BOT -----------------
if __name__ == "__main__":
    main()
