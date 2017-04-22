import discord
from discord.ext import commands
import datetime


class Moderation:

    def __init__(self, bot):
        self.bot = bot
        self.ban.enabled = bot.modules["moderation"]
        self.kick.enabled = bot.modules["moderation"]
        self.xban.enabled = bot.modules["moderation"]

    @commands.command()
    async def ban(self, ctx, user: discord.Member, delete_days=1):
        self.bot.cmd_log(ctx, "ban")
        if delete_days > 7:
            delete_days = 7
        if user:
            await ctx.guild.ban(user, delete_message_days=delete_days)
            self.bot.log.notice("Kicked {} from {}".format(user, ctx.guild.name))

    @commands.command()
    async def xban(self, ctx, user_id: int):
        self.bot.cmd_log(ctx, "xban")
        # Stolen from Joku
        # k thnx Laura
        # https://github.com/SunDwarf/Jokusoramame/blob/master/joku/cogs/mod.py#L135
        try:
            await ctx.bot.http.ban(user_id, ctx.message.guild.id, 0)
        except discord.Forbidden:
            await ctx.channel.send(":x: 403 FORBIDDEN")
        except discord.NotFound:
            await ctx.channel.send(":x: User not found.")
        else:
            await ctx.channel.send(":heavy_check_mark: Banned user {}.".format(user_id))

    @commands.command()
    async def kick(self, ctx, user: discord.Member):
        self.bot.cmd_log(ctx, "kick")
        if user:
            await ctx.guild.kick(user)
            self.bot.log.notice("Kicked {} from {}".format(user, ctx.guild.name))


def setup(bot):
    bot.add_cog(Moderation(bot))
