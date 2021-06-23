import discord
import os

from .planechase import planechase

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged ins as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('/startgame'):
        await message.channel.send()

    if message.content.startswith('/rpd'):
        await message.channel.send(s)

client.run(os.env('TOKEN'))