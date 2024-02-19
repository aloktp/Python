import os 
from os.path import exists
import copy

file_name = input('Which data file do you want to use? ').removesuffix('\n')
if not exists(file_name):
    print('Incorrect input, giving up.')
    sys.exit()  
town = []
fish = []  
with open(file_name) as file:
    for line in file:
        if line.isspace():
            continue
        else:
            line=[int(x) for x in line.split()]
            town.append(line[0])
            fish.append(line[1])
search_value_list=[]
## We are going to do binary search to get the search_values
lpv= 0 ##lpv is lowest possible value ##DONOT give lpv=min(fish). ##What if input is [30,40,50] and the maximum quantity of fish is actually 20? You would have totally missed the option of 20 then.
hpv=sum(fish)//len(fish) ##hpv is highest possible value
for j in range(100_000_000):    ## Cant give while True loop here because I need line 40 to work. 
    fish_copy=copy.deepcopy(fish)   #Shallow copy of fish, otherwise if we use "fish" list.. then its values become modified in the for loop and thus unable to be used in next check.
    town_copy=copy.deepcopy(town)   #Shallow copy of town
    search_value=(lpv+hpv)//2  #Only integer value is retained because of integer division i.e.// division operator. Hence, NO floating point decimals will be there.
    search_value_list.append(search_value)
    for i in range(len(fish_copy)-1):  #Upto 2nd last element, as we dont send any fish from right to left, and hence no fish will travel from last town to previous towns. 
        diff=abs(search_value-fish_copy[i])
        if fish_copy[i]<search_value:
            fish_copy[i+1] = fish_copy[i+1] - (diff+town[i+1]-town[i])
            fish_copy[i]=search_value
        elif fish_copy[i]>search_value:
            fish_copy[i+1]=fish_copy[i+1]+(diff-(town_copy[i+1]-town_copy[i]))
            fish_copy[i]=search_value
        else:   ##i.e. fish_copy[i]==search_value
            continue
    print(fish_copy)
    
    if j==0 and fish_copy[len(fish_copy)-1] < 0: ## i=0 means 1st iteration of for loop. In coast_1.txt, the binary search fails in first try itself, but we dont have any previous search_value to fetch the value 20. So, we take it from min(fish) and ALSO NOT min(fish_copy).
        search_value=min(fish)   ##NOT min(fish_copy)
        break
    if fish_copy[len(fish)-1] < 0: ##Since all towns are giving to their right side towns i.e. from left to right, and thus last town is NEVER giving anything to left towns, last town fish can never be a negative value.    
        search_value=search_value_list[len(search_value_list)-2] ## TO get second last element, Give search_value_list[len(search_value_list)-1] instead of i-1 or creating a new variable j. Because suppose there are 3 towns, but we search 7 times before we get result. So we cant use i. ## Or suppose now its [2,2,2,2,3] . If the next iteration of for loop happens, suppose its [3,3,3,3,-1] now. Then search_value becomes 3 which is wrong..
        break        
    if fish_copy[len(fish)-1] == search_value:
        break
    elif fish_copy[len(fish)-1] < search_value:
        if fish_copy[len(fish)-1] == search_value-1:   ## Suppose in coast_10.txt (check coast_12.txt also), our previous list is [216,216,218] and now its [217,217,216]. search_value becomes 217, but we want 216. i.e. min(fish) i.e. minimum element in [217,217,216] = 216 is the maximum quantity fish each town can have. And binary search should stop when difference between element [217,216] i.e.[search_value,element] is 1.
            search_value=min(fish_copy) ##Because binary search should stop if suppose list is [63,63,64]. i.e. lpv is updated to 63+1 =64. So, next search_value is (64+64)/2 = 64. i.e. Binary search should have been stopped whenever difference between two elements is just 1.  Binary search should continue only if lpv<hpv and hpv-lpv>1.  e.g. [63,65] is okay because next search value is (63+65)/2 = 64, which is neither 63 nor 65. Also since now lpv and hpv becomes 64. All future iterations search value remains same i.e. (64+64)/2 = 64 & it continues so on endlesslessly. 
            break
        hpv=search_value-1 
        if (lpv>hpv): ##Donot give lpv<=hpv as that is an acceptable condition.  #Preventing next iteration now itself AND preserving search_value of this iteration now itself by breaking out of loop.
            search_value=search_value_list[len(search_value_list)-2]  ##Suppose [18,18,20] now & next iteration of for loop, it will become [19,19,14] & it will stop there. i.e search_value should be previous search_value i.e. 18.  But in this program, it wont keep on going on if lpv=hpv, because line 43 ensures that. You can check coast_2.txt for that. It stops at 415 even if all elements are equal to 415 in output.
            break
    elif fish_copy[len(fish)-1] > search_value:  ## Suppose [6,6,8] now and if next iteration of for loop is initiated, it becomes [7,7,6]. That means, search_value becomes 7, which is wrong.
        if fish_copy[len(fish)-1] == search_value + 1:   ## Suppose in coast_5.txt, our previous list is [64,64,62] and now its [63,63,64]. Suppose if line 51 i.e. this line is not there and then line 51 -> If condition just 64>63 i.e. 63 is search value. Then it will update lpv = search_value+1. Then in line 53, it will be lpv>hpv i.e. next iteration will be prevented BUT search_value becomes previous search_value i.e 64, which is wrong. Correct search_value is min(fish) i.e. min[63,63,64] i.e. the fish list in this iteration.
            search_value=min(fish_copy) ##Because binary search should stop if suppose list is [63,63,64]. i.e. lpv is updated to 63+1 =64. So, next search_value is (64+64)/2 = 64. i.e. Binary search should have been stopped whenever difference between two elements is just 1.  Binary search should continue only if lpv<hpv and hpv-lpv>1.  e.g. [63,65] is okay because next search value is (63+65)/2 = 64, which is neither 63 nor 65. Also since now lpv and hpv becomes 64. All future iterations search value remains same i.e. (64+64)/2 = 64 & it continues so on endlesslessly. 
            break
        lpv=search_value+1                       
        if (lpv>hpv): ##Donot give lpv<=hpv as that is an acceptable condition.#Preventing next iteration now itself AND preserving search_value of this iteration now itself by breaking out of loop.
            search_value=search_value_list[len(search_value_list)-2]  ##Suppose [18,18,20] now & next iteration of for loop, it will become [19,19,14] & it will stop there. i.e. search_value should be previous search_value i.e. 18.    
            break
    else:   ##Unnecessary line 41 can be replaced with this else statement
        continue  
#Line 46 and Line 54 cannot be combined into one as Line 53 and Line 45 are different conditions.
print(search_value)
            
