import asyncio
from pyrogram import filters
from Manage import app

__MODULE__ = "TagAll"
__HELP__ = """/all - tag semua anggota group.
/cancel - membatalkan tagall


You can use markdown or html to save text too.

Checkout /markdownhelp to know more about formattings and other syntax.
"""


spam_chats = set()

@app.on_message(filters.command(["tagall", "all"]))
async def mention_all(client, message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        await message.reply("__This command can only be used in groups and channels!__")
        return

    is_admin = False
    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status in ["administrator", "creator"]:
            is_admin = True
    except Exception as e:
        pass

    if not is_admin:
        await message.reply("__Only admins can use this command!__")
        return

    mode = "text_on_cmd"
    msg = None

    if message.matches:
        msg = message.matches[0].group(1)
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message

    if not msg:
        await message.reply("__Please provide an argument or reply to a message!__")
        return

    spam_chats.add(chat_id)
    usrnum = 0
    usrtxt = ''

    async for member in client.iter_chat_members(chat_id):
        if chat_id not in spam_chats:
            break
        if member.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"👮 [{member.user.first_name}](tg://user?id={member.user.id})\n"
        if usrnum == 5:
            if mode == "text_on_cmd":
                txt = f"{msg}\n\n{usrtxt}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(usrtxt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ''

    try:
        spam_chats.remove(chat_id)
    except KeyError:
        pass

@app.on_message(filters.command("cancel"))
async def cancel_spam(client, message):
    chat_id = message.chat.id
    is_admin = False

    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status in ["administrator", "creator"]:
            is_admin = True
    except Exception as e:
        pass

    if not is_admin:
        await message.reply("__Only admins can use this command!__")
        return

    if chat_id not in spam_chats:
        await message.reply("__No active spam process to cancel...__")
    else:
        spam_chats.remove(chat_id)
        await message.reply("__Cancelled...__")