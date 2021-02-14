# Gilbert Velasquez
# CS 4375: Thoery of Operating Systems 
# Dr. Freudenthal
# This program corresponds to Lab Assignment #1. This code mimics a bash shell.

import os
import sys
import re
from read import my_getLine

PS1= "$"

while(1):
    os.write(1, PS1.encode())
    input = my_getLine()
    
    if len(input) == 0:
        break
    if input.lower() == "exit":
        os.write(2,"Shell Exited \n".encode())
        sys.exit(1)
    
    lines = input.split()
    rc = os.fork()
    
    if rc < 0:
        os.write(2,("Fork failed, returning \n").encode())
        sys.exit(1)
        
    elif rc == 0:
        for dir in re.split(":",os.environ['PATH']):
            program = "%s/%s" % (dir, lines[0])
            try:
                os.execve(program,lines,os.environ)
            except FileNotFoundError:
                pass
        os.write(2,("Command Fails").encode())
        sys.exit(1)
        
    else:
        childPidCode = os.wait()
