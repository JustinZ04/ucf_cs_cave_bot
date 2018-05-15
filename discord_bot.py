#!/usr/bin/env python
# Script to run the discord bot itself.
# Handles logging in and receiving the correct command to run the parse script. Outputs the current TA's holding office
# hours.

import discord
import config

from datetime import datetime
from parse_excel import parse

client = discord.Client()


@client.event
async def on_ready():
    # Logs the bot in so it goes online.
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')


@client.event
async def on_message(message):
    # Receives the '!cave' command and returns the current TA's holding office hours.
    # Make sure to parse the right spreadsheet, so use the channel name.
    if message.content.startswith('!cave'):
        if message.channel.name == 'cs1':  # Need to make sure name matches channel name of server.
            ta_list = parse(1)

        if message.channel.name == 'cs2' or message.channel.name == 'class-discussion':  # Need to make sure name matches channel name of server.
            ta_list = parse(2)

        if ta_list is None:
            await client.send_message(message.channel, "No TA's are in the cave right now!")

        else:
            s = '\n\n\n'.join(ta_list)
            await client.send_message(message.channel, s)

        # Log every time a '!cave' command is received to a log file.
        cur_time = datetime.now().time()
        file = open("logs/commands.log", "a")
        file.write(str(cur_time) + " Cave command typed\n")
        file.close()

# Holds the authorization token for the bot.
client.run(config.bot_token)
