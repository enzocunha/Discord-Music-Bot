import discord
from discord.ext import commands
import youtube_dl


class MusicPlayer(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        print('Music Player loaded succesfully.')

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Connecting to {channel.name}.")

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send(f'Disconnected.')

    @commands.command()
    async def clear(self, ctx, amount=100):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def play(self, ctx, youtube_url):
        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        channel = ctx.author.voice.channel
        voice = await channel.connect()
        await ctx.send(f"Connecting to {channel.name}.")

        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            url = info['formats'][0]['url']

            source = discord.FFmpegPCMAudio(url)
            player = voice.play(source)

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Paused.")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Resuming.")
