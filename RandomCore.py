#_*_ coding: utf-8 _*_

from requests import get  # to make GET request
import requests
#RANDOM CORE
url = 'http://150.203.48.55/API/jsonI.php'
data = []


def refill():
    global data
    resp = requests.get(url=url + '?length=1000&type=uint16')
    respdata = resp.json()
    for dice in respdata['data']:
        data.append(int(dice))
    

def check():
    global data
    if len(data) < 500:
        refill()

def get_rand():
    global data
    check()
    return data.pop()

def get_rand_max(maxValue):
    outvalue=0
    currentMax=65535
    while maxValue>currentMax :
        outvalue = outvalue+get_rand()
        currentMax = currentMax + 65535
    outvalue = outvalue+get_rand()
    currentMax = currentMax+65535
    return outvalue%maxValue
    
def get_rand_min_max(minValue, maxValue):
    if minValue>maxValue:
        temp = minValue
        minValue = maxValue
        maxValue = temp
        
    dif = maxValue-minValue
    return minValue+get_rand_max(dif)
    
   