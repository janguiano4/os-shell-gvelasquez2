# Gilbert Velasquez
# CS 4375: Thoery of Operating Systems 
# Dr. Freudenthal
# This program corresponds to Lab Assignment #1. This code mimics a bash shell.

import os
import sys
import re
import redirect
import pipe
from read import my_getLine

while(1):
    if 'PS1' in os.environ: # Requirement 1 Prompt String. Default = "$ "
        os.write(1,(os.environ['PS1']).encode())
    else:
        os.write(1, "$ ".encode())

    input = my_getLine() # Get input from method created in Lab Assignment #0
    args = input.split()
    
    if len(input) == 0: # If input is empty 
        break
    
    if args[0].lower() == "exit": # Requirement 4: exit command 
        os.write(2,"Shell Exited \n".encode())
        sys.exit(1)
    
    if args[0] == "cd": # Requirement 4: cd command
        if len(args) == 1:
            os.chdir("..")
        else:
            os.chdir(args[1])
        continue # Return to top of while
    
    rc = os.fork()

    if rc < 0: # Requirement 3: Command fails
        os.write(2,("Program terminated with exit code" + rc +"\n").encode())
        sys.exit(1)
        
    elif rc == 0: # Child process
        
        # Check for Redirection 
        if(redirect.hasRedirect(args)):
            if(redirect.isValid(args)): # Check syntax of command
                if(redirect.hasOutput(args)):
                    outputIndex = redirect.output(args)
                    os.close(1)
                    os.open(args[outputIndex],os.O_CREAT | os.O_WRONLY)
                    os.set_inheritable(1,True)
                
                if(redirect.hasInput(args)): 
                    inputIndex = redirect.input(args)
                    os.close(0)
                    os.open(args[inputIndex],os.O_RDONLY);
                    os.set_inheritable(0,True)
            else:
                os.write(2,("Invalid Redirection Syntax \n".encode()))
                sys.exit(1)
        
            for dir in re.split(":",os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program,args,os.environ) # Requirement 2
                except FileNotFoundError:
                    pass
            os.write(2,(args[0] + ":command not found \n").encode()) # Requirement 3: Command NF
            sys.exit(1)

        # Check for Pipe    
        elif(pipe.hasPipe(args)):
            if(pipe.isValid(args)):
                # Pipe work goes here
                x = 0
            else:
                os.write(2,("Invalid Pipe Syntax \n").encode())
                sys.exit(1)

            for dir in re.split(":",os.environ['PATH']):
                program = "%s/%s" % (dir,args[0])
                try:
                    os.execve(program,args,os.environ)
                except FileNotFoundError:
                    pass
                os.write(2,(args[0] + ":command not found \n").encode())
                sys.exit(1)

        # No Pipes or Redirections     
        else: 
            for dir in re.split(":",os.environ['PATH']):
                program = "%s/%s" % (dir,args[0])
                try:
                    os.execve(program,args,os.environ)
                except FileNotFoundError:
                    pass
            os.write(2,(args[0] + ":command not found \n").encode())
            sys.exit(1)
                                
    else: # Parent process 
        childPidCode = os.wait()
