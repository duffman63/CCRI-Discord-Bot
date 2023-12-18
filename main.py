#!/usr/bin/python3
import discord
from discord.ext import commands
import random

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

bot.run('MTE4NjM2NjEwMTU1OTQ1OTg0MQ.G-JsEL.4UXxya4xoE5pJgx-gDQUlxtfB_hpv8PUkllSis')
