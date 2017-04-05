import discord
from discord.ext import commands
import random

class RNG():
    def __init__(self, bot):
        self.bot = bot

    # OUT OF DATE

    #Rolls a dice
    @commands.command()
    async def dice(self, dice : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
            if limit > 200:
                await self.bot.say("Have you ever seen a dice with more that 200 sides? I didn't think so")
                return
            if rolls > 400:
                await self.bot.say("You're expecting me to sit and roll dice all day? 400 or less rolls please")
                return
        except Exception:
            await self.bot.say('Format has to be in NdN!')
            return
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)
        print("Run: Dice")

    #Picks a random answer from a list of options
    #the user provides
    @commands.command(pass_context=True, hidden=True)
    async def choice(self, ctx, *, choices : str):
        """Chooses between options provided."""
        choiceslist = choices.split(",")
        member = ctx.message.author
        choice = random.choice(choiceslist)
        if len(choiceslist) < 2:
            #this is kinda messy, I'd rather not have to have people use commas but hey it works
            #so I don't care too much
            #letting people do !choice a b c rather than !choice a, b, c
            #just looks nice
            await self.bot.say("Please enter more than one option, separated with commas")
        else:
            #this outputs messy as fuck and it's disgusting, try it on the server
            message = "{0.mention} asked me to choose between {1}, and I chose {2}"
        await self.bot.say(message.format(member, choiceslist, choice))
        print("Run: Choice")

def setup(bot):
    bot.add_cog(RNG(bot))