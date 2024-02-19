# Written by *** for COMP9021
#
# The function print_histogram() takes:
# - a positive integer (possibly 0) as first argument;
# - a character that represents one of 4 possible directions
#   as second argument;
# - the string 'blue' or 'red' as third argument.
# Both second and third arguments have default values.
#
# Uses the digits of the first argument to print out a histogram
# that "grows" in the direction given by the second argument,
# the square that marks the start of the first bar being of colour
# given by the third argument.
# What is printed out is a rectangle with a checkered pattern,
# the white squares "outside" the histogram "hiding" the pattern.
#
# The code points of the Unicode characters involved in this quiz are,
# in base 16: 21d0, 21d1, 21d2, 21d3, 1f7e6, 1f7e5 and 2b1c.
#
# You can assume that the function arguments are exactly as expected.
#That means no need to pass values to the function. No need to take input from user. Program is set in such a way somehow that All 17 TEST inputs are passed into the function concurrently. 
red  = '\U0001f7e5' #ASCIIin hexadecimal
blue ='\U0001f7e6'
white ='\u2b1c'

def print_histogram(n, direction='⇑', colour='blue'): ##Up direction and blue color are default values if no specific arguments for them are passed.
    L = list(str(n))  ##The integer input is converted to a list of the DIGITS of the integer convereted to string format. 
    largest_digit = max(int(x) for x in str(n))   ##Find the highest digit in the list.This will be the HEIGHT OR WIDTH of the histogram DEPENDING on the direction of histogram.
    if (colour=='blue'):
        if(direction=='⇑'):
            for i in range (1,largest_digit+1):
                for j in range(1, len(L)+1):
                    if(i>(largest_digit-int(L[j-1]))): ##i.e. everyplace other than the white box places.
                        if(largest_digit%2==0):
                            if((i+j)%2==0):
                                print(red, end="")
                            else:
                                print(blue, end="")
                        else:
                            if((i+j)%2==0):
                                print(blue, end="")
                            else:
                                print(red, end="")
                    else:
                        print(white, end="")
                print() ##To print newline. i.e. Cursor moves to next row.
        elif (direction=='⇓'):
            for i in range (1,largest_digit+1):
                for j in range(1, len(L)+1):
                    if(i<=int(L[j-1])):
                        if((i+j)%2==0):
                            print(blue, end="")
                        else:
                            print(red, end="")
                    else:
                        print(white, end="")
                print()    
        elif (direction=='⇒'):
            for i in range (1, len(L)+1):
                for j in range(1,largest_digit+1):  ##For left and right directions, the width of the histogram is equal to largest_digit & the height of the histogram is equal to the length of the List ie. number of digits in the number. 
                    if(j<=int(L[i-1])):
                        if((i+j)%2==0):
                            print(blue, end="")
                        else:
                            print(red, end="")
                    else:
                        print(white, end="")
                print()    
        elif (direction=='⇐'):
            for i in range (1, len(L)+1):
                for j in range(1,largest_digit+1):
                    if(j>(largest_digit-int(L[i-1]))):
                        if(largest_digit%2==0):
                            if((i+j)%2==0):
                                print(red, end="")
                            else:
                                print(blue, end="")
                        else:
                            if((i+j)%2==0):
                                print(blue, end="")
                            else:
                                print(red, end="")
                    else:
                            print(white, end="")
                print()    
    elif (colour=='red'):
        if(direction=='⇑'):
            for i in range (1,largest_digit+1):
                for j in range(1, len(L)+1):
                    if(i>(largest_digit-int(L[j-1]))):
                        if(largest_digit%2==0):
                            if((i+j)%2==0):
                                print(blue, end="")
                            else:
                                print(red, end="")
                        else:
                            if((i+j)%2==0):
                                print(red, end="")
                            else:
                                print(blue, end="")
                    else:
                        print(white, end="")
                print()
        elif (direction=='⇓'):
            for i in range (1,largest_digit+1):
                for j in range(1, len(L)+1):
                    if(i<=int(L[j-1])):
                        if((i+j)%2==0):
                            print(red, end="")
                        else:
                            print(blue, end="")
                    else:
                        print(white, end="")
                print()    
        elif (direction=='⇒'):
            for i in range (1, len(L)+1):
                for j in range(1,largest_digit+1):
                    if(j<=int(L[i-1])):
                        if((i+j)%2==0):
                            print(red, end="")
                        else:
                            print(blue, end="")
                    else:
                        print(white, end="")
                print()    
        elif (direction=='⇐'):
            for i in range (1, len(L)+1):
                for j in range(1,largest_digit+1):
                    if(j>(largest_digit-int(L[i-1]))):
                        if(largest_digit%2==0):
                            if((i+j)%2==0):
                                print(blue, end="")
                            else:
                                print(red, end="")
                        else:
                            if((i+j)%2==0):
                                print(red, end="")
                            else:
                                print(blue, end="")
                    else:
                            print(white, end="")
                print()
    