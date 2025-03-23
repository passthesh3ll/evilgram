# Evilgram Telegram Bot
![image](https://i.postimg.cc/SQGHtxt9/evilgram.png)

## Description

A telegram bot to anonymously get new Instagram stories from a target profile and store them in a telegram chat. Instaloader is used to scrape and filter new Instagram stories.

**You may use different instaloader cookies to access/bypass private profiles**

## Dependencies

* `requests`
* `python-telegram-bot`
* `instaloader`
* `asyncio`

## Configuration

1. Obtain a Telegram Bot Token using BotFather and put TOKEN and CHAT_ID in the variables at the beginning of the code
```python
TOKEN = ''
CHAT_ID = ''
```
2. Add your bot to the Telegram chat where you want to receive notifications
3. This bot relies on an instaloader session file. You must install and log in to [instaloader](https://instaloader.github.io/), follow the prompts to log in
```bash
instaloader --login YOUR_INSTAGRAM_USERNAME
```
4. Put your account username in the variable at the beginning of the code
```python
MY_INSTAGRAM_USERNAME= ''
```
5. Execute the bot from your terminal (you can schedule the bot with cron to get periodic updates about a profile)
```bash
python evilgram.py TARGET_INSTAGRAM_USERNAME
```
6. You can schedule the bot with cron

## Screen
![image](https://i.imgur.com/wiEID9l.png)
