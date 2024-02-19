# Written by *** for COMP9021
#
# Prompts the user for two positive integers, creates a list L
# of positive integers, makes a copy L1 of L and defines
# two functions.
# - remove_values_with_larger_neighbours(), called with L1 as argument,
#   that removes again and again in L1 the values with strictly larger
#   neighbours (on both sides). For instance, starting with the list
#   [6, 6, 0, 4, 7, 6, 4, 7]:
#   * 0 between 6 and 4 goes, which yields [6, 6, 4, 7, 6, 4, 7]
#   * first 4 between 6 and 7 goes, which yields [6, 6, 7, 6, 4, 7]
#   * 4 between 6 and 7 goes, which yields [6, 6, 7, 6, 7]
#   * 6 between 7 and 7 goes, which yields [6, 6, 7, 7], the final result.
# - ranges_of_indexes_of_no_smaller_neighbours() which returns a dictionary
#   whose keys are 0, ..., len(L)-1, that maps every such i to the tuple
#   (j1, j2) with j1 <= i <= j2, j1 minimal and j2 maximal such that
#   for all j with j1 <= j <= j2, the value of L at location j is at least
#   equal to the value of L at location i. Taking the same list as example:
#   * 0, index of 6 is mapped to (0, 1), range of indexes of 6, 6
#   * 1, index of 6 is mapped to (0, 1), range of indexes of 6, 6
#   * 2, index of 0 is mapped to (0, 7), range of indexes of all members of L
#   * 3, index of 4 is mapped to (3, 7), range of indexes of 4, 7, 6, 4, 7
#   * 4, index of 7 is mapped to (4, 4), range of indexes of 7
#   * 5, index of 6 is mapped to (4, 5), range of indexes of 7, 6
#   * 6, index of 4 is mapped to (3, 7), range of indexes of 4, 7, 6, 4, 7
#   * 7, index of 7 is mapped to (7, 7), range of indexes of 7


from random import seed, randrange   #seed function in line 43
import sys    ## I think what this allows is that exit function later on to exit the program.


try: 
    for_seed, length = (int(x) for x in
                  input('Enter two positive integers (possibly 0): ').split()) ## RHS is a tuple. If we input a string wrongly, then error because int function cant convert string to int. 
                       ##Only 2 variables in LHS. So Input function takes  only two inputs. Now whatever input user gives, only if its an integer, there will be no Valueerror. The split function ensures that the input of the string will be split at the space so that it can assign those 2 values to for_seed and length. If no gap between character of input, then only one value and hence Error that Python cant assign or apck the variables.
## length is for length of the list. for_seed is to create different lists for different integer input.                       
    if for_seed < 0 or length < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit() #Exits the whole program
seed(for_seed) #Very important. Seed function is used to save the state of a random function, so that it can generate same random numbers on multiple executions of the code on the same machine or on different machines (for a specific seed value). i.e. Everytime your run the program.. when list in created in line 44, the list of values created for a particular length is always same. e.g. List for length 8 will always be [6,6,0,4,7,6,4,7] everytime you run this program. This is to ensure Eric's input list stays same.
L = [randrange(length) for _ in range(length)] #All the elements in the list will be of value less than length of the list. Randrange function creates these values randomly to fill the list.
print('Here is the list L of generated values:')
print('  ', L)
print()

# The function modifies the list provided as argument
# and has no return statement.
def remove_values_with_larger_neighbours(L1):
#Next section is to check from start of list whether there are any values with larger neighbours.
    while True: #This while loop checks the whole list and on the first instance a large neighbour is found, the function removal_operation is called.
        has_changed = False
        for j in range(1,len(L1)-1): #The problem with for loop is if for i in range (1,3) i.e. only i will become only 1 & 2.
            if j == len(L1)-1:       # At the last element, we cant compare as there is not element after it. So we break.        
                break
            if (L1[j-1]>L1[j] and L1[j]<L1[j+1]): ## This if condition is why I chose range(1, len[L]-1) instead of (0,len[L]). Also L[-1] = L[len(L)-1] i.e. the last element of list.
                removal_operation(len(L1)-1) ## Passing the length of list to removal_operation
                has_changed = True
                break  ##This break is to break out of the for loop. Next the wile clause will be initiated again. We put this break statement because once a removal_operation function is done, we want the for loop to check from 1st element again in remove_values_with_larger_neighbours function.
        if not has_changed:
            break
# The following function does the actual removal. It doesnt break when an element with larger neighbour is found. The element will be removed and then program will carry on checking every element in the list till one full iteration of the list is over.
def removal_operation(n):
    for i in range(1,n):
        if i == len(L1)-1: #Seperate condition for last element
           break 
        if (L1[i-1]>L1[i] and L1[i]<L1[i+1]):
            L1.pop(i) ## The element having larger neighbour on either of the sides is removed.
            n=len(L1)-1 #If i give n=len(L1)-2 and rework the comparison condition in line no.69, too much trouble.
            break
# The function creates a dictionary and returns it.
def ranges_of_indexes_of_no_smaller_neighbours():
        Dictionary={} ## Very important to initalize Dictionary variable as an empty dictionary. Else "Dictionary is not defined" error comes.
        for i in range(len(L)): 
            if i!=0:
                for j in range(i-1,-1,-1): #function to find indices of maxima element on left side of current element
                    if (L[j]>=L[i]):
                        if (j==0):
                                m=j  ##This line 81 and line 85 has same effect. Line 80 & 81 can be removed & then the for loop should be changed to for j in range(i-1,0,-1).
                    else:
                           m=j+1
                           break
            else:
                m=0    ## For 1st element in list, maximal element on left is 1st element itself.    
            if i!=len(L)-1:
                for k in range(i+1,len(L)): ##function to find indices of maxima element on right side of current element
                    if L[k]>=L[i]:
                        if (k==len(L)-1):
                                        n=k  ##line 91 and 96 has same effect. For last element in list, maximal element on right is last element itself.     
                    else:                    ##Line 90 & 91 can be removed & then the for loop should be changed to for j in range(i+1,len(L)-2).
                        n=k-1
                        break
            else:
                 n=i     ##This is same as line 91. 
            Dictionary[i]=m,n #Dictionary with indices of maxima element on left and right side of current element, is updated at every instance of current element in for loop
        return Dictionary
    
# L1 denotes a copy of the list denoted by L.
L1 = list(L) # We are copying L to L1, because we are popping out elements in remove_values_with_larger_neighbours function. We want a master list L to remain the same. We want seperate Lists to pass as input to the 2 functions i.e. large_neighbours and no_of_indexes , so that we can operate on the list, and we can get seperate outputs for both functions.
remove_values_with_larger_neighbours(L1)
print('Removing again and again in a copy of L the values')
print('with strictly larger neighbours (on both sides):')
print('  ', L1)
print()
print('Dictionary mapping i to (j1, j2), with j1 minimal and j2 maximal,')
print('such that for all j with j1 <= j <= j2, the value of L at location j')
print('is at least equal to the value of L at location i:')
print(ranges_of_indexes_of_no_smaller_neighbours())