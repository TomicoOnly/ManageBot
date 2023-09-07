import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import YouBlockedUser
from Manage import app, bot1

__MODULE__ = "SangMata"
__HELP__ = "/sg - mengambil info history dari pengguna"

@app.on_message(filters.command("sg"))
async def sangmata(client, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("Balas ke pesan pengguna atau berikan ID pengguna")
        user = message.text.split(None, 1)[1]
        user = await app.get_users(user)
        user_id = user.id
        mention = user.mention
    else:
        user_id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.mention
    meira = await message.edit("mencari")
    bot = "SangMata_beta_bot"
    try:
        await bot1.send_message(bot, f"{user_id}")
    except YouBlockedUser:
        await bot1.unblock_user(bot)
        await bot1.send_message(bot, f"{user_id}")
    await asyncio.sleep(1)
    
    async for stalk in bot1.search_messages(bot, query="Name", limit=1):
        if not stalk:
            await meira.edit_text("**Orang Ini Belum Pernah Mengganti Namanya**")
            return
        elif stalk:
            await meira.edit(stalk.text)
            await stalk.delete()

    async for stalk in bot1.search_messages(bot, query="Username", limit=1):
        if not stalk:
            return
        elif stalk:
            await meira.reply(stalk.text)
            await stalk.delete()        
    