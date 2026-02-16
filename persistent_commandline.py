# persistent_commandline.py
# m 08/02/2026


import subprocess

def create_persistent_ps(): # PoC of attacker reverse shell
    """
    Creates an returns an powershell session that wont exit after command ran.
    """

    return subprocess.Popen(
        ["powershell", "-NoLogo", "-NoExit", "-Command", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Redirect stderr to stdout to avoid deadlock
        text=True,
        bufsize=1,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
def pexecute_command(ps, cmd) -> str: # PoC of attacker reverse shell
    """
    Takes a powershell session and a command string.
    Runs the command on the powershell session, returns the output.
    """
    marker = "__CMD_DONE__"
    
    # We use a single string to avoid multiple writes
    full_command = f"try {{ {cmd} }} catch {{ Write-Output $_.Exception.Message }}; Write-Output '{marker}'\n"
    
    ps.stdin.write(full_command)
    ps.stdin.flush()

    output = []
    while True:
        line = ps.stdout.readline()
        # Strip newline for comparison, but check if it's the marker
        if not line or marker in line:
            break
        output.append(line.rstrip())

    return "\n".join(output)

# # Example Usage:
# shell = create_persistent_ps()
# a = pexecute_command(shell,"whoami")