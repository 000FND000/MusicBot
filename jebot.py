#    Copyright (c) 2021 Infinity BOTs <https://t.me/Infinity_BOTs>
 
#    This program is free software: you can redistribute it and/or modify  
#    it under the terms of the GNU General Public License as published by  
#    the Free Software Foundation, version 3.
# 
#    This program is distributed in the hope that it will be useful, but 
#    WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
#    General Public License for more details.

import os
import aiohttp
from pyrogram import filters, Client
from pytube import YouTube
from youtubesearchpython import VideosSearch
from sample_config import Config
from ut import get_arg

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


Jebot = Client(
   "Song Downloader",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()


@Jebot.on_message(filters.command("s"))
async def song(client, message):
    message.chat.id
    user_id = message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("<b>Enter a song name❗\n\nExample: `/s satisfya`</b>")
        return ""
    status = await message.reply(
             text="<b>Downloading your song, Plz wait 🥺\n\nDev @ImJanindu 🇱🇰</b>",
             disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "Join Channel", url="https://t.me/Infinity_BOTs"
                                    )
                                ]
                            ]
                        ),
               parse_mode="html",
        reply_to_message_id=message.message_id
      )
    video_link = yt_search(args)
    if not video_link:
        await status.edit("<b>Song not found 😑</b>")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("<b>Failed to download song 🤕</b>")
        LOGGER.error(ex)
        return ""
    os.rename(download, f"{str(user_id)}.mp3")
    await Jebot.send_chat_action(message.chat.id, "upload_audio")
    await Jebot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")

@Jebot.on_message(filters.command("start"))
async def start(client, message):
   await Jebot.send_message(
           chat_id=message.chat.id,
           text="""<b>Hey There, I'm a Song Downloader Bot

Made by @Infinity_BOTs 🇱🇰

Hit /help  to find out more about how to use me</b>""",   
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "Help", callback_data="help"
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        "Developer", url="https://t.me/ImJanindu"
                                    )
                                ]
                            ]
                        ),        
        disable_web_page_preview=True,        
        parse_mode="html",
        reply_to_message_id=message.message_id
    )

static_data_filter = filters.create(
    lambda _, __, query: query.data == "help"
)

@Jebot.on_callback_query(static_data_filter)
def help(client, cb):
    await Jebot.edit_message(
           chat_id=message.chat.id,
           text="""<b>Send <code>/s [song name]</code> to download song

Example: <code>/s satisfya</code>

~ @Infinity_BOTs</b>""",
           parse_mode="html",
        reply_to_message_id=message.message_id
    )

Jebot.run()
