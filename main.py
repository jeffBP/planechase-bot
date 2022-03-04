import discord
import os
import time

import planechase as pc

client = discord.Client()

game_dict = {}

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    # Get game for message server
    server_id = message.guild.id
    if server_id not in game_dict.keys():
        game_dict[server_id] = pc.Planechase()
    game = game_dict[server_id]

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

    if message.content.startswith('/denylist_plane'):
        content_str = ""
        success = game.denylist_current_plane()
        if success:
            content_str = "Added plane ({}) to deny list!".format(game.get_current_plane_name())
        else:
            content_str = "Could not add plane ({}) to deny list. It may already be on it.".format(game.get_current_plane_name())
        await message.channel.send(content_str)

    if message.content.startswith('/show_denylist'):
        content_str = "**Planechase denylist**: "
        if game.get_denylist():
            for plane in game.get_denylist():
                content_str += plane + ", "
            content_str = content_str[:len(content_str)-2]
        await message.channel.send(content_str)
    
    if message.content.startswith('/remove_from_denylist'):
        content_str = ""
        planes_list = message.content.split(' [')[1] # Get plane list.
        planes_list = planes_list[:len(planes_list)-1] # Remove trailing close bracket.
        plane_names = planes_list.split(', ') # Split plane list along delimiter.
        for plane_name in plane_names:
            success = game.remove_plane_from_denylist(plane_name)
            if success:
                content_str += "Successfully removed plane ({}) from denylist!\n".format(plane_name)
            else:
                content_str += "Could not remove plane ({}) from denylist. Maybe check your spelling?\n".format(plane_name)
        await message.channel.send(content_str)
            
    if message.content.startswith('/help'):
        content_str = "**Bot commands:**\n"
        content_str += "**/start_game:** Start a new game and walks to a random plane.\n"
        content_str += "**/roll** or **/rpd:** Roll the planar die.\n"
        content_str += "**/plane:** Get information about the current plane.\n"
        content_str += "**/static:** Get the current plane's static ability.\n"
        content_str += "**/planeswalk:** Force planechase-bot to walk to the next plane.\n"
        content_str += "**/denylist_plane**: Add current plane to denylist.\n"
        content_str += "**/show_denylist**: Print current denylist to chat.\n"
        content_str += "**/remove_from_denylist [<plane_name>, ...]**: Remove planes in list *[<plane_name>, ...]* from denylist."
        await message.channel.send(content_str)

client.run(os.getenv('TOKEN'))
    