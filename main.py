#!/usr/bin/python3
import discord
from discord.ext import commands
import random
import time

f = open("token.txt")
token = f.read()
f.close()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents,help_command=None)

@bot.command()
async def help(ctx):
	await ctx.send("""CCRI Cybersecurity Discord Bot

Command Prefix: ?
Commands:
```
	help: Displays this message.
	ping: Pings the bot.
	term: Defines a Security+ term.
```
""")
@bot.command()
async def ping(ctx):
	await ctx.send('pong')
@bot.command()
async def term(ctx):
	f = open("terms.txt","r")
	terms = f.read().split("\n")
	f.close()
	random.shuffle(terms)
	myterm = await ctx.send(terms[0].split(": ")[0])
	time.sleep(3)
	await myterm.edit(content=terms[0])

bot.run(token)
