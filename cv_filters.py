from cv2 import *
import numpy as np
import math
import time

def d1_distance(a,b):
    return(math.fabs(a - b));

def lookup_filter(img):
    height, width, _ = img.shape;

    for x in range(width):
        for y in range(height):
            blue = img.item(y,x,0);
            green = img.item(y,x,1);
            red = img.item(y,x,2);

            blue, green, red = lookup_table[blue][green][red];

            img.itemset(y,x,0,blue);
            img.itemset(y,x,1,green);
            img.itemset(y,x,2,red);

    return(img);

def custom_filter(img):
    height, width, _ = img.shape;

    for x in range(width):
        for y in range(height):
            blue = img.item(y,x,0);
            green = img.item(y,x,1);
            red = img.item(y,x,2);

            blue, green, red = specific_filter(blue, green, red);

            img.itemset(y,x,0,blue);
            img.itemset(y,x,1,green);
            img.itemset(y,x,2,red);

    return(img);

def specific_filter(blue, green, red):
    max_distance = 30;

    if(blue == 0 and green == 0 and red == 0):
        return(0,0,0);

    if(d1_distance(green, -0.0029 * math.pow(red, 2) + 1.8065 * red - 11.735) > max_distance):
        return(0,0,0);
    if(d1_distance(blue, 0.0031 * math.pow(red, 2) + 0.0352 * red + 11.226) > max_distance):
        return(0,0,0);
    if(d1_distance(blue, 8.9468 * math.exp(0.012 * green)) > max_distance):
        return(0,0,0);

    return(blue, green, red);

###############################################################################
# Creates a lookup table, which is necessary for the high-performant lookup filter

print("Creating lookup table...");
start = time.time();
#lookup_table = np.array([[[specific_filter(b,g,r) for r in range(256)] for g in range(256)] for b in range(256)]);

print("Finished creating lookup table: {:0.2f}".format(time.time() - start));
