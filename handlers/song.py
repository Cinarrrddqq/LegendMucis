import os
import requests
import aiohttp
import yt_dlp
import wget

from pyrogram import Client, filters
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

from config import BOT_USERNAME
from helpers.filters import command



@Client.on_message(command(["song"]))
def bul(client, message):

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    
    query = " ".join(message.command[1:])
    m = message.reply("<b>Şarkınız Aranıyor ... 🔍</b>")
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
        m.edit("<b>❌ Üzgünüm şarkı bulunamadı.\n\n Lütfen başka şarkı ismi söyleyin.</b>")
        print(str(e))
        return
    m.edit("<b>📥 İndirme İşlemi Başladı...</b>")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"**╭───────────────**\n**├▷ ♬ Başlık: [{title[:35]}]({link})**\n**├───────────────**\n**├▷♬ Playlist @SongBotPlaylist**\n**╰───────────────**"
        res = f"**╭───────────────**\n**├▷ ♬ Başlık: [{title[:35]}]({link})**\n**├───────────────**\n**├▷👤 İsteyen** [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n**├───────────────**\n**├▷🌀 Bot: @{Config.BOT_USERNAME}**\n**╰───────────────**"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("📤 Yükleniyor..")
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name, performer="QocayefhMusic")
        m.delete()
        bot.send_audio(chat_id=Config.PLAYLIST_ID, audio=audio_file, caption=res, performer="QocayefhMusic", parse_mode='md', title=title, duration=dur, thumb=thumb_name)
    except Exception as e:
        m.edit("<b>❌ Hatanın, düzelmesini bekleyiniz.</b>")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

