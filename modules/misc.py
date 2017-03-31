import discord
from discord.ext import commands
import random
import json

class Misc():
    def __init__(self, bot):
        self.bot = bot

    # Allowed the removal of a tag from the data file
    @commands.command(hidden=True)
    async def deltag(self, command: str):
        with open("tags.json") as file:
            tags = json.load(file)
            file.close()
        with open("tags.json", "w") as file:
            if command in tags:
                del tags[command]
                save = json.dumps(tags)
                file.write(save)
                await self.bot.say("Tag %s has been removed :thumbsup:" %command)
                print("Unregistered tag %s" %command)
            else:
                save = json.dumps(tags)
                file.write(save)
                await self.bot.say("Tag not registered, could not delete :thumbsdown: ")
                print("Tag unregister error, no tag %s" %command)

    # Lists all the tags currently stored
    # Command output looks really ugly
    # Needs make-over
    @commands.command()
    async def tags(self):
        """Lists the tags availible to output"""
        with open("tags.json") as file:
            tags = json.load(file)
            taglist = "```Tags:"
            for x in tags.keys():
                taglist = "%s\n- %s" %(taglist, x)
            await self.bot.say("{0} ```".format(taglist))
            print("Run: Tags Listed")

    # Allows the user to find and execute a tags
    @commands.command()
    async def tag(self, input : str, output : str = None):
        """Searches tags for output"""
        with open("tags.json") as file:
            tags = json.load(file)
            if input in tags:
                await self.bot.say(tags[input])
                print("Run: Tag %s" %input)
            else:
                with open("tags.json", "w") as file:
                    tags[input] = output
                    save = json.dumps(tags)
                    file.write(save)
                    if output.startswith("http"):
                        await self.bot.say("Tag %s has been added with output <%s> :thumbsup:" % (input, output))
                    else:
                        await self.bot.say("Tag %s has been added with output %s :thumbsup:" % (input, output))
                    print("Registered tag %s" % input)
def setup(bot):
    bot.add_cog(Misc(bot))
