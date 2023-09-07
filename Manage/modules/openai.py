import openai
from pyrogram import filters

from Manage import app
from Manage.core.decorators.errors import capture_err
from os import getenv
OPENAI_API = getenv("OPENAI_API")

__MODULE__ = "OpenAI"
__HELP__ = "/ai - Bertanya via OpenAI"


class OpenAi:
    def text(self):
        openai.api_key = OPENAI_API
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"<b>Q: <code>{self}</code>\nA:</b>",
            temperature=0,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].text

    def photo(self):
        openai.api_key = OPENAI_API
        response = openai.Image.create(prompt=self, n=1, size="1024x1024")
        return response["data"][0]["url"]
    
@app.on_message(filters.command("ai"))
@capture_err    
async def ai(client, message):
    if len(message.command) == 1:
        return await message.edit_text(
            f"Ketik <code>/ask [pertanyaan]</code> untuk menggunakan OpenAI"
        )
    msg = await message.edit_text("`Memproses...`")
    meira = message.text.split(None, 1)[1]
    try:
        response = OpenAi.text(meira)
        await msg.edit_text(f"**Q:** {meira}\n\n**A:** {response}")
    except Exception as e:
        await msg.edit_text(f"**Terjadi Kesalahan!!\n`{e}`**")