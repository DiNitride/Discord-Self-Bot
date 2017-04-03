import discord
from discord.ext import commands
import random
import json

class Misc():
    def __init__(self, bot):
        self.bot = bot
        self.serverinfoaa.enabled = bot.modules["tags"]

    @commands.command()
    async def serverinfoaa(self, ctx):
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

    # @commands.command(hidden=True)
    # async def deltag(self, command: str):
    #     with open("tags.json") as file:
    #         tags = json.load(file)
    #         file.close()
    #     with open("tags.json", "w") as file:
    #         if command in tags:
    #             del tags[command]
    #             save = json.dumps(tags)
    #             file.write(save)
    #             await self.bot.say("Tag %s has been removed :thumbsup:" %command)
    #             print("Unregistered tag %s" %command)
    #         else:
    #             save = json.dumps(tags)
    #             file.write(save)
    #             await self.bot.say("Tag not registered, could not delete :thumbsdown: ")
    #             print("Tag unregister error, no tag %s" %command)
    #
    # @commands.command()
    # async def tags(self):
    #     """Lists the tags availible to output"""
    #     with open("tags.json") as file:
    #         tags = json.load(file)
    #         taglist = "```Tags:"
    #         for x in tags.keys():
    #             taglist = "%s\n- %s" %(taglist, x)
    #         await self.bot.say("{0} ```".format(taglist))
    #         print("Run: Tags Listed")
    #
    # @commands.command()
    # async def tag(self, input : str, output : str = None):
    #     """Searches tags for output"""
    #     with open("tags.json") as file:
    #         tags = json.load(file)
    #         if input in tags:
    #             await self.bot.say(tags[input])
    #             print("Run: Tag %s" %input)
    #         else:
    #             with open("tags.json", "w") as file:
    #                 tags[input] = output
    #                 save = json.dumps(tags)
    #                 file.write(save)
    #                 if output.startswith("http"):
    #                     await self.bot.say("Tag %s has been added with output <%s> :thumbsup:" % (input, output))
    #                 else:
    #                     await self.bot.say("Tag %s has been added with output %s :thumbsup:" % (input, output))
    #                 print("Registered tag %s" % input)
def setup(bot):
    bot.add_cog(Misc(bot))
