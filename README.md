# DocsBot-ChatGPT-Discord-Bot
 An interactive Discord chatbot powered by DocsBot.ai and OpenAI ChatGPT. 

Obtain answers from a DocsBot AI right within Discord using this bot, by prefixing queries with the !ask command. 

Features
- Per user session history
- Answers approaching 2000 characters are split into pieces
- Formatting and presentation of answers is mostly preserved through use of codeblocks
- Verbose output to logfile with status updates (optional)

Requirements
1. A pre-trained DocsBot.ai operating in the desired context
2. OpenAI Service and ChatGPT Plus
3. A ChatGPT-4 API key if using GPT-4
4. Manage Server permissions on the target Discord server

Usage
1. Configure the bot by adding a DocsBot team ID, bot ID, and Discord bot token
2. Start the bot with:
```
python docsbot.py
```
for verbose output:
```
python docsbot.py -v
```

CHANGELOG

- 1.1.00 - now outputs to a logfile by default, and returns an error if queries contain non-UTF-8 characters or are fewer than 10 characters.
