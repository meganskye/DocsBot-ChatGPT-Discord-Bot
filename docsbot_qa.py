import discord
from discord.ext import commands
import aiohttp  # async for speedier queries
import argparse  # enable verbosity if necessary
import logging  # output to a logfile

# Replace with current Discord bot token and API base URL
DISCORD_BOT_TOKEN = '{Discord_Bot_Token}'
API_BASE_URL = 'https://api.docsbot.ai/teams/{DocsBot_Team_ID}/bots/{DocsBot_Bot_ID}'

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
parser.add_argument('-l', '--logfile', action='store_true', help='Output to a logfile')
args = parser.parse_args()

# log everything to a file
if args.logfile:
    logging.basicConfig(filename='docsbot_qa.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# initialize intents
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.message_content = True

# initialize the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# call the DocsBot Q&A API
# this API retains no session history, so context is reset on every query.
async def get_answer(question):
    url = f'{API_BASE_URL}/ask'
    headers = {'Content-Type': 'application/json'}
    data = {'question': question, 'full_source': False}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                answer = (await response.json()).get('answer')
                return answer
            else:
                return 'Sorry, I am not able to obtain an answer to your question at this time.'

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
    if args.logfile:
        logging.info(f'Sent message: {answer}')

# indicate bot is ready
@bot.event
async def on_ready():
    output = f'{bot.user} is connected to Discord!'
    print(output)
    if args.logfile:
        logging.info(output)

# run bot
bot.run(DISCORD_BOT_TOKEN)
