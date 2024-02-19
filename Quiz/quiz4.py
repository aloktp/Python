# Written by *** for COMP9021
#
# Prompts the user for two positive integers and discovers special
# prime numbers in that range, as specified in the print() statements.

from math import sqrt
import sys


try: 
    n1, n2 = (int(x) for x in
                input('Enter two integers between 2 and 50,000,000: ').split()
             )
    if n1 < 2 or n2 < 2 or n1 > 50_000_000 or n2 > 50_000_000:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
if n1 > n2:
    n1, n2 = n2, n1

def sieve_of_primes_up_to(n):
    sieve = [True] * (n + 1)
    for p in range(2, round(sqrt(n)) + 1):
        if sieve[p]:
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return [p for p in range(2,n+1) if sieve[p] and p>=n1] 

min_nb_of_digits = 10
max_length = 0
min_prime = None
max_prime = None

# INSERT YOUR CODE HERE
sieve_values = sieve_of_primes_up_to(n2)
list_length = len(sieve_values)
L=[]
List_of_least_distinct_digits=[]  
List_of_least_distinct_digits_smallest_values=[]
for i in range(list_length):     
    L.append(len(set(str(sieve_values[i]))))
if (L!=[]):
    min_nb_of_digits=min(L)
for j in range(len(L)):
    if(L[j]==min(L)):
        List_of_least_distinct_digits.append(sieve_values[j])
if (L!=[]): #For cases like 3 3, where there is no prime number in between
    max_prime = max(List_of_least_distinct_digits)
    max_length=len(str(max_prime))
    for i in range(len(List_of_least_distinct_digits)):
        if (len(str(List_of_least_distinct_digits[i])))== max_length:
            List_of_least_distinct_digits_smallest_values.append(List_of_least_distinct_digits[i])
    min_prime = min(List_of_least_distinct_digits_smallest_values)
    if max_prime==min_prime:   #For unique prime cases, see bottom.
        max_prime=0
print()
if not max_length:
    print(f'There are no primes between {n1} and {n2}.')
    sys.exit()
if min_nb_of_digits == 1:
    print('Some primes between', n1, 'and', n2, 'have no two distinct digits.')
else:
    print('All primes between', n1, 'and', n2, 'have at least',
          f'{min_nb_of_digits} distinct digits.'
         )
print('Amongst the primes in that range that have a minimal number of\n'
      '  distinct digits, the longest ones have',
      max_length == 1 and '1 digit.' or f'{max_length} digits.'
     )
if not max_prime:
    print(f'There is actually a unique such prime; it is {min_prime}.')
    sys.exit()
print(f'The smallest such prime is {min_prime}, '
      f'and the largest such prime is {max_prime}.'
     )  