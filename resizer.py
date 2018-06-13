import glob
import os
from PIL import Image

count = 0;

for f in glob.glob('*.jpg'):
    try:
        im = Image.open(f);

        name = "image_" + str(count) + ".jpg";

        im.thumbnail((256,256));

        im.save(name);

        print("Resized Image", count);
        count += 1;
    except:
        print("Failure", i);
