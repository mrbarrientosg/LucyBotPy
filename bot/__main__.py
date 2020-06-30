import discord
from bot import private, error_handler, wolfram, music, copy_command
from discord.ext import commands


class Bot(commands.Bot):

    async def on_ready(self):
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


bot = Bot(command_prefix='lt:', description='Lucy Gühiart')

bot.add_cog(error_handler.CommandErrorHandler(bot))
bot.add_cog(private.Private(bot))
bot.add_cog(wolfram.Wolfram(bot))
bot.add_cog(music.Music(bot))
bot.add_cog(copy_command.CopyCommand(bot))
bot.run('NzI3MDAyMDcxMzQ5MzI5OTMw.Xvlffg.Q9cI34neuqdKhW7aeQAP4abFKYw')
