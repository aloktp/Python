import os, itertools, re ## Itertools for combinations of permutations and combinations. Re for regular expressions
from collections import defaultdict
import sys, copy

## In the question, there is sudoku=Sudoku('sudoku_1.txt'). The LHS sudoku is an object of the class Sudoku (in RHS). 
# Classes are by general style Capitalized.

class SudokuError(Exception): ##VERY IMPORTANT Exception is capitalized ##The () doesnot mean its a function and exception is a parameter.## All exceptions must be instances of a class that derives from BaseException                           
    pass                      ##No need to put sys.exit()
                            
class Sudoku:
    def __init__(self,file_name):
        self.file_name = file_name
        self.output_file_name = ''
        for i in file_name:
            if i=='.':
                break
            self.output_file_name += i
        #print(self.output_file_name)
        self.dictionary_marked_elements = []
        file_as_list=[] ##A row will be a list inside this list. i.e. File_as_list is a list of lists... it therefore contains all the lines in a matrix fashion
        with open (self.file_name) as file:
            count_no_of_lines=0
            for line in file:
                if line.isspace():  ##We are not going to write code to increment lines with space only.
                    continue
                else:
                    ## VERY IMPORTANT I used the line=line.split() earlier, but it wont work on sudoku_4.txt as the length of line becomes 1. Because in all otehr sudoku text files, there are gaps between digits in a row. In sudoku_4.txt, no gaps.
                    ## So, usually , its always better to use line.replace(" ",""). 
                    ## AND YES EVEN IF YOU HAVE MULTIPLE SPACES BETWEEN DIGITS, just having " " as 1st argument instead of "  " or "     " etc. inside the replace function will work because it replaces 1 single space individually and multiple spaces just have many individual spaces.
                    line=line.strip() ##VERY IMPORTANT . There is a space character after 1st line in sudoku_4. It wont go away with the replace function in the next line
                    line=line.replace(" ","")  ##Split will ignore the spaces and give only characters and feed it into line in LHS as a list
                    ## But, since we used line.replace(), line is now a string. SO , WE HAVE TO USE in(element) in the next condition
                    ## You cant use if not all(element.isdigit() for element in line), because line is now string, and for int(element) in line AND int(element).isdigit() doesnot work
                    ## VERY IMPORTANT You should not use if not all(int(element) in [0,1,2,3,4,5,6,7,8,9] for element in line) in the line below, because in sudoku_wrong_3.txt, there is a character "A", and we cant do int("A") i.e. error will come
                    ## AND BECAUSE OF THE ABOVE FACT, DONOT CLUB TOGETHER IF CONDITIONS USING OR i.e. This wont work -> if not all(element in ["0","1","2","3","4","5","6","7","8","9"] for element in line) or any(int(element)<0 or int(element)>9 for element in line) or len(line)!=9:  ## 9 columns max ##The code "(element.isdigit() for element in line)"" is necessary because line is a list.   # You typed any(int(element)<0 or int(element)>9 for element in line) in the beginning stages creating problem in sudoku_4.txt. Be careful of the brackets in this part. ##I just renamed all elements as elemnent1, elemnent 2 etc for ease of debugging 
                    if not all(element in ["0","1","2","3","4","5","6","7","8","9"] for element in line):  ## 9 columns max ##The code "(element.isdigit() for element in line)"" is necessary because line is a list.   # You typed any(int(element)<0 or int(element)>9 for element in line) in the beginning stages creating problem in sudoku_4.txt. Be careful of the brackets in this part. ##I just renamed all elements as elemnent1, elemnent 2 etc for ease of debugging
                        raise SudokuError("Incorrect input") ##Try and except block unnecessary if this output error message "Incorrect input" is there in this statement itself. I am just writing this statement to teach you all this. You can only correct duplicate error outputs of line 20 and line 25 if you use Class Exception
                    if any(int(element)<0 or int(element)>9 for element in line) or len(line)!=9: ##This line to be done only if there are no alphabets in a row i.e. condition in line 28 satisfies
                        raise SudokuError("Incorrect input")
                    line=[int(e) for e in line]   ##Converting the digits in string i.e. text form to integers .. because we need to be able to compare digits in a box, a row and column in the preassess function.
                    count_no_of_lines += 1
                    file_as_list.append(line)   ##One by one each row is appended as a single list to the list of lists that is file_as_list.
            if count_no_of_lines!=9:   ##if more than 9 rows.. but non empty columns
                raise SudokuError("Incorrect input")
            self.grid=file_as_list ### VERY IMPORTANT. This is what allows us to use the grid in other functions
            ### VERY IMPORTANT. YOU CANT PUT THE FOLLOWING FOR LOOPS IN THE END OF PREASSESS(). BECAUSE CHECK THE COMMANDS TO RUN. IN EVERY CASE, ITS SUDOKU FUNCTION WHICH IS COMMONLY RUN. IF YOU CHECK TEST No.9, see Preassess is not even used. So, you have to rectify the '0' issue here itself in Sudoku function.
            ## VERY IMPORTANT FROM HEREON, WE ASSUME THAT ONLY GRIDS THAT PASS THE SUDOKU TEST WILL BE PASSED ONTO BARE(), FORCED() etc.
            ## That means from here on, we can have a grid with blanks i.e. "" empty instead of zero.
            ## VERY VERY VERY IMPORTANT. The grid with empty "" instead of zeros will only pass to bare () function or ANY function run after Sudoku function
            ## IF AND ONLY IF THE SUDOKU FUNCTION IS RUN. THIS IS THE FEATURE OF CLASS METHODS etc. I have noted it down in Sample code text file.
            for i in range(9):
                for j in range(9):
                    if self.grid[i][j]==0: ##VERY VERY IMPORTANT. IN INPUT TEXT FILE, digits were string. But after line 34, they are integers. So, DONT DO if self.grid=="0" because its not a string anymore. Otherwise when tex file is made, 0 will appear.
                        self.grid[i][j]="" ## You CANT use self.grid[i][j].clear() as Attribute Error: 'int' object has no attribute 'clear'method ##DONOT replace 0 with None element as "None" will print out in Sudoku. clearing the element so that when representing the actual sudoku grid in bare() and thereon blank will show instead of 0
            #return self.output_file_name 
    def preassess(self):
        for i in range(9):
            row=[]
            column=[]
            for j in range(9):
                ## SINCE IN COMMANDS TO RUN TEXT FILE, SUDOKU() IS COMMON IN ALL TEST CASES & ITS BEFORE PREASSESS(), Because of lines 45 to 48, we cant give if self.grid[i][j]!=0
                if self.grid[i][j]!="":  ##Donot consider '0' values. Sudoku cant have 0. And there are usually many 0s in a row i.e. they are duplicates making our result wrong.
                    row.append(self.grid[i][j])  ##grid[i][j] i.e i,j  ## Getting all the elements already in a row
            if len(set(row))<len(row): ##to check if duplicate elements. A set cant have duplicate elements. It removes duplicate elements. So, if length of set(row)<length of row,.. then there were duplicate elements in row.
                print('There is clearly no solution.')
                sys.exit()
            for j in range(9):
                if self.grid[j][i]!="":
                    column.append(self.grid[j][i]) ##grid[j][i] i.e. j,i  ##Getting all the elements already in a column
            if len(set(column))<len(column): ##to check if duplicate elements in column
                print('There is clearly no solution.')
                sys.exit()
        ## Now to check if duplicate elements in a 3X3 box
        for a in [1,4,7]:   ##Centre element of a 3X3 box i.e. (i,j) = (1,1) or (1,4) or (1,7) or (4,1) or (4,4) or (4,7) or (7,1) or (7,4) or (7,7)
            for b in [1,4,7]:
                elements_in_a_box=[] ##Storing all the elements in a box. Now reinitializing it to empty list before start of next box.
                for i in range(a-1,a+2): ##For statement syntax exludes a+2 i.e. upto a+1 only
                    for j in range(b-1,b+2):
                        if self.grid[i][j]!="":
                            elements_in_a_box.append(self.grid[i][j]) 
                            
                if len(set(elements_in_a_box))<len(elements_in_a_box):  ##If duplicate elements in a box. A set can't have duplicates.
                    print('There is clearly no solution.')
                    sys.exit()
        print("There might be a solution.")
        ## sys.exit()  ## No need of Sys.exit() here cause already we reached end of function.                    
    
    def bare_tex_output(self):                        
    ## global grid ## NO NEED of global as name 'grid' is parameter and global ## I thought to make it global SO THAT FROM line 75 onwards TO ENSURE THAT grid wont have zeroes in it.
    ## VERY IMPORTANT - But in the actual program you submit with classes and objects, global keyword is not necessary
    ## VERY IMPORTANT - Note that the point of classes is to eliminate (truly) global state and to manage it within classes and objects.
    ## A method (function of a class) is not like a normal function. If you want the value a variable is assigned in a normal function to be reflected from then on, you need to use global keyword
    ## But in method, global keyword is not necessary. You can access it anywhere.
        bare_file_name= self.output_file_name + "_bare.tex"
        with open (bare_file_name,'w') as file:
            ## Strike the below comments from 91 to 97. I am able to use f-string.
            ####### It is almost impossible to use f-string because it wont accept unicode characters like \ backslash. With r-string that I used below, it wont feed variable value if I put inside curly braces i.e.{grid[0][0]} wont work in r-string
            ####### There is already \N newline , \ backslash and {} curly braces in the Latex code itself, which cause problems with f-string
            ####### Using f and r together also is basically useless for above reasons. i.e. fr"
            ####### I have decided therefore to store the whole latex code as a raw text i.e. using r-string. 
            #######I will try to insert the values of all grid elements in the raw string at the appropriate positions. 
            ####### Even though string is a list basically, insert function doesnt work with a string. So, we are only left with use of concatenation to solve the issue.
            ####### Python iteration index starts from 0 and not 1   
            ## Strike the above comments from 67 to 72. I am able to use f-string.
            ## The """ triple quotes in beginning and end preserves the same layout i.e. with indentations, paragraphs etc, just the same as in Latex code.
            ## Use triple braces i.e. "{{{grid[0][0]}} i.e. triple braces if you want variable value and bracket. 
            ## Double braces if you want a single bracket with text inside, the whole thing to be considered as text only.
            ## Change every \ backslash to \\ double backslash to escape backslash i.e. to get \ only
            ## Take care of backslash especially in the \\newcommand line 
            ## From line 102 , it is necessary to left indent if we want to match with sample tex file and its allowed to do so also because of the triple quotes.
            ## Make sure line 109,110 and 111 are in correct indentation
            ## VERY IMPORTANT. WHEN YOU EXECUTE THIS, EXECUTE IT IN THE ORDER in commands to run text file & USE TERMINAL. Otherwise, you wont know whats the difference in tex file outputed and sample file.
            ## The system("diff sol_sudoku_3_bare.tex sudoku_3_bare.tex; echo $?")' command in commands to run wont work in windows. So, just run till sudoku.bare_tex_output() , and compare the tex file outputed yourself with the sample tex file.
            latex_text_as_raw_string =  f"""\\documentclass[10pt]{{article}}
\\usepackage[left=0pt,right=0pt]{{geometry}}
\\usepackage{{tikz}}
\\usetikzlibrary{{positioning}}
\\usepackage{{cancel}}
\\pagestyle{{empty}}

\\newcommand{{\\N}}[5]{{\\tikz{{\\node[label=above left:{{\\tiny #1}},
                               label=above right:{{\\tiny #2}},
                               label=below left:{{\\tiny #3}},
                               label=below right:{{\\tiny #4}}]{{#5}};}}}}

\\begin{{document}}

\\tikzset{{every node/.style={{minimum size=.5cm}}}}

\\begin{{center}}
\\begin{{tabular}}{{||@{{}}c@{{}}|@{{}}c@{{}}|@{{}}c@{{}}||@{{}}c@{{}}|@{{}}c@{{}}|@{{}}c@{{}}||@{{}}c@{{}}|@{{}}c@{{}}|@{{}}c@{{}}||}}\\hline\\hline
% Line 1
\\N{{}}{{}}{{}}{{}}{{{self.grid[0][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[0][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[0][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[0][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[0][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[0][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[0][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[0][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[0][8]}}} \\\\ \\hline

% Line 2
\\N{{}}{{}}{{}}{{}}{{{self.grid[1][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[1][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[1][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[1][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[1][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[1][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[1][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[1][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[1][8]}}} \\\\ \\hline

% Line 3
\\N{{}}{{}}{{}}{{}}{{{self.grid[2][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[2][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[2][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[2][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[2][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[2][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[2][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[2][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[2][8]}}} \\\\ \\hline\\hline

% Line 4
\\N{{}}{{}}{{}}{{}}{{{self.grid[3][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[3][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[3][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[3][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[3][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[3][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[3][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[3][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[3][8]}}} \\\\ \\hline

% Line 5
\\N{{}}{{}}{{}}{{}}{{{self.grid[4][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[4][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[4][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[4][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[4][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[4][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[4][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[4][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[4][8]}}} \\\\ \\hline

% Line 6
\\N{{}}{{}}{{}}{{}}{{{self.grid[5][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[5][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[5][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[5][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[5][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[5][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[5][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[5][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[5][8]}}} \\\\ \\hline\\hline

% Line 7
\\N{{}}{{}}{{}}{{}}{{{self.grid[6][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[6][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[6][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[6][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[6][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[6][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[6][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[6][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[6][8]}}} \\\\ \\hline

% Line 8
\\N{{}}{{}}{{}}{{}}{{{self.grid[7][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[7][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[7][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[7][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[7][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[7][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[7][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[7][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[7][8]}}} \\\\ \\hline

% Line 9
\\N{{}}{{}}{{}}{{}}{{{self.grid[8][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[8][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[8][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[8][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[8][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[8][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[8][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[8][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[8][8]}}} \\\\ \\hline\\hline
\\end{{tabular}}
\\end{{center}}

\\end{{document}}
"""
            file.write(latex_text_as_raw_string)
    
    def forced_tex_output(self):
        ## Since in commands to run, we can see from test no.9 onwards, preassess is not executed before forced_text_output or bare() or marked() or worked().
        ## Hence, we have to run preassess ourselves inside all functions from now on to ensure that only a grid without duplicate elements in a row, or column actually produces a forced_output.
        ## If not such a grid without duplicates, it 
        ## Read the Sudoku algorithm Paper pdf to understand the logic. Nothing else
        frequency_of_a_digit=defaultdict(int) 
        for i in range(9):
            for j in range(9):
                if self.grid[i][j]!="":
                    frequency_of_a_digit[self.grid[i][j]]+=1
        ## There are 4 numbers with the highest frequency of 4. They are 1,4,7,9. But if you check sudoku_3_forced image in page 8 in assignment pdf, then you see its 7 which is filled out first. So i assume if there are many digits with same highest frequency, the digits are chosen in decreasing order. i.e. 9 has priority before 7 which has priority before 4 which has priority before 1.
        frequency_of_a_digit =  dict(sorted(frequency_of_a_digit.items(), key = lambda x: (x[1],x[0]), reverse = True)) ## You will get a tuple from the sorted function, which you have to convert to dictionary ## Equivalent to -x[1],-x[0] i.e. Both x[1] i.e. values and x[0] i.e. keys are preferred in decreasing order  ##It can only be done this way using syntax dict, sorted etc. Trust me.
        row_index=-1   ## Better not to initialize as 0. No need to unnecessarily rish giving wrong value to grid[0][0] in line 228
        column_index=-1 ## Better not to give 0 
        flag=0
        while(flag==0):
            temporary_grid=copy.deepcopy(self.grid)
            for f in frequency_of_a_digit.keys():
                for a in [1,4,7]:   ##Centre element of a 3X3 box i.e. (i,j) = (1,1) or (1,4) or (1,7) or (4,1) or (4,4) or (4,7) or (7,1) or (7,4) or (7,7)
                    for b in [1,4,7]:
                        elements_in_a_box=[] ##Storing all the elements in a box. Now reinitializing it to empty list before start of next box.
                        count=0 ## Count of how many cells in a box are there in which we can force the value of variable f
                        for i in range(a-1,a+2): ##For statement syntax exludes a+2 i.e. upto a+1 only
                            for j in range(b-1,b+2):
                                if self.grid[i][j]!="":
                                    elements_in_a_box.append(self.grid[i][j])
                        if f not in elements_in_a_box:
                            for c in range(a-1,a+2): ## YOU CAN USE i and j again. But BEST PRACTICE NOT TO USE THAT AS EXPLAINED in line 325. ALSO, I am giving a and b instead of i & j so that code is more legible and understandable and I will be able to distinguish b/w variables at line 199,200,204 and 205.
                                for d in range(b-1,b+2):   ## For statement syntax exludes a+2 i.e. upto a+1 only                                 
                                    row=[]
                                    column=[]
                                    elements_not_allowed_at_a_single_cell = []
                                    for m in range(0,9):  ##Getting all the elements already in a column
                                        if self.grid[c][m]!="":
                                            row.append(self.grid[c][m])
                                    for n in range(0,9):  ##Getting all the elements already in a column
                                        if self.grid[n][d]!="":
                                            column.append(self.grid[n][d])    
                                    elements_not_allowed_at_a_single_cell = set(elements_in_a_box + row + column) ##Set function removes duplicates
                                    if self.grid[c][d]=="": ## only empty fields should be filled. CELLS WHICH ALREADY HAVE DIGITS SHOULDNOT BE REPLACED.
                                        if f not in elements_not_allowed_at_a_single_cell: ## 8 unique elements
                                            row_index=c   ##If there is only once cell in which f can be put, then count in line 222 will be incremented once only. i.e. only 1 value will EVER enter row_index and column_index for A box of 3x3 for a given f.
                                            column_index=d
                                            count=count+1
                        if count==1:
                            self.grid[row_index][column_index]=f
            if self.grid==temporary_grid: ##move on to digit with next lower frequency i.e. line 197
                flag=1
        
        forced_file_name= self.output_file_name + "_forced.tex"
        with open (forced_file_name,'w') as file:
            latex_text_as_raw_string =  f"""\\documentclass[10pt]{{article}}
\\usepackage[left=0pt,right=0pt]{{geometry}}
\\usepackage{{tikz}}
\\usetikzlibrary{{positioning}}
\\usepackage{{cancel}}
\\pagestyle{{empty}}

\\newcommand{{\\N}}[5]{{\\tikz{{\\node[label=above left:{{\\tiny #1}},
                               label=above right:{{\\tiny #2}},
                               label=below left:{{\\tiny #3}},
                               label=below right:{{\\tiny #4}}]{{#5}};}}}}

\\begin{{document}}

\\tikzset{{every node/.style={{minimum size=.5cm}}}}

\\begin{{center}}
\\begin{{tabular}}{{||@{{}}c@{{}}|@{{}}c@{{}}|@{{}}c@{{}}||@{{}}c@{{}}|@{{}}c@{{}}|@{{}}c@{{}}||@{{}}c@{{}}|@{{}}c@{{}}|@{{}}c@{{}}||}}\\hline\\hline
% Line 1
\\N{{}}{{}}{{}}{{}}{{{self.grid[0][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[0][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[0][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[0][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[0][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[0][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[0][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[0][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[0][8]}}} \\\\ \\hline

% Line 2
\\N{{}}{{}}{{}}{{}}{{{self.grid[1][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[1][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[1][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[1][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[1][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[1][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[1][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[1][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[1][8]}}} \\\\ \\hline

% Line 3
\\N{{}}{{}}{{}}{{}}{{{self.grid[2][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[2][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[2][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[2][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[2][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[2][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[2][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[2][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[2][8]}}} \\\\ \\hline\\hline

% Line 4
\\N{{}}{{}}{{}}{{}}{{{self.grid[3][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[3][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[3][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[3][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[3][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[3][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[3][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[3][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[3][8]}}} \\\\ \\hline

% Line 5
\\N{{}}{{}}{{}}{{}}{{{self.grid[4][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[4][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[4][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[4][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[4][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[4][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[4][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[4][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[4][8]}}} \\\\ \\hline

% Line 6
\\N{{}}{{}}{{}}{{}}{{{self.grid[5][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[5][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[5][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[5][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[5][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[5][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[5][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[5][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[5][8]}}} \\\\ \\hline\\hline

% Line 7
\\N{{}}{{}}{{}}{{}}{{{self.grid[6][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[6][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[6][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[6][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[6][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[6][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[6][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[6][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[6][8]}}} \\\\ \\hline

% Line 8
\\N{{}}{{}}{{}}{{}}{{{self.grid[7][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[7][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[7][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[7][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[7][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[7][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[7][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[7][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[7][8]}}} \\\\ \\hline

% Line 9
\\N{{}}{{}}{{}}{{}}{{{self.grid[8][0]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[8][1]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[8][2]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[8][3]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[8][4]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[8][5]}}} &
\\N{{}}{{}}{{}}{{}}{{{self.grid[8][6]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[8][7]}}} & \\N{{}}{{}}{{}}{{}}{{{self.grid[8][8]}}} \\\\ \\hline\\hline
\\end{{tabular}}
\\end{{center}}

\\end{{document}}
"""
            file.write(latex_text_as_raw_string)        
            ## return elements_not_allowed_at_a_single_cell ## I can do these if I want to send to for e.g. marked_tex_output function in line 306
    def marked_tex_output(self):
        ## VERY VERY IMPORTANT. FROM NOW ON IN ALL FUNCTIONS, WE NEED TO PASS THE OUTPUT GRID OF FORCED FUNCTION, even if its not called by Eric on command line before executing these functions.
        ## If we just take self.grid here without calling forced function inside this marked_tex_output function, then we will only get the grid from __init__ i.e. input text file , and not the forced one. Try for yourself.
        ## VERY VERY IMPORTANT. Below is how we call the forced function. Sudoku with capital S is the class.
        Sudoku.forced_tex_output(self)  ##argument self is necessary
        ## Now from here on, if we use self.grid, it will be the self.grid of the output of forced_tex_output.
        ## HOWEVER, other variables that are not object variables. i.e. self.variable_name cannot be accessed. 
        ## If you try to access or print elements_not_allowed_at_a_single_cell variable, you wont get output. You will get error. Try it
        ## print(elements_not_allowed_at_a_single_cell) ## It wont work
        ## v = Sudoku.forced_tex_output(self) ## instead of line 301. I can then obviously get self.grid of forced and I will get value of elements_in_a_cell in v variable. ## I can try to "return" these variables of forced into a variable like in line 301. 
        ## print(v)
        dictionary_marked_elements={} ##Dictionary where (i,j,e) WILL BE the keys. e is the marked element. Value will be e or "".
        ## VERY VERY VERY IMPORTANT. You cant append values to an empty dictionary or to a key which doesnt exist. You have to create the keys first.
        for i in range(9):
            for j in range(9):
                for k in["top_left", "top_right", "bottom_left", "bottom_right"]:
                    dictionary_marked_elements[i,j,k] = [] ## Creating keys. Initiazing as empty list.
                    ## NOW ALL KEYS EXIST. OTHERWISE LINE 371 to 378 DOESNT WORK
        for a in [1,4,7]:   ##Centre element of a 3X3 box i.e. (i,j) = (1,1) or (1,4) or (1,7) or (4,1) or (4,4) or (4,7) or (7,1) or (7,4) or (7,7)
            for b in [1,4,7]:
                elements_in_a_box=[] ##Storing all the elements in a box. Now reinitializing it to empty list before start of next box.
                for i in range(a-1,a+2): ##For statement syntax exludes a+2 i.e. upto a+1 only
                    for j in range(b-1,b+2):
                        if self.grid[i][j]!="":
                            elements_in_a_box.append(self.grid[i][j])
                for c in range(a-1,a+2): ##For statement syntax exludes a+2 i.e. upto a+1 only
                    for d in range(b-1,b+2): ## YOU CAN USE i and j again. BUT YOU WONT BE ABLE TO ACCESS THE i & j value at line 320 and 321 at line 340 onwards. Because i & j will be the values in line 325 and 326
                        if self.grid[c][d]=="":  ## only empty fields should be filled. CELLS WHICH ALREADY HAVE DIGITS SHOULDNOT BE REPLACED.
                            row=[]
                            column=[]
                            elements_not_allowed_at_a_single_cell = []
                            for m in range(0,9):  ##Getting all the elements already in a column
                                if self.grid[c][m]!="":
                                    row.append(self.grid[c][m])
                            for n in range(0,9):  ##Getting all the elements already in a column
                                if self.grid[n][d]!="":
                                    column.append(self.grid[n][d])    
                            elements_not_allowed_at_a_single_cell = set(elements_in_a_box + row + column) ##Set function removes duplicates
                            elements_allowed_in_the_cell={1,2,3,4,5,6,7,8,9}-elements_not_allowed_at_a_single_cell
                            elements_allowed_in_the_cell=list(sorted(elements_allowed_in_the_cell)) ##Sets are not iterable or subscriptable. Lists are
                            ## VERY VERY IMPORTANT. A DICITIONARY VALUE CAN BE EMPTY. BUT A DICTIONARY KEY CANT BE EMPTY. IT WILL GIVE KEY ERROR. 
                            ## "HANDLING" THE KEY ERROR EXCEPTION LIKE WE DID SUDOKUERROR in line  IS##You have to sort it. Otherwise you get 9,7 instead of 7,9 i.e. in that order for position (4,8) and fail sudoku_4  NOT MUCH USEFUL.
                            ## BECAUSE THE ERROR APPEARS WHEN WE USE PRINT COMMAND AGAIN i.e. for k in range(1,10): print (dictionary_marked_elements[0,0,k])
                            ## TRY AND EXCEPT BLOCK IS COMPULSORY TO HANDLE EXCEPTIONS.
                            ## try : ## No use because we want the exception to be bypassed when printing the dictionary.
                                ## for f in elements_not_allowed_at_a_single_cell:
                                    ##dictionary_marked_elements[i,j,f]=" " 
                            ## except KeyError:
                            ## pass
                            ## So Another method I tried is to give 1 blank space instead of empty. But it too gives key error.
                            ## for f in elements_not_allowed_at_a_single_cell:
                            ## dictionary_marked_elements[i,j,f]=" "
                            ## for k in range(1,10): 
                                ## print (dictionary_marked_elements[0,0,k])
                            ## So, now I will do try , except and exception thing on print statement. It works for my purpose. 
                            ## You also dont need to do :-
                            ## for f in elements_not_allowed_at_a_single_cell:
                                    ##dictionary_marked_elements[i,j,f]=""   ## But I will keep it if in future its necessary
                            ## for f in elements_not_allowed_at_a_single_cell:
                            ## dictionary_marked_elements[i,j,f]=""   
                            ## try:  ##NO NEED TO DO TRY BLOCK. NO NEED BECAUSE THE ISSUE I WAS HAVING IS NOT NULL VALUE. IT WAS NULL KEY. I SOLVED IT WITH BY CREATING ALL POSSIBLE KEYS OF THE DICTIONARY FIRST
                            ## for k in range(1,10):
                                ##   print (dictionary_marked_elements[0,0,k])
                            ## except KeyError:
                            ## pass ## Basically do nothing. This whole try except block wont show you any output, if you execute it.but that is okay for my purpose
                            ## I can wrap the try and except block around the latex_text_as_string.
                            for e in elements_allowed_in_the_cell:
                                if e == 1 or e == 2:
                                    dictionary_marked_elements[c,d,"top_left"].append(e)
                                if e == 3 or e == 4:
                                    dictionary_marked_elements[c,d,"top_right"].append(e)
                                if e == 5 or e == 6:
                                    dictionary_marked_elements[c,d,"bottom_left"].append(e)
                                if e == 7 or e == 8 or e == 9:
                                    dictionary_marked_elements[c,d,"bottom_right"].append(e)
                            ## ALL THE FOLLOWING ARE SEPERATE IF-ELSE CONDITIONS
                            if dictionary_marked_elements[c,d,"top_left"] == []: #Empty list
                                dictionary_marked_elements[c,d,"top_left"] = ""
                            else :
                                dictionary_marked_elements[c,d,"top_left"] = ' '.join(str(x) for x in dictionary_marked_elements[c,d,"top_left"])
                            
                            
                            if dictionary_marked_elements[c,d,"top_right"] == []: 
                                dictionary_marked_elements[c,d,"top_right"] = ""
                            else:
                                dictionary_marked_elements[c,d,"top_right"] = ' '.join(str(x) for x in dictionary_marked_elements[c,d,"top_right"])
                            
                                
                            if dictionary_marked_elements[c,d,"bottom_left"] == []: 
                                dictionary_marked_elements[c,d,"bottom_left"] = ""
                            else:
                                dictionary_marked_elements[c,d,"bottom_left"] = ' '.join(str(x) for x in dictionary_marked_elements[c,d,"bottom_left"])                            
                            
                            
                            if dictionary_marked_elements[c,d,"bottom_right"] == []: 
                                dictionary_marked_elements[c,d,"bottom_right"] = ""    
                            else:
                                dictionary_marked_elements[c,d,"bottom_right"] = ' '.join(str(x) for x in dictionary_marked_elements[c,d,"bottom_right"])
                        else:
                            dictionary_marked_elements[c,d,"top_left"]=""
                            dictionary_marked_elements[c,d,"top_right"]=""
                            dictionary_marked_elements[c,d,"bottom_left"]=""
                            dictionary_marked_elements[c,d,"bottom_right"]=""
        self.dictionary_marked_elements = dictionary_marked_elements
        marked_file_name = self.output_file_name + "_marked.tex"
        with open (marked_file_name,'w') as file:
            latex_text_as_raw_string =  f"""\\documentclass[10pt]{{article}}
\\usepackage[left=0pt,right=0pt]{{geometry}}
\\usepackage{{tikz}}
\\usetikzlibrary{{positioning}}
\\usepackage{{cancel}}
\\pagestyle{{empty}}

\\newcommand{{\\N}}[5]{{\\tikz{{\\node[label=above left:{{\\tiny #1}},
                               label=above right:{{\\tiny #2}},
                               label=below left:{{\\tiny #3}},
                               label=below right:{{\\tiny #4}}]{{#5}};}}}}

\\begin{{document}}

\\tikzset{{every node/.style={{minimum size=.5cm}}}}

\\begin{{center}}
\\begin{{tabular}}{{||@{{}}c@{{}}|@{{}}c@{{}}|@{{}}c@{{}}||@{{}}c@{{}}|@{{}}c@{{}}|@{{}}c@{{}}||@{{}}c@{{}}|@{{}}c@{{}}|@{{}}c@{{}}||}}\\hline\\hline
% Line 1
\\N{{{dictionary_marked_elements[0, 0, 'top_left']}}}{{{dictionary_marked_elements[0, 0, 'top_right']}}}{{{dictionary_marked_elements[0, 0, 'bottom_left']}}}{{{dictionary_marked_elements[0, 0, 'bottom_right']}}}{{{self.grid[0][0]}}} & \\N{{{dictionary_marked_elements[0, 1, 'top_left']}}}{{{dictionary_marked_elements[0, 1, 'top_right']}}}{{{dictionary_marked_elements[0, 1, 'bottom_left']}}}{{{dictionary_marked_elements[0, 1, 'bottom_right']}}}{{{self.grid[0][1]}}} & \\N{{{dictionary_marked_elements[0, 2, 'top_left']}}}{{{dictionary_marked_elements[0, 2, 'top_right']}}}{{{dictionary_marked_elements[0, 2, 'bottom_left']}}}{{{dictionary_marked_elements[0, 2, 'bottom_right']}}}{{{self.grid[0][2]}}} &
\\N{{{dictionary_marked_elements[0, 3, 'top_left']}}}{{{dictionary_marked_elements[0, 3, 'top_right']}}}{{{dictionary_marked_elements[0, 3, 'bottom_left']}}}{{{dictionary_marked_elements[0, 3, 'bottom_right']}}}{{{self.grid[0][3]}}} & \\N{{{dictionary_marked_elements[0, 4, 'top_left']}}}{{{dictionary_marked_elements[0, 4, 'top_right']}}}{{{dictionary_marked_elements[0, 4, 'bottom_left']}}}{{{dictionary_marked_elements[0, 4, 'bottom_right']}}}{{{self.grid[0][4]}}} & \\N{{{dictionary_marked_elements[0, 5, 'top_left']}}}{{{dictionary_marked_elements[0, 5, 'top_right']}}}{{{dictionary_marked_elements[0, 5, 'bottom_left']}}}{{{dictionary_marked_elements[0, 5, 'bottom_right']}}}{{{self.grid[0][5]}}} &
\\N{{{dictionary_marked_elements[0, 6, 'top_left']}}}{{{dictionary_marked_elements[0, 6, 'top_right']}}}{{{dictionary_marked_elements[0, 6, 'bottom_left']}}}{{{dictionary_marked_elements[0, 6, 'bottom_right']}}}{{{self.grid[0][6]}}} & \\N{{{dictionary_marked_elements[0, 7, 'top_left']}}}{{{dictionary_marked_elements[0, 7, 'top_right']}}}{{{dictionary_marked_elements[0, 7, 'bottom_left']}}}{{{dictionary_marked_elements[0, 7, 'bottom_right']}}}{{{self.grid[0][7]}}} & \\N{{{dictionary_marked_elements[0, 8, 'top_left']}}}{{{dictionary_marked_elements[0, 8, 'top_right']}}}{{{dictionary_marked_elements[0, 8, 'bottom_left']}}}{{{dictionary_marked_elements[0, 8, 'bottom_right']}}}{{{self.grid[0][8]}}} \\\\ \\hline

% Line 2
\\N{{{dictionary_marked_elements[1, 0, 'top_left']}}}{{{dictionary_marked_elements[1, 0, 'top_right']}}}{{{dictionary_marked_elements[1, 0, 'bottom_left']}}}{{{dictionary_marked_elements[1, 0, 'bottom_right']}}}{{{self.grid[1][0]}}} & \\N{{{dictionary_marked_elements[1, 1, 'top_left']}}}{{{dictionary_marked_elements[1, 1, 'top_right']}}}{{{dictionary_marked_elements[1, 1, 'bottom_left']}}}{{{dictionary_marked_elements[1, 1, 'bottom_right']}}}{{{self.grid[1][1]}}} & \\N{{{dictionary_marked_elements[1, 2, 'top_left']}}}{{{dictionary_marked_elements[1, 2, 'top_right']}}}{{{dictionary_marked_elements[1, 2, 'bottom_left']}}}{{{dictionary_marked_elements[1, 2, 'bottom_right']}}}{{{self.grid[1][2]}}} &
\\N{{{dictionary_marked_elements[1, 3, 'top_left']}}}{{{dictionary_marked_elements[1, 3, 'top_right']}}}{{{dictionary_marked_elements[1, 3, 'bottom_left']}}}{{{dictionary_marked_elements[1, 3, 'bottom_right']}}}{{{self.grid[1][3]}}} & \\N{{{dictionary_marked_elements[1, 4, 'top_left']}}}{{{dictionary_marked_elements[1, 4, 'top_right']}}}{{{dictionary_marked_elements[1, 4, 'bottom_left']}}}{{{dictionary_marked_elements[1, 4, 'bottom_right']}}}{{{self.grid[1][4]}}} & \\N{{{dictionary_marked_elements[1, 5, 'top_left']}}}{{{dictionary_marked_elements[1, 5, 'top_right']}}}{{{dictionary_marked_elements[1, 5, 'bottom_left']}}}{{{dictionary_marked_elements[1, 5, 'bottom_right']}}}{{{self.grid[1][5]}}} &
\\N{{{dictionary_marked_elements[1, 6, 'top_left']}}}{{{dictionary_marked_elements[1, 6, 'top_right']}}}{{{dictionary_marked_elements[1, 6, 'bottom_left']}}}{{{dictionary_marked_elements[1, 6, 'bottom_right']}}}{{{self.grid[1][6]}}} & \\N{{{dictionary_marked_elements[1, 7, 'top_left']}}}{{{dictionary_marked_elements[1, 7, 'top_right']}}}{{{dictionary_marked_elements[1, 7, 'bottom_left']}}}{{{dictionary_marked_elements[1, 7, 'bottom_right']}}}{{{self.grid[1][7]}}} & \\N{{{dictionary_marked_elements[1, 8, 'top_left']}}}{{{dictionary_marked_elements[1, 8, 'top_right']}}}{{{dictionary_marked_elements[1, 8, 'bottom_left']}}}{{{dictionary_marked_elements[1, 8, 'bottom_right']}}}{{{self.grid[1][8]}}} \\\\ \\hline

% Line 3
\\N{{{dictionary_marked_elements[2, 0, 'top_left']}}}{{{dictionary_marked_elements[2, 0, 'top_right']}}}{{{dictionary_marked_elements[2, 0, 'bottom_left']}}}{{{dictionary_marked_elements[2, 0, 'bottom_right']}}}{{{self.grid[2][0]}}} & \\N{{{dictionary_marked_elements[2, 1, 'top_left']}}}{{{dictionary_marked_elements[2, 1, 'top_right']}}}{{{dictionary_marked_elements[2, 1, 'bottom_left']}}}{{{dictionary_marked_elements[2, 1, 'bottom_right']}}}{{{self.grid[2][1]}}} & \\N{{{dictionary_marked_elements[2, 2, 'top_left']}}}{{{dictionary_marked_elements[2, 2, 'top_right']}}}{{{dictionary_marked_elements[2, 2, 'bottom_left']}}}{{{dictionary_marked_elements[2, 2, 'bottom_right']}}}{{{self.grid[2][2]}}} &
\\N{{{dictionary_marked_elements[2, 3, 'top_left']}}}{{{dictionary_marked_elements[2, 3, 'top_right']}}}{{{dictionary_marked_elements[2, 3, 'bottom_left']}}}{{{dictionary_marked_elements[2, 3, 'bottom_right']}}}{{{self.grid[2][3]}}} & \\N{{{dictionary_marked_elements[2, 4, 'top_left']}}}{{{dictionary_marked_elements[2, 4, 'top_right']}}}{{{dictionary_marked_elements[2, 4, 'bottom_left']}}}{{{dictionary_marked_elements[2, 4, 'bottom_right']}}}{{{self.grid[2][4]}}} & \\N{{{dictionary_marked_elements[2, 5, 'top_left']}}}{{{dictionary_marked_elements[2, 5, 'top_right']}}}{{{dictionary_marked_elements[2, 5, 'bottom_left']}}}{{{dictionary_marked_elements[2, 5, 'bottom_right']}}}{{{self.grid[2][5]}}} &
\\N{{{dictionary_marked_elements[2, 6, 'top_left']}}}{{{dictionary_marked_elements[2, 6, 'top_right']}}}{{{dictionary_marked_elements[2, 6, 'bottom_left']}}}{{{dictionary_marked_elements[2, 6, 'bottom_right']}}}{{{self.grid[2][6]}}} & \\N{{{dictionary_marked_elements[2, 7, 'top_left']}}}{{{dictionary_marked_elements[2, 7, 'top_right']}}}{{{dictionary_marked_elements[2, 7, 'bottom_left']}}}{{{dictionary_marked_elements[2, 7, 'bottom_right']}}}{{{self.grid[2][7]}}} & \\N{{{dictionary_marked_elements[2, 8, 'top_left']}}}{{{dictionary_marked_elements[2, 8, 'top_right']}}}{{{dictionary_marked_elements[2, 8, 'bottom_left']}}}{{{dictionary_marked_elements[2, 8, 'bottom_right']}}}{{{self.grid[2][8]}}} \\\\ \\hline\\hline

% Line 4
\\N{{{dictionary_marked_elements[3, 0, 'top_left']}}}{{{dictionary_marked_elements[3, 0, 'top_right']}}}{{{dictionary_marked_elements[3, 0, 'bottom_left']}}}{{{dictionary_marked_elements[3, 0, 'bottom_right']}}}{{{self.grid[3][0]}}} & \\N{{{dictionary_marked_elements[3, 1, 'top_left']}}}{{{dictionary_marked_elements[3, 1, 'top_right']}}}{{{dictionary_marked_elements[3, 1, 'bottom_left']}}}{{{dictionary_marked_elements[3, 1, 'bottom_right']}}}{{{self.grid[3][1]}}} & \\N{{{dictionary_marked_elements[3, 2, 'top_left']}}}{{{dictionary_marked_elements[3, 2, 'top_right']}}}{{{dictionary_marked_elements[3, 2, 'bottom_left']}}}{{{dictionary_marked_elements[3, 2, 'bottom_right']}}}{{{self.grid[3][2]}}} &
\\N{{{dictionary_marked_elements[3, 3, 'top_left']}}}{{{dictionary_marked_elements[3, 3, 'top_right']}}}{{{dictionary_marked_elements[3, 3, 'bottom_left']}}}{{{dictionary_marked_elements[3, 3, 'bottom_right']}}}{{{self.grid[3][3]}}} & \\N{{{dictionary_marked_elements[3, 4, 'top_left']}}}{{{dictionary_marked_elements[3, 4, 'top_right']}}}{{{dictionary_marked_elements[3, 4, 'bottom_left']}}}{{{dictionary_marked_elements[3, 4, 'bottom_right']}}}{{{self.grid[3][4]}}} & \\N{{{dictionary_marked_elements[3, 5, 'top_left']}}}{{{dictionary_marked_elements[3, 5, 'top_right']}}}{{{dictionary_marked_elements[3, 5, 'bottom_left']}}}{{{dictionary_marked_elements[3, 5, 'bottom_right']}}}{{{self.grid[3][5]}}} &
\\N{{{dictionary_marked_elements[3, 6, 'top_left']}}}{{{dictionary_marked_elements[3, 6, 'top_right']}}}{{{dictionary_marked_elements[3, 6, 'bottom_left']}}}{{{dictionary_marked_elements[3, 6, 'bottom_right']}}}{{{self.grid[3][6]}}} & \\N{{{dictionary_marked_elements[3, 7, 'top_left']}}}{{{dictionary_marked_elements[3, 7, 'top_right']}}}{{{dictionary_marked_elements[3, 7, 'bottom_left']}}}{{{dictionary_marked_elements[3, 7, 'bottom_right']}}}{{{self.grid[3][7]}}} & \\N{{{dictionary_marked_elements[3, 8, 'top_left']}}}{{{dictionary_marked_elements[3, 8, 'top_right']}}}{{{dictionary_marked_elements[3, 8, 'bottom_left']}}}{{{dictionary_marked_elements[3, 8, 'bottom_right']}}}{{{self.grid[3][8]}}} \\\\ \\hline

% Line 5
\\N{{{dictionary_marked_elements[4, 0, 'top_left']}}}{{{dictionary_marked_elements[4, 0, 'top_right']}}}{{{dictionary_marked_elements[4, 0, 'bottom_left']}}}{{{dictionary_marked_elements[4, 0, 'bottom_right']}}}{{{self.grid[4][0]}}} & \\N{{{dictionary_marked_elements[4, 1, 'top_left']}}}{{{dictionary_marked_elements[4, 1, 'top_right']}}}{{{dictionary_marked_elements[4, 1, 'bottom_left']}}}{{{dictionary_marked_elements[4, 1, 'bottom_right']}}}{{{self.grid[4][1]}}} & \\N{{{dictionary_marked_elements[4, 2, 'top_left']}}}{{{dictionary_marked_elements[4, 2, 'top_right']}}}{{{dictionary_marked_elements[4, 2, 'bottom_left']}}}{{{dictionary_marked_elements[4, 2, 'bottom_right']}}}{{{self.grid[4][2]}}} &
\\N{{{dictionary_marked_elements[4, 3, 'top_left']}}}{{{dictionary_marked_elements[4, 3, 'top_right']}}}{{{dictionary_marked_elements[4, 3, 'bottom_left']}}}{{{dictionary_marked_elements[4, 3, 'bottom_right']}}}{{{self.grid[4][3]}}} & \\N{{{dictionary_marked_elements[4, 4, 'top_left']}}}{{{dictionary_marked_elements[4, 4, 'top_right']}}}{{{dictionary_marked_elements[4, 4, 'bottom_left']}}}{{{dictionary_marked_elements[4, 4, 'bottom_right']}}}{{{self.grid[4][4]}}} & \\N{{{dictionary_marked_elements[4, 5, 'top_left']}}}{{{dictionary_marked_elements[4, 5, 'top_right']}}}{{{dictionary_marked_elements[4, 5, 'bottom_left']}}}{{{dictionary_marked_elements[4, 5, 'bottom_right']}}}{{{self.grid[4][5]}}} &
\\N{{{dictionary_marked_elements[4, 6, 'top_left']}}}{{{dictionary_marked_elements[4, 6, 'top_right']}}}{{{dictionary_marked_elements[4, 6, 'bottom_left']}}}{{{dictionary_marked_elements[4, 6, 'bottom_right']}}}{{{self.grid[4][6]}}} & \\N{{{dictionary_marked_elements[4, 7, 'top_left']}}}{{{dictionary_marked_elements[4, 7, 'top_right']}}}{{{dictionary_marked_elements[4, 7, 'bottom_left']}}}{{{dictionary_marked_elements[4, 7, 'bottom_right']}}}{{{self.grid[4][7]}}} & \\N{{{dictionary_marked_elements[4, 8, 'top_left']}}}{{{dictionary_marked_elements[4, 8, 'top_right']}}}{{{dictionary_marked_elements[4, 8, 'bottom_left']}}}{{{dictionary_marked_elements[4, 8, 'bottom_right']}}}{{{self.grid[4][8]}}} \\\\ \\hline

% Line 6
\\N{{{dictionary_marked_elements[5, 0, 'top_left']}}}{{{dictionary_marked_elements[5, 0, 'top_right']}}}{{{dictionary_marked_elements[5, 0, 'bottom_left']}}}{{{dictionary_marked_elements[5, 0, 'bottom_right']}}}{{{self.grid[5][0]}}} & \\N{{{dictionary_marked_elements[5, 1, 'top_left']}}}{{{dictionary_marked_elements[5, 1, 'top_right']}}}{{{dictionary_marked_elements[5, 1, 'bottom_left']}}}{{{dictionary_marked_elements[5, 1, 'bottom_right']}}}{{{self.grid[5][1]}}} & \\N{{{dictionary_marked_elements[5, 2, 'top_left']}}}{{{dictionary_marked_elements[5, 2, 'top_right']}}}{{{dictionary_marked_elements[5, 2, 'bottom_left']}}}{{{dictionary_marked_elements[5, 2, 'bottom_right']}}}{{{self.grid[5][2]}}} &
\\N{{{dictionary_marked_elements[5, 3, 'top_left']}}}{{{dictionary_marked_elements[5, 3, 'top_right']}}}{{{dictionary_marked_elements[5, 3, 'bottom_left']}}}{{{dictionary_marked_elements[5, 3, 'bottom_right']}}}{{{self.grid[5][3]}}} & \\N{{{dictionary_marked_elements[5, 4, 'top_left']}}}{{{dictionary_marked_elements[5, 4, 'top_right']}}}{{{dictionary_marked_elements[5, 4, 'bottom_left']}}}{{{dictionary_marked_elements[5, 4, 'bottom_right']}}}{{{self.grid[5][4]}}} & \\N{{{dictionary_marked_elements[5, 5, 'top_left']}}}{{{dictionary_marked_elements[5, 5, 'top_right']}}}{{{dictionary_marked_elements[5, 5, 'bottom_left']}}}{{{dictionary_marked_elements[5, 5, 'bottom_right']}}}{{{self.grid[5][5]}}} &
\\N{{{dictionary_marked_elements[5, 6, 'top_left']}}}{{{dictionary_marked_elements[5, 6, 'top_right']}}}{{{dictionary_marked_elements[5, 6, 'bottom_left']}}}{{{dictionary_marked_elements[5, 6, 'bottom_right']}}}{{{self.grid[5][6]}}} & \\N{{{dictionary_marked_elements[5, 7, 'top_left']}}}{{{dictionary_marked_elements[5, 7, 'top_right']}}}{{{dictionary_marked_elements[5, 7, 'bottom_left']}}}{{{dictionary_marked_elements[5, 7, 'bottom_right']}}}{{{self.grid[5][7]}}} & \\N{{{dictionary_marked_elements[5, 8, 'top_left']}}}{{{dictionary_marked_elements[5, 8, 'top_right']}}}{{{dictionary_marked_elements[5, 8, 'bottom_left']}}}{{{dictionary_marked_elements[5, 8, 'bottom_right']}}}{{{self.grid[5][8]}}} \\\\ \\hline\\hline

% Line 7
\\N{{{dictionary_marked_elements[6, 0, 'top_left']}}}{{{dictionary_marked_elements[6, 0, 'top_right']}}}{{{dictionary_marked_elements[6, 0, 'bottom_left']}}}{{{dictionary_marked_elements[6, 0, 'bottom_right']}}}{{{self.grid[6][0]}}} & \\N{{{dictionary_marked_elements[6, 1, 'top_left']}}}{{{dictionary_marked_elements[6, 1, 'top_right']}}}{{{dictionary_marked_elements[6, 1, 'bottom_left']}}}{{{dictionary_marked_elements[6, 1, 'bottom_right']}}}{{{self.grid[6][1]}}} & \\N{{{dictionary_marked_elements[6, 2, 'top_left']}}}{{{dictionary_marked_elements[6, 2, 'top_right']}}}{{{dictionary_marked_elements[6, 2, 'bottom_left']}}}{{{dictionary_marked_elements[6, 2, 'bottom_right']}}}{{{self.grid[6][2]}}} &
\\N{{{dictionary_marked_elements[6, 3, 'top_left']}}}{{{dictionary_marked_elements[6, 3, 'top_right']}}}{{{dictionary_marked_elements[6, 3, 'bottom_left']}}}{{{dictionary_marked_elements[6, 3, 'bottom_right']}}}{{{self.grid[6][3]}}} & \\N{{{dictionary_marked_elements[6, 4, 'top_left']}}}{{{dictionary_marked_elements[6, 4, 'top_right']}}}{{{dictionary_marked_elements[6, 4, 'bottom_left']}}}{{{dictionary_marked_elements[6, 4, 'bottom_right']}}}{{{self.grid[6][4]}}} & \\N{{{dictionary_marked_elements[6, 5, 'top_left']}}}{{{dictionary_marked_elements[6, 5, 'top_right']}}}{{{dictionary_marked_elements[6, 5, 'bottom_left']}}}{{{dictionary_marked_elements[6, 5, 'bottom_right']}}}{{{self.grid[6][5]}}} &
\\N{{{dictionary_marked_elements[6, 6, 'top_left']}}}{{{dictionary_marked_elements[6, 6, 'top_right']}}}{{{dictionary_marked_elements[6, 6, 'bottom_left']}}}{{{dictionary_marked_elements[6, 6, 'bottom_right']}}}{{{self.grid[6][6]}}} & \\N{{{dictionary_marked_elements[6, 7, 'top_left']}}}{{{dictionary_marked_elements[6, 7, 'top_right']}}}{{{dictionary_marked_elements[6, 7, 'bottom_left']}}}{{{dictionary_marked_elements[6, 7, 'bottom_right']}}}{{{self.grid[6][7]}}} & \\N{{{dictionary_marked_elements[6, 8, 'top_left']}}}{{{dictionary_marked_elements[6, 8, 'top_right']}}}{{{dictionary_marked_elements[6, 8, 'bottom_left']}}}{{{dictionary_marked_elements[6, 8, 'bottom_right']}}}{{{self.grid[6][8]}}} \\\\ \\hline

% Line 8
\\N{{{dictionary_marked_elements[7, 0, 'top_left']}}}{{{dictionary_marked_elements[7, 0, 'top_right']}}}{{{dictionary_marked_elements[7, 0, 'bottom_left']}}}{{{dictionary_marked_elements[7, 0, 'bottom_right']}}}{{{self.grid[7][0]}}} & \\N{{{dictionary_marked_elements[7, 1, 'top_left']}}}{{{dictionary_marked_elements[7, 1, 'top_right']}}}{{{dictionary_marked_elements[7, 1, 'bottom_left']}}}{{{dictionary_marked_elements[7, 1, 'bottom_right']}}}{{{self.grid[7][1]}}} & \\N{{{dictionary_marked_elements[7, 2, 'top_left']}}}{{{dictionary_marked_elements[7, 2, 'top_right']}}}{{{dictionary_marked_elements[7, 2, 'bottom_left']}}}{{{dictionary_marked_elements[7, 2, 'bottom_right']}}}{{{self.grid[7][2]}}} &
\\N{{{dictionary_marked_elements[7, 3, 'top_left']}}}{{{dictionary_marked_elements[7, 3, 'top_right']}}}{{{dictionary_marked_elements[7, 3, 'bottom_left']}}}{{{dictionary_marked_elements[7, 3, 'bottom_right']}}}{{{self.grid[7][3]}}} & \\N{{{dictionary_marked_elements[7, 4, 'top_left']}}}{{{dictionary_marked_elements[7, 4, 'top_right']}}}{{{dictionary_marked_elements[7, 4, 'bottom_left']}}}{{{dictionary_marked_elements[7, 4, 'bottom_right']}}}{{{self.grid[7][4]}}} & \\N{{{dictionary_marked_elements[7, 5, 'top_left']}}}{{{dictionary_marked_elements[7, 5, 'top_right']}}}{{{dictionary_marked_elements[7, 5, 'bottom_left']}}}{{{dictionary_marked_elements[7, 5, 'bottom_right']}}}{{{self.grid[7][5]}}} &
\\N{{{dictionary_marked_elements[7, 6, 'top_left']}}}{{{dictionary_marked_elements[7, 6, 'top_right']}}}{{{dictionary_marked_elements[7, 6, 'bottom_left']}}}{{{dictionary_marked_elements[7, 6, 'bottom_right']}}}{{{self.grid[7][6]}}} & \\N{{{dictionary_marked_elements[7, 7, 'top_left']}}}{{{dictionary_marked_elements[7, 7, 'top_right']}}}{{{dictionary_marked_elements[7, 7, 'bottom_left']}}}{{{dictionary_marked_elements[7, 7, 'bottom_right']}}}{{{self.grid[7][7]}}} & \\N{{{dictionary_marked_elements[7, 8, 'top_left']}}}{{{dictionary_marked_elements[7, 8, 'top_right']}}}{{{dictionary_marked_elements[7, 8, 'bottom_left']}}}{{{dictionary_marked_elements[7, 8, 'bottom_right']}}}{{{self.grid[7][8]}}} \\\\ \\hline

% Line 9
\\N{{{dictionary_marked_elements[8, 0, 'top_left']}}}{{{dictionary_marked_elements[8, 0, 'top_right']}}}{{{dictionary_marked_elements[8, 0, 'bottom_left']}}}{{{dictionary_marked_elements[8, 0, 'bottom_right']}}}{{{self.grid[8][0]}}} & \\N{{{dictionary_marked_elements[8, 1, 'top_left']}}}{{{dictionary_marked_elements[8, 1, 'top_right']}}}{{{dictionary_marked_elements[8, 1, 'bottom_left']}}}{{{dictionary_marked_elements[8, 1, 'bottom_right']}}}{{{self.grid[8][1]}}} & \\N{{{dictionary_marked_elements[8, 2, 'top_left']}}}{{{dictionary_marked_elements[8, 2, 'top_right']}}}{{{dictionary_marked_elements[8, 2, 'bottom_left']}}}{{{dictionary_marked_elements[8, 2, 'bottom_right']}}}{{{self.grid[8][2]}}} &
\\N{{{dictionary_marked_elements[8, 3, 'top_left']}}}{{{dictionary_marked_elements[8, 3, 'top_right']}}}{{{dictionary_marked_elements[8, 3, 'bottom_left']}}}{{{dictionary_marked_elements[8, 3, 'bottom_right']}}}{{{self.grid[8][3]}}} & \\N{{{dictionary_marked_elements[8, 4, 'top_left']}}}{{{dictionary_marked_elements[8, 4, 'top_right']}}}{{{dictionary_marked_elements[8, 4, 'bottom_left']}}}{{{dictionary_marked_elements[8, 4, 'bottom_right']}}}{{{self.grid[8][4]}}} & \\N{{{dictionary_marked_elements[8, 5, 'top_left']}}}{{{dictionary_marked_elements[8, 5, 'top_right']}}}{{{dictionary_marked_elements[8, 5, 'bottom_left']}}}{{{dictionary_marked_elements[8, 5, 'bottom_right']}}}{{{self.grid[8][5]}}} &
\\N{{{dictionary_marked_elements[8, 6, 'top_left']}}}{{{dictionary_marked_elements[8, 6, 'top_right']}}}{{{dictionary_marked_elements[8, 6, 'bottom_left']}}}{{{dictionary_marked_elements[8, 6, 'bottom_right']}}}{{{self.grid[8][6]}}} & \\N{{{dictionary_marked_elements[8, 7, 'top_left']}}}{{{dictionary_marked_elements[8, 7, 'top_right']}}}{{{dictionary_marked_elements[8, 7, 'bottom_left']}}}{{{dictionary_marked_elements[8, 7, 'bottom_right']}}}{{{self.grid[8][7]}}} & \\N{{{dictionary_marked_elements[8, 8, 'top_left']}}}{{{dictionary_marked_elements[8, 8, 'top_right']}}}{{{dictionary_marked_elements[8, 8, 'bottom_left']}}}{{{dictionary_marked_elements[8, 8, 'bottom_right']}}}{{{self.grid[8][8]}}} \\\\ \\hline\\hline
\\end{{tabular}}
\\end{{center}}

\\end{{document}}
"""

            file.write(latex_text_as_raw_string)

    def worked_tex_output(self):
        ## Start at a cell
        ## Go with the order of checking row first, then column, then box ... for preemptive elements and cells ... just because I dont want to waste time any further . In lecture, Eric showed examples of row checking first. I will try to stick to that order and hope it works.
        ## First look at row for preemptive sets. n elements of n cells  .. with n>2 and n = n i.e. number of preemptive elements and number of cells having those preemptive elements or subsets of those preemptive elements
        ## A cell in the preemptive set can have just 1 possible element also. e.g. 3 cells of preemptive set {2,4,9} can have possible elements (2,4), (2,9) and (9). Note the (9) in that cell i.e. just 1 possible element allowed.
        ## remove the elements of preemptive sets in all OTHER boxes of the row. i.e. make sure you dont remove elements in the preemptive cells.
        ## Give \cancel in string to strike out elements in latex
        ## At every cancellation , check IF only 1 possible element in a cell. If so, fill that cell with that number.
        ## Then, you can remove that number in the possible elements of all cells in the column of that cell (THE CELL NOT IN PREEMPTIVE SET), row of that cell and box of that cell.
        ## Stop the whole loop operation until the latest self.grid is same as the self.grid in the previous operation i.e. unable to strike off elements in whole self.grid anymore.                 
        
        def box(a,b):
            all_cell_positions_of_a_box=[]
            cell_postitions_list_having_possible_elements_in_a_box=[]
            for i in range(a-1,a+2): ##For statement syntax exludes a+2 i.e. upto a+1 only
                for j in range(b-1,b+2):
                    all_cell_positions_of_a_box.append([i,j])
                    if self.grid[i][j]== "":   ##Cell doesnt already have a number
                        cell_postitions_list_having_possible_elements_in_a_box.append([i,j])
            preemptive_set_positions_list_in_box=[]
            preemptive_elements_in_box=[]
            for n in range(2,len(cell_postitions_list_having_possible_elements_in_a_box)): ##Minimum 2 cells in preemptive set
                set_of_combinations = itertools.combinations(cell_postitions_list_having_possible_elements_in_a_box, n) ## Order of elements doesnt matter in combinations. Hence number of output is lesser than in permutations. 6C2+6C3+6C4+6C5 = 56 for 1st box in sudoku_4 ##combinations i.e. permutations and combinations maths
                for s in set_of_combinations:
                    preemptive_set_or_not_check=" " #Just initializing it as a string
                    for h in s:
                        ##print(self.dictionary_marked_elements[h[0],h[1],"top_left"], self.dictionary_marked_elements[h[0],h[1],"top_right"], self.dictionary_marked_elements[h[0],h[1],"bottom_left"], self.dictionary_marked_elements[h[0],h[1],"bottom_right"] )
                        preemptive_set_or_not_check += re.sub(r'/cancel\d+\s', '', self.dictionary_marked_elements[h[0],h[1],"top_left"]) + re.sub(r'/cancel\d+\s', '', self.dictionary_marked_elements[h[0],h[1],"top_right"]) + re.sub(r'/cancel\d+\s', '', self.dictionary_marked_elements[h[0],h[1],"bottom_left"]) + re.sub(r'/cancel\d+\s', '', self.dictionary_marked_elements[h[0],h[1],"bottom_right"]) 
                        ##print(preemptive_set_or_not_check)
                        ## preemptive_set_or_not_check += self.dictionary_marked_elements[h[0],h[1],"top_left"] + self.dictionary_marked_elements[h[0],h[1],"top_right"] + self.dictionary_marked_elements[h[0],h[1],"bottom_left"] + self.dictionary_marked_elements[h[0],h[1],"bottom_right"]  ## This h[0] and h[1] is necessary to get the i and j of a position as it is in a list e.g.[0,1]
                        #Preemptive_set_or_not_check is a string and will have SPACES because of join operation on e.g. line 383
                        preemptive_set_or_not_check=list(set([x for x in preemptive_set_or_not_check if x!=" "]))
                        if len(preemptive_set_or_not_check) == len(s):
                            preemptive_set_positions_list_in_box = list(s)
                            preemptive_elements_in_box=sorted(preemptive_set_or_not_check)   ##Set function in line 511 doesnot sort.
                            ##print(all_cell_positions_of_a_box)
                            ##print(preemptive_set_positions_list_in_box) 
                            ##print(preemptive_elements_in_box)         ##This will give the last values in set of combinations and preemptive_check_or_not. Even if there may be multiple possible preemptive sets and elements, its unnecessary to choose one. Eric said so "Will the order of finding preemptive sets in ... row, column, box .. matter ?" "If you think about it, you will see the order does not matter; you just do not want to miss any" . As most sudoku have unique solution.
                            ##Now our aim is to remove the preemptive elements from cells other than the preemptive_set_positions_list_in_box
                            # Convert inner lists to tuples, because its a list of lists. Inner lists are not hashable or some bullshit.
                            all_cell_positions_of_a_box = [tuple(pos) for pos in all_cell_positions_of_a_box]
                            all_cell_positions_of_a_box = set(all_cell_positions_of_a_box)
                            preemptive_set_positions_list_in_box = [tuple(pos) for pos in preemptive_set_positions_list_in_box]
                            preemptive_set_positions_list_in_box = set(preemptive_set_positions_list_in_box)
                            other_cell_positions_of_a_box=all_cell_positions_of_a_box - preemptive_set_positions_list_in_box    ##only set can have addition , subtraction operations. Lists cant do that.
                            ##print(other_cell_positions_of_a_box)
                            ## print(preemptive_set_positions_list_in_box)
                        ## A Set in Python is iterable
                            for i,j in other_cell_positions_of_a_box:
                                for k in preemptive_elements_in_box:
                                    ##Now we remove the elements in the position stored in variable k
                                    ## TAKE NOTE OF THE R-STRING
                                    if self.grid[i][j]=="": ## Unnecessary because any cells which have all possible elements cancelled as checked in the below if statements wont be processed. But still I am doing it for clarity and to reduce execution time in Eric's computer.
                                        if k in self.dictionary_marked_elements[i,j,"top_left"]: 
                                            if fr"\cancel{k}" not in self.dictionary_marked_elements[i,j,"top_left"]:  #i.e. Not already cancelled
                                                self.dictionary_marked_elements[i,j,"top_left"] = self.dictionary_marked_elements[i,j,"top_left"].replace(k, fr"\cancel{k}") ## Output will be like '\\cancel2' i.e. will have 2 backslashes which is necessary in Latex to escape backslash
                                                matches = re.findall(r'\b(?<!\\cancel)\d+\b',  self.dictionary_marked_elements[i,j,"top_left"] + " " + self.dictionary_marked_elements[i,j,"top_right"] + " " + self.dictionary_marked_elements[i,j,"bottom_left"] + " " + self.dictionary_marked_elements[i,j,"bottom_right"])  ##Every digit except cancelled.
                                                if len(matches)==1:
                                                    self.grid[i][j]=int(matches[0]) ##That is only 1 non-cancel digit left, then that digit would become the number in the cell                                                                                                    
                                                    rows(i)
                                                    columns(j)
                                                    if i<3: 
                                                        if j<3:
                                                            a,b=1,1
                                                        if j>2 and j<6:
                                                            a,b=1,4 
                                                        if j>5:
                                                            a,b=1,7
                                                    elif i>2 and i<6:
                                                        if j<3:
                                                            a,b=4,1
                                                        if j>2 and j<6:
                                                            a,b=4,4 
                                                        if j>5:
                                                            a,b=4,7
                                                    elif i>5 and i<10:
                                                        if j<3:
                                                            a,b=7,1
                                                        if j>2 and j<6:
                                                            a,b=7,4 
                                                        if j>5:
                                                            a,b=7,7
                                                    box(a,b)
                                        if k in self.dictionary_marked_elements[i,j,"top_right"]: 
                                            if fr"\cancel{k}" not in self.dictionary_marked_elements[i,j,"top_right"]:
                                                self.dictionary_marked_elements[i,j,"top_right"] = self.dictionary_marked_elements[i,j,"top_right"].replace(k, fr"\cancel{k}")
                                                matches = re.findall(r'\b(?<!\\cancel)\d+\b',  self.dictionary_marked_elements[i,j,"top_left"] + " " + self.dictionary_marked_elements[i,j,"top_right"] + " " + self.dictionary_marked_elements[i,j,"bottom_left"] + " " + self.dictionary_marked_elements[i,j,"bottom_right"])  ##Every digit except cancelled.
                                                if len(matches)==1:
                                                    self.grid[i][j]=int(matches[0])
                                                    rows(i)
                                                    columns(j)
                                                    if i<3: 
                                                        if j<3:
                                                            a,b=1,1
                                                        if j>2 and j<6:
                                                            a,b=1,4 
                                                        if j>5:
                                                            a,b=1,7
                                                    elif i>2 and i<6:
                                                        if j<3:
                                                            a,b=4,1
                                                        if j>2 and j<6:
                                                            a,b=4,4 
                                                        if j>5:
                                                            a,b=4,7
                                                    elif i>5 and i<10:
                                                        if j<3:
                                                            a,b=7,1
                                                        if j>2 and j<6:
                                                            a,b=7,4 
                                                        if j>5:
                                                            a,b=7,7
                                                    box(a,b)
                                        if k in self.dictionary_marked_elements[i,j,"bottom_left"]: 
                                            if fr"\cancel{k}" not in self.dictionary_marked_elements[i,j,"bottom_left"]:
                                                self.dictionary_marked_elements[i,j,"bottom_left"] = self.dictionary_marked_elements[i,j,"top_left"].replace(k, fr"\cancel{k}")
                                                matches = re.findall(r'\b(?<!\\cancel)\d+\b',  self.dictionary_marked_elements[i,j,"top_left"] + " " + self.dictionary_marked_elements[i,j,"top_right"] + " " + self.dictionary_marked_elements[i,j,"bottom_left"] + " " + self.dictionary_marked_elements[i,j,"bottom_right"])  ##Every digit except cancelled.
                                                if len(matches)==1:
                                                    self.grid[i][j]=int(matches[0])                    
                                                    rows(i)
                                                    columns(j)
                                                    if i<3: 
                                                        if j<3:
                                                            a,b=1,1
                                                        if j>2 and j<6:
                                                            a,b=1,4 
                                                        if j>5:
                                                            a,b=1,7
                                                    elif i>2 and i<6:
                                                        if j<3:
                                                            a,b=4,1
                                                        if j>2 and j<6:
                                                            a,b=4,4 
                                                        if j>5:
                                                            a,b=4,7
                                                    elif i>5 and i<10:
                                                        if j<3:
                                                            a,b=7,1
                                                        if j>2 and j<6:
                                                            a,b=7,4 
                                                        if j>5:
                                                            a,b=7,7
                                                    box(a,b)
                                        if k in self.dictionary_marked_elements[i,j,"bottom_right"]: 
                                            if fr"\cancel{k}" not in self.dictionary_marked_elements[i,j,"bottom_right"]:
                                                self.dictionary_marked_elements[i,j,"bottom_right"] = self.dictionary_marked_elements[i,j,"bottom_right"].replace(k, fr"\cancel{k}")
                                                matches = re.findall(r'\b(?<!\\cancel)\d+\b',  self.dictionary_marked_elements[i,j,"top_left"] + " " + self.dictionary_marked_elements[i,j,"top_right"] + " " + self.dictionary_marked_elements[i,j,"bottom_left"] + " " + self.dictionary_marked_elements[i,j,"bottom_right"])  ##Every digit except cancelled.
                                                if len(matches)==1:
                                                    self.grid[i][j]=int(matches[0])
                                                    rows(i)
                                                    columns(j)
                                                    if i<3: 
                                                        if j<3:
                                                            a,b=1,1
                                                        if j>2 and j<6:
                                                            a,b=1,4 
                                                        if j>5:
                                                            a,b=1,7
                                                    elif i>2 and i<6:
                                                        if j<3:
                                                            a,b=4,1
                                                        if j>2 and j<6:
                                                            a,b=4,4 
                                                        if j>5:
                                                            a,b=4,7
                                                    elif i>5 and i<10:
                                                        if j<3:
                                                            a,b=7,1
                                                        if j>2 and j<6:
                                                            a,b=7,4 
                                                        if j>5:
                                                            a,b=7,7
                                                    box(a,b)
            
        def rows(c):
            ## Checking rows
            for f in range(1):   ##Centre element of a 3X3 row i.e. (i,j) = (1,1) or (1,4) or (1,7) or (4,1) or (4,4) or (4,7) or (7,1) or (7,4) or (7,7)
                for j in range(9):
                    all_cell_positions_of_a_row=[]
                    cell_postitions_list_having_possible_elements_in_a_row=[] ##Storing all the elements in a row. Now reinitializing it to empty list before start of next row.
                    all_cell_positions_of_a_row.append([c,j])
                    if self.grid[c][j]== "":   ##Cell doesnt already have a number
                        cell_postitions_list_having_possible_elements_in_a_row.append([c,j])
                preemptive_set_positions_list_in_row=[]
                preemptive_elements_in_row=[]
                for n in range(2,len(cell_postitions_list_having_possible_elements_in_a_row)): ##Minimum 2 cells in preemptive set
                    set_of_combinations = itertools.combinations(cell_postitions_list_having_possible_elements_in_a_row, n) ## Order of elements doesnt matter in combinations. Hence number of output is lesser than in permutations. 6C2+6C3+6C4+6C5 = 56 for 1st row in sudoku_4 ##combinations i.e. permutations and combinations maths
                    for s in set_of_combinations:
                        preemptive_set_or_not_check=" " #Just initializing it as a string
                        for h in s:
                            preemptive_set_or_not_check += re.sub(r'/cancel\d+\s', '', self.dictionary_marked_elements[h[0],h[1],"top_left"]) + re.sub(r'/cancel\d+\s', '', self.dictionary_marked_elements[h[0],h[1],"top_right"]) + re.sub(r'/cancel\d+\s', '', self.dictionary_marked_elements[h[0],h[1],"bottom_left"]) + re.sub(r'/cancel\d+\s', '', self.dictionary_marked_elements[h[0],h[1],"bottom_right"]) 

                            ##preemptive_set_or_not_check += self.dictionary_marked_elements[h[0],h[1],"top_left"] + self.dictionary_marked_elements[h[0],h[1],"top_right"] + self.dictionary_marked_elements[h[0],h[1],"bottom_left"] + self.dictionary_marked_elements[h[0],h[1],"bottom_right"]  ## This h[0] and h[1] is necessary to get the i and j of a position as it is in a list e.g.[0,1]
                            #Preemptive_set_or_not_check is a string and will have SPACES because of join operation on e.g. line 383
                            preemptive_set_or_not_check=list(set([x for x in preemptive_set_or_not_check if x!=" "]))
                            if len(preemptive_set_or_not_check) == len(s):
                                preemptive_set_positions_list_in_row = list(s)
                                preemptive_elements_in_row=sorted(preemptive_set_or_not_check)   ##Set function in line 511 doesnot sort.
                                ##print(all_cell_positions_of_a_row)
                                ##print(preemptive_set_positions_list_in_row) 
                            ##print(preemptive_elements_in_row)         ##This will give the last values in set of combinations and preemptive_check_or_not. Even if there may be multiple possible preemptive sets and elements, its unnecessary to choose one. Eric said so "Will the order of finding preemptive sets in ... row, column, row .. matter ?" "If you think about it, you will see the order does not matter; you just do not want to miss any" . As most sudoku have unique solution.
                                ##Now our aim is to remove the preemptive elements from cells other than the preemptive_set_positions_list_in_row
                                # Convert inner lists to tuples, because its a list of lists. Inner lists are not hashable or some bullshit.
                                all_cell_positions_of_a_row = [tuple(pos) for pos in all_cell_positions_of_a_row]
                                all_cell_positions_of_a_row = set(all_cell_positions_of_a_row)
                                preemptive_set_positions_list_in_row = [tuple(pos) for pos in preemptive_set_positions_list_in_row]
                                preemptive_set_positions_list_in_row = set(preemptive_set_positions_list_in_row)
                                other_cell_positions_of_a_row=all_cell_positions_of_a_row - preemptive_set_positions_list_in_row    ##only set can have addition , subtraction operations. Lists cant do that.
                                ##print(other_cell_positions_of_a_row)
                            ##print(preemptive_set_positions_list_in_row
                            ## A Set in Python is iterable
                                for i,j in other_cell_positions_of_a_row:
                                    for k in preemptive_elements_in_row:
                                        ##Now we remove the elements in the position stored in variable k
                                        ## TAKE NOTE OF THE R-STRING
                                        if self.grid[i][j]=="": ## Unnecessary because any cells which have all possible elements cancelled as checked in the below if statements wont be processed. But still I am doing it for clarity and to reduce execution time in Eric's computer.
                                            if k in self.dictionary_marked_elements[i,j,"top_left"]: 
                                                if fr"\cancel{k}" not in self.dictionary_marked_elements[i,j,"top_left"]:  #i.e. Not already cancelled
                                                    self.dictionary_marked_elements[i,j,"top_left"] = self.dictionary_marked_elements[i,j,"top_left"].replace(k, fr"\cancel{k}") ## Output will be like '\\cancel2' i.e. will have 2 backslashes which is necessary in Latex to escape backslash
                                                    matches = re.findall(r'\b(?<!\\cancel)\d+\b',  self.dictionary_marked_elements[i,j,"top_left"] + " " + self.dictionary_marked_elements[i,j,"top_right"] + " " + self.dictionary_marked_elements[i,j,"bottom_left"] + " " + self.dictionary_marked_elements[i,j,"bottom_right"])  ##Every digit except cancelled.
                                                    if len(matches)==1:
                                                        self.grid[i][j]=int(matches[0]) ##That is only 1 non-cancel digit left, then that digit would become the number in the cell
                                                        rows(i)
                                                        columns(j)
                                                        if i<3: 
                                                            if j<3:
                                                                a,b=1,1
                                                            if j>2 and j<6:
                                                                a,b=1,4 
                                                            if j>5:
                                                                a,b=1,7
                                                        elif i>2 and i<6:
                                                            if j<3:
                                                                a,b=4,1
                                                            if j>2 and j<6:
                                                                a,b=4,4 
                                                            if j>5:
                                                                a,b=4,7
                                                        elif i>5 and i<10:
                                                            if j<3:
                                                                a,b=7,1
                                                            if j>2 and j<6:
                                                                a,b=7,4 
                                                            if j>5:
                                                                a,b=7,7
                                                        box(a,b)
                                            if k in self.dictionary_marked_elements[i,j,"top_right"]: 
                                                if fr"\cancel{k}" not in self.dictionary_marked_elements[i,j,"top_right"]:
                                                    self.dictionary_marked_elements[i,j,"top_right"] = self.dictionary_marked_elements[i,j,"top_right"].replace(k, fr"\cancel{k}")
                                                    matches = re.findall(r'\b(?<!\\cancel)\d+\b',  self.dictionary_marked_elements[i,j,"top_left"] + " " + self.dictionary_marked_elements[i,j,"top_right"] + " " + self.dictionary_marked_elements[i,j,"bottom_left"] + " " + self.dictionary_marked_elements[i,j,"bottom_right"])  ##Every digit except cancelled.
                                                    if len(matches)==1:
                                                        self.grid[i][j]=int(matches[0])
                                                        rows(i)
                                                        columns(j)
                                                        if i<3: 
                                                            if j<3:
                                                                a,b=1,1
                                                            if j>2 and j<6:
                                                                a,b=1,4 
                                                            if j>5:
                                                                a,b=1,7
                                                        elif i>2 and i<6:
                                                            if j<3:
                                                                a,b=4,1
                                                            if j>2 and j<6:
                                                                a,b=4,4 
                                                            if j>5:
                                                                a,b=4,7
                                                        elif i>5 and i<10:
                                                            if j<3:
                                                                a,b=7,1
                                                            if j>2 and j<6:
                                                                a,b=7,4 
                                                            if j>5:
                                                                a,b=7,7
                                                        box(a,b)
                                            if k in self.dictionary_marked_elements[i,j,"bottom_left"]: 
                                                if fr"\cancel{k}" not in self.dictionary_marked_elements[i,j,"bottom_left"]:
                                                    self.dictionary_marked_elements[i,j,"bottom_left"] = self.dictionary_marked_elements[i,j,"top_left"].replace(k, fr"\cancel{k}")
                                                    matches = re.findall(r'\b(?<!\\cancel)\d+\b',  self.dictionary_marked_elements[i,j,"top_left"] + " " + self.dictionary_marked_elements[i,j,"top_right"] + " " + self.dictionary_marked_elements[i,j,"bottom_left"] + " " + self.dictionary_marked_elements[i,j,"bottom_right"])  ##Every digit except cancelled.
                                                    if len(matches)==1:
                                                        self.grid[i][j]=int(matches[0])                    
                                                        rows(i)
                                                        columns(j)
                                                        if i<3: 
                                                            if j<3:
                                                                a,b=1,1
                                                            if j>2 and j<6:
                                                                a,b=1,4 
                                                            if j>5:
                                                                a,b=1,7
                                                        elif i>2 and i<6:
                                                            if j<3:
                                                                a,b=4,1
                                                            if j>2 and j<6:
                                                                a,b=4,4 
                                                            if j>5:
                                                                a,b=4,7
                                                        elif i>5 and i<10:
                                                            if j<3:
                                                                a,b=7,1
                                                            if j>2 and j<6:
                                                                a,b=7,4 
                                                            if j>5:
                                                                a,b=7,7
                                                        box(a,b)
                                            if k in self.dictionary_marked_elements[i,j,"bottom_right"]: 
                                                if fr"\cancel{k}" not in self.dictionary_marked_elements[i,j,"bottom_right"]:
                                                    self.dictionary_marked_elements[i,j,"bottom_right"] = self.dictionary_marked_elements[i,j,"bottom_right"].replace(k, fr"\cancel{k}")
                                                    matches = re.findall(r'\b(?<!\\cancel)\d+\b',  self.dictionary_marked_elements[i,j,"top_left"] + " " + self.dictionary_marked_elements[i,j,"top_right"] + " " + self.dictionary_marked_elements[i,j,"bottom_left"] + " " + self.dictionary_marked_elements[i,j,"bottom_right"])  ##Every digit except cancelled.
                                                    if len(matches)==1:
                                                        self.grid[i][j]=int(matches[0])
                                                        rows(i)
                                                        columns(j)
                                                        if i<3: 
                                                            if j<3:
                                                                a,b=1,1
                                                            if j>2 and j<6:
                                                                a,b=1,4 
                                                            if j>5:
                                                                a,b=1,7
                                                        elif i>2 and i<6:
                                                            if j<3:
                                                                a,b=4,1
                                                            if j>2 and j<6:
                                                                a,b=4,4 
                                                            if j>5:
                                                                a,b=4,7
                                                        elif i>5 and i<10:
                                                            if j<3:
                                                                a,b=7,1
                                                            if j>2 and j<6:
                                                                a,b=7,4 
                                                            if j>5:
                                                                a,b=7,7
                                                        box(a,b)
                                        
        def columns(d):
            ## Checking columns
            for g in range(1):   ##Centre element of a 3X3 column i.e. (i,j) = (1,1) or (1,4) or (1,7) or (4,1) or (4,4) or (4,7) or (7,1) or (7,4) or (7,7)
                for i in range(9):
                    all_cell_positions_of_a_column=[]
                    cell_postitions_list_having_possible_elements_in_a_column=[] ##Storing all the elements in a column. Now reinitializing it to empty list before start of next column.
                    all_cell_positions_of_a_column.append([i,d])
                    if self.grid[i][d]== "":   ##Cell doesnt already have a number
                        cell_postitions_list_having_possible_elements_in_a_column.append([i,d])
                preemptive_set_positions_list_in_column=[]
                preemptive_elements_in_column=[]
                for n in range(2,len(cell_postitions_list_having_possible_elements_in_a_column)): ##Minimum 2 cells in preemptive set
                    set_of_combinations = itertools.combinations(cell_postitions_list_having_possible_elements_in_a_column, n) ## Order of elements doesnt matter in combinations. Hence number of output is lesser than in permutations. 6C2+6C3+6C4+6C5 = 56 for 1st column in sudoku_4 ##combinations i.e. permutations and combinations maths
                    for s in set_of_combinations:
                        preemptive_set_or_not_check=" " #Just initializing it as a string
                        for h in s:
                            preemptive_set_or_not_check += re.sub(r'/cancel\d+\s', '', self.dictionary_marked_elements[h[0],h[1],"top_left"]) + re.sub(r'/cancel\d+\s', '', self.dictionary_marked_elements[h[0],h[1],"top_right"]) + re.sub(r'/cancel\d+\s', '', self.dictionary_marked_elements[h[0],h[1],"bottom_left"]) + re.sub(r'/cancel\d+\s', '', self.dictionary_marked_elements[h[0],h[1],"bottom_right"]) 
                            ##preemptive_set_or_not_check += self.dictionary_marked_elements[h[0],h[1],"top_left"] + self.dictionary_marked_elements[h[0],h[1],"top_right"] + self.dictionary_marked_elements[h[0],h[1],"bottom_left"] + self.dictionary_marked_elements[h[0],h[1],"bottom_right"]  ## This h[0] and h[1] is necessary to get the i and j of a position as it is in a list e.g.[0,1]
                            #Preemptive_set_or_not_check is a string and will have SPACES because of join operation on e.g. line 383
                            preemptive_set_or_not_check=list(set([x for x in preemptive_set_or_not_check if x!=" "]))
                            if len(preemptive_set_or_not_check) == len(s):
                                preemptive_set_positions_list_in_column = list(s)
                                preemptive_elements_in_column=sorted(preemptive_set_or_not_check)   ##Set function in line 511 doesnot sort.
                                ##print(all_cell_positions_of_a_column)
                                ##print(preemptive_set_positions_list_in_column) 
                            ##print(preemptive_elements_in_column)         ##This will give the last values in set of combinations and preemptive_check_or_not. Even if there may be multiple possible preemptive sets and elements, its unnecessary to choose one. Eric said so "Will the order of finding preemptive sets in ... column, column, column .. matter ?" "If you think about it, you will see the order does not matter; you just do not want to miss any" . As most sudoku have unique solution.
                                ##Now our aim is to remove the preemptive elements from cells other than the preemptive_set_positions_list_in_column
                                # Convert inner lists to tuples, because its a list of lists. Inner lists are not hashable or some bullshit.
                                all_cell_positions_of_a_column = [tuple(pos) for pos in all_cell_positions_of_a_column]
                                all_cell_positions_of_a_column = set(all_cell_positions_of_a_column)
                                preemptive_set_positions_list_in_column = [tuple(pos) for pos in preemptive_set_positions_list_in_column]
                                preemptive_set_positions_list_in_column = set(preemptive_set_positions_list_in_column)
                                other_cell_positions_of_a_column=all_cell_positions_of_a_column - preemptive_set_positions_list_in_column    ##only set can have addition , subtraction operations. Lists cant do that.
                                ##print(other_cell_positions_of_a_column)
                            ##print(preemptive_set_positions_list_in_column
                            ## A Set in Python is iterable
                                for i,j in other_cell_positions_of_a_column: ## No need to change order of i,j to j,i because its not index for for-loop. Its the values of the other_cell_positions_in_a_column_list
                                    for k in preemptive_elements_in_column:
                                        ##Now we remove the elements in the position stored in variable k
                                        ## TAKE NOTE OF THE R-STRING
                                        if self.grid[i][j]=="": ## Unnecessary because any cells which have all possible elements cancelled as checked in the below if statements wont be processed. But still I am doing it for clarity and to reduce execution time in Eric's computer.
                                            if k in self.dictionary_marked_elements[i,j,"top_left"]: 
                                                if fr"\cancel{k}" not in self.dictionary_marked_elements[i,j,"top_left"]:  #i.e. Not already cancelled
                                                    self.dictionary_marked_elements[i,j,"top_left"] = self.dictionary_marked_elements[i,j,"top_left"].replace(k, fr"\cancel{k}") ## Output will be like '\\cancel2' i.e. will have 2 backslashes which is necessary in Latex to escape backslash
                                                    matches = re.findall(r'\b(?<!\\cancel)\d+\b',  self.dictionary_marked_elements[i,j,"top_left"] + " " + self.dictionary_marked_elements[i,j,"top_right"] + " " + self.dictionary_marked_elements[i,j,"bottom_left"] + " " + self.dictionary_marked_elements[i,j,"bottom_right"])  ##Every digit except cancelled.
                                                    if len(matches)==1:
                                                        self.grid[i][j]=int(matches[0]) ##That is only 1 non-cancel digit left, then that digit would become the number in the cell
                                                        rows(i)
                                                        columns(j)
                                                        if i<3: 
                                                            if j<3:
                                                                a,b=1,1
                                                            if j>2 and j<6:
                                                                a,b=1,4 
                                                            if j>5:
                                                                a,b=1,7
                                                        elif i>2 and i<6:
                                                            if j<3:
                                                                a,b=4,1
                                                            if j>2 and j<6:
                                                                a,b=4,4 
                                                            if j>5:
                                                                a,b=4,7
                                                        elif i>5 and i<10:
                                                            if j<3:
                                                                a,b=7,1
                                                            if j>2 and j<6:
                                                                a,b=7,4 
                                                            if j>5:
                                                                a,b=7,7
                                                        box(a,b)
                                            if k in self.dictionary_marked_elements[i,j,"top_right"]: 
                                                if fr"\cancel{k}" not in self.dictionary_marked_elements[i,j,"top_right"]:
                                                    self.dictionary_marked_elements[i,j,"top_right"] = self.dictionary_marked_elements[i,j,"top_right"].replace(k, fr"\cancel{k}")
                                                    matches = re.findall(r'\b(?<!\\cancel)\d+\b',  self.dictionary_marked_elements[i,j,"top_left"] + " " + self.dictionary_marked_elements[i,j,"top_right"] + " " + self.dictionary_marked_elements[i,j,"bottom_left"] + " " + self.dictionary_marked_elements[i,j,"bottom_right"])  ##Every digit except cancelled.
                                                    if len(matches)==1:
                                                        self.grid[i][j]=int(matches[0])
                                                        rows(i)
                                                        columns(j)
                                                        if i<3: 
                                                            if j<3:
                                                                a,b=1,1
                                                            if j>2 and j<6:
                                                                a,b=1,4 
                                                            if j>5:
                                                                a,b=1,7
                                                        elif i>2 and i<6:
                                                            if j<3:
                                                                a,b=4,1
                                                            if j>2 and j<6:
                                                                a,b=4,4 
                                                            if j>5:
                                                                a,b=4,7
                                                        elif i>5 and i<10:
                                                            if j<3:
                                                                a,b=7,1
                                                            if j>2 and j<6:
                                                                a,b=7,4 
                                                            if j>5:
                                                                a,b=7,7
                                                        box(a,b)
                                            if k in self.dictionary_marked_elements[i,j,"bottom_left"]: 
                                                if fr"\cancel{k}" not in self.dictionary_marked_elements[i,j,"bottom_left"]:
                                                    self.dictionary_marked_elements[i,j,"bottom_left"] = self.dictionary_marked_elements[i,j,"top_left"].replace(k, fr"\cancel{k}")
                                                    matches = re.findall(r'\b(?<!\\cancel)\d+\b',  self.dictionary_marked_elements[i,j,"top_left"] + " " + self.dictionary_marked_elements[i,j,"top_right"] + " " + self.dictionary_marked_elements[i,j,"bottom_left"] + " " + self.dictionary_marked_elements[i,j,"bottom_right"])  ##Every digit except cancelled.
                                                    if len(matches)==1:
                                                        self.grid[i][j]=int(matches[0])                    
                                                        rows(i)
                                                        columns(j)
                                                        if i<3: 
                                                            if j<3:
                                                                a,b=1,1
                                                            if j>2 and j<6:
                                                                a,b=1,4 
                                                            if j>5:
                                                                a,b=1,7
                                                        elif i>2 and i<6:
                                                            if j<3:
                                                                a,b=4,1
                                                            if j>2 and j<6:
                                                                a,b=4,4 
                                                            if j>5:
                                                                a,b=4,7
                                                        elif i>5 and i<10:
                                                            if j<3:
                                                                a,b=7,1
                                                            if j>2 and j<6:
                                                                a,b=7,4 
                                                            if j>5:
                                                                a,b=7,7
                                                        box(a,b)
                                            if k in self.dictionary_marked_elements[i,j,"bottom_right"]: 
                                                if fr"\cancel{k}" not in self.dictionary_marked_elements[i,j,"bottom_right"]:
                                                    self.dictionary_marked_elements[i,j,"bottom_right"] = self.dictionary_marked_elements[i,j,"bottom_right"].replace(k, fr"\cancel{k}")
                                                    matches = re.findall(r'\b(?<!\\cancel)\d+\b',  self.dictionary_marked_elements[i,j,"top_left"] + " " + self.dictionary_marked_elements[i,j,"top_right"] + " " + self.dictionary_marked_elements[i,j,"bottom_left"] + " " + self.dictionary_marked_elements[i,j,"bottom_right"])  ##Every digit except cancelled.
                                                    if len(matches)==1:
                                                        self.grid[i][j]=int(matches[0])
                                                        rows(i)
                                                        columns(j)
                                                        if i<3: 
                                                            if j<3:
                                                                a,b=1,1
                                                            if j>2 and j<6:
                                                                a,b=1,4 
                                                            if j>5:
                                                                a,b=1,7
                                                        elif i>2 and i<6:
                                                            if j<3:
                                                                a,b=4,1
                                                            if j>2 and j<6:
                                                                a,b=4,4 
                                                            if j>5:
                                                                a,b=4,7
                                                        elif i>5 and i<10:
                                                            if j<3:
                                                                a,b=7,1
                                                            if j>2 and j<6:
                                                                a,b=7,4 
                                                            if j>5:
                                                                a,b=7,7
                                                        box(a,b)
        
        
        for count in range(10):
            for i in range(9):
                for j in range(9):
                    rows(i)
                    columns(j)
                    if i<3: 
                        if j<3:
                            a,b=1,1
                        if j>2 and j<6:
                            a,b=1,4 
                        if j>5:
                            a,b=1,7
                    elif i>2 and i<6:
                        if j<3:
                            a,b=4,1
                        if j>2 and j<6:
                            a,b=4,4 
                        if j>5:
                            a,b=4,7
                    elif i>5 and i<10:
                        if j<3:
                            a,b=7,1
                        if j>2 and j<6:
                            a,b=7,4 
                        if j>5:
                            a,b=7,7
                    box(a,b)
            
            

                                                        
        worked_file_name = self.output_file_name + "_worked.tex"
        with open (worked_file_name,'w') as file:
            latex_text_as_raw_string =  f"""\\documentclass[10pt]{{article}}
\\usepackage[left=0pt,right=0pt]{{geometry}}
\\usepackage{{tikz}}
\\usetikzlibrary{{positioning}}
\\usepackage{{cancel}}
\\pagestyle{{empty}}

\\newcommand{{\\N}}[5]{{\\tikz{{\\node[label=above left:{{\\tiny #1}},
                            label=above right:{{\\tiny #2}},
                            label=below left:{{\\tiny #3}},
                            label=below right:{{\\tiny #4}}]{{#5}};}}}}

\\begin{{document}}

\\tikzset{{every node/.style={{minimum size=.5cm}}}}

\\begin{{center}}
\\begin{{tabular}}{{||@{{}}c@{{}}|@{{}}c@{{}}|@{{}}c@{{}}||@{{}}c@{{}}|@{{}}c@{{}}|@{{}}c@{{}}||@{{}}c@{{}}|@{{}}c@{{}}|@{{}}c@{{}}||}}\\hline\\hline
% Line 1
\\N{{{self.dictionary_marked_elements[0, 0, 'top_left']}}}{{{self.dictionary_marked_elements[0, 0, 'top_right']}}}{{{self.dictionary_marked_elements[0, 0, 'bottom_left']}}}{{{self.dictionary_marked_elements[0, 0, 'bottom_right']}}}{{{self.grid[0][0]}}} & \\N{{{self.dictionary_marked_elements[0, 1, 'top_left']}}}{{{self.dictionary_marked_elements[0, 1, 'top_right']}}}{{{self.dictionary_marked_elements[0, 1, 'bottom_left']}}}{{{self.dictionary_marked_elements[0, 1, 'bottom_right']}}}{{{self.grid[0][1]}}} & \\N{{{self.dictionary_marked_elements[0, 2, 'top_left']}}}{{{self.dictionary_marked_elements[0, 2, 'top_right']}}}{{{self.dictionary_marked_elements[0, 2, 'bottom_left']}}}{{{self.dictionary_marked_elements[0, 2, 'bottom_right']}}}{{{self.grid[0][2]}}} &
\\N{{{self.dictionary_marked_elements[0, 3, 'top_left']}}}{{{self.dictionary_marked_elements[0, 3, 'top_right']}}}{{{self.dictionary_marked_elements[0, 3, 'bottom_left']}}}{{{self.dictionary_marked_elements[0, 3, 'bottom_right']}}}{{{self.grid[0][3]}}} & \\N{{{self.dictionary_marked_elements[0, 4, 'top_left']}}}{{{self.dictionary_marked_elements[0, 4, 'top_right']}}}{{{self.dictionary_marked_elements[0, 4, 'bottom_left']}}}{{{self.dictionary_marked_elements[0, 4, 'bottom_right']}}}{{{self.grid[0][4]}}} & \\N{{{self.dictionary_marked_elements[0, 5, 'top_left']}}}{{{self.dictionary_marked_elements[0, 5, 'top_right']}}}{{{self.dictionary_marked_elements[0, 5, 'bottom_left']}}}{{{self.dictionary_marked_elements[0, 5, 'bottom_right']}}}{{{self.grid[0][5]}}} &
\\N{{{self.dictionary_marked_elements[0, 6, 'top_left']}}}{{{self.dictionary_marked_elements[0, 6, 'top_right']}}}{{{self.dictionary_marked_elements[0, 6, 'bottom_left']}}}{{{self.dictionary_marked_elements[0, 6, 'bottom_right']}}}{{{self.grid[0][6]}}} & \\N{{{self.dictionary_marked_elements[0, 7, 'top_left']}}}{{{self.dictionary_marked_elements[0, 7, 'top_right']}}}{{{self.dictionary_marked_elements[0, 7, 'bottom_left']}}}{{{self.dictionary_marked_elements[0, 7, 'bottom_right']}}}{{{self.grid[0][7]}}} & \\N{{{self.dictionary_marked_elements[0, 8, 'top_left']}}}{{{self.dictionary_marked_elements[0, 8, 'top_right']}}}{{{self.dictionary_marked_elements[0, 8, 'bottom_left']}}}{{{self.dictionary_marked_elements[0, 8, 'bottom_right']}}}{{{self.grid[0][8]}}} \\\\ \\hline

% Line 2
\\N{{{self.dictionary_marked_elements[1, 0, 'top_left']}}}{{{self.dictionary_marked_elements[1, 0, 'top_right']}}}{{{self.dictionary_marked_elements[1, 0, 'bottom_left']}}}{{{self.dictionary_marked_elements[1, 0, 'bottom_right']}}}{{{self.grid[1][0]}}} & \\N{{{self.dictionary_marked_elements[1, 1, 'top_left']}}}{{{self.dictionary_marked_elements[1, 1, 'top_right']}}}{{{self.dictionary_marked_elements[1, 1, 'bottom_left']}}}{{{self.dictionary_marked_elements[1, 1, 'bottom_right']}}}{{{self.grid[1][1]}}} & \\N{{{self.dictionary_marked_elements[1, 2, 'top_left']}}}{{{self.dictionary_marked_elements[1, 2, 'top_right']}}}{{{self.dictionary_marked_elements[1, 2, 'bottom_left']}}}{{{self.dictionary_marked_elements[1, 2, 'bottom_right']}}}{{{self.grid[1][2]}}} &
\\N{{{self.dictionary_marked_elements[1, 3, 'top_left']}}}{{{self.dictionary_marked_elements[1, 3, 'top_right']}}}{{{self.dictionary_marked_elements[1, 3, 'bottom_left']}}}{{{self.dictionary_marked_elements[1, 3, 'bottom_right']}}}{{{self.grid[1][3]}}} & \\N{{{self.dictionary_marked_elements[1, 4, 'top_left']}}}{{{self.dictionary_marked_elements[1, 4, 'top_right']}}}{{{self.dictionary_marked_elements[1, 4, 'bottom_left']}}}{{{self.dictionary_marked_elements[1, 4, 'bottom_right']}}}{{{self.grid[1][4]}}} & \\N{{{self.dictionary_marked_elements[1, 5, 'top_left']}}}{{{self.dictionary_marked_elements[1, 5, 'top_right']}}}{{{self.dictionary_marked_elements[1, 5, 'bottom_left']}}}{{{self.dictionary_marked_elements[1, 5, 'bottom_right']}}}{{{self.grid[1][5]}}} &
\\N{{{self.dictionary_marked_elements[1, 6, 'top_left']}}}{{{self.dictionary_marked_elements[1, 6, 'top_right']}}}{{{self.dictionary_marked_elements[1, 6, 'bottom_left']}}}{{{self.dictionary_marked_elements[1, 6, 'bottom_right']}}}{{{self.grid[1][6]}}} & \\N{{{self.dictionary_marked_elements[1, 7, 'top_left']}}}{{{self.dictionary_marked_elements[1, 7, 'top_right']}}}{{{self.dictionary_marked_elements[1, 7, 'bottom_left']}}}{{{self.dictionary_marked_elements[1, 7, 'bottom_right']}}}{{{self.grid[1][7]}}} & \\N{{{self.dictionary_marked_elements[1, 8, 'top_left']}}}{{{self.dictionary_marked_elements[1, 8, 'top_right']}}}{{{self.dictionary_marked_elements[1, 8, 'bottom_left']}}}{{{self.dictionary_marked_elements[1, 8, 'bottom_right']}}}{{{self.grid[1][8]}}} \\\\ \\hline

% Line 3
\\N{{{self.dictionary_marked_elements[2, 0, 'top_left']}}}{{{self.dictionary_marked_elements[2, 0, 'top_right']}}}{{{self.dictionary_marked_elements[2, 0, 'bottom_left']}}}{{{self.dictionary_marked_elements[2, 0, 'bottom_right']}}}{{{self.grid[2][0]}}} & \\N{{{self.dictionary_marked_elements[2, 1, 'top_left']}}}{{{self.dictionary_marked_elements[2, 1, 'top_right']}}}{{{self.dictionary_marked_elements[2, 1, 'bottom_left']}}}{{{self.dictionary_marked_elements[2, 1, 'bottom_right']}}}{{{self.grid[2][1]}}} & \\N{{{self.dictionary_marked_elements[2, 2, 'top_left']}}}{{{self.dictionary_marked_elements[2, 2, 'top_right']}}}{{{self.dictionary_marked_elements[2, 2, 'bottom_left']}}}{{{self.dictionary_marked_elements[2, 2, 'bottom_right']}}}{{{self.grid[2][2]}}} &
\\N{{{self.dictionary_marked_elements[2, 3, 'top_left']}}}{{{self.dictionary_marked_elements[2, 3, 'top_right']}}}{{{self.dictionary_marked_elements[2, 3, 'bottom_left']}}}{{{self.dictionary_marked_elements[2, 3, 'bottom_right']}}}{{{self.grid[2][3]}}} & \\N{{{self.dictionary_marked_elements[2, 4, 'top_left']}}}{{{self.dictionary_marked_elements[2, 4, 'top_right']}}}{{{self.dictionary_marked_elements[2, 4, 'bottom_left']}}}{{{self.dictionary_marked_elements[2, 4, 'bottom_right']}}}{{{self.grid[2][4]}}} & \\N{{{self.dictionary_marked_elements[2, 5, 'top_left']}}}{{{self.dictionary_marked_elements[2, 5, 'top_right']}}}{{{self.dictionary_marked_elements[2, 5, 'bottom_left']}}}{{{self.dictionary_marked_elements[2, 5, 'bottom_right']}}}{{{self.grid[2][5]}}} &
\\N{{{self.dictionary_marked_elements[2, 6, 'top_left']}}}{{{self.dictionary_marked_elements[2, 6, 'top_right']}}}{{{self.dictionary_marked_elements[2, 6, 'bottom_left']}}}{{{self.dictionary_marked_elements[2, 6, 'bottom_right']}}}{{{self.grid[2][6]}}} & \\N{{{self.dictionary_marked_elements[2, 7, 'top_left']}}}{{{self.dictionary_marked_elements[2, 7, 'top_right']}}}{{{self.dictionary_marked_elements[2, 7, 'bottom_left']}}}{{{self.dictionary_marked_elements[2, 7, 'bottom_right']}}}{{{self.grid[2][7]}}} & \\N{{{self.dictionary_marked_elements[2, 8, 'top_left']}}}{{{self.dictionary_marked_elements[2, 8, 'top_right']}}}{{{self.dictionary_marked_elements[2, 8, 'bottom_left']}}}{{{self.dictionary_marked_elements[2, 8, 'bottom_right']}}}{{{self.grid[2][8]}}} \\\\ \\hline\\hline

% Line 4
\\N{{{self.dictionary_marked_elements[3, 0, 'top_left']}}}{{{self.dictionary_marked_elements[3, 0, 'top_right']}}}{{{self.dictionary_marked_elements[3, 0, 'bottom_left']}}}{{{self.dictionary_marked_elements[3, 0, 'bottom_right']}}}{{{self.grid[3][0]}}} & \\N{{{self.dictionary_marked_elements[3, 1, 'top_left']}}}{{{self.dictionary_marked_elements[3, 1, 'top_right']}}}{{{self.dictionary_marked_elements[3, 1, 'bottom_left']}}}{{{self.dictionary_marked_elements[3, 1, 'bottom_right']}}}{{{self.grid[3][1]}}} & \\N{{{self.dictionary_marked_elements[3, 2, 'top_left']}}}{{{self.dictionary_marked_elements[3, 2, 'top_right']}}}{{{self.dictionary_marked_elements[3, 2, 'bottom_left']}}}{{{self.dictionary_marked_elements[3, 2, 'bottom_right']}}}{{{self.grid[3][2]}}} &
\\N{{{self.dictionary_marked_elements[3, 3, 'top_left']}}}{{{self.dictionary_marked_elements[3, 3, 'top_right']}}}{{{self.dictionary_marked_elements[3, 3, 'bottom_left']}}}{{{self.dictionary_marked_elements[3, 3, 'bottom_right']}}}{{{self.grid[3][3]}}} & \\N{{{self.dictionary_marked_elements[3, 4, 'top_left']}}}{{{self.dictionary_marked_elements[3, 4, 'top_right']}}}{{{self.dictionary_marked_elements[3, 4, 'bottom_left']}}}{{{self.dictionary_marked_elements[3, 4, 'bottom_right']}}}{{{self.grid[3][4]}}} & \\N{{{self.dictionary_marked_elements[3, 5, 'top_left']}}}{{{self.dictionary_marked_elements[3, 5, 'top_right']}}}{{{self.dictionary_marked_elements[3, 5, 'bottom_left']}}}{{{self.dictionary_marked_elements[3, 5, 'bottom_right']}}}{{{self.grid[3][5]}}} &
\\N{{{self.dictionary_marked_elements[3, 6, 'top_left']}}}{{{self.dictionary_marked_elements[3, 6, 'top_right']}}}{{{self.dictionary_marked_elements[3, 6, 'bottom_left']}}}{{{self.dictionary_marked_elements[3, 6, 'bottom_right']}}}{{{self.grid[3][6]}}} & \\N{{{self.dictionary_marked_elements[3, 7, 'top_left']}}}{{{self.dictionary_marked_elements[3, 7, 'top_right']}}}{{{self.dictionary_marked_elements[3, 7, 'bottom_left']}}}{{{self.dictionary_marked_elements[3, 7, 'bottom_right']}}}{{{self.grid[3][7]}}} & \\N{{{self.dictionary_marked_elements[3, 8, 'top_left']}}}{{{self.dictionary_marked_elements[3, 8, 'top_right']}}}{{{self.dictionary_marked_elements[3, 8, 'bottom_left']}}}{{{self.dictionary_marked_elements[3, 8, 'bottom_right']}}}{{{self.grid[3][8]}}} \\\\ \\hline

% Line 5
\\N{{{self.dictionary_marked_elements[4, 0, 'top_left']}}}{{{self.dictionary_marked_elements[4, 0, 'top_right']}}}{{{self.dictionary_marked_elements[4, 0, 'bottom_left']}}}{{{self.dictionary_marked_elements[4, 0, 'bottom_right']}}}{{{self.grid[4][0]}}} & \\N{{{self.dictionary_marked_elements[4, 1, 'top_left']}}}{{{self.dictionary_marked_elements[4, 1, 'top_right']}}}{{{self.dictionary_marked_elements[4, 1, 'bottom_left']}}}{{{self.dictionary_marked_elements[4, 1, 'bottom_right']}}}{{{self.grid[4][1]}}} & \\N{{{self.dictionary_marked_elements[4, 2, 'top_left']}}}{{{self.dictionary_marked_elements[4, 2, 'top_right']}}}{{{self.dictionary_marked_elements[4, 2, 'bottom_left']}}}{{{self.dictionary_marked_elements[4, 2, 'bottom_right']}}}{{{self.grid[4][2]}}} &
\\N{{{self.dictionary_marked_elements[4, 3, 'top_left']}}}{{{self.dictionary_marked_elements[4, 3, 'top_right']}}}{{{self.dictionary_marked_elements[4, 3, 'bottom_left']}}}{{{self.dictionary_marked_elements[4, 3, 'bottom_right']}}}{{{self.grid[4][3]}}} & \\N{{{self.dictionary_marked_elements[4, 4, 'top_left']}}}{{{self.dictionary_marked_elements[4, 4, 'top_right']}}}{{{self.dictionary_marked_elements[4, 4, 'bottom_left']}}}{{{self.dictionary_marked_elements[4, 4, 'bottom_right']}}}{{{self.grid[4][4]}}} & \\N{{{self.dictionary_marked_elements[4, 5, 'top_left']}}}{{{self.dictionary_marked_elements[4, 5, 'top_right']}}}{{{self.dictionary_marked_elements[4, 5, 'bottom_left']}}}{{{self.dictionary_marked_elements[4, 5, 'bottom_right']}}}{{{self.grid[4][5]}}} &
\\N{{{self.dictionary_marked_elements[4, 6, 'top_left']}}}{{{self.dictionary_marked_elements[4, 6, 'top_right']}}}{{{self.dictionary_marked_elements[4, 6, 'bottom_left']}}}{{{self.dictionary_marked_elements[4, 6, 'bottom_right']}}}{{{self.grid[4][6]}}} & \\N{{{self.dictionary_marked_elements[4, 7, 'top_left']}}}{{{self.dictionary_marked_elements[4, 7, 'top_right']}}}{{{self.dictionary_marked_elements[4, 7, 'bottom_left']}}}{{{self.dictionary_marked_elements[4, 7, 'bottom_right']}}}{{{self.grid[4][7]}}} & \\N{{{self.dictionary_marked_elements[4, 8, 'top_left']}}}{{{self.dictionary_marked_elements[4, 8, 'top_right']}}}{{{self.dictionary_marked_elements[4, 8, 'bottom_left']}}}{{{self.dictionary_marked_elements[4, 8, 'bottom_right']}}}{{{self.grid[4][8]}}} \\\\ \\hline

% Line 6
\\N{{{self.dictionary_marked_elements[5, 0, 'top_left']}}}{{{self.dictionary_marked_elements[5, 0, 'top_right']}}}{{{self.dictionary_marked_elements[5, 0, 'bottom_left']}}}{{{self.dictionary_marked_elements[5, 0, 'bottom_right']}}}{{{self.grid[5][0]}}} & \\N{{{self.dictionary_marked_elements[5, 1, 'top_left']}}}{{{self.dictionary_marked_elements[5, 1, 'top_right']}}}{{{self.dictionary_marked_elements[5, 1, 'bottom_left']}}}{{{self.dictionary_marked_elements[5, 1, 'bottom_right']}}}{{{self.grid[5][1]}}} & \\N{{{self.dictionary_marked_elements[5, 2, 'top_left']}}}{{{self.dictionary_marked_elements[5, 2, 'top_right']}}}{{{self.dictionary_marked_elements[5, 2, 'bottom_left']}}}{{{self.dictionary_marked_elements[5, 2, 'bottom_right']}}}{{{self.grid[5][2]}}} &
\\N{{{self.dictionary_marked_elements[5, 3, 'top_left']}}}{{{self.dictionary_marked_elements[5, 3, 'top_right']}}}{{{self.dictionary_marked_elements[5, 3, 'bottom_left']}}}{{{self.dictionary_marked_elements[5, 3, 'bottom_right']}}}{{{self.grid[5][3]}}} & \\N{{{self.dictionary_marked_elements[5, 4, 'top_left']}}}{{{self.dictionary_marked_elements[5, 4, 'top_right']}}}{{{self.dictionary_marked_elements[5, 4, 'bottom_left']}}}{{{self.dictionary_marked_elements[5, 4, 'bottom_right']}}}{{{self.grid[5][4]}}} & \\N{{{self.dictionary_marked_elements[5, 5, 'top_left']}}}{{{self.dictionary_marked_elements[5, 5, 'top_right']}}}{{{self.dictionary_marked_elements[5, 5, 'bottom_left']}}}{{{self.dictionary_marked_elements[5, 5, 'bottom_right']}}}{{{self.grid[5][5]}}} &
\\N{{{self.dictionary_marked_elements[5, 6, 'top_left']}}}{{{self.dictionary_marked_elements[5, 6, 'top_right']}}}{{{self.dictionary_marked_elements[5, 6, 'bottom_left']}}}{{{self.dictionary_marked_elements[5, 6, 'bottom_right']}}}{{{self.grid[5][6]}}} & \\N{{{self.dictionary_marked_elements[5, 7, 'top_left']}}}{{{self.dictionary_marked_elements[5, 7, 'top_right']}}}{{{self.dictionary_marked_elements[5, 7, 'bottom_left']}}}{{{self.dictionary_marked_elements[5, 7, 'bottom_right']}}}{{{self.grid[5][7]}}} & \\N{{{self.dictionary_marked_elements[5, 8, 'top_left']}}}{{{self.dictionary_marked_elements[5, 8, 'top_right']}}}{{{self.dictionary_marked_elements[5, 8, 'bottom_left']}}}{{{self.dictionary_marked_elements[5, 8, 'bottom_right']}}}{{{self.grid[5][8]}}} \\\\ \\hline\\hline

% Line 7
\\N{{{self.dictionary_marked_elements[6, 0, 'top_left']}}}{{{self.dictionary_marked_elements[6, 0, 'top_right']}}}{{{self.dictionary_marked_elements[6, 0, 'bottom_left']}}}{{{self.dictionary_marked_elements[6, 0, 'bottom_right']}}}{{{self.grid[6][0]}}} & \\N{{{self.dictionary_marked_elements[6, 1, 'top_left']}}}{{{self.dictionary_marked_elements[6, 1, 'top_right']}}}{{{self.dictionary_marked_elements[6, 1, 'bottom_left']}}}{{{self.dictionary_marked_elements[6, 1, 'bottom_right']}}}{{{self.grid[6][1]}}} & \\N{{{self.dictionary_marked_elements[6, 2, 'top_left']}}}{{{self.dictionary_marked_elements[6, 2, 'top_right']}}}{{{self.dictionary_marked_elements[6, 2, 'bottom_left']}}}{{{self.dictionary_marked_elements[6, 2, 'bottom_right']}}}{{{self.grid[6][2]}}} &
\\N{{{self.dictionary_marked_elements[6, 3, 'top_left']}}}{{{self.dictionary_marked_elements[6, 3, 'top_right']}}}{{{self.dictionary_marked_elements[6, 3, 'bottom_left']}}}{{{self.dictionary_marked_elements[6, 3, 'bottom_right']}}}{{{self.grid[6][3]}}} & \\N{{{self.dictionary_marked_elements[6, 4, 'top_left']}}}{{{self.dictionary_marked_elements[6, 4, 'top_right']}}}{{{self.dictionary_marked_elements[6, 4, 'bottom_left']}}}{{{self.dictionary_marked_elements[6, 4, 'bottom_right']}}}{{{self.grid[6][4]}}} & \\N{{{self.dictionary_marked_elements[6, 5, 'top_left']}}}{{{self.dictionary_marked_elements[6, 5, 'top_right']}}}{{{self.dictionary_marked_elements[6, 5, 'bottom_left']}}}{{{self.dictionary_marked_elements[6, 5, 'bottom_right']}}}{{{self.grid[6][5]}}} &
\\N{{{self.dictionary_marked_elements[6, 6, 'top_left']}}}{{{self.dictionary_marked_elements[6, 6, 'top_right']}}}{{{self.dictionary_marked_elements[6, 6, 'bottom_left']}}}{{{self.dictionary_marked_elements[6, 6, 'bottom_right']}}}{{{self.grid[6][6]}}} & \\N{{{self.dictionary_marked_elements[6, 7, 'top_left']}}}{{{self.dictionary_marked_elements[6, 7, 'top_right']}}}{{{self.dictionary_marked_elements[6, 7, 'bottom_left']}}}{{{self.dictionary_marked_elements[6, 7, 'bottom_right']}}}{{{self.grid[6][7]}}} & \\N{{{self.dictionary_marked_elements[6, 8, 'top_left']}}}{{{self.dictionary_marked_elements[6, 8, 'top_right']}}}{{{self.dictionary_marked_elements[6, 8, 'bottom_left']}}}{{{self.dictionary_marked_elements[6, 8, 'bottom_right']}}}{{{self.grid[6][8]}}} \\\\ \\hline

% Line 8
\\N{{{self.dictionary_marked_elements[7, 0, 'top_left']}}}{{{self.dictionary_marked_elements[7, 0, 'top_right']}}}{{{self.dictionary_marked_elements[7, 0, 'bottom_left']}}}{{{self.dictionary_marked_elements[7, 0, 'bottom_right']}}}{{{self.grid[7][0]}}} & \\N{{{self.dictionary_marked_elements[7, 1, 'top_left']}}}{{{self.dictionary_marked_elements[7, 1, 'top_right']}}}{{{self.dictionary_marked_elements[7, 1, 'bottom_left']}}}{{{self.dictionary_marked_elements[7, 1, 'bottom_right']}}}{{{self.grid[7][1]}}} & \\N{{{self.dictionary_marked_elements[7, 2, 'top_left']}}}{{{self.dictionary_marked_elements[7, 2, 'top_right']}}}{{{self.dictionary_marked_elements[7, 2, 'bottom_left']}}}{{{self.dictionary_marked_elements[7, 2, 'bottom_right']}}}{{{self.grid[7][2]}}} &
\\N{{{self.dictionary_marked_elements[7, 3, 'top_left']}}}{{{self.dictionary_marked_elements[7, 3, 'top_right']}}}{{{self.dictionary_marked_elements[7, 3, 'bottom_left']}}}{{{self.dictionary_marked_elements[7, 3, 'bottom_right']}}}{{{self.grid[7][3]}}} & \\N{{{self.dictionary_marked_elements[7, 4, 'top_left']}}}{{{self.dictionary_marked_elements[7, 4, 'top_right']}}}{{{self.dictionary_marked_elements[7, 4, 'bottom_left']}}}{{{self.dictionary_marked_elements[7, 4, 'bottom_right']}}}{{{self.grid[7][4]}}} & \\N{{{self.dictionary_marked_elements[7, 5, 'top_left']}}}{{{self.dictionary_marked_elements[7, 5, 'top_right']}}}{{{self.dictionary_marked_elements[7, 5, 'bottom_left']}}}{{{self.dictionary_marked_elements[7, 5, 'bottom_right']}}}{{{self.grid[7][5]}}} &
\\N{{{self.dictionary_marked_elements[7, 6, 'top_left']}}}{{{self.dictionary_marked_elements[7, 6, 'top_right']}}}{{{self.dictionary_marked_elements[7, 6, 'bottom_left']}}}{{{self.dictionary_marked_elements[7, 6, 'bottom_right']}}}{{{self.grid[7][6]}}} & \\N{{{self.dictionary_marked_elements[7, 7, 'top_left']}}}{{{self.dictionary_marked_elements[7, 7, 'top_right']}}}{{{self.dictionary_marked_elements[7, 7, 'bottom_left']}}}{{{self.dictionary_marked_elements[7, 7, 'bottom_right']}}}{{{self.grid[7][7]}}} & \\N{{{self.dictionary_marked_elements[7, 8, 'top_left']}}}{{{self.dictionary_marked_elements[7, 8, 'top_right']}}}{{{self.dictionary_marked_elements[7, 8, 'bottom_left']}}}{{{self.dictionary_marked_elements[7, 8, 'bottom_right']}}}{{{self.grid[7][8]}}} \\\\ \\hline

% Line 9
\\N{{{self.dictionary_marked_elements[8, 0, 'top_left']}}}{{{self.dictionary_marked_elements[8, 0, 'top_right']}}}{{{self.dictionary_marked_elements[8, 0, 'bottom_left']}}}{{{self.dictionary_marked_elements[8, 0, 'bottom_right']}}}{{{self.grid[8][0]}}} & \\N{{{self.dictionary_marked_elements[8, 1, 'top_left']}}}{{{self.dictionary_marked_elements[8, 1, 'top_right']}}}{{{self.dictionary_marked_elements[8, 1, 'bottom_left']}}}{{{self.dictionary_marked_elements[8, 1, 'bottom_right']}}}{{{self.grid[8][1]}}} & \\N{{{self.dictionary_marked_elements[8, 2, 'top_left']}}}{{{self.dictionary_marked_elements[8, 2, 'top_right']}}}{{{self.dictionary_marked_elements[8, 2, 'bottom_left']}}}{{{self.dictionary_marked_elements[8, 2, 'bottom_right']}}}{{{self.grid[8][2]}}} &
\\N{{{self.dictionary_marked_elements[8, 3, 'top_left']}}}{{{self.dictionary_marked_elements[8, 3, 'top_right']}}}{{{self.dictionary_marked_elements[8, 3, 'bottom_left']}}}{{{self.dictionary_marked_elements[8, 3, 'bottom_right']}}}{{{self.grid[8][3]}}} & \\N{{{self.dictionary_marked_elements[8, 4, 'top_left']}}}{{{self.dictionary_marked_elements[8, 4, 'top_right']}}}{{{self.dictionary_marked_elements[8, 4, 'bottom_left']}}}{{{self.dictionary_marked_elements[8, 4, 'bottom_right']}}}{{{self.grid[8][4]}}} & \\N{{{self.dictionary_marked_elements[8, 5, 'top_left']}}}{{{self.dictionary_marked_elements[8, 5, 'top_right']}}}{{{self.dictionary_marked_elements[8, 5, 'bottom_left']}}}{{{self.dictionary_marked_elements[8, 5, 'bottom_right']}}}{{{self.grid[8][5]}}} &
\\N{{{self.dictionary_marked_elements[8, 6, 'top_left']}}}{{{self.dictionary_marked_elements[8, 6, 'top_right']}}}{{{self.dictionary_marked_elements[8, 6, 'bottom_left']}}}{{{self.dictionary_marked_elements[8, 6, 'bottom_right']}}}{{{self.grid[8][6]}}} & \\N{{{self.dictionary_marked_elements[8, 7, 'top_left']}}}{{{self.dictionary_marked_elements[8, 7, 'top_right']}}}{{{self.dictionary_marked_elements[8, 7, 'bottom_left']}}}{{{self.dictionary_marked_elements[8, 7, 'bottom_right']}}}{{{self.grid[8][7]}}} & \\N{{{self.dictionary_marked_elements[8, 8, 'top_left']}}}{{{self.dictionary_marked_elements[8, 8, 'top_right']}}}{{{self.dictionary_marked_elements[8, 8, 'bottom_left']}}}{{{self.dictionary_marked_elements[8, 8, 'bottom_right']}}}{{{self.grid[8][8]}}} \\\\ \\hline\\hline
\\end{{tabular}}
\\end{{center}}

\\end{{document}}
"""

            file.write(latex_text_as_raw_string)
                                       
                                

