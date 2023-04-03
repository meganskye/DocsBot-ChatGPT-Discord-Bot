import discord
from discord.ext import commands
import aiohttp  # async for speedier queries
import argparse  # enable verbosity if necessary
import json
import asyncio
import logging  # enable logging if necessary

# Replace with current Discord bot token and API base URL
DISCORD_BOT_TOKEN = '{Discord_Bot_Token}'
API_BASE_URL = 'https://api.docsbot.ai/teams/{DocsBot_Team_ID}/bots/{DocsBot_Bot_ID}/chat'

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
parser.add_argument('-l', '--logfile', action='store_true', help='Log output to a logfile')
args = parser.parse_args()

# log everything to a file
if args.logfile:
    logging.basicConfig(filename='docsbot_chat.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# initialize intents
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.message_content = True

# initialize bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# call the DocsBot chat/streaming API
async def get_answer(question):
    final_answer = None
    history = []
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(API_BASE_URL) as ws:
            data = {'question': question, 'full_source': False, 'history': history}
            await ws.send_json(data)
            async for msg in ws:
                data = json.loads(msg.data)
                if data['sender'] == 'bot':
                    if data['type'] == 'stream':
                        final_answer = data['message'] if final_answer is None else final_answer + data['message']
                    elif data['type'] == 'end':
                        end_data = json.loads(data['message'])
                        final_answer = end_data['answer']
                        break
    return final_answer

# Q&A command for the bot
@bot.command(name='ask')
async def ask(ctx, *, question):
    if args.verbose:
        output = f'Question: {question}'
        print(output)
        if args.logfile:
            logging.info(output)
    answer = await get_answer(question)
    if args.verbose:
        output = f'Answer: {answer}'
        print(output)
        if args.logfile:
            logging.info(output)
    await ctx.send(answer)

# show bot is ready
@bot.event
async def on_ready():
    output = f'{bot.user} is connected to Discord!'
    print(output)
    if args.logfile:
        logging.info(output)

# run bot
bot.run(DISCORD_BOT_TOKEN)