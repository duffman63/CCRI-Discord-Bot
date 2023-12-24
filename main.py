import discord
from discord.ext import commands
import random
import asyncio
import time
from fuzzywuzzy import fuzz


def load_terms(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        terms_definitions = [line.strip().split(':') for line in lines]
    return dict(terms_definitions)

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)


TOKEN = ''
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
        
        # init start_time
        start_time = time.time()

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

        # awarding points and updating point dict
        points_dict[user_id] = points_dict.get(user_id, 0) + points

        await message.channel.send(f'Correct! {message.author.mention} guessed the term and earned {points} points!')
        current_term, current_def, message_count = None, None, 0

    elif current_term is not None:
        similarity_score = fuzz.ratio(message.content.lower(), current_term.lower())
        if similarity_score >= 70:
            await message.channel.send(f"Close! you're {100 - similarity_score}% close!")
        else:
            await message.channel.send(f'Nope! Try again.')


    elif message.content.lower().startswith('!leaderboard'):
        leaderboard = sorted(points_dict.items(), key=lambda x: x[1], reverse=True)
        leaderboard_str = '\n'.join(f'{index + 1}. {client.get_user(int(user_id))}: {points}' for index, (user_id, points) in enumerate(leaderboard))
        await message.channel.send(f'leaderboard:\n{leaderboard_str}')

async def quiz_timeout_task(channel):
    await asyncio.sleep(quiz_timeout)
    if current_term is not None:
        await channel.send(f'Time is up! The correct answer was: **{current_term}**')
        current_term, current_def, message_count = None, None, 0

# executing
client.run(TOKEN)
