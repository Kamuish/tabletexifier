
import math

def compute_digits(number):
    if number > 0:
        digits = int(math.log10(number))+1
    elif number == 0:
        digits = 1
    else:
        digits = int(math.log10(-number))+2 # +1 if you don't count the '-' 
    return digits