# Discord-Self-Bot
# This project is old and outdated, and probably broken in many places. I do not recomend you use it. It has not been updated in months, nor am I currently maintaining it right now. When I have more time, I'll rewrite it.

A Discord Self bot to do helpful things, by DiNitride#7899. A self bot is a bot that runs on your
personal account, that is only usable by you, everywhere. Use at own risk.

## Features:

This Self Bot has a primary function of utility, rather than providing access to external sources (e.g. Game Statistics or searching for animes (Heck off Weebs), so either you will need to write your own cog for the bot, or use a server bot. A lot of the functions of the bot mirror functions of Discord but simply provide a more convinient method of accessing them (Primarily for mobile users)

#### Moderation

The self bot has kicking and banning functions built in for basic moderation, however this is simply a quicker method of accessing these options for mobile users. Other moderation options such as muting or time outs are best left to server moderation bots. This is a method of existing moderators to quickly access these tools while on mobile, rather than providing further moderation functions than Discord itself. **THIS IS NOT A SERVER MODERATION BOT**
###### Coming soon in Moderation
The ability to X Ban users (Ban a user while they are not in the server) will be implemented soon.

#### Utility

Using the self bot allows the user to search the entirety of Discord for any user or server by ID and get basic information about it. It also allows the user to get the same information about the current server easily, and also further information regarding the relationship between a user and the server (Such as join date and roles).
###### Coming Soon in Utils
The ability to set the users 'playing' game to anything of preference.

#### Tags (Currently in development)

The self bot also has a tagging system for the user to save things with a name and call them back later, in a similar way to [RoboDanny seen in the Discord Py channel on Discord API](https://github.com/Rapptz/RoboDanny) (and probably many other bots), however tags are only createable and accessible by the user so can be used to store personal tags and can be accessed everywhere by the user.

#### Spotify (And/or General Music) Integration (A possible thing I might do, maybe not, we'll see)

I may consider implementing the functionality of my [Discord Music Status](https://github.com/DiNitride/Discord-Music-Status) into this self bot, however in a improved state that is easier to user. *However this function would be **ONLY** be userful for users that run the self bot off the same PC as they use / run their Music player off.*4

## Install Instructions:

Clone the repository to your local PC or server
```
git clone https://github.com/DiNitride/Discord-Self-Bot
```
Create a `token.txt` file in the `/config/` folder and place your login token inside of this. The token can be found in your browser's application menu (In chrome, go to Inspect > Application tab > Storage > Local Storage > discord link)

Default config files should be created and updated for you when you first run the bot. Finally run `run.py` to start the bot and it should log in and run quietly.

## Requirements

- [discord.py Rewrite](https://github.com/Rapptz/discord.py/tree/rewrite)
