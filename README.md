# DocsBot-ChatGPT-Discord-Bot
 An interactive Discord chatbot powered by DocsBot.ai and OpenAI ChatGPT. Docsbot.ai has been chosen in this case due to ease of managing source material, and multiple instances.

Obtain answers from a DocsBot AI right within Discord using this bot, by prefixing queries with the !ask command. 

Features
- Per user session history
- Answers approaching 2000 characters are split into pieces
- Logs to a file in the same directory by default
- Queries are prequalified to contain UTF-8 characters only and lengths greater than 10
- Threaded responses to queries that auto-archive after 60 minutes.

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

- 1.1.00 - outputs to a logfile by default, returns an error if queries contain non-UTF-8 characters, and returns an error if queries contain fewer than 10 characters.
- 1.2.00 - implemented threaded responses that auto-archive after 60 minutes, formatting of codeblocks is now preserved, and markdown intepreted correctly.
