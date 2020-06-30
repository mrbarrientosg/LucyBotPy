import discord
import validators
from discord.ext import commands


class Answer:
    def __init__(self, prg, res):
        self.prg = prg
        self.res = res

    def embed(self):
        embed = discord.Embed()
        embed.title = self.prg
        if validators.url(self.res):
            embed.set_image(url = self.res )
        else:
            embed.add_field(name = "respuesta", value = self.res, inline = False)

        return embed

class Answers:
    def __init__(self):
        self.respuestas = dict()


    def agregarRespuesta(self, curso, res:Answer):
        if not curso in self.respuestas:
            self.respuestas[curso] = list()
        self.respuestas[curso].append(res)

    def lista(self,curso):
        if not curso in self.respuestas:
            return list()

        return self.respuestas[curso]

    def delete(self, curso, i):
        if not curso in self.respuestas:
            return False

        if i < 1 or i > len(self.respuestas):
            return False

        self.respuestas[curso].pop(i-1)
        return True


class CopyCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.answers = Answers()


    @commands.group()
    async def copi(self, ctx):

        if ctx.invoked_subcommand is None:
            await ctx.send(
                '{}, amorosa no sabes ocupar el copi, ve mi flor de ayuda!! ❤️'.format(ctx.author.mention))

    @copi.command()
    async def add(self, ctx, curso, prg, res = None):
        res2 = None
        if ctx.message.attachments:
            res2 = ctx.message.attachments[0].url
        elif res is not None:
            res2 = res

        else:
            return await ctx.send("Amorosa una pregunta siempre tiene respuesta ❤️")
        ans = Answer(prg, res2)
        self.answers.agregarRespuesta(curso, ans)
        await ctx.send("Querido, se te agrego la respuesta correctamente, la cuidare como mi flor")

    @copi.command()
    async def list(self, ctx, curso):
        respuestas = self.answers.lista(curso)

        list = ""
        for i, respuesta in enumerate(respuestas):
            list += '`{}.` [**{}**]\n'.format(i + 1,respuesta.prg)

        embed = (discord.Embed(description='**{} preguntas:**\n\n{}'.format(len(respuestas), list)))
        await ctx.send(embed=embed)

    @copi.command()
    async def view(self,ctx, curso, i:int ):
        respuestas = self.answers.lista(curso)
        if i < 1 or i > len(respuestas):
            return await ctx.send("Querida ese indice esta fuera de rango")
        respuesta = respuestas[i-1]
        channel = await ctx.author.create_dm()
        await channel.send(embed = respuesta.embed())

    @copi.command()
    async def delete(self,ctx, curso, i:int ):
        if not self.answers.delete(curso,i):
            return await ctx.send("Querida no pudo ser eliminada")
        else:
            return await ctx.send("Querida logramos eliminarla")

    @copi.command()
    async def courses(self, ctx):
        list = ""
        for curso in self.answers.respuestas:
            list += '[**{}**] ({})\n'.format(curso,len(self.answers.respuestas[curso]))

        embed = (discord.Embed(description='** cursos:**\n\n{}'.format(list)))
        await ctx.send(embed=embed)