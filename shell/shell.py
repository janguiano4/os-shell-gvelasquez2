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


def piping(args): # Method to execute piping. Seperated to allow for multiple pipes 
    leftHS,rightHS = pipe.getCommands(args) # Get left and right hand sides of pipe 
    pr,pw = os.pipe() # Create pipe 

    rc = os.fork() # Fork off children 

    if rc < 0:
        os.write(2,("fork failed, returning %d\n" %rc).encode())
        sys.exit(1)

    elif rc == 0: # Child who will run command 1
        
        os.close(1) # Disconnect from display 
        os.dup(pw) # Connect to input of the pipe 
        os.set_inheritable(1,True)
        
        for fd in (pr,pw): # Disconnect extra connections from the pipe 
            os.close(fd)
            
        for dir in re.split(":",os.environ['PATH']):
            program = "%s/%s" % (dir, leftHS[0])
            try:
                os.execve(program,leftHS,os.environ) # Replace memory with contents of command
            except FileNotFoundError:
                pass
        os.write(2,(leftHS[0] + ":command not found \n").encode())
        sys.exit(1)
        
    else: # Child who will run command 2
        
        os.close(0) # Disconnect from keyboard
        os.dup(pr) # Connect to output of pipe 
        os.set_inheritable(0,True)
        
        for fd in (pr,pw): # Disconnect extra connections to pipe 
            os.close(fd)
            
        if pipe.hasPipe(rightHS): # More than one pipe
            piping(rightHS)
            
        for dir in re.split(":",os.environ['PATH']):
            program = "%s/%s" % (dir,rightHS[0])
            try:
                os.execve(program,rightHS,os.environ) # Replace memeory with contents of command
            except FileNotFoundError:
                pass
            
        os.write(2,(rightHS[0] + ":command not found \n").encode())
        sys.exit(1)
                

os.environ.pop("PS1") # Reset
        
while(1):
    if 'PS1' in os.environ: # Requirement 1 Prompt String. Default = "$ "
        os.write(1,(os.environ['PS1']).encode())
    else:
        os.write(1, "$ ".encode())

    input = my_getLine() # Get input from method created in Lab Assignment #0
    args = input.split()
    
    if len(input) == 0: # If input is empty 
        break
    
    if input.lower() == "exit": # Requirement 4: exit command
        os.write(2,("Shell Exited \n".encode()))
        sys.exit(1)

    if args[0] == "cd": #Requirement 4: cd command
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
                    outputIndex = redirect.output(args) # Get Output Index
                    os.close(1) # Close stdout
                    os.open(args[outputIndex],os.O_CREAT | os.O_WRONLY) # Open Output
                    os.set_inheritable(1,True)
                    args.remove('>') # Remove redirection from command 
                    args.remove(args[outputIndex]) # ^
                
                if(redirect.hasInput(args)): 
                    inputIndex = redirect.input(args) # Get Input Index
                    os.close(0) # Close stdin
                    os.open(args[inputIndex],os.O_RDONLY); # Open Input
                    os.set_inheritable(0,True)
                    args.remove('<') # Remove redirection from command
                    args.remove(args[inputIndex]) # ^
            else:
                os.write(2,("Invalid Redirection Syntax \n".encode()))
                sys.exit(1)
        
            for dir in re.split(":",os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program,args,os.environ) # Replace memeory with contents of  command
                except FileNotFoundError:
                    pass
            os.write(2,(args[0] + ":command not found \n").encode()) # Requirement 3: Command NF
            sys.exit(1)

        # Check for Pipe    
        elif(pipe.hasPipe(args)):
            if(pipe.isValid(args)):
                piping(args) 
            else:
                os.write(2,("Invalid Pipe syntax").encode())
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
