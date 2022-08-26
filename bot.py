from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import time
import discord
from discord.ext import tasks
from ggcal import calendar_info3, to_datetime, ctrl_index

client = discord.Client()

@client.event
async def on_ready():
    print("on_ready")
    print(client.user.name) #bot name
    print(discord.__version__) #discord.pyのversion
    print("--------")
    print(f"waiting {60 - datetime.now().second} sec for loop to start")
    time.sleep(60 - datetime.now().second)
    scheduling_notice.start()

    await client.change_presence(activity=discord.Game(name = ""))

load_dotenv()
categoryId = int(os.environ['categoryId'])
timesId = int(os.environ['timesId'])
mokumokuId = int(os.environ['mokumokuId'])
noticeId = int(os.environ['noticeId'])


@client.event
async def on_message(message):
    #botの送信ははじく
    if message.author.bot:
        return


    #times投稿
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

#予定通知
day = (datetime.now()).day
schedule = calendar_info3()
sche_index = ctrl_index(datetime.now(), schedule)
@tasks.loop(seconds=60)
async def scheduling_notice():
    global day
    global schedule
    global sche_index
    now = datetime.now()

    sche_datetime = to_datetime(schedule[sche_index])
    
    if timedelta(hours=23, minutes=59, seconds=55) <= sche_datetime - now <= timedelta(days=1, seconds=5):
        await client.get_channel(noticeId).send(f"`{sche_datetime}`より`{schedule[sche_index][1]}`があります")

    sche_index = ctrl_index(now, schedule)
    if now.day - day == 1 or sche_index == None:
        print("update\n")
        day = now.day
        schedule = calendar_info3()
        sche_index = ctrl_index(now, schedule)

    print(now)
    print(sche_datetime)
    print(sche_datetime - now)
    print(timedelta(hours=23, minutes=59, seconds=57) <= sche_datetime - now <= timedelta(days=1, seconds=3))
    print("\n")

TOKEN = os.environ['TOKEN']
client.run(TOKEN)