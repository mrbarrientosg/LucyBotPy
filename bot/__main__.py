import discord
from bot import private, error_handler
from discord.ext import commands


bot = commands.Bot(command_prefix='l:', description='Lucy Gühiart')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a mi general 😍"))

bot.add_cog(error_handler.CommandErrorHandler(bot))
bot.add_cog(private.Private(bot))
bot.run('NzI1MjQyOTMyMzkwNTI2OTk2.XvNmVg.dB42G_Tqne-bIzPZxUsjmFXzteo')
