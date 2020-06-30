import re
import discord
import wolframalpha
from discord.ext import commands

ipv4_regex = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
ipv6_regex = re.compile(
    r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')


class Wolfram(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.wolf = wolframalpha.Client('T779G9-JRYWTKWU4J')

    @commands.command()
    async def wolf(self, ctx, query):
        res = self.wolf.query(query)

        for pod in res.pods:
            if pod.text:
                await self.printPod(ctx, pod.text, pod.title)
            elif 'img' in pod:
                await self.printImgPod(ctx, list(pod.img)[0].src, pod.title)

            for subpod in pod.subpods:
                if 'text' in subpod:
                    await self.printPod(ctx, subpod.text, subpod.title)
                elif 'img' in subpod:
                    await self.printImgPod(ctx, list(subpod.img)[0].src, subpod.title)

    async def printPod(self, ctx, text, title):
        text = text.replace("Wolfram|Alpha", "Lucy")
        text = text.replace("Wolfram", "Wolf")
        text = re.sub(ipv4_regex, "IP Redacted", text)
        text = re.sub(ipv6_regex, "IP Redacted", text)
        await ctx.send("__**" + title + ":**__\n" + "`" + text + "`")

    async def printImgPod(self, ctx, img, title):
        embed = discord.Embed(title=title)
        embed.set_image(url=img)
        await ctx.send(embed=embed)
