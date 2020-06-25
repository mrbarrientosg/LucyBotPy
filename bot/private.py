import discord
import uuid
import asyncio
import typing
import numpy as np
from discord.ext import commands


class Private(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bg_task = None
        self.channels = list()

    @commands.group()
    async def private(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid sub command passed...')

    @private.command()
    async def create(self, ctx, *args: typing.Union[discord.Member, discord.User]):
        # Mantengo todos los miembros en un arreglo
        all_members = np.array(args)
        all_members = np.append(all_members, ctx.author)  # se agrega el mismo autor del mensaje

        # Elimino todos los bot de los miembros que pasan por argumento
        all_members = np.array([member for member in all_members if not member.bot])

        # Obtengo los miembres que ya esta en un privado y hago un join con los actuales
        private_members = [member for member in all_members if any('private' in role.name for role in member.roles)]
        all_members = np.array([member for member in all_members if not member in private_members])

        # Valido las condiciones
        if all_members.size == 0:
            return await ctx.send('{}, amorosa ya estas en un canal privado, besos!! ❤️'.format(ctx.author.mention))
        elif private_members:
            return await ctx.send('{}, amorosa hay amigos que ya estan en un privado 1313 ❤️'.format(ctx.author.mention))

        # Hay que verficar que esten todos conectados
        not_connected_members = [member for member in all_members if
                                 member.voice is None or member.voice.afk or member.voice.channel is None]

        all_members = np.array([member for member in all_members if not member in not_connected_members])

        if all_members.size == 1:
            return await ctx.send(
                '{}, amorosa no hay nadie conectado para hacer un privado ❤️'.format(ctx.author.mention))
        elif self._check_empty_members(all_members, ctx.author):
            return await ctx.send(
                '{}, amiga aqui aceptamos solo socialismo nada de soledad ❤️'.format(ctx.author.mention))
        elif ctx.author.voice is None:
            return await ctx.send(
                '{}, amiga tienes que estar conectada, no puedes dejar a tu(s) amiga(s) sola(s) ❤️'.format(ctx.author.mention))

        guild = ctx.guild
        id = uuid.uuid1().node
        name = 'private-{}'.format(id)

        role = None

        try:
            role = await guild.create_role(name=name)
        except discord.HTTPException:
            return await ctx.send('{}, amiga me dio un lag mental, no puedo ayudarte!! ❤️'.format(ctx.author.mention))

        category = discord.utils.get(guild.categories, name='privado')

        voice_channel = None

        try:
            voice_channel = await guild.create_voice_channel(name=name, category=category)
        except discord.HTTPException:
            await role.delete()
            return await ctx.send('{}, amiga me dio un lag mental, no puedo ayudarte!! ❤️'.format(ctx.author.mention))

        try:
            permission = discord.PermissionOverwrite()
            permission.update(connect=True,
                              speak=True,
                              move_members=False,
                              manage_roles=False,
                              manage_permissions=False,
                              view_channel=True)
            await voice_channel.set_permissions(target=role, overwrite=permission)
        except discord.HTTPException:
            await voice_channel.delete()
            await role.delete()
            return await ctx.send('{}, amiga me dio un lag mental, no puedo ayudarte!! ❤️'.format(ctx.author.mention))

        exception = False
        count = 0
        for user in all_members:
            try:
                await user.add_roles(role)
                await user.move_to(voice_channel)
            except discord.HTTPException:
                count += 1
                if not exception:
                    await ctx.send(
                        '{}, tu(s) amiga(s) se quedo dormida, asi que no la puedo mover ❤️'.format(ctx.author.mention))
                    exception = True

        for member in not_connected_members:
            try:
                await member.add_roles(role)
            except discord.HTTPException:
                return await ctx.send('{}, amiga me dio un lag mental, no puedo ayudarte!! ❤️'.format(ctx.author.mention))

        if len(all_members) == count:
            await voice_channel.delete()
            await role.delete()
            return

        if not self.channels:
            self.bg_task = self.bot.loop.create_task(self._check_channels())

        self.channels.append((voice_channel, role))

    def _check_empty_members(self, members, author):
        if members.size == 0:
            return True

        users = [member for member in members if member.id == author.id]
        members = [member for member in members if not member in users]

        if users and not members:
            return True
        else:
            return False

    async def _check_channels(self):
        await self.bot.wait_until_ready()

        while True:
            print(len(self.channels))
            if not self.channels:
                self.bg_task.cancel()
                self.bg_task = None

            for channel, role in self.channels:
                if not channel.members:
                    await channel.delete()
                    await role.delete()
                    self.channels.remove((channel, role))

            await asyncio.sleep(10)  # 1800
