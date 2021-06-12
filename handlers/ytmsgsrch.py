# Original Code From DaisyXMusic
# Copyright (C) 2021  Inuka asith 


# the logging things
import logging

from pyrogram.types import Message
from search_engine_parser import GoogleSearch
from youtube_search import YoutubeSearch
from pyrogram import Client, filters

from helpers.database import db, Database
from helpers.dbthings import handle_user_status
from config import LOG_CHANNEL

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

import pyrogram

logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(filters.private)
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)

@Client.on_message(pyrogram.filters.command(["ytsearch", "ytsearch@MusicsNexa_bot"]))
async def ytsearch(_, message: Message):
    chat_id = message.from_user.id
        if not await db.is_user_exist(chat_id):
            await db.add_user(chat_id)
            await Client.send_message(
        chat_id=LOG_CHANNEL,
        text=f"**📢 News ** \n#New_Music_Lover **Started To Using Meh!** \n\nFirst Name: `{message.from_user.first_name}` \nUser ID: `{message.from_user.id}` \nProfile Link: [{message.from_user.first_name}](tg://user?id={message.from_user.id})",
        parse_mode="markdown"
    )
    try:
        if len(message.command) < 2:
            await message.reply_text("`/ytsearch` needs an argument!")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("**Searching For Your Keyword** 😒")
        results = YoutubeSearch(query, max_results=4).to_dict()
        thumb = "https://telegra.ph/file/a4b7d13da17c3cc828ab9.jpg"
        i = 0
        text = ""
        while i < 4:
            text += f"Title - {results[i]['title']}\n"
            text += f"Duration - {results[i]['duration']}\n"
            text += f"Views - {results[i]['views']}\n"
            text += f"Channel - {results[i]['channel']}\n"
            text += f"https://youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.delete()
        await m.reply_photo(thumb, caption=text)
    except Exception as e:
        await message.reply_text(str(e))
