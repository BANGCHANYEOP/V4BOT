import discord
import asyncio
import datetime
import threading
import os

client = discord.Client()
#channel = ''

radelTime = datetime.datetime.now() + datetime.timedelta(days=365)
tmp_radelTime = datetime.datetime.now() + datetime.timedelta(days=365)
radelTimeString = '99:99:99'

tmp_radelTimeString = ''
radelFlag = False

nowTimeString = '1'

# 1-6에서 생성된 토큰을 이곳에 입력해주세요.
token = os.environ["BOT_TOKEN"]

async def my_background_task():
    await client.wait_until_ready()
    global channel
    global nowTimeString
    global radelTime
    global radelTimeString
    global tmp_radelTimeString
    global radelFlag

    while not client.is_closed:
        now = datetime.datetime.now()
        priv = now + datetime.timedelta(minutes=1)
        privTimeString = priv.strftime('%H:%M:%S')
        nowTimeString = now.strftime('%H:%M:%S')
        print('loop check ' + radelTime.strftime('%H:%M:%S') + ' ' + nowTimeString + ' ' + privTimeString)

        if channel != '':
            if radelTime <= now:
                radelFlag = False
                tmp_radelTime = radelTime
                radelTimeString = '99:99:99'
                radelTime = now
                await client.send_message('비텐-스톤드계곡상류-라드엘 탐 입니다.')


            if radelTime <= priv:
                if radelFlag == False:
                    radelFlag = True
                    await client.send_message('비텐-스톤드계곡상류-라드엘 1분 전 입니다.')

    await asyncio.sleep(1)  # task runs every 60 seconds
client.loop.create_task(my_background_task())

async def joinVoiceChannel():
    channel = client.get_channel("일반")
    await client.join_voice_channel(channel)


# 봇이 구동되었을 때 동작되는 코드입니다.
@client.event
async def on_ready():
    print("Logged in as ")  # 화면에 봇의 아이디, 닉네임이 출력됩니다.
    print(client.user.name)
    print(client.user.id)
    print("===========")

client.loop.create_task(my_background_task())

# 봇이 새로운 메시지를 수신했을때 동작되는 코드입니다.
@client.event
async def on_message(message):
    if message.author.bot:  # 만약 메시지를 보낸사람이 봇일 경우에는
        return None  # 동작하지 않고 무시합니다.

    global channel
    global nowTimeString

    global radelTime

    global radelTimeString

    global tmp_radelTimeString

    global radelFlag

    id = message.author.id  # id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
    channel = message.channel  # channel이라는 변수에는 메시지를 받은 채널의 ID를 담습니다.

    modify = ''
    try:
        hello = message.content
        length = len(hello)  # UTF-8로 인코딩 했을 때 바이트 수를 구함
        print(hello)
        print(length)

        if length == 11:
            hours = hello[6:8]
            minutes = hello[9:11]
            now = datetime.datetime.now()
            now = now.replace(hour=int(hours), minute=int(minutes))
        elif length == 12:
            hours = hello[7:9]
            minutes = hello[10:12]
            now = datetime.datetime.now()
            now = now.replace(hour=int(hours), minute=int(minutes))
        elif length == 10:
            hours = hello[5:7]
            minutes = hello[8:10]
            now = datetime.datetime.now()
            now = now.replace(hour=int(hours), minute=int(minutes))
        else:
            now = datetime.datetime.now()
            nowTimeString = now.strftime('%H:%M:%S')
    except:
        print('exception');
        now = datetime.datetime.now()
        nowTimeString = now.strftime('%H:%M:%S')

    if message.content.startswith('!라드엘 컷'):
        radelFlag = False
        radelTime = nextTime = now + datetime.timedelta(minutes=1)
        print(nextTime)
        tmp_radelTimeString = radelTimeString = nextTime.strftime('%H:%M:%S')
        await message.channel.send('다음 라드엘 ' + radelTimeString)

    if message.content.startswith('!불러오기'):
        file = open("D:\my_bot.db", 'r')

        while True:
            line = file.readline();

            if not line: break

            # await message.channel.send(channel, line)

            if (line.startswith('라드엘 : ')):
                hours = line[8:10]
                minutes = line[11:13]
                now2 = datetime.datetime.now()
                now2 = now.replace(hour=int(hours), minute=int(minutes))
                radelTime = now2
                radelTimeString = radelTime.strftime('%H:%M:%S')


        file.close()
        await message.channel.send('불러오기 완료')

    if message.content.startswith('!보스탐'):

        datelist = [radelTimeString, ]

        information = '----- 보스탐 정보 -----\n'

        for timestring in sorted(datelist):
            # print(timestring)

            if timestring == radelTimeString:
                if radelTimeString != '99:99:99':
                    information += ' 라드엘 : ' + radelTimeString + '\n'

            #elif timestring == gudeTimeString:
            #    if gudeTimeString != '99:99:99':
            #        information += ' - 거드 : ' + gudeTimeString + '\n'

        if radelTimeString == '99:99:99':
            information += ' - 라드엘\n'

        await message.channel.send(information)

        file = open("D:\my_bot.db", 'w')
        file.write(information);
        file.close()

    if message.content.startswith('!현재시간'):
        await message.channel.send(datetime.datetime.now().strftime('%H:%M:%S'))

client.run(token)

