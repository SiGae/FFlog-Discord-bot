import discord
import asyncio
import private
import json
import urllib.request
from urllib import parse
import requests

client = discord.Client()

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
    if message.content.startswith('/ff'):
        msg = message.content.split()

        out = []
        cl = []
        
        lc ="https://www.fflogs.com:443/v1/parses/character/{}/{}/KR".format(msg[2], server[msg[1]])
        param = {
            'api_key' : private.ffkey,
            'metric' : "rdps",
            'zone' : 29,

        }
        urlopen = requests.get(lc, params = param)
        js = json.loads(urlopen.text)

        cnt = 65
        for i in js:

            if cnt == i['encounterID'] and 101 == i['difficulty']:
                out.append(i['percentile'])
                cl.append(job[i['spec']])
                cnt += 1
        
        while len(out) != 4:
            out.append("None")
            cl.append("None")

        await message.channel.send('```[1. {}]\n{}\n[2. {}]\n{}\n[3. {}]\n{}\n[4. {}]\n{}```'.format(cl[0], out[0],cl[1], out[1],cl[2], out[2],cl[3], out[3]))

client.run(private.key)

