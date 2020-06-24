import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if 'ping' in message.content:
            await message.channel.send('pong')


client = MyClient()
client.run('NzI1MjQyOTMyMzkwNTI2OTk2.XvNmVg.dB42G_Tqne-bIzPZxUsjmFXzteo')
