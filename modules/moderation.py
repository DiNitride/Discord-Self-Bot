import discord
from discord.ext import commands
import datetime

class Moderation():
    def __init__(self, bot):
        self.bot = bot
        self.serverinfo.enabled = bot.modules["moderation"]
        self.ban.enabled = bot.modules["moderation"]
        self.kick.enabled = bot.modules["moderation"]

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


    @commands.command()
    async def whois(self, ctx, id):
        self.bot.cmd_log(ctx, "whois")
        isUser = True
        id = int(id)
        obj = self.bot.get_user(id)
        self.bot.log.notice("Searched for user with ID {}".format(id))
        if not obj:
            isUser = False
            obj = self.bot.get_guild(id)
            self.bot.log.notice("Searched for guild with ID {}".format(id))
        if obj:
            if isUser:
                profile = await obj.profile()
                embed = discord.Embed(colour=discord.Colour(0x30f9c7), description="ID: {}".format(obj.id),
                                      timestamp=datetime.datetime.utcfromtimestamp(1490992111))

                embed.set_thumbnail(
                    url=obj.avatar_url)
                embed.set_author(name=obj)
                embed.set_footer(text="Who Is")

                embed.add_field(name="Friends?", value=obj.friends)
                embed.add_field(name="Mutual Guilds", value=profile.mutual_guilds)
                embed.add_field(name="Is Bot?", value=obj.bot)
                embed.add_field(name="Account Creation Date", value=obj.created_at)



                await ctx.send(obj)
        else:
            await ctx.send("Nothing found :skull_crossbones: ")


def setup(bot):
    bot.add_cog(Moderation(bot))
