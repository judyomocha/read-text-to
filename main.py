# @title
from turtledemo.minimal_hanoi import play

import discord
import asyncio
import os
import subprocess
import ffmpeg
import html
import pickle
import numpy as np

from collections import defaultdict, deque
from pathlib import Path
from discord import Intents
from google.cloud import texttospeech
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from source import creat_MP3
from discord.player import FFmpegPCMAudio
from discord.channel import VoiceChannel
from dotenv import load_dotenv

CHANNEL_ID = os.environ['CHANNEL_ID']
TOKEN = os.environ['TOKEN']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

def get_credentials(client_secret_file, scopes,
                    token_storage_pkl='token.pickle'):
    creds = None
    # token.pickleファイルにユーザのアクセス情報とトークンが保存される
    # ファイルは初回の認証フローで自動的に作成される
    if os.path.exists(token_storage_pkl):
        with open(token_storage_pkl, 'rb') as token:
            creds = pickle.load(token)

    # 有効なクレデンシャルがなければ、ユーザーにログインしてもらう
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file, scopes=scopes)
            creds = flow.run_local_server(port=0)

        # クレデンシャルを保存（次回以降の認証のため）
        with open(token_storage_pkl, 'wb') as token:
            pickle.dump(creds, token)

    return creds


intents: Intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Login!!!')



@client.event
@client.event
async def on_message(message):
    global voiceChannel
    if message.author.bot:
        return
    if message.channel.id == int(CHANNEL_ID):
        if message.content == '!con':
            voiceChannel = await VoiceChannel.connect(message.author.voice.channel)
            await message.channel.send('読み上げるよ！')
            return
        if message.content == '!en':
            voiceChannel.stop()
            await message.channel.send('またね！')
            await voiceChannel.disconnect()
            return
        else:
            discord.VoiceClient = VoiceChannel.connect(message.author.voice.channel)
            discord.VoiceClient.play(discord.FFmpegPCMAudio("output.mp3"))



client.run(TOKEN)