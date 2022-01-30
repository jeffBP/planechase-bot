import discord
import os
import time

import planechase as pc

client = discord.Client()

game = pc.Planechase()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/start_game'):
        content_str = "Welcome to planechase!"
        await message.channel.send(content_str)

    rpd_outcome = None
    if message.content.startswith('/rpd') or message.content.startswith('/roll'):
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
    
    if message.content.startswith('/planeswalk'):
        game.planeswalk()
    
    if message.content.startswith('/plane') or message.content.startswith('/start_game') or rpd_outcome == "planeswalk": 
        pic_file = discord.File(fp=game.get_current_plane_image(), filename='plane.png')
        content_str = "**Current Location**: {}\n".format(game.get_current_plane_name())
        content_str += "**Type**: {}\n\n".format(game.get_current_plane_type_line())
        await message.channel.send(content_str, file=pic_file)
        time.sleep(0.3)

    if message.content.startswith('/static') or message.content.startswith('/start_game') or message.content.startswith('/plane') or rpd_outcome=="planeswalk":
        content_str = "**Static ability**: {}".format(game.get_current_plane_static_ability())
        await message.channel.send(content_str)

    if message.content.startswith('/chaos') or message.content.startswith('/start_game') or message.content.startswith('/plane') or rpd_outcome == "chaos" or rpd_outcome == "planeswalk":
        content_str = "**Chaos ability**: {}".format(game.get_current_plane_chaos_ability() if game.get_current_plane_chaos_ability() else "None")
        await message.channel.send(content_str)
    
    if message.content.startswith('/help'):
        content_str = "**Bot commands:**\n"
        content_str += "**/start_game:** Start a new game and walks to a random plane.\n"
        content_str += "**/roll** or **/rpd:** Roll the planar die.\n"
        content_str += "**/plane:** Get information about the current plane.\n"
        content_str += "**/static:** Get the current plane's static ability.\n"
        content_str += "**/planeswalk:** Force planechase-bot to walk to the next plane."
        await message.channel.send(content_str)

client.run(os.getenv('TOKEN'))
    