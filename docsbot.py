import os
import sys
import discord
from discord.ext import commands
import aiohttp
import argparse
import logging
import textwrap
# import nltk
import asyncio
import re

# Replace with current Discord bot token and API base URL
DISCORD_BOT_TOKEN = ''
API_BASE_URL = 'https://api.docsbot.ai/teams/''/bots/'''

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
args = parser.parse_args()

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# use a logfile
script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
log_filename = f"{script_name}.log"
file_handler = logging.FileHandler(log_filename, encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# log status every 30 minutes
async def report_status():
    while True:
        status_message = f'{bot.user} is online and ready'
        logger.info(status_message)
        print(status_message)
        await asyncio.sleep(1800)

# initialize intents
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.message_content = True

# initialize the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# check if the query length is fewer than ten characters
def is_valid_length(question):
    return len(question) >= 10

# check if the query includes forbidden characters
def is_utf8(question):
    try:
        question.encode('utf-8').decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False

# check if a line starts a code block
def is_code_block_start(line):
    return line.startswith("```")

# check if a line ends a code block
def is_code_block_end(line):
    return line.endswith("```")

# call the DocsBot Chat API
async def get_answer(question, history=[]):
    url = f'{API_BASE_URL}/chat'
    headers = {'Content-Type': 'application/json'}
    data = {'question': question, 'full_source': True, 'history': history}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                json_data = await response.json()
                answer = json_data.get('answer')
                new_history = json_data.get('history')
                return answer, new_history
            else:
                logger.error(f"Error: {response.status}")
                logger.error(await response.text())
                return 'Error 500: Sorry, I am not able to obtain an answer to your question at this time. Please try again.', history

chat_history = {}

@bot.command(name='ask')
async def ask(ctx, *, question):
    user_id = str(ctx.message.author.id)
    logger.info(f"User {user_id} asked: {question}")

    if not is_utf8(question):
        await ctx.send("Error: Your question should contain UTF-8 characters, only.")
        return
    if not is_valid_length(question):
        await ctx.send("Error: Your question should be at least 10 characters long.")
        return

    if user_id not in chat_history:
        chat_history[user_id] = []

    answer, new_history = await get_answer(question, history=chat_history[user_id])
    chat_history[user_id] = new_history

    # start a public thread based on the original message and archive it automatically after 60 minutes
    thread_name = f"{ctx.author.name} asked:"
    thread = await ctx.channel.create_thread(name=thread_name, auto_archive_duration=60, message=ctx.message)

    async def send_answer():
        paragraphs = answer.split("\n")
        message_parts = []
        current_part = ""
        inside_code_block = False

        for paragraph in paragraphs:
            if is_code_block_start(paragraph):
                inside_code_block = True
            elif is_code_block_end(paragraph):
                inside_code_block = False

            formatted_paragraph = paragraph.strip()

            if not inside_code_block:
                # preserve * and ** for italic and bold formatting
                formatted_paragraph = re.sub(r'(?<!\\)\*(?!\*)', r'*', formatted_paragraph)
                formatted_paragraph = re.sub(r'(?<!\\)(\*\*)(?!\*)', r'**', formatted_paragraph)

                # escape other markdown formatting characters
                formatted_paragraph = discord.utils.escape_markdown(formatted_paragraph)

                # replace URLs with clickable links
                formatted_paragraph = re.sub(r'(https?://\S+)', r'<\1>', formatted_paragraph)

            if len(current_part) + len(formatted_paragraph) + 1 <= 1900:
                if current_part:
                    current_part += "\n"
                current_part += formatted_paragraph
            else:
                message_parts.append(current_part)
                current_part = formatted_paragraph

        if current_part:
            message_parts.append(current_part)

        if len(message_parts) > 1:
            for i, part in enumerate(message_parts):
                await thread.send(f"Multi-part Answer {i + 1}:\n{part}")
                logger.info(f"Multi-part Answer {i + 1}: {part}")
        else:
            await thread.send(f"{message_parts[0]}")
            logger.info(f"Answer: {message_parts[0]}")

    await send_answer()

# indicate bot is ready and log online status at the interval defined in report_status
@bot.event
async def on_ready():
    print(f'{bot.user} is now connected to Discord!')
    bot.loop.create_task(report_status())

# run bot
bot.run(DISCORD_BOT_TOKEN)