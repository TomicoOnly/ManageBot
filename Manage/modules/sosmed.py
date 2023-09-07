import asyncio
import requests
from pyrogram import filters, Client, enums
from pyrogram.types import Message
from Manage import app, bot1, BOT_NAME

__MODULE__ = "Sosmed"
__HELP__ = "/sosmed - download media dari sosmed"

@app.on_message(filters.command("sosmed"))
async def sosmed_down(client, message):
    if len(message.command) < 2:
        return await message.reply("berikan link sosmed")
    meira = await message.reply("Processing...")
    link = message.text.split()[1]
    bot = "thisvidbot"
    await bot1.unblock_user(bot)
    xnxx = await bot1.send_message(bot, link)
    await asyncio.sleep(8)
    async for sosmed in bot1.search_messages(bot):
        if sosmed.video:
            try:
                await bot1.download_media(sosmed)
                await meira.delete()
                await client.send_photo(message.chat.id, sosmed, caption=f"**powered by{BOT_NAME}**")
                await sosmed.delete()
                await xnxx.delete()
            except Exception as e:
                await xnxx.edit(e)
        else :
            await message.reply("eror, bot tidak merespon")