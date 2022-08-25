from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import time
import discord
from discord.ext import tasks
from ggcal import calendar_info1 

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
day = datetime.now().day
schedule = calendar_info1()
@tasks.loop(seconds=60)
async def scheduling_notice():
    global day
    global schedule
    now = datetime.now()
    if day - now.day == 1:
        schedule = calendar_info1()
        day = datetime.now().day
    
    day_time = str(schedule[0]).split("T")
    sche_day = str(day_time[0]).split("-")
    sche_time = str(day_time[1]).split(":")

    sche_datetime = datetime(year=int(sche_day[0]), month=int(sche_day[1]), day=int(sche_day[2]), hour=int(sche_time[0]), minute=int(sche_time[1]))

    if timedelta(hours=23, minutes=59, seconds=57) <= sche_datetime - now <= timedelta(days=1, seconds=3):
        await client.get_channel(noticeId).send(f"`{sche_datetime}`より`{schedule[1]}`があります")

    print(now)
    print(sche_datetime)
    print(sche_datetime - now)
    print(timedelta(hours=23, minutes=59, seconds=57) <= sche_datetime - now <= timedelta(days=1, seconds=3))
    print("\n")



TOKEN = os.environ['TOKEN']
client.run(TOKEN)