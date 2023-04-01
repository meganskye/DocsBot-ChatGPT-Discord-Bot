import discord
from discord.ext import commands
import aiohttp # async for speedier queries
import argparse  # enable verbosity if necessary

# configure the DocsBot team ID, bot ID, and Discord bot token here.
DISCORD_BOT_TOKEN = '{Discord_bot_token}'
API_BASE_URL = 'https://api.docsbot.ai/teams/{teamID}/bots/{botID}'

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
args = parser.parse_args()

# initialize intents
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.message_content = True

# initialize the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# call the DocsBot Q&A API 
# this API retains no session history, so context is reset on every query.
# in this mode, users need to pass in previous output along with new input to obtain responses in the same context.
async def get_answer(question): 
    url = f'{API_BASE_URL}/ask'
    headers = {'Content-Type': 'application/json'}
    data = {'question': question, 'full_source': False}

    async with aiohttp.ClientSession() as session:  # Use aiohttp.ClientSession
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
        print(f'Question: {question}')
    answer = await get_answer(question)  # Add await here
    if args.verbose:
        print(f'Answer: {answer}')
    await ctx.send(answer)

# indicate bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} is connected to Discord!')

# run bot
bot.run(DISCORD_BOT_TOKEN)