import discord
from discord.ext import commands
import random
import json
import asyncio

class Tags():
    def __init__(self, bot):
        self.bot = bot
        try:
            with open("config/tags.json") as f:
                self.tags = json.load(f)
        except FileNotFoundError:
            with open("config/tags.json", "w") as f:
                self.tags = {}
                f.write(json.dumps(self.tags))

        self.bot.bg_task = self.bot.loop.create_task(self.save_tags())


    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, tag):


    async def save_tags(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open("config/tags.json", "w") as f:
                f.write(json.dumps(self.tags))
            self.bot.log.notice("Saved Tags")
            await asyncio.sleep(120)



def setup(bot):
    bot.add_cog(Tags(bot))
