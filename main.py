#!/usr/bin/python3
import discord
from discord.ext import commands
import random

f = open("token.txt")
token = f.read()
f.close()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

@bot.command()
async def ping(ctx):
	await ctx.send('pong')
@bot.command()
async def term(ctx):
	f = open("terms.txt","r")
	terms = f.read().split("\n")
	f.close()
	random.shuffle(terms)
	await ctx.send(terms[0].split(": ")[0])
	await ctx.send(terms[0].split(": ")[1])

bot.run(token)
