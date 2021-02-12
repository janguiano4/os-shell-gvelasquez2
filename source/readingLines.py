# Gilbert Velasquez
# CS 4375: Theory of Operating Systems
# Dr. Fruedenthal
# This Program has the methods my_getChar(), my_getLine(), my_readLines(). This code incorporates the C code snipet for my_getChar() provided by Dr. Fruedenthal. 

from os import read

next = 0
limit = 0

# This method calls read to fill a buffer, and gets one character at a time. 
def my_getChar():
    global next
    global limit
    
    if next == limit:
        next = 0
        limit = read(0,1000)
        
        if limit == 0:
            return "EOF"
        
    if next < len(limit) -1: # Check to make sure limit[next] wont go out of bounds. -1 because we dont increment "next" until after this line. 
        c = chr(limit[next]) # convert from ascii to character 
        next +=1
        return c
    
    else:
        return "EOF"

    
# This method returns the next line obtained from file descriptor 0 as a String or an empty String if an EOF is reached.
    
def my_getLine():
    global next
    global limit
    line = ""
    char = my_getChar()
    while (char != '' and char != "EOF"): # Check to see if we have a character to append.
        line += char
        char = my_getChar()
    next = 0 # reset next and limit after we have have finished a line. 
    limit = 0
    return line
    

# This method reaths from a {File or Keyboard} and prints out the contents of the input. Clearly line-by-line.
    
def my_readLines():    
    numLines = 0
    inLine = my_getLine()
    while len(inLine):
        numLines += 1
        print(f"### Line {numLines}: <{str(inLine)}> ###\n")
        inLine = my_getLine()
    print(f"EOF after {numLines}\n")

