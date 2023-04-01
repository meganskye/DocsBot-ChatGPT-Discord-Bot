import discord
from discord.ext import commands
import aiohttp # async for speedier queries
import argparse # enable verbosity if necessary
import json 
import asyncio 

# configure the DocsBot team ID, bot ID, and Discord bot token here.
DISCORD_BOT_TOKEN = '{Discord_bot_token}'
API_BASE_URL = 'https://api.docsbot.ai/teams/{teamID}/bots/{botID}/chat'

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
args = parser.parse_args()

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
                        # Append the received message to the final answer
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
        print(f'Question: {question}')
    answer = await get_answer(question)
    if args.verbose:
        print(f'Answer: {answer}')
    await ctx.send(answer)

# show bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} is connected to Discord!')

# run bot
bot.run(DISCORD_BOT_TOKEN)