# Written by *** for COMP9021
#
# Prompts the user for a positive integer N, a symbol s and
# the name of a file, assumed to be stored in the working directory.
#
# The file can contain anywhere any number of blank lines
# (that is, lines containing an arbitrary number of spaces
# and tabs--an empty line being the limiting case).
#
# Nonblank lines are always of the form: last_name first_name, gender
# with no space anywhere except a single space after the comma
# and a single space between last_name and first_name (actually,
# your code should naturally not care whether there is just 1 space
# or more than 1 space between last_name and first_name).
#
# Draws a rhombus made of stars with N spaces before the leftmost star
# and with s in the middle, and outputs the contents of the file,
# ignoring any blank line and reformatting all other lines.

import sys
from os.path import exists

try:
    nb_of_spaces = int(input('Enter a positive integer (possibly 0): '))
    symbol = input('Input a symbol: ').removesuffix('\n')
    if nb_of_spaces < 0 or len(symbol) != 1:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
file_name = input('Input the name of a file '
                  'in the working directory: '
                 ).removesuffix('\n')
if not exists(file_name):
    print('Incorrect input, giving up.')
    sys.exit()

# POSSIBLY ADD FUNCTIONS

print('Here is a rhombus:')
# ENTER CODE TO PRINT OUT 2 BLANK LINES AND IN-BETWEEN, THE LOSANGE
# To print top blank line
print()
# To print 1st 3 rows of rhombus
for i in range (3):
    print(" " * nb_of_spaces, end ="")
    for j in range (i+3):
        if ((i+j)%2 == 0):
            if (i == 0 and j == 0):
                print(" ", end = "")
            elif (i == 2 & j==2):
                print(symbol, end ="")
            else:
                print("*", end ="") 
        else:
            print(" ", end="")            
    print()
# To print last 2 rows of rhombus
for i in range (2):
    print(" " * nb_of_spaces, end ="")
    for j in range(4):
        if ((i+j)%2==1):
            if(i==1 and j==0):
                print(" ", end ="")
            else:
                print("*", end ="")
        elif (i==1 and j==3):
             continue                         
        else:
             print(" ", end ="")
    print()
# To print bottom blank line    
print() 
# On to next part of the quiz
print('Here are the people listed in the file:')
with open(file_name) as file:
    for line in file:
        if line.isspace():
            continue
        else:
            line=line.replace(',',"")
            line=line.split()
            if (line[2]=='M'):
                print("Mr.", end= " ")
            elif (line[2]=='F'):
                print("Mrs.", end = " ")
            else:
                print ("Wrong Gender")
                continue
            print (line[1], end=" ")
            print (line[0])
