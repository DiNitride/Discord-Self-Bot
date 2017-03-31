import discord
from discord.ext import commands

class Moderation():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverinfo(self, ctx):
        """Basic info on the server"""
        server = ctx.guild
        afk = server.afk_timeout / 60
        await ctx.send(
            "```xl\n" +
            "Name: {0.name}\n".format(server) +
            "Server ID: {0.id}\n".format(server) +
            "Region: {0.region}\n".format(server) +
            "Existed since: {0.created_at}\n".format(server) +
            "Owner: {0.owner}\n".format(server) +
            "AFK Timeout and Channel: {0} minutes in '{1.afk_channel}'\n".format(afk, server) +
            "Member Count: {0.member_count}\n".format(server) +
            "```")
        self.bot.cmd_log(ctx, "Server info")

def setup(bot):
    bot.add_cog(Moderation(bot))
