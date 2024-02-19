# Written by *** for COMP9021
#
# Prompts the user for two years Y1 and Y2 in the range 1946--2021
# and a proportion p, hence a number in [0, 1], and finds out which names
# were given between Y1 and Y2 with a proportion as a (female or male) name
# at least equal to p, the proportion as a female name and the proportion
# as a male name being as close as possible.
# - When many names exist with that minimal difference in proportions,
#   results are output from largest to smallest proportion as a (female
#   or male) name.
# - When many names exist with that minimal difference in proportions
#   and the same proportion as a (female or male) name, results are
#   output with names in lexicographic order.
#
# Given a name N,
# - the proportion of N as a (female or male) name is the number of times
#   N has been given between Y1 and Y2 as either a female or a male name
#   divided by the total number of newborns between Y1 and Y2;
# - the proportion of N as a female name is the number of times N has been
#   given between Y1 and Y2 as a female name divided by the total number of
#   female newborns between Y1 and Y2;
# - the proportion of N as a male name is the number of times N has been
#   given between Y1 and Y2 as a male name divided by the total number of
#   male newborns between Y1 and Y2.
#
# The directory named names is stored in the working directory.
#
# IF YOU USE ABSOLUTE PATHS, YOUR PROGRAM CAN ONLY FAIL TO RUN PROPERLY
# ON MY MACHINE AND YOU WILL SCORE 0 TO THE QUIZ, WITH NO CHANCE FOR YOU
# TO FIX THIS MISTAKE AFTER RESULTS HAVE BEEN RELEASED.
#
# YOU CANNOT USE pandas FOR THIS QUIZ; IF YOU DO, YOU WILL SCORE 0
# TO THE QUIZ.


from collections import defaultdict
from pathlib import Path
import csv
import sys


try: 
    year_1, year_2 = (int(x) for x in
                input('Enter two integers between 1946 and 2021: ').split()
                     )
    if year_1 < 1946 or year_2 < 1946 or year_1 > 2021 or year_2 > 2021:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try: 
    target_proportion = float(input('Enter a real between 0 and 1: '))
    if target_proportion < 0 or target_proportion > 1:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

# INSERT YOUR CODE HERE
if year_1 > year_2:
    year_1, year_2 = year_2, year_1
names_dir=Path('names')
count_of_a_name=defaultdict(lambda: [0,0])
no_of_males=0
no_of_females=0
for file in sorted(names_dir.glob('*.txt')): ##Sorted not necessary. Remove later
    year=int(file.name[3:7])
    if year>=year_1 and year<=year_2:
        with open(file) as file_name:
            name_csv=csv.reader(file_name)
            for first_name,gender,count in name_csv:
                if gender=='M':
                    count_of_a_name[first_name][0] += float(count)   ##VERY IMPORTANT. Syntax count_of_a_name[[first_name][0]] is wrong.
                    no_of_males+=int(count)  ##Count is string in file.
                elif gender=='F':
                    count_of_a_name[first_name][1] += float(count)
                    no_of_females+=int(count) ##Count is string in file.
    else:
        continue  ##Year not between year_1 and year_2

no_of_newborns=no_of_males+no_of_females

temp_dictionary={} ##dictionary with only names with proportion above target proportion
our_output_dict={}
j=0
count=0
counter=0
for i in count_of_a_name:
    male_or_female_proportion = (count_of_a_name[i][0] + count_of_a_name[i][1])/no_of_newborns
    male_proportion = count_of_a_name[i][0]/no_of_males
    female_proportion = count_of_a_name[i][1]/no_of_females
    abs_diff_btw_male_and_female = abs(male_proportion - female_proportion)
    if male_or_female_proportion >= target_proportion:
        temp_dictionary[i]=[abs_diff_btw_male_and_female,female_proportion,male_proportion,male_or_female_proportion]
        j=j+1
        if count==0:   ##First time lowest_diff=1st abs_diff in list
            lowest_diff_bw_male_and_female = abs_diff_btw_male_and_female
        else:
            if abs_diff_btw_male_and_female<lowest_diff_bw_male_and_female:
                lowest_diff_bw_male_and_female = abs_diff_btw_male_and_female 
        count=count+1    ##Two purposes - one for line92 and line99

if count==0:
    print(f'No name was given as both female and male names between {year_1} and {year_2}\n  with a proportion of at least {target_proportion} as a (female or male) name.')
else:
    print(f'{lowest_diff_bw_male_and_female} is the smallest difference in absolute value\n  between the proportion of a name as a female name\n  and the proportion of that name as a male name,\n  the proportion of that name as a (female or male) name\n  being at least {target_proportion}.')
    print("It applies to the following name(s).")
    for i in sorted(temp_dictionary.keys()): ##Sorting by only the keys of the dictionary. i.e. in our case, names only
        if temp_dictionary[i][0]==lowest_diff_bw_male_and_female:
            if counter==0:
                print(f'  - {i}, with the following proportions:\n    * {temp_dictionary[i][1]} as a female name;\n    * {temp_dictionary[i][2]} as a male name;\n    * {temp_dictionary[i][3]} as a (female or male) name.')
            else:
                print(f'  - {i}:\n    * same proportion as a female name;\n    * same proportion as a male name;\n    * same proportion as a (female or male) name.')
            counter=counter+1
        
    
    
        





    

    