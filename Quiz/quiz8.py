# Written by * for COMP9021

# Defines:
# - a class: DarkCorridor, implementing 1 special method
# - another class: Pacer, implementing 3 special methods
#   and (at least) 2 extra methods:
#   * pace()
#   * now_here_in_dark_corridor()
# - a function: compare_stress(), that takes two Pacer objects
#   as arguments.

# Uses the Unicode characters of code point 9654, 9664 and 11036.
right=chr(9654)
left=chr(9664)
white_square=chr(11036)

class DarkCorridorError(Exception):
    pass

class DarkCorridor:
    def __init__(self,length):
        if length<=0:
            raise DarkCorridorError("The length of the corridor should be strictly positive")
        self.length = int(length)
        self.list_squares=[white_square]* self.length 

    ## VERY IMPORTANT. YOU CANT USE print(white_square * self.length) INSIDE _Str_ method or any method in this program. Because you are not calling the method as an instance of the object. i.e. if the command to run was corridor._str_ , then
    def __str__(self):
        return ' ' + ' '.join(self.list_squares)# DONT USE PRINT FUNCTION. BECAUSE WE DONT HAVE A RETURN statement in this _str_ function, what happens is when this function is called, it will also return "None" which will be visible in output.
        ##If we just type return ' '.join(white_square for _ in range(self.length)) .. the output wil have a space before the 1st white square
    def __repr__(self):
        return f'{self.__class__.__name__}({self.length})'  ##OR you can use format method instead of f string i.e. return '{self.class.name_}({self.length})'.format(self=self)
        ##YOU CAN EITHER TYPE {self._class.name_} or you can directly type DarkCorridor .. because it will anyway print it
    def send_list(self):
        return self.list_squares ##This is not printing lke in line 29. Its sending address of the list.
        
class Pacer:    
    def __init__(self,name,corridor):
        self.name=name
        self.corridor=corridor
        self.pos=0 #Right now its in first position of list
        self.flag=True
        self.list_of_squares=corridor.send_list()
        self.counter = 0

    def __str__(self):
        return f'{self.name} in {self.corridor}'  ##You can also use self.object._str_()  .. instead of str(self.object) .. the syntax is much cleaner

    def __repr__(self):
        return f'{self.__class__.__name__}(\'{self.name}\', {self.corridor.__repr__()})'  ## The () is necessary if using this synatx OR use repr(self.object) instead of self.object.repr_() . It is much more cleaner syntax
    ## YOU HAVE TO GIVE \ backslash to esacpe the ' apostrophe. Even double quotes wont work.
    ## VERY IMPORTANT. The () is necessary in above, because you are calling the method itself. If you were calling a variable.e.g robot.is_sitting .. where robot is object and it gets the value of is_sitting variable which was initialized in _init_ function  but in the maybe sit() method inside the Roboter class itself., the value of is_sitting was changed when we involed sit() method inside Robot class by using command robot.sit()  and then when we check i_sitting usiong robot.is_sitting .. it shows new value.  Side note .. The object is first invoked using robot=Roboter(variables or arguments as necessary)
    def pace(self,no_of_steps):
        ## self.pos+=no_of_steps
        for i in range(no_of_steps):
            if self.flag==True:
                current_position=self.pos+1 ##Incrementing position from 0 to 2 #self.pos is previous position. tmp is current position
            else:
                current_position=self.pos-1 ## Decrementing position from 2 to 0
            if current_position == len(self.list_of_squares):
                current_position-=1
            if current_position < 0:
                current_position+=1
            if self.counter != 0 and (self.counter + 1)%len(self.list_of_squares) == 0:
                self.flag=bool(1-int(self.flag)) ##Change arrows
            self.pos=current_position
            self.counter+=1


    def now_here_in_dark_corridor(self):
        print(' ',end="")
        for i in range(0,len(self.list_of_squares)):
            if i==self.pos and self.flag==True:
                if i==len(self.list_of_squares)-1:
                    print(right) ##The end of output shouldnot have a space
                else:
                    print(right, end=" ")
            elif i==self.pos and self.flag==False:
                if i==len(self.list_of_squares)-1:
                    print(left)
                else:
                    print(left, end=" ")
            else:
                if i==len(self.list_of_squares)-1:
                    print(self.list_of_squares[i])
                else:
                     print(self.list_of_squares[i], end=" ")


def compare_stress(person_1, person_2): ##Two pacer objects passed to a function in the main part of program
    if person_1.counter==person_2.counter:
        print(f'{person_1.name} and {person_2.name} are both as stressed ({person_1.counter} steps).')
    elif (person_1.counter>person_2.counter):
        print(f'{person_1.name} ({person_1.name} steps) is more stressed than {person_2.name} ({person_2.counter} steps).')
    else:
        print(f'{person_2.name} ({person_2.counter} steps) is more stressed than {person_1.name} ({person_1.counter} steps).')