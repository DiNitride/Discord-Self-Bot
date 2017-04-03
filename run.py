import discord
from discord.ext import commands
import json
import datetime
import time
from logbook import Logger, StreamHandler
import sys
import inspect

StreamHandler(sys.stdout).push_application()
log = Logger('Self Bot')

log.notice("Loading config files")
try:
    with open("config/config.json") as f:
        _config = json.load(f)
except FileNotFoundError:
    log.error("Config file not found, loading defaults")
    df = open("config/defaults/default.config.json")
    _config = json.load(df)
    with open("config/config.json", "w") as f:
        log.info("Saved new config to file")
        f.write(json.dumps(_config))

try:
    with open("config/modules.json") as f:
        _modules = json.load(f)
except FileNotFoundError:
    log.error("Module loading list not found, loading defaults")
    df = open("config/defaults/default.modules.json")
    _modules = json.load(df)
    with open("config/modules.json", "w") as f:
        log.info("Saved module loading to file")
        f.write(json.dumps(_modules))

description = "A self bot to do things that are useful"
bot = commands.Bot(command_prefix=[_config["prefix"]], description=description, self_bot=True)

log.info("Linking logger, module loading list and config to bot")
bot.log = log
bot.log.info("Logger linked to bot")
bot.config = _config
bot.log.info("Config linked to bot")
bot.modules = _modules
bot.log.info("Module loading linked to bot")

try:
    with open("config/modules.json") as f:
        modules = json.load(f)
except FileNotFoundError:
    log.error("Module file not found, loading defaults")

def command_debug_message(ctx, name):
    if isinstance(ctx.channel, discord.DMChannel):
        bot.log.debug("Command: {} run in DM's by user {}/{}".format(name, ctx.author, ctx.author.id))
    elif isinstance(ctx.channel, discord.GroupChannel):
        bot.log.debug("Command: {} run in group chat {}/{} by user {}/{}".format(name, ctx.channel.name, ctx.channel.id, ctx.author, ctx.author.id))
    else:
        bot.log.debug("Command: {} run in channel #{}/{} on server {}/{} by user {}/{}".format(name, ctx.channel.name, ctx.channel.id, ctx.guild, ctx.guild.id, ctx.author, ctx.author.id))

bot.cmd_log = command_debug_message


@bot.event
async def on_ready():
    bot.log.notice("Logged in as {} with ID {}".format(bot.user.name, bot.user.id))
    bot.load_extension("modules.moderation")
    bot.log.notice("Loaded moderation")
    bot.load_extension("modules.tags")
    bot.log.notice("Loaded tags")


@bot.command()
async def ping(ctx):
    """Pong"""
    bot.cmd_log(ctx, "Ping Pong :ping_pong: ")

    before = time.monotonic()
    await (await bot.ws.ping())
    after = time.monotonic()
    _ping = (after - before) * 1000

    await ctx.send("Ping Pong :ping_pong: **{0:.0f}ms**".format(_ping))


@bot.command(name="eval")
async def _eval(ctx, code):
    """Evaluates a line of code provided"""
    heck = "off"
    hel = "yea"
    fuck = "off"
    code = code.strip("` ")
    try:
        result = eval(code)
        if inspect.isawaitable(result):
            result = await result
    except Exception as e:
        await ctx.send("```py\nInput: {}\n{}: {}```".format(code, type(e).__name__, e))
    else:
        await ctx.send("```py\nInput: {}\nOutput: {}\n```".format(code, result))
    await ctx.message.delete()

bot.remove_command("help")


@bot.command()
async def help(ctx):
    await ctx.send("Docs coming soon(tm)")


@bot.command()
async def info(ctx):
    """Shows information about the bot"""
    bot.cmd_log(ctx, "Bot Info")
    if ctx.channel.permissions_for(ctx.author).embed_links:
        embed = discord.Embed(colour=discord.Colour(0x158a2b), url="https://github.com/DiNitride/Discord-Self-Bot",
                              description="This self bot was written in Python using the discord.py library.",
                              timestamp=datetime.datetime.utcfromtimestamp(1490950035))

        embed.set_thumbnail(
            url="https://discordapp.com/api/users/95953002774413312/avatars/43731ce5807eb8503cd3559a3c13e780.jpg")
        embed.set_author(name="Discord Self Bot",
                         icon_url="https://discordapp.com/api/users/173709318133121024/avatars/ffc5b1ed120323748e20621b4c802329.jpg")
        embed.set_footer(text="Running on {}'s Account".format(ctx.author))

        embed.add_field(name="Source Code", value="https://github.com/DiNitride/Discord-Self-Bot")
        embed.add_field(name="Author", value="Written by DiNitride#7899")
        embed.add_field(name="Discord.py Version", value=discord.__version__)

        await ctx.send(embed=embed)
    else:
        await ctx.send("```\n"
                       "This self bot was written in Python using the discord.py library.\n"
                       "Source Code: https://github.com/DiNitride/Discord-Self-Bot\n"
                       "Author: DiNitride#7899\n"
                       "Discord.py version: {}\n```".format(discord.__version__))

async def save_module_loading():
    data = json.dumps(bot.modules)
    with open("config/modules.json", "w") as f:
        f.write(data)
        bot.log.notice("Saved module list")


@bot.command(name="enable")
async def _enable(ctx, extension: str):
    extension = extension.lower()
    if extension not in bot.modules.keys():
        bot.log.error("Tried to enable module {} but it is not a valid module".format(extension))
        await ctx.send("Invalid module")
    else:
        bot.modules[extension] = True
        bot.log.debug("Unloading extension")
        bot.unload_extension("modules." + extension)
        bot.log.debug("Loading extension")
        bot.load_extension("modules." + extension)
        bot.log.notice("Enabled Module")
        await ctx.send("Enabled Module")
        await save_module_loading()


@bot.command(name="disable")
async def _disable(ctx, extension: str):
    extension = extension.lower()
    if extension not in bot.modules.keys():
        bot.log.error("Tried to disable module {} but it is not a valid module".format(extension))
        await ctx.send("Invalid module")
    else:
        bot.modules[extension] = False
        bot.log.debug("Unloading extension")
        bot.unload_extension("modules." + extension)
        bot.log.debug("Loading extension")
        bot.load_extension("modules." + extension)
        bot.log.notice("Disabled module {}".format(extension))
        await ctx.send("Disabled Module")
        await save_module_loading()

try:
    with open("config/token.txt") as token:
        bot.log.notice("Logging into account")
        bot.run(token.read(), bot=False)
except FileNotFoundError:
    bot.log.critical("Token File does not exist, please create 'token.txt' inside /config")
