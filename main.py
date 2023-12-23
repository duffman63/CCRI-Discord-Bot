import discord
from discord.ext import commands
import random
import asyncio
import time

def load_terms():
    with open(GasGastropoda/CCRI-Discord-Bot/terms.txt, 'r') as file:
        lines = file.readlines()
        terms_definitions = [line.strip().split(':') for line in lines]
    return dict(terms_definitions)

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# reminder to load token from another file (google "how to import variable from another file")
TOKEN = MTE4Nzk2ODQyMTA2NTkxNjQxNg.G-4YvF.4qvLxhTphTW-0He-pUqEkUjhyJDhOKkGaiJTDg
TERMS_FILE = 'terms.txt'

terms_dict = load_terms(TERMS_FILE)
current_term = None
current_def = None
message_count = 0
quiz_int_messages = 5
quiz_timeout = 30
points_dict = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global current_term, current_def, message_count, quiz_int_messages, quiz_timeout, points_dict

    if message.author == client.user:
        return
    
    if message.content.lower() == '!startquiz':
        current_term, current_def = random.choice(list(terms_dict.items()))
        await message.channel.send(f'Quiz started! What term(s) matches the following definition: **{current_def}**?')

        timeout_task = asyncio.create_task(quiz_timeout_task(message.channel))
        await timeout_task

    elif message.content.lower() == '!endquiz':
        await message.channel.send(f'Too bad! The correct answer was: **{current_term}**')
        current_term, current_def, message_count = None, None, 0

    elif message.content.lower().startswith('!sentinterval'):
        try:
            new_interval = int(message.content.split()[1])
            quiz_int_messages = new_interval
            await message.channel.send(f'Quiz interval has been successfully set to {new_interval} messages.')
        except (IndexError, ValueError):
            await message.channel.send('Nice try dimwit! Try an input like `!setinterval 15` to have the bot start a quiz every 15 messages.')

    elif message.content.lower().startswith('!settimeout'):
        try:
            new_timeout = int(message.content.split()[1])
            quiz_timeout = new_timeout
            await message.channel.send(f'Quiz timeout set to {new_timeout} seconds.')
        except (IndexError, ValueError):
            await message.channel.send('Nice try dimwit! Try an input like `!settimeout 30` to have the bot time out after 30 seconds.')
    
    elif current_term is not None and message.content.lower() == current_term.lower():
        # this is when the user guesses correctly
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)

        #calculating points based on response time
        points = max(0, round((quiz_timeout - elapsed_time) * 10))
        user_id = str(message.author.id)
