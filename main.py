#!/usr/bin/python3
import discord
from discord.ext import commands
import random
import time
import os
import asyncio

#token
f = open("token.txt")
token = f.read()
f.close()
intents = discord.Intents.all()
bot = discord.Client(intents=intents)

#quiz init
with open("terms.txt", 'r') as file:
    lines = file.readlines()
    terms_definitions = [line.strip().split(':') for line in lines]
terms_dict = dict(terms_definitions)
current_term = None
current_def = None
message_count = 0
quiz_int_messages = 5
quiz_timeout = 30
points_dict = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    global terms_dict, current_term, current_def, message_count, quiz_int_messages, quiz_timeout, points_dict, start_time
    if message.author == bot.user:
        return
    elif message.content.startswith("?startquiz"):
        current_term, current_def = random.choice(list(terms_dict.items()))
        start_time = time.time()
        await message.channel.send(f'Quiz started! What term(s) matches the following definition: **{current_def}**?')
        print(current_term) #for testing purposes
        timeout_task = asyncio.create_task(quiz_timeout_task(message.channel))
        await timeout_task
    elif message.content.startswith("?endquiz"):
        await message.channel.send(f'The correct answer was: **{current_term}**')
        current_term, current_def, message_count = None, None, 0
    elif message.content.lower().startswith('!settimeout'):
        try:
            new_timeout = int(message.content.split()[1])
            quiz_timeout = new_timeout
            await message.channel.send(f'Quiz timeout set to {new_timeout} seconds.')
        except (IndexError, ValueError):
            await message.channel.send('Try an input like `!settimeout 30` to have the bot time out after 30 seconds.')
    elif message.content.startswith("?leaderboard"):
        leaderboardvar = sorted(points_dict.items(), key=lambda x: x[1], reverse=True)
        leaderboard_str = '\n'.join(f'{index + 1}. {bot.get_user(int(user_id))}: {points}' for index, (user_id, points) in enumerate(leaderboardvar))
        await message.channel.send(f'Leaderboard:\n{leaderboard_str}')
    elif current_term is not None: #quiz
        if message.content.startswith(current_term): 
            #correct
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2)
            points = max(0, round((quiz_timeout - elapsed_time) * 10))
            user_id = str(message.author.id)
            points_dict[user_id] = points_dict.get(user_id, 0) + points
            await message.channel.send(f'Correct! {message.author.mention} guessed the term and earned {points} points!')
            current_term, current_def, message_count = None, None, 0
        else:
            #incorrect
            await message.channel.send(f'Nope! Try again.')

async def quiz_timeout_task(channel):
    global terms_dict, current_term, current_def, message_count, quiz_int_messages, quiz_timeout, points_dict
    await asyncio.sleep(quiz_timeout)
    if current_term is not None:
        await channel.send(f'Time is up! The correct answer was: **{current_term}**')
        current_term, current_def, message_count = None, None, 0

bot.run(token)
