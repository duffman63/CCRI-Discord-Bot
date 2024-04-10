#!/usr/bin/python3
import discord
from discord.ext import commands
import random
import time
import os
import asyncio
import subprocess
import hashlib

#token
f = open("token.txt")
token = f.read()
f.close()
intents = discord.Intents.all()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.id == 876428967291260930:
        if message.content.startswith("?wp"):
            runme = "sudo -u ubuntu wp --path=/srv/www/wordpress/ %s" % message.content[4:]
            output = subprocess.check_output(runme.split(" "))
            h = hashlib.new('sha256')
            h.update(output)
            out = open("/home/ubuntu/CCRI-Discord-Bot/output/%s.txt" % h.hexdigest(),"w+")
            out.write(output.decode("utf-8"))
            out.close()
            await message.channel.send(file=discord.File("/home/ubuntu/CCRI-Discord-Bot/output/%s.txt" % h.hexdigest()))
            os.system("rm /home/ubuntu/CCRI-Discord-Bot/output/*")
bot.run(token)
