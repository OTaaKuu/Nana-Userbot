# ffmpeg -i video_1573046696-542963.mp4 -vf scale=500x500 -strict -2 vid.mp4

import asyncio
import subprocess
import os
import asyncio
import requests
import logging
import time
import pafy
import re
import requests
import shutil
import traceback
import sys

from bs4 import BeautifulSoup
from pathlib import Path

from nana import app, Command, Owner
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton
from nana.helpers.parser import cleanhtml, escape_markdown
from nana.modules.downloads import download_reply_nocall

__MODULE__ = "Video Note"
__HELP__ = """
Video Note Maker

──「 **VN Maker** 」──
-> `mkvn`
Reply a video to make it as video note
"""



@app.on_message(Filters.user("self") & Filters.command(["mkvn"], Command))
async def vn_maker(client, message):
	if message.reply_to_message and message.reply_to_message.video:
		await message.edit("__Downloading...__")
		dlvid = await download_reply_nocall(client, message)
		if dlvid:
			await message.edit("__Converting...__")
			try:
				process = subprocess.Popen("ffmpeg", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			except Exception as err:
				if "The system cannot find the file specified" in str(err) or "No such file or directory" in str(err):
					await message.edit("You need to install ffmpeg first!\nCheck your saved messages for more information!")
					await client.send_message(Owner, "Hello 🙂\nYou need to install ffmpeg to make audio works better, here is guide how to install it:\n\n**If you're using linux**, go to your terminal, type:\n`sudo apt install ffmpeg`\n\n**If you're using Windows**, download ffmpeg here:\n`https://ffmpeg.zeranoe.com/builds/`\nAnd then extract (if was archive), and place ffmpeg.exe to workdir (in current dir)\n\n**If you're using heroku**, type this in your workdir:\n`heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git`\nOr if you not using heroku term, follow this guide:\n1. Go to heroku.com\n2. Go to your app in heroku\n3. Change tabs/click Settings, then search for Buildpacks text\n4. Click button Add build pack, then type `https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest`\n5. Click Save changes, and you need to rebuild your heroku app to take changes!\n\nNeed help?\nGo @AyraSupport and ask there")
					return
			os.system(f'''ffmpeg -loglevel panic -i "{dlvid}" -vf scale="'if(gt(iw,ih),-1,299):if(gt(iw,ih),299,-1)', crop=299:299" -strict -2 -y "{dlvid}_converted.mp4"''')
			# ffmpeg -i video_1573046696-542963.mp4 -vf scale=500x500 -strict -2 vid.mp4
			await client.send_video_note(message.chat.id, f"{dlvid}_converted.mp4", reply_to_message_id=message.reply_to_message.message_id)
			await message.delete()
			os.remove(dlvid)
			os.remove(dlvid+"_converted.mp4")
