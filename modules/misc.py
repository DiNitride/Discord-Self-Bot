import discord
from discord.ext import commands

class Misc:


    def __init__(self, bot):
        self.bot = bot

    # Thank u 2 Jamiea 4 the sauce code 4 this
    @commands.command()
    async def emoji(self, ctx, *, text: str):
        """Converts sentence to emoji sentence"""
        output_string = []
        text = text.upper()
        for i in text.replace(" ", "   "):
            if 64 < ord(i) < 91:
                output_string.append(chr(ord(i) + 127397))
            elif 47 < ord(i) < 58:
                output_string.append(i + chr(8419))
            else:
                output_string.append(i)
        await ctx.message.edit(content=" ".join(output_string))
        self.bot.cmd_log(ctx, "Emoji")


def setup(bot):
    bot.add_cog(Misc(bot))
