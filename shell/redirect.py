# Gilbert Velasquez
# CS 4375: Theory of Operating Systems
# Dr. Fruedenthal
# This program is to be used with the shell.py program to help implement redirections.

def hasRedirect(args): # A method that checks if there is either a < or > in the args list
    if '<' in args or '>' in args:
        return True
    return False

def isValid(args): # A method that determines if the redirect syntax is used correctly 
    numIn = 0
    numOut = 0
    for i in range(len(args)):
        if args[i] == '<': # Count the number of Inputs (Max is 1)
            numIn += 1
            
        if args[i] == '>': # Count the number of Outpts (Max is 1)
            numOut +=1
            
        if (args[i] == '<' or args[i] == '<'):
            if(i+1 >= len(args)): # Check if a redirect points to nothing
               return False
           
            elif(args[i+1] == '<' or args[i+1] == '<'): # Check if we have two concurrent symbols
                return False
        
    if numIn > 1 or numOut > 1: # Check if we have too many inputs/outputs
        return False
    else:
        return True

def hasInput(args): # A method that determines if there is an Input redirection
    for i in range(len(args)):
        if args[i] == '<':
            return True
    return False


def hasOutput(args): # A method that determines if there is an Output redirection 
    for i in range(len(args)):
        if args[i] == '>':
            return True
    return False 

    
def input(args): # A method that returns the index of the Input redirect, -1 if none 
    for i in range(len(args)):
        if args[i] == '<' and i+1 < len(args):
            return i+1
        else:
            return -1

def output(args): # A method that returns the index of the Output redirect, -1 if none
    for i in range(len(args)):
        if args[i] == '>' and i+1 < len(args):
            return i+1
        else:
            return -1
                   
#list1 = ["cat", ">", "input.txt"]
#list2 = ["cat"]
#list3 = ["cat", ">","txt",">"]

#print(isValid(list1))
#print(hasRedirect(list2))
#print(hasRedirect(list3))
