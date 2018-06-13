from PIL import Image

new_size = 256;

for i in range(3923):
    new_im = Image.new("RGB", (new_size, new_size));

    im = Image.open("Easy_Melon_Images_Full/melon_" + str(i) + ".jpg");
    im.thumbnail((new_size, new_size), resample=Image.BICUBIC);

    name = "Easy_256/image_" + str(i) + ".jpg";

    new_im.paste(im, (0,0));
    new_im.save(name);
