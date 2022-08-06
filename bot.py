# from discord.ext import commands,tasks
from unicodedata import category
from dotenv import load_dotenv
import os
import discord

client = discord.Client()

@client.event
async def on_ready():
    print("on_ready")
    print(client.user.name) #bot name
    print(discord.__version__) #discord.pyのversion
    print("--------")
    await client.change_presence(activity=discord.Game(name = "under development"))

load_dotenv()
categoryId = int(os.environ['categoryId'])
timesId = int(os.environ['timesId'])

@client.event
async def on_message(message):
    #botの送信ははじく
    if message.author.bot:
        return

    #timesカテゴリのみを監視、timelineチャンネルは無視
    if message.channel.category_id == categoryId and message.channel.id != timesId:
        await client.get_channel(timesId).send(message.channel.mention + " " + message.author.name + "\n" + message.content)
        
        if message.attachments:
            for i in message.attachments:
                await client.get_channel(timesId).send(i)


TOKEN = os.environ['TOKEN']
client.run(TOKEN)