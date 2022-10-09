"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import discord
from discord import Intents
from google.cloud import texttospeech
import os
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
CHANNEL_ID = os.environ['CHANNEL_ID']

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
async def on_message(message):
    global voiceChannel
    if message.author.bot:
        return
    if message.channel.id == int(CHANNEL_ID):
        if message.content == '!con':
            with open("output.txt", "wb") as out:
                out.write(response.text_content)
                print('Text content written to file "output.txt"')
        else:
            return

client.run(TOKEN)

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput("message.txt")

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)
# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')
    

if __name__ == '__main__':
    creat_MP3('outpu.mp3')