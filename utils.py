import pygame

def lerp(min_val,max_val,value):
    if value<=0:
        return min_val
    if value>=1:
        return max_val
    return min_val+(value-0)*((max_val-min_val)/(1-0))


