import asyncio
import requests
from pyrogram import filters, Client, enums
from pyrogram.types import Message
from Manage import app, bot1, BOT_NAME
from Manage.core.decorators.errors import capture_err

__MODULE__ = "Toanime"
__HELP__ = "/toanime - merubah foto menjadi anime style photo"

__MODULE__ = "Tulis"
__HELP__ = "/tulis - merubah text menjadi tulisan tangan"


@app.on_message(filters.command("toanime"))
@capture_err
async def convert_image(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.edit("**Mohon Balas Pesan Ini Ke Media**")
    if message.reply_to_message:
        await message.edit("`processing ...`")
    reply_message = message.reply_to_message
    photo = reply_message.photo.file_id
    bot = "qq_neural_anime_bot"
    xxx = await bot1.send_photo(bot, photo=photo)
    await asyncio.sleep(30)
    await message.delete()
    async for result in bot1.search_messages(bot, filter=enums.MessagesFilter.PHOTO, limit=1):
        if result.photo:
            await bot1.download_media(result)
            await client.send_photo(message.chat.id, result, caption=f"**powered by{BOT_NAME}**")
            await result.delete()
            await xxx.delete()
        else :
            await message.reply("eror, bot tidak merespon")

@app.on_message(filters.command("tulis"))
async def handwrite(client, message):
    if message.reply_to_message:
        input_txt = message.reply_to_message.text
    else:
        input_txt = message.text.split(None, 1)[1]
    msg_procces = await message.reply("`Processing...`")
    output_txt = requests.get(f"https://api.sdbots.tk/write?text={input_txt}").url
    await message.reply_photo(
        photo=output_txt,
        caption=f"**Powered by {BOT_NAME}**")
    await msg_procces.delete()