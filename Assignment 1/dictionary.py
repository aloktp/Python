##So plan to start my program is to first get the input as a string. 
##Remove all the whitespace characters in the list using replace function, which is the Best as it removes every white space, even the ones in between characters. 
##Then check if all characters are all alphabetical (i.e. no digits, symbols etc) using isalpha. 
##Then check if all characters are lowercase using islower function. 
##Then check the length of the string is between 3 and 10 character using len function.
##Then convert it into a list.
import sys
while True:
    try:
        user_input=input("Enter between 3 and 10 lowercase letters: ")
        user_input=user_input.replace(" ","")
        if not user_input.isalpha() or not user_input.islower():
            raise ValueError
        if len(user_input)<3 or len(user_input)>10:
            raise ValueError
        break
    except ValueError:
        print("Incorrect input, giving up...")
        sys.exit()   ##Clarify this with lecturer. When I remove this line, Error comes because of the way in input function is processed. input() is waiting for input but none is provided. Clarify .
##Actual program 2nd part begins
##sum of values of user input = sum of values of dicitonary word IS NOT A NECESSARY CONDITION. So ignore that.
## Basically two conditions to be satisified to solve this problem
##1st one - Sum of values of acceptable dictionary word is less than or equal to Sum of values of input word
##If a non matching character is found, ignore the word and move on to next
##Number of times a specific character is repeated in dicitonary word should be be less than or equal to the same in user input word e.g. user input='mamal'. Dicitonary word cant be 'mammal, because 2 instances of 'm' compared to 3 instances of'm'.
##There are no uppercase characters in the words in the dictionary. So no need to convert to lowercase to compare it to user_input.
##We have to remove newline characters in the end of a line in dictionary. Otherwise, error while storing words in output_words_list dictionary.
#The only special characters in the dictionary are '  e.g.don't , industry' s etc. We have to remove those too.
##The plan is to replace matching characters with nullspaces. 
##In line 39, use STRIP function to remove newline character at end of line. Otherwise, words of same length will be ignored.
##Since in line 36, with open.. its default syntax, i.e. only read operation. So, even if you assign like in line 39, dictionary.txt wont be modified. Even otherwise, line is a shallow copy. So, nothing is going to be modified in dicitonary.txt
##Idea is if matching character is found, remove it in both lists.
##AND THEN go back to start of loop again. LOOP MUST START FROM INDEX 0 if matching character is found.
alphabet_values={'a':2,'b':5,'c':4,'d':4,'e':1,'f':6,'g':5,'h':5,'i':1,'j':7,'k':6,'l':3,'m':5,'n':2,'o':3,'p':5,'q':7,'r':2,'s':1,'t':2,'u':4,'v':6,'w':6,'x':7,'y':5,'z':7}
output_words_list={} ##Empty list for now. Its our list of acceptable output words.
sum_values_list = []  ##Empty list. List of only the sum of values of acceptable words.
j=0           ##IT SHOULD NOT BE KEPT INSIDE LOOP. Indices of dicitonary output_words_list
with open("dictionary.txt") as file:       ##Please ensure working directory(use pwd command) is in COMP9021/Assignment 1 folder for Jupyterlab to be able to fetch dictionary.txt
    for line in file:           ##Instead of this you can rework this for loop to for i in range(len(line)) and then rework other necessary statements to follow through with this version to work, but unnecessary.
        line=line.strip()    ## Very IMPORTANT. Otherwise dictionary wont work.## To remove newline characters at end of line. And in rare occasion, if spaces in the start of line - If not there in whole dictionary, then rstrip() function is enough.
        if(len(line)<=len(user_input)):  ##Dictionary word cant have more number of characters than input word.
            ## We need to save a copy of line as a LIST, as only remove or pop operation is useful.
            line_copy=line    ##Shallow copy of string line
            line_copy=line_copy.replace("'","")  ##IMPORTANT. Removing ' character if any in word with nullspace. e.g. don't , industry' s
            line_copy_list=list(line_copy)      ##Shallow copy. VERY NECESSARY. ##line_copy is a string. replace, lstrip and rstrip function replaces ALL instances of a character. So, USELESS for us.   
            ##Saving it with new name i.e. line_copy_list instead of line_copy itself(what i mean is line_copy=list(line_copy) is NOT USEFUL. As I need the word string, not the list to be stored in output dictionary. So, I shouldnt loose the value of line_copy
            ## We need to save a copy of line_copy as a LIST, as only remove or pop operation is useful.
            input_copy=list(user_input)        ##Shallow copy of m. VERY important, as characters have to be removed from m too if matching characters found
            sum_dict_word=0  #Sum of values of all characters in user input. Now initialized as zero.
            flag=0
            while (flag==0):
                for i in line_copy_list:    ##Dont use for i in line_Copy as we need to remove matching characters.##That is iteration over each character in line_copy.
                    sum_dict_word=sum_dict_word+alphabet_values[i]   #Sum of values of all characters in user input                
                    if i in input_copy:         ##The in keyword has two purposes: The in keyword is used to check if a value is present in a sequence (list, range, string etc.). And The in keyword is also used to iterate through a sequence in a for loop:
                    ##Internally, the in keyword executes a for loop, and compares i with all elements in line_copy. ## So NO need to manually specify a for loop statement ie. for i in m, is not necessary, for as to compare individual character of line_copy against all individual characters of string m.
                    ## if i in input_copy: is basically one to many comparison. 1st character of line_copy is compared with all (if no matching characters found) characters  of string m in a loop wise fashion.
                        line_copy_list.remove(i)  
                        input_copy.remove(i) ##VERY IMPORTANT. This WILL ensure that condition of number of duplicates of a character allowed is checked               
                        break  ##So as to start again from start of loop i.e. index0 ##IMPORTANT break statement. Because e.g. input_copy=['a','a','h','h']. line_copy_list = ['a','a','h']. After first iteration i.e. index 0, i is 'a' => user_input=['a','a','h'] and line_copy_list=['a','h']. but next i becomes 'h' instead of 'a', because index is 1. i is 'h' instead of 'a', because removal operation shifts elements to the left And this is bad for our program.
                    else:  #You need not have this else statement also. But its good for efficiency, otherwise the forloop goes through the full word.
                        flag=1 ## flag initialisation should come before break. To break out or while loop. To reach, next iteration i.e. Next line or next word in dictionary.  
                        break ##Unacceptable word because of non-matching character  ##If i is not there in string m e.g. the character'd' is not there in 'abc' OR , break keyword will initate next for loop instance in FILE i.e.next word i.e. next line in dicitonary.                   
                if line_copy_list==[]: ##For an acceptable word, line_copy_list will become Empty. e.g. user_input='abb'. Dictionary word='a'
                    output_words_list[j]=line_copy,sum_dict_word  ##NOT line_copy_list. DONOT use Line_copy_list. Use line_copy i.e. string ##Tuple of word and sum of values. Tuple is okay. List is also okay. Both are "iterable". ##i.e. Only acceptable words reach here and are stored in dictionary output_words_list
                    sum_values_list.append(sum_dict_word) ##DONOT write sum_values_list = sum_values_list.append(sum_dict_word)     
                    j=j+1
                    flag=1
if output_words_list=={}:  #EMPTY DICITONARY, NOT EMPTY LIST. Otherwise, sample input 'zz zz zz' will give error. This code is for Non acceptable words in the whole dictionary
    print("No word is built from some of those letters.")
else:
    highest_value=max(sum_values_list)
    print(f'The highest score is {highest_value}.')
    highest_value_words=[output_words_list[x][0] for x in output_words_list if output_words_list[x][1]==highest_value]
    if len(highest_value_words)==1:
        print(f'The highest scoring word is {highest_value_words[0]}')
    else:
        print("The highest scoring words are, in alphabetical order:")
        for i in highest_value_words:
            print("    "+i)
                    
        
                        
                
        
                         

    
