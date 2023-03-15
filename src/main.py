import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from music_cog import MusicPlayer

# Load the .env file to get the bot's token
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Create a new bot instance with the desired command prefix and intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Define an event listener that triggers when the bot is ready to run
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.add_cog(MusicPlayer(bot))

# Start the bot
bot.run(TOKEN)
