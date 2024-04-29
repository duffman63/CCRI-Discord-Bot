#!/usr/bin/python3
import discord
from discord.ext import commands
import random
import time
import os
import asyncio
import subprocess
import hashlib
import re
import typing
import sys
import json

with open("help.json","r") as f:
    helparray = json.loads(f.read())

urlgetter = "sudo -u ubuntu wp --path=/srv/www/wordpress/ config get"
theout = subprocess.check_output(urlgetter.split(" "))
for test in theout.decode("utf-8").split("\n"):
    if "WP_HOME" in test:
        website = test.split("\t")[1]
        break

f = open("token.txt")
token = f.read()
f.close()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?',intents=intents,help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as "{bot.user}" inegrated with {website}!')

@bot.command(name='help')
async def help(ctx, *args):
    thehelp = "```" + json.dumps(helparray, indent=4).replace("\"","").replace("{","").replace("}","") + "```"
    if args is not None:
        try:
            await ctx.send("```%s: %s```" % (args[0],helparray[args[0]]))
        except:
            await ctx.send(thehelp)
    else:
        await ctx.send(thehelp)
@bot.command(name='wp')
async def wp(ctx, *args):
    if ctx.author.id == 876428967291260930:
        runme = "sudo -u ubuntu wp --path=/srv/www/wordpress/ %s" % " ".join(args)
        output = subprocess.check_output(runme.split(" "))
        out = open("/home/ubuntu/CCRI-Discord-Bot/output.txt","w+")
        out.write(output.decode("utf-8"))
        out.close()
        if len(output.decode("utf-8")) > 1990:
            await ctx.send(file=discord.File("/home/ubuntu/CCRI-Discord-Bot/output.txt"))
        else:
            await ctx.send("```%s```" % output.decode("utf-8"))
        os.system("rm /home/ubuntu/CCRI-Discord-Bot/output.txt")
@bot.command(name='addresource')
async def addresource(ctx, name, link):
    if ctx.author.id == 876428967291260930:
        f = open("/srv/www/wordpress/wp-content/resources.txt","r")
        resources = f.read().split("\n\n")
        f.close()
        del resources[-1]
        entry = """<!-- wp:list-item -->
<li>%s: <a href="%s">%s</a></li>
<!-- /wp:list-item -->""" % (name, link, link)
        resources.append(entry)
        resources.append("""</ul>
<!-- /wp:list -->""")
        os.system("sudo rm /srv/www/wordpress/wp-content/resources.txt")
        w = open("/srv/www/wordpress/wp-content/resources.txt","w+")
        w.write("\n\n".join(resources))
        w.close()
        os.system("sudo -u ubuntu wp --path='/srv/www/wordpress/' db query 'UPDATE wp_posts SET post_content = \"%s\" WHERE ID=16;'" % re.escape("\n\n".join(resources)).replace("\"","\\\""))
        await ctx.send("Added to resources page: %s/resources/" % website)
@bot.command(name='roll')
async def roll(ctx, low: typing.Optional[int], high: typing.Optional[int]):
    if low:
        if high:
            if low > high:
                await ctx.send("Low number is bigger than high number!")
                return
            else:
                await ctx.send(str(random.randrange(low,high,4)))
        else:
            await ctx.send(str(random.randrange(low,sys.maxsize,4)))
    else:
        await ctx.send(str(random.randrange(0,sys.maxsize,4)))
bot.run(token)
