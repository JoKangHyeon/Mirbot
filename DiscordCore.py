#_*_ coding: utf-8 _*_

import discord
import DiceRoller
import Fun
import RandomCore
import DataSystem
import time
import re
import requests

client = discord.Client()

helpEmbed = discord.Embed(title="도움말")
helpEmbed.add_field(name="help",value="도움말을 보여줘요.\n예)'help",inline=False)
helpEmbed.add_field(name="roll",value="주사위를 굴려요\n예)'roll 2d6+3",inline=False)
helpEmbed.add_field(name="8ball",value="미르봇에게 무엇이든 물어세요\n예)'8ball 그가 또 펌블을 굴릴까?",inline=False)
helpEmbed.add_field(name="choose",value="미르봇이 대신 골라줘요\n예)'choose 피자 치킨",inline=False)
helpEmbed.add_field(name="say/sayd",value="미르봇에게 말을 시키세요. sayd는 명령어를 바로 치워줘요\n예)'say 안녕!",inline=False)
helpEmbed.add_field(name="clear",value="메세지를 치워줘요\n예)'clear 5",inline=False)
helpEmbed.add_field(name="bet",value="a~b사이에서 숫자 하나를 골라요.\n예)'bet 5 10",inline=False)
helpEmbed.add_field(name="서버변경", value="현재 접속중인 보이스 서버를 변경해요\n예)'서버변경 자동",inline=False)
helpEmbed.add_field(name="측정", value="이미지의 음란도를 측정합니다. 명령어와 함께 이미지를 업로드해주세요",inline=False)
helpEmbed.add_field(name="\u200B",value="\u200B",inline=False)
helpEmbed.add_field(name="value 시스템",value="변수를 저장해뒀다가 꺼내쓸 수 있어요.\n예)'roll 2d6+STR",inline=False)
helpEmbed.add_field(name="setvalue",value="변수에 값을 저장해요.\n예)'setvalue STR 10",inline=False)
helpEmbed.add_field(name="removevalue",value="변수를 삭제해요.\n예)'removevalue STR",inline=False)
helpEmbed.add_field(name="showvalue",value="변수 리스트를 보여줘요.\n예)'showvalue",inline=False)
helpEmbed.add_field(name="\u200B",value="\u200B",inline=False)
helpEmbed.add_field(name="단축키",value="단축 명령어들이에요",inline=False)
helpEmbed.add_field(name="10",value="1d10을 굴려요\n예)'10+3",inline=False)
helpEmbed.add_field(name="20",value="1d20을 굴려요\n예)'20*3",inline=False)
helpEmbed.add_field(name="4",value="4df를 굴려요\n예)'4-3",inline=False)
helpEmbed.add_field(name="6",value="1d6을 굴려요\n예)'6/3",inline=False)
helpEmbed.add_field(name="66",value="2d6을 굴려요\n예)'66%3",inline=False)


p6 = re.compile("'6+")


