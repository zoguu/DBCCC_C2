# get_sysinfo.py
# m 08/2/2026

import platform
import requests

def get_sysinfo() -> str: # proof of concept of a attacker gathering system information to SELL
    """
    Takes 0 arguments and returns USER,OS,IP information in a structured matter.
    """
    ip = requests.get("https://api.ipify.org").text.replace(",",".")
    return_string = f"""|-| INFO |-| \n
 USER : {platform.node()} \n
 OS : {platform.platform()}  | {platform.system()} | {platform.release()} \n
 IP : {ip}
"""
    return return_string

def get_sysinfo_raw() -> list: # proof of concept of a attacker gathering system information to EXPLOIT
    """ 
    Takes 0 arguments and returns USER,OS,IP info in a list
    """
    user = platform.node()
    os = [platform.platform(),platform.system(),platform.release()]
    ip = requests.get("https://api.ipify.org").text.replace(",",".")
    return [user,os,ip]
    