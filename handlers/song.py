

import asyncio
import math
import os
import time
from random import randint
from urllib.parse import urlparse

import aiofiles
import aiohttp
import requests
import yt_dlp
from config import BOT_NAME as bn
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

from helpers.decorators import humanbytes
from helpers.filters import command, other_filters


ydl_opts = {
    'format': 'best',
    'keepvideo': True,
    'prefer_ffmpeg': False,
    'geo_bypass': True,
    'outtmpl': '%(title)s.%(ext)s',
    'quite': True
}


@Client.on_message(command(["song", f"song@{bn}"]) & ~filters.edited)
def song(_, message):
    query = " ".join(message.command[1:])
    m = message.reply(" 𝙋𝙧𝙤𝙘𝙚𝙨𝙨𝙞𝙣𝙜...𝙃𝙤𝙡𝙙 𝙊𝙣...")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit("**𝙒𝙝𝙞𝙘𝙝 𝙎𝙤𝙣𝙜 𝙔𝙤𝙪 𝙒𝙖𝙣𝙩 ??**\n𝙐𝙨𝙖𝙜𝙚`/song <song name>`")
        print(str(e))
        return
    m.edit(" 𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙𝙞𝙣𝙜...𝙔𝙤𝙪𝙧 𝙒𝙞𝙨𝙝...")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"**🎧 𝙐𝙥𝙡𝙤𝙖𝙙𝙚𝙙 𝘽𝙮 @Alone_boy_xd_01**"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit(" 𝙐𝙥𝙡𝙤𝙖𝙙𝙞𝙣𝙜...𝙔𝙤𝙪𝙧 𝙎𝙤𝙣𝙜...")
        message.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            parse_mode="md",
            title=title,
            duration=dur,
        )
        m.delete()
    except Exception as e:
        m.edit("𝙁𝙖𝙞𝙡𝙚𝙙 𝙩𝙤 𝙛𝙞𝙣𝙙 𝙩𝙝𝙖𝙩 𝙨𝙤𝙣𝙜")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


@Client.on_message(
    command(["vsong", f"vsong@{bn}", "video", f"video@{bn}"]) & ~filters.edited
)
async def vsong(client, message):
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        message.from_user.mention
    except Exception as e:
        print(e)
    try:
        msg = await message.reply(" **𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙𝙞𝙣𝙜... 𝙔𝙤𝙪𝙧 𝙑𝙞𝙙𝙚𝙤...**")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"𝙁𝙖𝙞𝙡𝙚𝙙 𝙏𝙤 𝙁𝙞𝙣𝙙 𝙔𝙤𝙪𝙧 𝙑𝙞𝙙𝙚𝙤...𝙎𝙤𝙧𝙧𝙮😔")
    preview = wget.download(thumbnail)
    await msg.edit("**𝙐𝙥𝙡𝙤𝙖𝙙𝙞𝙣𝙜...𝙔𝙤𝙪𝙧 𝙑𝙞𝙙𝙚𝙤**")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data["title"],
    )
    try:
        os.remove(file_name)
        await msg.delete()
    except Exception as e:
        print(e)


@Client.on_message(command(["lyric", f"lyric@{bn}"]))
async def lyrics(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("» **give a lyric name too.**")
            return
        query = message.text.split(None, 1)[1]
        rep = await message.reply_text("**𝙎𝙚𝙖𝙧𝙘𝙝𝙞𝙣𝙜...𝙒𝙖𝙞𝙩 𝙇'𝙞𝙡 𝘽𝙞𝙩**")
        resp = requests.get(
            f"https://api-tede.herokuapp.com/api/lirik?l={query}"
        ).json()
        result = f"{resp['data']}"
        await rep.edit(result)
    except Exception:
        await rep.edit("❌ **𝙉𝙤 𝙎𝙪𝙘𝙝 𝙩𝙮𝙥𝙚 𝙊𝙛 𝙇𝙮𝙧𝙞𝙘𝙨 𝙁𝙤𝙪𝙣𝙙 ...𝙎𝙥𝙚𝙡𝙡 𝘾𝙤𝙧𝙧𝙚𝙘𝙩𝙡𝙮.**")