API_URL = 'https://dapi.kakao.com/v2/vision/adult/detect'
MYAPP_KEY = "KAKAO API KEY HERE"
HEADER = {"Content-Type":"application/x-www-form-urlencoded",'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}
def detect_adult(link_img):
    try:
        while True:
            data = {'image_url' : link_img}
            resp = requests.post(API_URL,headers=HEADER, data=data)
            resp.raise_for_status()

            if resp.json()['result'] is not None:
                return resp.json()['result']

    except Exception as e:
        print(str(e))
        print(resp.json())

@client.event
async def on_ready():  # 봇이 준비되었을때 호출되는 이벤트
    game = discord.Game("안녕하세요! "+("　"*20))
    await client.change_presence(status=discord.Status.online,activity=game)
    print("준비 완료")
    
@client.event
async def on_message(message):  # 이벤트(메세지가 왔을 때)
    if message.content.lower().startswith("'roll "):
        embed = DiceRoller.roll(message.author, message.content)
        embed.description = message.author.mention + ' 가 주사위를 굴립니다\n' + message.content[6:].replace('*',r'\*')
        await message.channel.send(embed=embed)
    if message.content.lower().startswith("'8ball ") :
        embed = Fun.EightBall(message.content[7:])
        embed.description = message.author.mention
        await message.channel.send(embed=embed)
    if message.content.lower().startswith("'choose "):
        embed = Fun.Choose(message.content[8:])
        embed.description = message.author.mention
        await message.channel.send(embed=embed)
    if message.content.lower().startswith("'sayd"):
            await message.channel.send(message.content[6:])
            await message.delete()
    elif message.content.lower().startswith("'say") :
            await message.channel.send(message.content [5:])
    if message.content.lower().startswith("'clear"):
        so = int(message.content[7:])+1
        await message.channel.purge(limit=so)
    if message.content.lower().startswith("'setvalue "):
        keyData = message.author.id,message.content.split(' ')[1]
        valueData = message.content.split(' ')[2]
        DataSystem.setValue(message.author.id,keyData,valueData)
        await message.channel.send(keyData + "에 " + valueData + "를 저장했어요!")
    if message.content.lower().startswith("'removevalue "):
        keyData = message.content.split(' ')[1]
        result = DataSystem.removeValue(message.author.id,keyData)
        if result : 
            await message.channel.send(keyData + "를 삭제했어요!")
        else : 
            await message.channel.send(keyData + "는 없어요!")
    if message.content.lower().startswith("'showvalue"):
        embed=discord.Embed(title="변수 목록")
        values = DataSystem.getValue(message.author.id)
        for value in values:
            embed.add_field(name=value,value=values[value])
        await message.channel.send(embed=embed)
    if message.content.lower().startswith("'help"):
        await message.channel.send(embed=helpEmbed)
    if message.content.lower().startswith("'deck"):
        indata = message.content.split(' ')
        data1 = 0
        data2 = 0
        if len(indata)>2:
            data1 = int(indata[1])
            data2 = int(indata[2])
        else:
            data1 = 1
            data2 = int(indata[1])
        deckData = DiceRoller.shuffleDeck(data1,data2)
        outstring = ""
        for i in deckData :
            outstring = outstring + str(i) + " "
        await message.channel.send(outstring)
    if message.content.lower().startswith("'bet"):
        indata = message.content.lower().split(' ')
        data1 = int(indata[1])
        data2 = int(indata[2])

        await message.channel.send(RandomCore.get_rand_min_max(data1,data2+1))
    if message.content=="ㅋㅋㅋㅋ":
        await message.channel.send("ㅋㅋㅋ")
    if message.content.lower().startswith("'서버변경"):
        voice_region = {"자동":None,"브라질":discord.VoiceRegion.brazil,"홍콩":discord.VoiceRegion.hongkong,
                        "인도":discord.VoiceRegion.india,"일본":discord.VoiceRegion.japan,
                        "러시아":discord.VoiceRegion.russia,"싱가폴":discord.VoiceRegion.singapore,
                        "남아프리카":discord.VoiceRegion.southafrica,"한국":discord.VoiceRegion.south_korea,
                        "시드니":discord.VoiceRegion.sydney,"미국중부":discord.VoiceRegion.us_central,
                        "미국동부":discord.VoiceRegion.us_east,"미국남부":discord.VoiceRegion.us_south,
                        "미국서부":discord.VoiceRegion.us_west }
        reg = message.content[6:]
        if reg not in voice_region.keys():
            output = ""
            for ch in voice_region.keys():
                output += ch + ","
            output = reg+"는 사용할 수 없는 지역이에요!\n" + output[:-1] + "중에 골라주세요!"
            await message.channel.send(output)
            return

        if message.author.voice is not None:
            await message.author.voice.channel.edit(rtc_region=voice_region[reg])
        else:
            await message.channel.send("음성방을 찾을 수 없어요!")
    if message.content.lower().startswith("'측정"):
        lis_attach = []
        outstring = ""
        if len(message.attachments) is not 0:
            for at in message.attachments:
                if at.content_type.startswith('image/'):
                    lis_attach.append(at)
        else:
            await message.channel.send("이미지를 찾을 수 없어요!")

        if len(lis_attach) is not 0:
            for i in range(len(lis_attach)):
                aud_data = detect_adult(lis_attach[i])
                outstring += "{0}번 이미지\n건전 : {1}\n약간 : {2}\n음란 : {3}"\
                    .format(i+1,aud_data['normal'],aud_data['soft'],aud_data['adult'])
        else:
            await message.channel.send("이미지를 찾을 수 없어요!")
        await message.channel.send(outstring)

#QUICK SLOT
    if message.content.lower().startswith("'10"):
        embed = DiceRoller.roll(message.author, "'roll 1d10" + message.content[3:])
        await message.channel.send(embed=embed)
    if message.content.lower().startswith("'20"):
        embed = DiceRoller.roll(message.author, "'roll 1d20" + message.content[3:])
        await message.channel.send(embed=embed)
    if message.content.lower().startswith("'4"):
        embed = DiceRoller.roll(message.author, "'roll 4df" + message.content[2:])
        await message.channel.send(embed=embed)
    m=p6.match(message.content.lower())
    if m:
        embed = DiceRoller.roll(message.author, "'roll "+str(m.end()-m.start()-1)+"d6" + message.content[m.end():])
        await message.channel.send(embed=embed)



def running():
    try:
        client.run("DISCORD API KEY HERE")  # 클라이언트(봇)작동 개시
    except Exception as e:
        print (e)
        print("에러 발생, 10초후 복구를 시도합니다.")
        time.sleep(300)
        running()
        raise

running()
