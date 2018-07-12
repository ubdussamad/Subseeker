#||||||||||||||||||| Comparison Statics
#Simple Statistical methods for comparing
#strings for best hit selection.
#Authors: Mohammed S. Haque , Rita Thomas (Co-author)

#----------Required Declaration-------------
#This file contains comparison methods
#which have some minor traces
#of code that is derived from the
#Hidden Analysis* GmbH  toolkit.
#All the derived techniques are DECLASSIFIED
#for public usage and are FREE to distribute.
#Read adyybnhc1kge2.onion for more details.

from re import findall
import math
import time

def time_wrapper(func):
    def wrapee(*args,**kwargs):
        epoch = time.time()
        obj = func(*args,**kwargs)
        print('Time delta: %f'%(time.time()-epoch,))
        return obj
    return wrapee

def find_dominant_spacer(string):
    '''Returns the most frequent separator
    in the string, if there is no separator
    it returns -1.
    Dominance is calculated by the number of times that separator has
    come up in the target string.'''
    
    sample_seprators = ['\s','[_]','[-]','[.]','[~]']
    seprators = [ findall(j,string.lower()) for j in sample_seprators ]
    valid_seprators = [i for i in seprators if i]
    valid_seprators = valid_seprators if valid_seprators else [[None],[None]] #Protection
    weights = [len(i) for i in valid_seprators]
    max_weight = max(weights)
    dominant_seprator = valid_seprators[weights.index(max_weight)][0]
    return dominant_seprator

def word_match( string_A , string_B ):
    b = string_B.lower().split(find_dominant_spacer(string_B))
    a = string_A.lower().split(find_dominant_spacer(string_A))
    hits = sum([ 1 for i in a if (i in b)])
    average = (hits)/(((len(a)+len(b))/2.0))
    return average

def letter_match( string_A , string_B ):
    b = ''.join(string_B.lower().split(find_dominant_spacer(string_B)))
    a = ''.join(string_A.lower().split(find_dominant_spacer(string_A)))
    score = 0
    for i,j in zip(a,b):
        if i==j:
            score+=1
    return score/(((len(a)+len(b))/2.0))

@time_wrapper
def compare(a,b):
    return(((letter_match(a,b)*4)+(word_match(a,b)*2))/6) 
