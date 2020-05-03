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
                cnt += 1
        
        while len(out) != 4:
            out.append("None")

        await message.channel.send('```1층: {}\n2층: {}\n3층: {}\n4층: {}```'.format(out[0], out[1], out[2], out[3]))

client.run(private.key)

