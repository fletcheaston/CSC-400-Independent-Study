from cv2 import *
import numpy as np
import math
import time

min_val = 30;
size = 10;

def d1_distance(a,b):
    return(math.fabs(a - b));

def split_filter(img, rg_table, gb_table, br_table):
    height, width, _ = img.shape;

    blue_layer, green_layer, red_layer = cv2.split(img);

    for x in range(width):
        for y in range(height):
            blue = blue_layer.item(y,x);
            green = green_layer.item(y,x);
            red = red_layer.item(y,x);

            if(blue < min_val or green < min_val or red < min_val):
                blue_layer.itemset(y,x,0);
                green_layer.itemset(y,x,0);
                red_layer.itemset(y,x,0);
            else:
                if(rg_table[red][green] == 0 or gb_table[green][blue] == 0 or br_table[blue][red] == 0):
                    blue_layer.itemset(y,x,0);
                    green_layer.itemset(y,x,0);
                    red_layer.itemset(y,x,0);

    return(cv2.merge((blue_layer,green_layer,red_layer)));

def green_v_red(g,r):
    if(d1_distance(g, -0.0029 * math.pow(r, 2) + 1.8065 * r - 11.735) > 20):
        return(0);
    return(1);

def blue_v_green(b,g):
    if(d1_distance(b, 8.9468 * math.exp(0.012 * g)) > 50):
        return(0);
    return(1);

def blue_v_red(b,r):
    if(d1_distance(b, 0.0031 * math.pow(r, 2) + 0.0352 * r + 11.226) > 30):
        return(0);
    return(1);

''' Deprecated, will remove later.
###############################################################################
# Creates lookup tables for each combo of pixel values
print("Creating lookup table...");
start = time.time();

green_red_table = np.array([[green_v_red(g,r) for r in range(256)] for g in range(256)]);

blue_green_table = np.array([[blue_v_green(b,g) for g in range(256)] for b in range(256)]);

blue_red_table = np.array([[blue_v_red(b,r) for r in range(256)] for b in range(256)]);

circle_table = np.array([[0.1 * (size // 2 - d2_distance(size // 2,size // 2,x,y)) for x in range(size)] for y in range(size)]);

cv2.imwrite("Circle.jpg", circle_table);

print("Finished creating lookup table: {:0.2f}".format(time.time() - start));
'''
