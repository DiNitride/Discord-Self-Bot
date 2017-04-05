import discord
from discord.ext import commands
import datetime


class Moderation:

    def __init__(self, bot):
        self.bot = bot
        self.ban.enabled = bot.modules["moderation"]
        self.kick.enabled = bot.modules["moderation"]

    @commands.command()
    async def ban(self, ctx, user: discord.Member, delete_days=1):
        self.bot.cmd_log(ctx, "ban")
        if delete_days > 7:
            delete_days = 7
        if user:
            await ctx.guild.ban(user, delete_message_days=delete_days)
            self.bot.log.notice("Kicked {} from {}".format(user, ctx.guild.name))

    @commands.command()
    async def kick(self, ctx, user: discord.Member):
        self.bot.cmd_log(ctx, "kick")
        if user:
            await ctx.guild.kick(user)
            self.bot.log.notice("Kicked {} from {}".format(user, ctx.guild.name))


def setup(bot):
    bot.add_cog(Moderation(bot))
