import discord
from bot import private, error_handler
from discord.ext import commands

bot = commands.Bot(command_prefix='l:', description='Lucy Gühiart')


@bot.event
async def on_ready():
    for guild in bot.guilds:
        text_channel = [text for text in guild.text_channels if text.name.startswith('lprivate-')]

        if text_channel:
            for channel in text_channel:
                await channel.delete()

        voice_channel = [voice for voice in guild.voice_channels if voice.name.startswith('lprivate-')]

        if voice_channel:
            for channel in voice_channel:
                await channel.delete()

        roles = [role for role in guild.roles if role.name.startswith('lprivate-')]

        if voice_channel:
            for role in roles:
                await role.delete()

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a mi general 😍"))


bot.add_cog(error_handler.CommandErrorHandler(bot))
bot.add_cog(private.Private(bot))
bot.run('NzI1MjQyOTMyMzkwNTI2OTk2.XvNmVg.dB42G_Tqne-bIzPZxUsjmFXzteo')
