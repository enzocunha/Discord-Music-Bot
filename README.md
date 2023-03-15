
# Discord Music Bot

This is a simple music bot for Discord, built using Python and the Discord.py library. The bot allows users to play and queue musics from YouTube within a Discord server.

# Installation

`pip install -r requirements.txt`

> **Note:** Currently waiting for patched version for youtube-dl and using [this solution](https://stackoverflow.com/a/75602237)

# Usage

1.  First, you will need to create a Discord bot and get its token. You can follow the steps outlined in the [Discord Developer Portal](https://discord.com/developers/docs/intro) to create a new bot and get its token.
2.  Next, you will need to put the bot token in an environment variable. This is important for security reasons, as you do not want to hardcode your bot token in your code. To do this, create a new file called `.env` in the root directory of your project and add the following line:
`DISCORD_TOKEN=your bot token`
3.  Finally, you can run the bot with `python src/main.py` in your terminal.

## Commands

Once the bot is running, you can use the following commands to control the music playback:

-   `!join`: makes the bot join a voice channel
-   `!play youtube_url`: plays a song with the given name or URL
-   `!queue`: shows the current song queue
-   `!pause`: pauses the current song
-   `!resume`: resumes the paused song

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
