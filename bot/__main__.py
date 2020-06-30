import discord
from bot import private, error_handler, wolfram, music, copy_command
from discord.ext import commands
from discord.utils import get


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

            if roles:
                for role in roles:
                    await role.delete()

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a mi general 😍"))

    async def on_member_join(self, member):
        rol = get(member.guild.roles, name="Nuevo")
        await member.add_roles(rol)
        channel = get(member.guild.text_channels, name="bienvenido")
        await channel.send('Holi {} de ahora me puedes llamar Lucy ❤️, debes elegir si ser procrastinador, socialista '
                           'o ambos, enviame !procrastinador o !socialista, y si quieres ser ambos enviames ambos o '
                           'es muy tonto lo que digo 🥰 ❤️'.format(member.mention))

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        rol_nuevo = get(message.author.roles, name="Nuevo")

        if message.channel.name == "bienvenido" and rol_nuevo:
            soc = '!socialista' in message.content.lower()
            pro = '!procrastinador' in message.content.lower()

            if soc:
                rol = get(message.author.guild.roles, name="Socialista")
                await message.author.add_roles(rol)

            if pro:
                rol = get(message.author.guild.roles, name="Procrastinador")
                await message.author.add_roles(rol)

            if soc or pro:
                await message.author.remove_roles(rol_nuevo)

            if not soc and not pro:
                await message.channel.send(
                    '{} amoroso debes decirme si ser !procrastinador o !socialista ❤️'.format(message.author.mention))


bot = Bot(command_prefix='l:', description='Lucy Gühiart')

bot.add_cog(error_handler.CommandErrorHandler(bot))
bot.add_cog(private.Private(bot))
bot.add_cog(wolfram.Wolfram(bot))
bot.add_cog(music.Music(bot))
bot.add_cog(copy_command.CopyCommand(bot))
bot.run('NzI1MjQyOTMyMzkwNTI2OTk2.XvNmVg.dB42G_Tqne-bIzPZxUsjmFXzteo')
