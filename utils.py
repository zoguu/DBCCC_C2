# utils.py
# m : 14/02/2026
# utility functions
import os

def get_full_command(msgargs) -> str:
    """
    Returns a full string command.
    
    :param msgargs: Command arguments
    """

    msgcontent = msgargs[0]
    full_command = ""

    for text in msgargs:
             
             if text is msgcontent : pass
             else :
                 
                 full_command = f"{full_command} {text}"

    return full_command

def filetest(filepath,tests) -> list:
      """
      Docstring for filetest
      
      :param filepath: Path to the file including the name and extension.
      :param tests: A list of tests you wanna do , ex : tests = [1,3]
      """
      problems = []

      if 1 in tests and not os.path.exists(filepath):
        problems.append("File does not exist.")
      if 2 in tests and os.path.isdir(filepath):
        problems.append("File is a directory.")
      if 3 in tests and  not os.access(filepath, os.R_OK):
        problems.append("File is not readable.")
      if 4 in tests and not os.path.getsize(filepath) < 8 * 1024 * 1024: # discord file size limit is 8mb, if its bigger we cant send it.
        problems.append("File is too big to send. [>8mb]")

      return problems

def getfilename_fromfullpath(filepath : str) -> str:
    """
    Returns the file name and extension from full filepath.
    
    :param filepath : str => Filepath
    """
    
    directory_nest = filepath.split("/")
    filename_place = len(directory_nest) - 1
    
    return directory_nest[filename_place]