import discord
from discord.ext import commands



class CopyCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def copy(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                '{}, amorosa no sabes ocupar el private, ve mi flor de ayuda!! ❤️'.format(ctx.author.mention))