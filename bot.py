from dotenv import load_dotenv
import os
import discord
from ggcal import calendar_info3 

client = discord.Client()

@client.event
async def on_ready():
    print("on_ready")
    print(client.user.name) #bot name
    print(discord.__version__) #discord.pyのversion
    print("--------")
    await client.change_presence(activity=discord.Game(name = ""))

load_dotenv()
categoryId = int(os.environ['categoryId'])
timesId = int(os.environ['timesId'])
mokumokuId = int(os.environ['mokumokuId'])

#times投稿
@client.event
async def on_message(message):
    #botの送信ははじく
    if message.author.bot:
        return

    if message.content == "calendar":
        await message.channel.send(calendar_info3()[0][0])

    #timesカテゴリのみを監視、timelineチャンネルは無視
    if message.channel.category_id == categoryId and message.channel.id != timesId:
        await client.get_channel(timesId).send(message.channel.mention + " " + message.author.name + "\n" + message.content)
        
        if message.attachments:
            for i in message.attachments:
                await client.get_channel(timesId).send(i)

#もくもく会入室通知
@client.event
async def on_voice_state_update(member, before, after):
    if after.channel.id == mokumokuId and after is not before and after.self_mute is before.self_mute and after.self_stream is before.self_stream and after.self_deaf is before.self_deaf:
        await client.get_channel(timesId).send("<#" + str(mokumokuId) + ">" + " " + member.name + "\n" + "もくもく会に参加しました")



TOKEN = os.environ['TOKEN']
client.run(TOKEN)