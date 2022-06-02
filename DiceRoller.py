#_*_ coding: utf-8 _*_

import re
import RandomCore
import discord
import DataSystem
from random import shuffle, seed


pattern = re.compile("(\d+)d(\d+|f|F)")

def roll(author,data):
    data = data[6:].replace(' ', 'd')
    orignal = data
    
    values = DataSystem.getValue(author.id)

    for key in values.keys():
        data = data.replace(key, values[key])

    match = pattern.findall(data)
    
    output=discord.Embed(title="")
    
    for dice in match:
        result = rollDice(dice[0],dice[1])
        output.add_field(name=dice[0]+'d'+dice[1],value=result[0],inline=False)
        data = data.replace(dice[0]+'d'+dice[1],result[1],1)
    print(data)
    output.add_field(name='총합',value=data.replace('*','\*')+"="+str(eval(data)),inline=False)
    output.description = author.mention + ' 가 주사위를 굴립니다\n' + orignal[6:].replace('*','\*')
    return output


def rollDice(data1, data2):
    if data2=='f' or data2=='F':
        data1 = int(data1)
        if(data1>200 or data1<=0):
            return None
        outstr = ""
        outvalue = 0
        for i in range(data1):
            dice=RandomCore.get_rand_max(3)
            outstr = outstr+"["+['-',' ','+'][dice]+"] "
            outvalue = outvalue+(dice-1)
        return (outstr,str(outvalue))
    else:
        data1 = int(data1)
        data2 = int(data2)
        if(data1>200 or data1<=0):
            return None
        outstr = ""
        outvalue = 0
        
        for i in range(data1):
            dice=RandomCore.get_rand_max(data2)+1
            outstr = outstr+"["+str(dice)+"] "
            outvalue = outvalue+dice
        
        return (outstr,str(outvalue))

def shuffleDeck(data1, data2):
    outdata = []
    if data1 > data2:
        temp = data1
        data1 = data2
        data2 = temp

    for i in range(data2 - data1 + 1):
        outdata.append(data1+i)
    seed(RandomCore.get_rand())
    shuffle(outdata)
    return outdata

