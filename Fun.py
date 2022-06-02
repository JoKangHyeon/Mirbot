#_*_ coding: utf-8 _*_

import re
import RandomCore
import discord
eightballAnswer = ['분명히 될거야!', '확실히 그래', '의심할 필요도 없잖아?',
                   '맞아, 확실히!', '그래도 괜찮아', '내가 봤어, 확실해!',
                   '아마도-', '보기엔 괜찮아 보여', '응', '그럴 거야',
                   '괜찮아!', '물론!', '어떻게든?', '좋아! 질러봐!',
                   'OK!', '화이팅이에요!', '할 수 있어!', '대성공! >ㅂ<)',
                   '넌 강해졌어, 돌격해!', '예에에에이!',
                   '잘 모르겠네-', '지금은 모르겠어', '몰라!',
                   '모르겠어!', '글쎄-', '잘 모르겠네...', '나중에 물어봐!',
                   '나중에 알려줄게', '미르는 자고 있어- 나중에 물어봐', '그건 왜?',
                   '높',  '그건 아냐-', '그럴 거라고 생각도 하지 마!',
                   '난 응원하고 있는데, 주사위는 아니래',  '보기엔... 아닌것 같아!',
                   '그건 아냐!',  '무리무리-',  '무리-', '절대 아냐!']
                   
                   
def EightBall(question):
    outmessage = eightballAnswer[RandomCore.get_rand_max(len(eightballAnswer))]
    embed = discord.Embed(color=0x800080)
    embed.add_field(name = ":question: 질문", value = question)
    embed.add_field(name = ":exclamation: 로봇 미르의 대답!", value=outmessage)
    return embed
    
def Choose(question):
    out = question.split(' ')
    choosed = out[RandomCore.get_rand_max(len(out))]
    embed = discord.Embed(color=0x800080)
    embed.add_field(name = ":exclamation: 로봇 미르의 대답!", value=choosed)
    return embed
