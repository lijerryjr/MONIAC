###################
# Math functions
# This file contains basic math functions used
###################

def distance(x1, y1, x2, y2):
    #Distance formula
    return ((x2-x1)**2+(y2-y1)**2)**0.5

def magnitude(vector):
    #Find the magnitude of a vector
    return (vector[0]**2+vector[1]**2)**0.5

def roundUp(x):
    if x%1==0:
        return int(x)
    else:
        return int(x)+1