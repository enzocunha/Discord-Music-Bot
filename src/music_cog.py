import discord
from discord.ext import commands
import youtube_dl


class MusicPlayer(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        print('Music Player loaded succesfully.')
        self.YDL_OPTIONS = YDL_OPTIONS = {
            'format': 'bestaudio', 'noplaylist': 'True'}
        self.queue = []

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send('You need to be in a voice channel to use this command.')
            return

        if not ctx.voice_client is None:
            await ctx.send('Already joined a voice channel.')
            return

        channel = ctx.author.voice.channel
        self.voice_channel = await channel.connect()
        await ctx.send(f'Connecting to {channel.name}.')

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('Not connected to any voice channel.')
            return

        await ctx.voice_client.disconnect()
        self.voice_channel = None
        await ctx.send('Disconnected.')

    @commands.command()
    async def clear(self, ctx, amount=100):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def play(self, ctx, youtube_url):
        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        if ctx.voice_client is None:
            await ctx.send('Make me join a voice channel first.')
            return

        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            url = info['formats'][0]['url']

            source = discord.FFmpegPCMAudio(url)
            player = ctx.voice_client.play(source)

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Paused.")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Resuming.")

