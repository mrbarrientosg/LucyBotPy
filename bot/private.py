import discord
import uuid
import asyncio
import typing
import numpy as np
from discord.ext import commands
from enum import Enum


class ChannelTypePrivate(Enum):
    voice = 1
    both = 2
    none = 3


class ChannelTypeConverter(commands.Converter):
    async def convert(self, ctx, argument: str):
        try:
            return ChannelTypePrivate[argument]
        except:
            return ChannelTypePrivate.none


class Private(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_task = None
        self.channels = list()

    @commands.group()
    async def private(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                '{}, amorosa no sabes ocupar el private, ve mi flor de ayuda!! ❤️'.format(ctx.author.mention))

    @private.command()
    async def remove(self, ctx):
        if not any('private' in role.name for role in ctx.author.roles):
            return await ctx.send(
                '{}, amiga no estas en un privado ❤️'.format(ctx.author.mention))

        role = [role for role in ctx.author.roles if role.name.startswith('lprivate-')][0]

        if ctx.author.voice is not None and ctx.author.voice.channel is not None:
            if ctx.author.voice.channel.name == role.name:
                await ctx.author.move_to(None)

        return await ctx.author.remove_roles(role)

    @private.command()
    async def invite(self, ctx, *args: typing.Union[discord.Member, discord.User]):
        if not any('lprivate' in role.name for role in ctx.author.roles):
            return await ctx.send(
                '{}, amiga tienes que estar en un privado para invitar ❤️'.format(ctx.author.mention))

        all_members = np.array([member for member in args if not member.bot])
        all_members = np.array([member for member in all_members if member.id != ctx.author.id])

        private_members = [member for member in all_members if any('lprivate' in role.name for role in member.roles)]
        all_members = np.array([member for member in all_members if not member in private_members])

        role = [role for role in ctx.author.roles if role.name.startswith('lprivate-')][0]

        for member in all_members:
            try:
                await member.add_roles(role)
            except discord.HTTPException:
                return await ctx.send(
                    '{}, amiga me dio un lag mental, no puedo ayudarte!! ❤️'.format(ctx.author.mention))

        if all_members:
            await ctx.send(
                'amiga {}, {} te ha invitado a un privado ❤️'.format(' '.join(member.mention for member in all_members),
                                                                     ctx.author.mention))
        else:
            return await ctx.send(
                '{}, amiga ya invitaste a tus amigos, invita a otros no seas ingrata!! ❤️'.format(ctx.author.mention))

    @private.command()
    async def create(self, ctx, type: ChannelTypeConverter, *args: typing.Union[discord.Member, discord.User]):
        if type == ChannelTypePrivate.none:
            return await ctx.send('{}, amorosa te falta el tipo del canal!! ❤️'.format(ctx.author.mention))

        # Mantengo todos los miembros en un arreglo
        all_members = np.array(args)
        all_members = np.append(all_members, ctx.author)  # se agrega el mismo autor del mensaje

        # Elimino todos los bot de los miembros que pasan por argumento
        all_members = np.array([member for member in all_members if not member.bot])

        # Obtengo los miembres que ya esta en un privado y hago un join con los actuales
        private_members = [member for member in all_members if any('lprivate' in role.name for role in member.roles)]
        all_members = np.array([member for member in all_members if not member in private_members])

        # Valido las condiciones
        if all_members.size == 0:
            return await ctx.send('{}, amorosa ya estas en un canal privado, besos!! ❤️'.format(ctx.author.mention))
        elif private_members:
            return await ctx.send(
                '{}, amorosa hay amigos que ya estan en un privado 1313 ❤️'.format(ctx.author.mention))

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
                '{}, amiga tienes que estar conectada, no puedes dejar a tu(s) amiga(s) sola(s) ❤️'.format(
                    ctx.author.mention))

        guild = ctx.guild
        id = uuid.uuid4().node
        name = 'lprivate-{}'.format(id)

        role = None

        try:
            role = await guild.create_role(name=name)
        except discord.HTTPException:
            return await ctx.send('{}, amiga me dio un lag mental, no puedo ayudarte!! ❤️'.format(ctx.author.mention))

        category = discord.utils.get(guild.categories, name='privado')

        channel = None

        try:
            if type is ChannelTypePrivate.voice:
                channel = await guild.create_voice_channel(name=name, category=category)
            else:
                channel = (await guild.create_text_channel(name=name, category=category), await guild.create_voice_channel(name=name, category=category))
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
            if type is ChannelTypePrivate.both:
                await channel[0].set_permissions(target=role, overwrite=permission)
                await channel[1].set_permissions(target=role, overwrite=permission)
            else:
                await channel.set_permissions(target=role, overwrite=permission)

        except discord.HTTPException:
            await self._remove_channels(channel, type)
            await role.delete()
            return await ctx.send('{}, amiga me dio un lag mental, no puedo ayudarte!! ❤️'.format(ctx.author.mention))

        exception = False
        for user in all_members:
            try:
                await user.add_roles(role)

                if type is ChannelTypePrivate.voice:
                    await user.move_to(channel)
                elif type is ChannelTypePrivate.both:
                    await user.move_to(channel[1])

            except discord.HTTPException:
                if not exception:
                    await ctx.send(
                        '{}, tu(s) amiga(s) se quedo dormida, asi que no la puedo mover ❤️'.format(ctx.author.mention))
                    exception = True

        for member in not_connected_members:
            try:
                await member.add_roles(role)
            except discord.HTTPException:
                return await ctx.send(
                    '{}, amiga me dio un lag mental, no puedo ayudarte!! ❤️'.format(ctx.author.mention))

        if not self.channels:
            self.voice_task = self.bot.loop.create_task(self._check_voice_channels())

        self.channels.append((channel, type, role))

    def _check_empty_members(self, members, author):
        if members.size == 0:
            return True

        users = [member for member in members if member.id == author.id]
        members = [member for member in members if not member in users]

        if users and not members:
            return True
        else:
            return False

    async def _check_voice_channels(self):
        await self.bot.wait_until_ready()

        while True:
            await asyncio.sleep(900)

            if not self.channels:
                self.voice_task.cancel()
                self.voice_task = None

            for channel, type, role in self.channels:
                if type is ChannelTypePrivate.voice and not channel.members:
                    await self._remove_channels(channel, type)
                    await role.delete()
                    self.channels = [r for _, _, r in self.channels if r.name != role.name]
                elif type is ChannelTypePrivate.both and not channel[1].members:
                    await self._remove_channels(channel, type)
                    await role.delete()
                    self.channels = [r for _, _, r in self.channels if r.name != role.name]

    async def _remove_channels(self, channel, type):
        if type is ChannelTypePrivate.both:
            await channel[0].delete()
            await channel[1].delete()
        else:
            await channel.delete()
