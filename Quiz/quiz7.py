# WRITTEN BY *** FOR COMP9021
#
# Randomly fills a grid of size 10 x 10 with 0s and 1s and computes:
# - the size of the largest homogenous region starting from the top left
#   corner,  so the largest region consisting of connected cells all
#   filled with 1s or all filled with 0s, depending on the value stored
#   in the top left corner;
# - the size of the largest area with a checkers pattern.


from random import seed, randint
from collections import defaultdict
import sys
import copy

dim = 10

def display_grid():
    for i in range(dim):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(dim)))

try:
    arg_for_seed, density = (int(x) for x in 
                    input('Enter two positive integers: ').split()
                            )
    if arg_for_seed < 0 or density < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
grid = [[int(randint(0, density) != 0) for _ in range(dim)]
            for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display_grid()
grid_copy=copy.deepcopy(grid)
# INSERT YOUR CODE HERE
cell_count=1 ## Cell count is made 1 & not 0 , because we need to count the first element at (0,0) also.
def recursive_search(grid_copy,i,j,n):
    global cell_count
    ##Because (i,j) is explored in this iteration, we have to give it some false value to ensure it is never affecting the count again.
    grid_copy[i][j]='a'  ##I can give any value. I can give any value Except n. Not necessary to give 1 or 0 itself i.e. for opposite value of n .. as I will have to write another if statement for that ... i.e if n==1: grid[i][j]=0 elif n==0: grid[i][j]=1
##North
    if i-1!=-1:
        if grid_copy[i-1][j]==n:
            cell_count=cell_count+1
            recursive_search(grid_copy,i-1,j,n)
##South
    if i+1!=10:    
        if grid_copy[i+1][j]==n:
            cell_count=cell_count+1
            recursive_search(grid_copy,i+1,j,n)
##West
    if j-1!=-1:
        if grid_copy[i][j-1]==n:
            cell_count=cell_count+1
            recursive_search(grid_copy,i,j-1,n)
##East
    if j+1!=10:
        if grid_copy[i][j+1]==n:
            cell_count=cell_count+1
            recursive_search(grid_copy,i,j+1,n)
    return cell_count

if grid[0][0]==0:
    n=0
else:             ##grid[0][0]=1
    n=1
maximum_cell_count=recursive_search(grid_copy,0,0,n)
print(f'The size of the largest homogenous region from the top left corner is {maximum_cell_count}.')

## CHECKERBOARD PATTERN IF YOU WANT TO UNDERSTAND CODE IS BELOW, EXECUTE IT. IMAGINE THE BLACK AND WHITE SQUARES OF A CHESSBOARD. OR SUPERIMPOSE A CHESS BOARD ON TOP OF THE GRID. BUT THE TOP LEFT ELEMENT i.e. STARTING ELEMENT IF WHITE .. THEN CHESSBOARD TOP LEFT SQUARE SHOULD BE WHITE .. IF BLACK , THEN CHESSBOARD TOP LEFT BLACK.
##for i in range(10):
##    for j in range(10):
    ##    if grid[i][j]==1:
    ##     print('\u2b1b',end="")
    ## else:
      ##   print('\u2b1c',end="")
    ## print("\n")

##THE MOST IMPORTANT THING IN THIS PART IS TO NOT FORGET TO INCLUDE STARTING ELEMENT IN PREVIOUSLY VISITED IN THE BEGINNING ITSELF. OTHERWISE DUPLICATION OF STARTING CELL COUNT ETC., ALL SORTS OF PROBLEMS OCCUR

previously_visited = defaultdict(int)
grid_copy2=copy.deepcopy(grid)
## WE CANT USE GRID_COPY AGAIN FOR CHECKERBOARD FUNCTION. It will have many 'a' values. Its global variable. So, we use grid_copy 2.
def checkerboard(grid_copy2,i,j):
    ## if i give  grid_copy[i][j]='a' like in line 43, it will create problems. line 89,94,99,104 etc may not work.
    ## So, instead we store the values of i & j as keys of a dictionary. And we ensure that these (i,j) values are never traversed again
    ## North
    global checker_count ##Very important. Surrounding an element. There can be 4 paths. If this statement is not there, checker_count of East path (which may have up, down, left, right traversals in 2nd stage) will be seperate. Checker_count of South path will be seperate etc. The checker_path returned will be the last checker_count of a direction. 
    ## Making Checker_count global ensures that any change in checker_count in ALL Recursive function calls add together. On start from next iteration in for loop at 117 and 118, checker_count will be set to 0.
    previously_visited[i,j]+=1
    ##North
    if i-1!=-1:
        if (i-1,j) not in previously_visited.keys():
            if grid_copy2[i-1][j]!=grid_copy2[i][j]: ##If grid[i][j]==0, then neighbours should be 1. If grid[i][j]==1, then neighbours should be 0.
                checker_count=checker_count+1
                checkerboard(grid_copy2,i-1,j)
    ##South
    if i+1!=10:    
        if (i+1,j) not in previously_visited.keys():
            if grid_copy2[i+1][j]!=grid_copy2[i][j]:
                checker_count=checker_count+1
                checkerboard(grid_copy2,i+1,j)
    ##West
    if j-1!=-1:
        if (i,j-1) not in previously_visited.keys():
            if grid_copy2[i][j-1]!=grid_copy2[i][j]:
                checker_count=checker_count+1
                checkerboard(grid_copy2,i,j-1)
    ##East
    if j+1!=10:
        if (i,j+1) not in previously_visited.keys():
          if grid_copy2[i][j+1]!=grid_copy2[i][j]:
                checker_count=checker_count+1
                checkerboard(grid_copy2,i,j+1)
    return checker_count   ## IT WILL REACH THIS STATEMENT ONLY IF THERE ARE NO NEIGHBOURS.

max_checker_count=1 ## IMPORTANT
for i in range(10):     ##VERY IMPORTANT. IF YOU WANT TO CHECK ONLY FROM A PARTICULAR (i,j) e.g.(3,8) instead of starting to debug THE WHOLE SEQUENCE OF STEPS from (0,0), input the values for i in range(3,10): for j in range(10)
    for j in range(10):  ##IT IS VERY NECESSARY FOR DEBUGGING
        checker_count=1 ##Count should always include the starting point of the checker.
        previously_visited.clear()
        current_checker_count=checkerboard(grid_copy2,i,j) ##So as to get maximum checker_count value and store it
        if current_checker_count > max_checker_count:
            max_checker_count = current_checker_count
        
print(f'The size of the largest area with a checkers structure is {max_checker_count}.')
                      
            
                