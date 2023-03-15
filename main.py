import os
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands
import youtube_dl

TOKEN = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Start of commands
@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("You need to be in a voice channel to use this command."
                       )
        return

    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f"Connecting to {channel.name}.")


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send(f'Disconnected.')
    
    
@bot.command()
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)
    
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    
# End of commands
bot.run(TOKEN)