import discord
import os
import time

import planechase as pc

client = discord.Client()

game = pc.Planechase()

@client.event
async def on_ready():
    print("We have logged ins as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/startgame'):
        content_str = "Welcome to planechase!"
        await message.channel.send(content_str)

    rpd_outcome = None
    if message.content.startswith('/rpd'):
        content_str="Rolling planar die..."
        await message.channel.send(content_str)
        rpd_outcome = game.roll_planar_die()
        if (rpd_outcome==""):
            content_str = "Nothing Happens."
            await message.channel.send(content_str)
        elif (rpd_outcome=="chaos"):
            content_str = "Chaos rolled!"
            await message.channel.send(content_str)
        elif (rpd_outcome=="planeswalk"):
            content_str = "Planeswalk rolled!"
            await message.channel.send(content_str)
    
    if message.content.startswith('/plane') or message.content.startswith('/startgame') or rpd_outcome == "planeswalk": 
        pic_file = discord.File(fp=game.get_current_plane_image())
        content_str = "**Current Plane**: {}\n\n".format(game.get_current_plane_name())
        print(len(pic_file))
        # await message.channel.send(content_str, file=pic_embed)
        time.sleep(0.3)

    if message.content.startswith('/static') or message.content.startswith('/startgame') or message.content.startswith('/plane'):
        content_str = "**Static ability**: {}".format(game.get_current_plane_static_ability())
        await message.channel.send(content_str)

    if message.content.startswith('/chaos') or message.content.startswith('/startgame') or message.content.startswith('/plane') or rpd_outcome == "chaos":
        content_str = "**Chaos ability**: {}".format(game.get_current_plane_chaos_ability() if game.get_current_plane_chaos_ability() else "None")
        await message.channel.send(content_str)
    
    if message.content.startswith('/help'):
        content_str = "**Bot commands:**\n"
        content_str += "**/start_game:** Start a new game and walks to a random plane.\n"
        content_str += "**/rpd:** Roll the planar die.\n"
        content_str += "**/plane:** Get information about the current plane.\n"
        content_str += "**/static:** Get the current plane's static ability.\n"
        content_str += "**/chaos:** Get the current plane's chaos ability if it has one."
        await message.channel.send(content_str)

client.run(os.getenv('TOKEN'))
    