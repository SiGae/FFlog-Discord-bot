import discord
import asyncio
import private
import json
import urllib.request
from urllib import parse
import requests
from operator import itemgetter

client = discord.Client()


def SliceByLayer(rawData):
    output = []
    classflag = []
    layer = []
    cnt = -1
    for i in rawData:
        if i['difficulty'] == 101 or i['encounterID'] == 1050:
            layer.append({
                'encounterID' : i['encounterID'],
                'spec' : i['spec'],
                'percentile' : i['percentile']
            }
        )

    for i in layer:
        if not(i['encounterID'] in classflag):
            output.append([])
            classflag.append(i['encounterID'])
            cnt += 1
        output[cnt].append(i)
    print(classflag)

    return output

def sortedByPercentile(rawData):
    output = []
    for i in rawData:
        data = sorted(i, key = itemgetter('percentile', 'spec'), reverse = True)
        output.append(data)
    return output

def SliceBySpecDetail(rawData):
    spec = []
    output = []
    data = sorted(rawData, key=itemgetter('spec', 'percentile'), reverse = True)
    for i in data:
        if not(i['spec'] in spec):
            spec.append(i['spec'])
            output.append(i)
    return output

def SliceBySpec(rawData):
    output = []
    for i in rawData:
        output.append(SliceBySpecDetail(i))
    output = sortedByPercentile(output)
    return output

def Alexander(rawData, job, server):
    msg = rawData.split()

    out = []
    cl = []
    
    lc ="https://www.fflogs.com:443/v1/parses/character/{}/{}/KR".format(msg[2], server[msg[1]])
    param = {
        'api_key' : private.ffkey,
        'metric' : "rdps",
        'zone' : 32,
        'timeframe' : 'historical'

    }

    urlopen = requests.get(lc, params = param)
    js = json.loads(urlopen.text)

    print(js)

    
    data = SliceBySpec(SliceByLayer(js))
    cnt = "절알렉산더"
    workString = ""
    for i in data:
        workString += "{}\n".format(cnt)
        workSubString = ""
        for j in i:
            workSubString += "\t{}: {}\n".format(job[j['spec']], j['percentile'])
        workString += workSubString
        workString += "\n"
    return workString

def edenAwake(rawData, job, server):
    msg = rawData.split()

    out = []
    cl = []
    
    lc ="https://www.fflogs.com:443/v1/parses/character/{}/{}/KR".format(msg[2], server[msg[1]])
    param = {
        'api_key' : private.ffkey,
        'metric' : "rdps",
        'zone' : 29,
        'timeframe' : 'historical'

    }
    urlopen = requests.get(lc, params = param)
    js = json.loads(urlopen.text)

    
    data = SliceBySpec(SliceByLayer(js))
    cnt = 1
    workString = ""
    for i in data:
        workString += "{}.\n".format(cnt)
        workSubString = ""
        cnt +=1
        for j in i:
            workSubString += "\t{}: {}\n".format(job[j['spec']], j['percentile'])
        workString += workSubString
        workString += "\n"
    return workString


@client.event
async def on_message(message):

    job = {
        "Astrologian" : "점성술사",
        "Bard" : "음유시인",
        "Black Mage" : "흑마도사",
        "Dark Knight" : "암흑기사",
        "Dragoon" : "용기사",
        "Machinist" : "기공사",
        "Monk" : "몽크",
        "Ninja" : "닌자",
        "Paladin" : "나이트",
        "Scholar" : "학자",
        "Summoner" : "소환사",
        "Warrior" : "전사",
        "White Mage" : "백마도사",
        "Red Mage" : "적마도사",
        "Samurai" : "사무라이",
        "Dancer" : "무도가",
        "Gunbreaker" : "건브레이커"
 
    }

    server = {
    '모그리' : 'moogle',
    '초코보' : 'chocobo',
    '카벙클' : 'carbuncle',
    '톤베리' : 'tonberry'
    }
    print(message.content)
    tempsmg = message.content.split()
    if tempsmg[0] == "/ff":
        msg = message.content.split()
        workString = Alexander(message.content, job, server)
        print(workString) 


        await message.channel.send('```\n{}\n```'.format(workString))

        workString = edenAwake(message.content, job, server)
        print(workString) 


        await message.channel.send('```\n각영\n{}\n```'.format(workString))

    if tempsmg[0] == "/ffua":
        msg = message.content.split()
        workString = Alexander(message.content, job, server)
        print(workString) 


        await message.channel.send('```\n{}\n```'.format(workString))

    if tempsmg[0] == "/ffeg":

        workString = edenAwake(message.content, job, server)
        print(workString) 


        await message.channel.send('```\n{}\n```'.format(workString))



client.run(private.key)

