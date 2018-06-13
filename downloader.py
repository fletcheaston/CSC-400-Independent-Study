import requests
import time
from PIL import Image

base_path = "NeuralTrainer/People_Full/image_";

with open("people.txt") as f:
    content = f.readlines();

for i in range(len(content)):
    content[i] = content[i].split('?')[0].strip();

count = 0;

for i in range(len(content)):
    try:
        img_data = requests.get(content[i]).content;
        with open(base_path + str(count) + ".png", "wb") as handler:
            handler.write(img_data);

        new_im = Image.new("RGB", (512, 512));

        im = Image.open(base_path + str(count) + ".png");
        im.thumbnail((512, 512), resample=Image.BICUBIC);

        name = "NeuralTrainer/People_512/image_" + str(count) + ".jpg";

        new_im.paste(im, (0,0));
        new_im.save(name);

        count += 1;

        print("Success on: {!r}".format(i));
    except:
        print("Failed on: {!r}".format(i));
