import discord
import uuid
import asyncio
import typing
from discord.ext import commands


class Private(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bg_task = None
        self.channels = list()

    @commands.command()
    async def private(self, ctx, *args: typing.Union[discord.Member, discord.User]):
        is_bot = filter(lambda user: user.bot, args)

        if list(is_bot):
            return await ctx.send('{}, amiga los bots no son personas, saludos 😘 ❤️'.format(ctx.author.mention))

        if not args or ctx.author.id == args[0].id:
            return await ctx.send(
                '{}, amiga aqui aceptamos solo socialismo nada de soledad ❤️'.format(ctx.author.mention))

        has_private = filter(lambda role: role.name.startswith('private-'), ctx.author.roles)

        if list(has_private):
            return await ctx.send('{}, amorosa ya estas en un canal privado, besos!! ❤️'.format(ctx.author.mention))

        members_private = list()

        for member in args:
            if not any('private' in role.name for role in member.roles):
                members_private.append(member)

        if not members_private:
            return await ctx.send('{}, amorosa hay amigos que ya estan en un privado 1313 ❤️'.format(ctx.author.mention))

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
            permission.connect = True
            permission.speak = True
            permission.move_members = False
            permission.manage_roles = False
            permission.manage_permissions = False
            permission.view_channel = True
            await voice_channel.set_permissions(target=role, overwrite=permission)
        except discord.HTTPException:
            await voice_channel.delete()
            await role.delete()
            return await ctx.send('{}, amiga me dio un lag mental, no puedo ayudarte!! ❤️'.format(ctx.author.mention))

        exception = False
        count = 0
        for user in members_private:
            try:
                await user.add_roles(role)
                await user.move_to(voice_channel)
            except discord.HTTPException:
                count += 1
                if not exception:
                    await ctx.send(
                        '{}, tu(s) amiga(s) se quedo dormida, asi que no la puedo mover ❤️'.format(ctx.author.mention))
                    exception = True

        if len(members_private) == count:
            await voice_channel.delete()
            await role.delete()
            return

        try:
            await ctx.author.add_roles(role)
            await ctx.author.move_to(voice_channel)
        except discord.HTTPException:
            await ctx.send('{}, amiga no te veo conectado para moverte ❤️'.format(ctx.author.mention))

        if not self.channels:
            self.bg_task = self.bot.loop.create_task(self._check_channels())

        self.channels.append((voice_channel, role))

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
