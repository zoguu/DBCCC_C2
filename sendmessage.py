# sendmessage.py
# m 08/02/2026
# handles message sending to avoid errors.

import os
import discord

def get_chunks(text):
    for i in range(0, len(text), 1999):
        yield text[i:i + 1999]

async def sendmsg(channel,msg):
    """
    Takes the channel the message is supposed to be sent.
    Takes an string message.
    Sends the message.
    If any errors, sends that instead.
    """
    if type(msg) != str : await channel.send("Message was not string, might be errors or cutoff.")
    if msg == "" or msg == " ":
        await channel.send("Empty message was supposed to be send, refrained.")
    else:

        if len(msg) > 2000:
                for chunk in get_chunks(msg):
                     await channel.send(chunk)
                     
        else : await channel.send(msg)

async def sendfile(channel,filepath):
    """
     Tries to send the file at the path to user.
     Sends the output file or the relevant error as an message.
     
     :param channel: The channel message was sent in.
     :param filepath: File PATH.
    """

    problems = [] # problems we have about sending the file.
    # lets see if we actually can send the file first.
    if not os.path.exists(filepath):
        problems.append("File does not exist.")
    if os.path.isdir(filepath):
        problems.append("File is a directory.")
    if not os.access(filepath, os.R_OK):
        problems.append("File is not readable.")
    if not os.path.getsize(filepath) < 8 * 1024 * 1024: # discord file size limit is 8mb, if its bigger we cant send it.
        problems.append("File is too big to send. [>8mb]")
    if len(problems) != 0:
        Message = f"There were problems sending : {problems}"
        
        await sendmsg(channel,Message)
    else:
        file_to_send = discord.File(filepath)
        await channel.send(file=file_to_send)


