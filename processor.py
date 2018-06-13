import tensorflow as tf
from scipy import misc
import numpy as np
from PIL import Image

def filename_to_array(filename):
    array = list(misc.imread(filename));
    return(array);

def array_to_file(filename, array):
    misc.imsave(filename, array);

def check_ratio(pixel):
    r = pixel[0];
    g = pixel[1];
    b = pixel[2];

    r_b = r / max(b, 1);
    r_g = r / max(g, 1);
    b_g = b / max(g, 1);

    if(r > 220 and g > 220 and b > 220):
        return(False);
    if(g <= 1.2 * b):
        return(False);
    if(r >= 1.1 * g):
        return(False);
    if(r_b <= 1.5 * b_g):
        return(False);
    if(1.2 <= r_b):
        return(True);
    return(False);

size = 256;
count = 57;

for i in range(count):
    '''new_size = (size, size);
    new_im = Image.new("RGB", new_size);

    im = Image.open("Easy_Melon_Images_256/image_" + str(i) + ".jpg");
    name = "Easy_Melon_Images_256/image_" + str(i) + ".png";

    new_im.paste(im, (0,0));
    new_im.save(name);'''

    image = filename_to_array("Easy_Melon_Images_256/image_" + str(i) + ".png");

    for y in range(size):
        for x in range(size):
            pixel = image[y][x];
            if(check_ratio(pixel) == False):
                image[y][x][0] = 0;
                image[y][x][1] = 0;
                image[y][x][2] = 0;

    array_to_file("Processed_Easy_Melon_Images_256/image_" + str(i) + ".png", image);

    print("Image {!r} processed.".format(i));
