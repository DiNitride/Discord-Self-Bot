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
            content = None
            embed = None
            if isUser:
                profile = await obj.profile()
                if ctx.channel.permissions_for(ctx.author).embed_links:

                    embed = discord.Embed(colour=discord.Colour(0x30f9c7), description="ID: {}".format(obj.id),
                                          timestamp=datetime.datetime.utcfromtimestamp(1490992111))

                    embed.set_thumbnail(
                        url=obj.avatar_url)
                    embed.set_author(name=obj)
                    embed.set_footer(text="Who Is")

                    embed.add_field(name="Friends?", value=obj.is_friend())
                    embed.add_field(name="Mutual Guilds", value=str(len(profile.mutual_guilds)))
                    embed.add_field(name="Nitro?", value=profile.premium)
                    embed.add_field(name="Account Creation Date", value=obj.created_at)
                else:
                    content = "```\n" \
                              "{}\nID: {}\n" \
                              "Friends?: {}\n" \
                              "Nitro?: {}\n" \
                              "Account Creation Data: {}\n" \
                              "```".format(
                        obj, obj.id, obj.is_friend(), len(profile.mutual_guilds), profile.premium, obj.created_at
                    )
            else:
                if ctx.channel.permissions_for(ctx.author).embed_links:

                    embed = discord.Embed(title="ID: 58934178071780", colour=discord.Colour(0x610073),
                                          timestamp=datetime.datetime.utcfromtimestamp(1491012420))

                    embed.set_thumbnail(
                        url=obj.icon_url)
                    embed.set_author(name=obj.name)
                    embed.set_footer(text="Who Is")

                    embed.add_field(name="Members", value=str(len(obj.members)))
                    embed.add_field(name="Roles", value=str(len(obj.roles)))
                    embed.add_field(name="Channels", value=str(len(obj.channels)))
                    embed.add_field(name="AFK Channel", value=obj.afk_channel)
                    embed.add_field(name="AFK Timeout", value=str(obj.afk_timeout / 60))
                    embed.add_field(name="Owner", value=obj.owner)
                    embed.add_field(name="Creation Date", value=obj.created_at)
                    embed.add_field(name="Region", value=obj.region)
                    embed.add_field(name="Verification Level", value=obj.verification_level)

                else:
                    content = "```\n" \
                              "{}\nID: {}\n" \
                              "Members: {}\n" \
                              "Channels: {}\n" \
                              "Roles: {}\n" \
                              "AFK Channel: {}\n" \
                              "AFK Timeout: {}\n" \
                              "Owner: {}\n" \
                              "Creation Date: {}\n" \
                              "Region: {}\n" \
                              "Verification Level: {}\n" \
                              "```".format(
                        obj.name, obj.id, len(obj.members), len(obj.channels), len(obj.roles), obj.afk_channel,
                        str(obj.afk_timeout / 60), obj.owner, obj.created_at, obj.region, obj.verification_level
                    )


            await ctx.send(content=content, embed=embed)

        else:
            await ctx.send("Nothing found :skull_crossbones: ")


def setup(bot):
    bot.add_cog(Moderation(bot))
