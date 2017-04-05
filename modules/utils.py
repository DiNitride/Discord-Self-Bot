import discord
from discord.ext import commands
import datetime


async def construct_serverinfo(obj):
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

    content = "```\n" \
              "Server Name: {}\nID: {}\n" \
              "Members: {}\n" \
              "Channels: {}\n" \
              "Roles: {}\n" \
              "AFK Channel: {}\n" \
              "AFK Timeout: {}\n" \
              "Owner: {}\n" \
              "Creation Date: {}\n" \
              "Region: {}\n" \
              "Verification Level: {}\n" \
              "```".format(obj.name, obj.id, len(obj.members), len(obj.channels),
                           len(obj.roles), obj.afk_channel, str(obj.afk_timeout / 60), obj.owner,
                           obj.created_at, obj.region, obj.verification_level)

    return embed, content

async def construct_userinfo(obj):
    profile = await obj.profile()
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

    content = "```\n" \
              "{}\nID: {}\n" \
              "Friends?: {}\n" \
              "Mututal Guilds: {}\n" \
              "Nitro?: {}\n" \
              "Account Creation Data: {}\n" \
              "```".format(obj, obj.id, obj.is_friend(), len(profile.mutual_guilds),
                           profile.premium, obj.created_at)

    return embed, content


class Utils:

    def __init__(self, bot):
        self.bot = bot
        self.whois.enabled = bot.modules["utils"]
        self.about.enabled = bot.modules["utils"]
        self.server.enabled = bot.modules["utils"]

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
                embed, content = await construct_userinfo(obj)
            else:
                embed, content = await construct_serverinfo(obj)
            if ctx.channel.permissions_for(ctx.author).embed_links:
                await ctx.send(embed=embed)
            else:
                await ctx.send(content)
        else:
            await ctx.send("Nothing found :skull_crossbones: ")

        await ctx.message.delete()

    @commands.group(invoke_without_command=True)
    async def about(self, ctx, userObj: discord.Member = None):
        """Information on a user"""
        if userObj is None:
            userObj = ctx.author
        embed, content = await construct_userinfo(userObj)
        if ctx.channel.permissions_for(ctx.author).embed_links:
            embed.set_footer(text="About")
            embed.add_field(name="Roles", value=str(len(userObj.roles)))
            embed.add_field(name="Date Joined Guild", value=userObj.joined_at)
            embed.add_field(name="Game", value=userObj.game)
            embed.add_field(name="Status", value=userObj.status)
            embed.add_field(name="Nickname", value=userObj.nick)
            await ctx.send(embed=embed)
        else:
            content = content.strip("`")
            content += "Roles: {}\n" \
                       "Date Joined Guild: {}\n" \
                       "Game: {}\n" \
                       "Status: {}\n" \
                       "Nickname: {}\n" \
                       "```".format(len(userObj.roles), userObj.joined_at, userObj.game, userObj.status, userObj.nick)

            await ctx.send("```\n" + content)
        await ctx.message.delete()
        self.bot.cmd_log(ctx, "About User")

    @about.command()
    async def server(self, ctx):
        """Basic info on the server"""
        embed, content = await construct_serverinfo(ctx.guild)
        if ctx.channel.permissions_for(ctx.author).embed_links:
            embed.set_footer(text="About Server")
            await ctx.send(embed=embed)
        else:
            await ctx.send(content)
        await ctx.message.delete()
        self.bot.cmd_log(ctx, "About Server")


def setup(bot):
    bot.add_cog(Utils(bot))
