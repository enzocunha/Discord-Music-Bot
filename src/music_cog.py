import discord
from discord.ext import commands
import youtube_dl


class MusicPlayer(commands.Cog):
    def __init__(self, bot) -> None:
        """
        Initializes the MusicPlayer class.

        :param bot: A Discord bot object.
        """

        self.bot = bot
        print('Music Player loaded succesfully.')
        self.YDL_OPTIONS = YDL_OPTIONS = {
            'format': 'bestaudio', 'noplaylist': 'True'}
        self.queue = []

    @commands.command()
    async def join(self, ctx):
        """
        A command to join a voice channel.

        :param ctx: A Context object that contains information about the command invocation context.
        """

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
        """
        A command to disconnect the bot from the current voice channel.

        :param ctx: A Context object that contains information about the command invocation context.
        """

        if ctx.voice_client is None:
            await ctx.send('Not connected to any voice channel.')
            return

        await ctx.voice_client.disconnect()
        self.voice_channel = None
        await ctx.send('Disconnected.')

    @commands.command()
    async def play(self, ctx, youtube_url):
        """
        A command to play a YouTube video in a voice channel.

        :param ctx: A Context object that contains information about the command invocation context.
        :param youtube_url: A string representing the URL of the YouTube video to play.
        """

        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        if ctx.voice_client is None:
            await ctx.send('Make me join a voice channel first.')
            return

        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            url = info['formats'][0]['url']
            title = info['title']

            self.queue.append({'title': title, 'url': url})
            await ctx.send(f'Adding {title} to queue.')

            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)

    async def play_next(self, ctx):
        """
        A helper function that plays the next song in the queue.

        :param ctx: A Context object that contains information about the command invocation context.
        """

        if len(self.queue) == 0:
            return

        song = self.queue.pop(0)
        title = song['title']
        url = song['url']
        source = discord.FFmpegPCMAudio(url)

        await ctx.send(f'Playing {title}')
        ctx.voice_client.play(
            source, after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))

    @commands.command()
    async def pause(self, ctx):
        """
        A command that pauses the currently playing song.

        :param ctx: A Context object that contains information about the command invocation context.
        """

        ctx.voice_client.pause()
        await ctx.send("Paused.")

    @commands.command()
    async def resume(self, ctx):
        """
        A command that resumes the currently paused song.

        :param ctx: A Context object that contains information about the command invocation context.
        """

        ctx.voice_client.resume()
        await ctx.send("Resuming.")

    @commands.command()
    async def queue(self, ctx):
        """
        A command that displays the current song queue.

        :param ctx: A Context object that contains information about the command invocation context.
        """

        if len(self.queue) == 0:
            await ctx.send('The queue is currently empty.')
        else:
            queue_message = 'Queue:\n'
            for index, song in enumerate(self.queue):
                queue_message += f'{index + 1}. {song["title"]}\n'
            await ctx.send(queue_message)
