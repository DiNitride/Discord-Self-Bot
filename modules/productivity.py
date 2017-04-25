import discord
from discord.ext import commands
import random
import json
import asyncio

DIGITS = ('\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}',
          '\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}',
          '\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}',
          '\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}',
          '\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}',
          '\N{DIGIT SIX}\N{COMBINING ENCLOSING KEYCAP}',
          '\N{DIGIT SEVEN}\N{COMBINING ENCLOSING KEYCAP}',
          '\N{DIGIT EIGHT}\N{COMBINING ENCLOSING KEYCAP}',
          '\N{DIGIT NINE}\N{COMBINING ENCLOSING KEYCAP}',
          '\N{KEYCAP TEN}')
ARROWS = ('\N{LEFTWARDS BLACK ARROW}',
          '\N{BLACK RIGHTWARDS ARROW}')
CANCEL = '\N{CROSS MARK}'
UNDO = '\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS}'  # :arrows_counterclockwise:
DONE = '\N{WHITE HEAVY CHECK MARK}'

class Productivity:


    def __init__(self, bot):
        self.bot = bot
        try:
            with open("config/tags.json") as f:
                try:
                    self.tags = json.load(f)
                except json.decoder.JSONDecodeError:
                    with open("config/tags.json", "w") as f:
                        self.tags = {}
                        f.write(json.dumps(self.tags))
        except FileNotFoundError:
            with open("config/tags.json", "w") as f:
                self.tags = {}
                f.write(json.dumps(self.tags))

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, tag):
        """Provides tag access and management s!help tag for more"""
        if tag in self.tags:
            await ctx.message.edit(content=self.tags[tag])
        else:
            await ctx.message.edit(content=":x: Tag was not found")
        self.bot.cmd_log(ctx, "Tag {} called".format(tag))

    @tag.command()
    async def new(self, ctx, tag):
        """Creates a new tag"""
        if len(tag) > 50:
            await ctx.message("Tag names cannot be more than 50 characters long")
            self.bot.cmd_log(ctx, "Why so long tag names smh")
            return

        if tag in self.tags.keys():
            await ctx.send("")

        await ctx.message.edit(content="Creating new tag with name: {}, please enter tag content")

        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel

        try:
            output = await self.bot.wait_for("message", check=check, timeout=120)
            await output.delete()
            output = output.content
            self.tags[tag] = output
            await ctx.message.edit(content="Tag successfully! {} : {}".format(tag, output))
            self.bot.cmd_log(ctx, "Tag {} : {} created".format(tag, output))
        except asyncio.TimeoutError:
            await ctx.message.edit(content=":alarm_clock: Timed out! Tag not created")
            self.bot.cmd_log(ctx, "Tag creation failed")
        await self.save_tags()

    @tag.command(name="del")
    async def delete(self, ctx, tag):
        """Deletes a tag"""
        if tag in self.tags:
            del self.tags[tag]
            await ctx.message.edit(content="Tag {} deleted".format(tag))
            self.bot.cmd_log(ctx, "Tag {} deleted".format(tag))
        else:
            await ctx.message.edit(content=":x: Tag was not found")
            self.bot.cmd_log(ctx, "Tag deletion failed".format(tag))
        await self.save_tags()

    @tag.command()
    async def list(self, ctx):
        """Lists saved tags"""
        await ctx.message.delete()
        await self.reaction_menu(self.tags.keys(), ctx.message.author, ctx.message.channel, count=0, timeout=60,
                                 code=True, per_page=10)
        self.bot.cmd_log(ctx, "Tag list")

    async def save_tags(self):
        with open("config/tags.json", "w") as f:
            f.write(json.dumps(self.tags))
        self.bot.log.notice("Saved Tags")

    # Credit to sgtlaggy#5516 for the code this is based off
    # this is disgusting and messy but
    # oh well
    # sorry for ruining your lovely code laggy
    async def reaction_menu(self, options, user, destination, count=1, *, timeout=60,
                            code=True, per_page=10, header='', return_from=None):
        def check(r, u):
            return u == user

        if return_from is None:
            return_from = options
        elif len(return_from) != len(options):
            return None
        if count:
            reactions = (*DIGITS, *ARROWS, CANCEL, UNDO, DONE)
            if count > len(options):
                count = len(options)
            per_page = 10
        else:
            reactions = (*ARROWS, CANCEL, UNDO, DONE)
        pag = commands.Paginator(prefix='```' if code else '',
                                 suffix='```' if code else '')
        page_len = 0
        for ind, line in enumerate(options):
            if count:
                pag.add_line('{}. {}'.format(ind % 10 + 1, line))
            else:
                pag.add_line(line)
            page_len += 1
            if page_len == per_page:
                pag.close_page()
                page_len = 0
        pages = pag.pages
        page = 0
        header = header + '\n'
        choices = []
        msg = await destination.send(content=header + pages[page])
        while True:
            await msg.add_reaction(CANCEL)
            if page:
                await msg.add_reaction(ARROWS[0])
            if page != len(pages) - 1:
                await msg.add_reaction(ARROWS[1])
            try:
                res, r_user = await self.bot.wait_for('reaction_remove', check=check, timeout=timeout)
            except asyncio.TimeoutError:
                await msg.delete()
                return None
            if res.emoji == CANCEL:
                await msg.delete()
                return None
            elif res.emoji == ARROWS[0]:
                page -= 1
            elif res.emoji == ARROWS[1]:
                page += 1
            head = header + pages[page]
            await msg.edit(content=head)
        await msg.delete()
        return [return_from[ind] for ind in choices]


def setup(bot):
    bot.add_cog(Productivity(bot))
