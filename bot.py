import discord
import asyncio
import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
import private

client = discord.Client()

@client.event
async def on_message(message):

    server = {
    '모그리' : 'moogle',
    '초코보' : 'chocobo',
    '카벙클' : 'carbuncle',
    '톤베리' : 'tonberry'
    }
    print(message)
    print(message.content)
    if message.content.startswith('/ff'):
        msg = message.content.split()
        lc = 'https://ko.fflogs.com/character/kr/{}/{}'.format(server[msg[1]], msg[2])
        await message.channel.send(lc)

        driver = webdriver.Firefox()
        # driver.implicitly_wait(1)
        driver.get(lc)
        # sleep(1)

        h = driver.page_source

        soup = BeautifulSoup(h, 'html.parser')
        avg = soup.find("div", {"class" : 'best-perf-avg'})
        avg = avg.find('b')

        allavg = avg.text
        avg = soup.find_all("td", {"class" : 'hist-cell'})
        
        print(allavg)
        allavg = allavg.replace("\n\t", "]\n")
        li = []
        for i in avg:
            li.append(i.text.replace("\n\n", "\n"))

        await message.channel.send('```[전체: {}1층: {}2층: {}3층: {}4층: {}```'.format(allavg, li[0], li[1], li[2], li[3]))

client.run(private.key)

