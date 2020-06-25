import discord
from bot import private, error_handler
from discord.ext import commands


bot = commands.Bot(command_prefix='!', description='Lucy Gühiart')



"""
@bot.command()
async def ping(ctx, name, category_name=None):

    if category_name is None:
        category = discord.utils.get(ctx.guild.categories, id=ctx.channel.category_id)
    else:
        category = discord.utils.get(ctx.guild.categories, name=category_name)
        
    # Setting `Watching ` status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a tu vieja"))
    
    guild = ctx.message.guild
    await guild.create_voice_channel(name, category=category)
"""

bot.add_cog(error_handler.CommandErrorHandler(bot))
bot.add_cog(private.Private(bot))
bot.run('NzI1MjQyOTMyMzkwNTI2OTk2.XvNmVg.dB42G_Tqne-bIzPZxUsjmFXzteo')
