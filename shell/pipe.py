# Gilbert Velasquez
# CS 4375: Theory of Operating Systems
# Dr. Fruedenthal
# This program is to be used with the shell.py program to help implement pipes.

def hasPipe(args): # A method that checks if there is a | in the args list
    if '|' in args:
        return True
    return False

def isValid(args): 
    if args[0] == '|' or args[len -1] == '|': # If there is a pipe at the first or last index
        Return False
    
    for i in range(len(args)):
        if(args[i] == '|'):
    
            if(i+1 >= len(args)): # If a pipe points to nothing
                return False
            
            if(args[i+1] == '|'): # Two consecutive pipes 
                return False
            
    return True # Valid Syntax for Piping 
            
        

