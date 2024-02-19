# Written by *** for COMP9021
#
# Computes the number of stars found in a grid of size 10 x 10 for a given
# star size, and outputs the grid replacing the * at the centre of a star
# with its size.
#
# This is a star of size 1:
#      *   *
#        * 
#      *   *
#
# This is a star of size 2:
#      *       *
#        *   *
#          * 
#        *   *
#      *       *


from collections import defaultdict
from random import seed, randrange
import sys
import copy ## VERY NECESSARY


dim = 10

def display_grid():
    print('  ', '-' * (2 * dim + 3))
    for row in grid:
        print('   |', *row, '|')
    print('  ', '-' * (2 * dim + 3))

try: 
    for_seed, density = (int(x) for x in input('Enter two integers, the second '
                                               'one being strictly positive: '
                                              ).split()
                    )
    if density <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
grid = [['*' if randrange(density) != 0 else ' ' for _ in range(dim)]
            for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display_grid()

## VERY IMPORTANT - in line 63 etc.. the if statements, the things inside parenthesis has preference over the and statement outside. This is necessary for correct output.
## VERY IMPORTANT - IN NORMAL CASES, i.e. without Parenthesis PYTHON GIVES 'AND' OPERATOR PREFERENCE OVER 'OR' OPERATOR in EXPRESSIONS.
# INSERT YOUR CODE HERE
##VERY IMPORTANT. DONOT CREATE A SHALLOW COPY. 
## import copy ... command of module in line 23
new_grid = copy.deepcopy(grid) ## ENSURE THAT THIS IS NOT SHALLOW COPY. Otherwise location of new_grid is same as grid. Hence, any changes to new_grid will affect grid too.
def star_finder():
    global grid
    for i in range(dim):
        for j in range(dim):
            if i==0 or j==0 or i==dim-1 or j==dim-1 or grid[i][j]==' ':    ## boundary element. No star possible around it.
                continue                  
            star_count=0
            k=0 ##This is also VERY NECESSARY. Break functionS present below donot reset the value of k
            for k in range(1,5): ##4 is the highest star that can be possible in a 10 by 10 grid. Check yourself              
                ## North west
                if (i-k)!=-1 and (j-k)!=-1:
                    if grid[i - k][j - k]=='*':
                    ## North east
                        if (i-k)!=-1 and (j+k)!= dim:
                            if grid[i - k][j + k]=='*':
                        ## South west
                                if (i+k)!= dim and (j-k)!=-1:
                                    if grid[i + k][j - k]=='*':
                            ## South East
                                        if (i+k)!= dim and (j+k)!=dim: 
                                            if grid[i + k][j + k]=='*':                        
                                                 star_count=star_count+1
                                                 new_grid[i][j]=star_count
                                            else:    ##These breaks are also necessary. Else check input 0 3. k will not reset to 0 as its necessary if if grid[i + k][j + k]!='*' i.e. not equal to *
                                                break
                                        else:
                                            break
                                    else:        ##Necessary break
                                        break
                                else:
                                    break
                            else:
                                break
                        else:
                            break
                    else:
                        break                        
                else:
                    break
    grid=new_grid
star_finder()

star_dictionary=defaultdict(int)
for i in range(dim):
    for j in range(dim):
        if grid[i][j]!=' ' and grid[i][j]!='*':##VERY IMPORTANT. And Operator for EITHER 2 NOT's
            star_dictionary[grid[i][j]] += 1
            
## YOU HAVE TO SORT THE DICTIONARY BY KEYS. OTHERWISE YOU GET WRONG INPUT FOR TEST 3.
## THE LINES SHOULD BE DISPLAYED IN ORDER OR ASCENDING KEYS.

### Below are the quick examples

# Example 1: Sort the dictionary by key in ascending order 
#new_dict = dict(sorted(my_dict.items())) 

# Example 2: Sort the dictionary by key in descending order
#new_dict = dict(sorted(my_dict.items(),  reverse = True)) 

# Example 3: Sort the dictionary by key using dict comprehension
#Keys = list(my_dict.keys())
#Keys.sort()
#new_dict = {key: my_dict[key] for key in Keys}

# Example 4: Sort only keys using sorted()
#print(sorted(my_dict))

# Example 5: Sort the dictionary by keys using items()
#new_dict = dict(sorted(my_dict.items(), key=lambda item: item[0]))


star_dictionary=dict(sorted(star_dictionary.items())) ## Items or keys you can type .. same effect

for key,value in star_dictionary.items(): ##VERY IMPORTANT. YOU CANT LOOP THROUGH A DICTIONARY THE NORMAL WAY.
## YOU CAN USE ITEMS() TO ITERATE THROUGH KEYS AND VALUES.
## YOU CAN USE KEYS() TO ITERATE THROUGH KEYS ONLY.
## YOU CAN USE VALUES() TO ITERATE THROUGH VALUES ONLY.
    if value==1:
        print(f'There is {value} star of size {key}.')   
    else:
        print(f'There are {value} stars of size {key}.')   
print("Here are the centres of the stars of those sizes.")
display_grid()


                
    
