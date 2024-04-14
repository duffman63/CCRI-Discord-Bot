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

#token
f = open("token.txt")
token = f.read()
f.close()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?',intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command(name='wp',help='This is the wp integration with the bot.')
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
@bot.command(name='addresource',help='Add a cyber resource to the resources page on the website.')
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
        os.system("rm /srv/www/wordpress/wp-content/resources.txt")
        w = open("/srv/www/wordpress/wp-content/resources.txt","w+")
        w.write("\n\n".join(resources))
        w.close()
        os.system("sudo -u ubuntu wp --path='/srv/www/wordpress/' db query 'UPDATE wp_posts SET post_content = \"%s\" WHERE ID=16;'" % re.escape("\n\n".join(resources)).replace("\"","\\\""))
        ctx.send("Added to resources page: https://0dd81521480e933f.chalphychateau.com/resources/")
bot.run(token)
