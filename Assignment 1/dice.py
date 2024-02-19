while True:
    try:
        x = int(input('Enter the desired goal cell number: '))  #i.e we want to know the top, front ad right of dice at 29th position in Ulam spiral.
        if x <= 0:
            raise ValueError
        break
    except ValueError:
        print('Incorrect value, try again')
import time
start_time=time.time()
front = 2; right = 1; top = 3; back=5;left=6; bottom = 4;
direction_list = ['R','D','L','U']
k=0
n=1
count = 1 ##We are counting when count will reach n and then program will stop
if x==1:
    front = 2; right = 1; top = 3; back=5;left=6; bottom = 4;
else:
    while(count<x):
        for i in range(2): #Because same number of steps is repeated twice in the spiral
            for j in range(n%4 if n>12 else n): #n is the number of times a direction is repeated.
                direction = direction_list[k]
                count=count+1   ## Count or number in the spiral also increases everytime a direction is executed.
                r=right;l=left;t=top;bo=bottom;f=front;ba=back;  #bo for bottom and ba for back
                n
                if direction=='R':  ## This program wont work 
                    right=t;top=l;bottom=r;left=bo;  ###This program wont work because right=top means right is updated; and then later bottom = right means bottom value becomes wrong.
                elif direction=='D': ## This program wont work 
                    front=t;top=ba;back=bo;bottom=f;
                elif direction=='L': ## This program wont work 
                    left=t;top=r;bottom=l;right=bo;
                else :   ## direction = 'U' ## This program wont work 
                    front=bo;top=f;back=t;bottom=ba;               
                if count==x:
                    break
            if count==x: ## Without line 27 and 28, if you run for x=4, it will give wrong result.
                 break                    
            if k!=3:
                k=k+1   ##k cant become 4 because there is no index 4 in directions_list. ALSO I need not give the condition k!=3 and i!=1 , because UP direction always ends on the 2nd leg of repeated directions in the Ulam spiral i.e.i=2 And never in the 1st leg of repeated directions i.e. i=1 
            else: 
                k=0
        n=n+1   ## The number of steps in a same direction increases after every 2 directions are over
print(f'On cell {x}, {top} is at the top, {front} at the front, and {right} on the right.')
end_time=time.time()
final_time=end_time - start_time
print(final_time)

        
