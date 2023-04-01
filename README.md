# DocsBot-ChatGPT-Discord-Bot
 An interactive Discord chatbot powered by DocsBot.ai and OpenAI ChatGPT. 

About
There are two bots here. One utilizes a simple Q&A mode that resets the context of a conversation after every query. The other uses chat mode, which remembers the context of conversations by passing the Q&A session history as input along with new inquiries.

Requirements
1. A pre-trained DocsBot.ai operating in the desired context
2. OpenAI Service and ChatGPT Plus
3. A ChatGPT-4 API key if using GPT-4
4. Manage Server permissions on the target Discord server

Usage
1. Configure the bot by editing the appropriate file and adding a DocsBot team ID, bot ID, and Discord bot token. 
2. Save the file as docsbot.py
3. Start the bot with:
```
python docsbot.py
```
or for verbose output:
```
python docsbot.py -v
```