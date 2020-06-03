from spotify_client import Spotify_Client
import discord

import argparse
import os
import sys
import time
import logging

logger = logging.getLogger('spotify_rythm_bot')
logger.setLevel(logging.INFO)

def load_discord_token():
    discord_token = os.getenv("DISCORD_TOKEN")
    if discord_token == "" or discord_token == None:
        logger.error("Unable to load discord token")
        sys.exit(2)
    return discord_token


def parse_commandline():
    parser = argparse.ArgumentParser()
    #parser.add_argument('playlist', type=str)
    args = parser.parse_args()
    return args


def main():
    args = parse_commandline()

    discord_token = load_discord_token()
    discord_client = discord.Client()
    spotify_client = Spotify_Client()
    
    @discord_client.event
    async def on_ready():
        logger.info(f'{discord_client.user} has connected to Discord')
        for guild in discord_client.guilds:
            logger.info(f'Connected to server: {guild.name}')
    
    @discord_client.event
    async def on_message(message):
        if message.author == discord_client.user:
            return

        if message.content.lower().startswith("!play https://open.spotify.com/"):
            channel = message.author.voice.channel
            voice_context = await channel.connect()

            for command_url in message.content.split()[1:]:
                rythm_bot_commands = spotify_client.parse_link(command_url)
                for command in rythm_bot_commands:
                    time.sleep(2)
                    await message.channel.send(command)
                    time.sleep(2)
                    
            await voice_context.disconnect()

    logger.info("Starting discord client.")
    discord_client.run(discord_token, bot=False)


if __name__ == "__main__":
    main()
