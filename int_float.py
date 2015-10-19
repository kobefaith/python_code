import math

def is_sqr(x): 
    comp1 = math.sqrt(x)     #check the result of sqrt is float or int 
    comp2 = int(math.sqrt(x))
    if (comp1-comp2 > 0):
        return False
    else:
        return True
   

print filter(is_sqr, range(1, 101))