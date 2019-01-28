import cv2
import time
import glob

count = 0;
size = 512;

for f in glob.glob('*.MOV'):

    vidcap = cv2.VideoCapture(f);
    success, image = vidcap.read();

    success = True;

    while(success):
        try:
            success, image = vidcap.read();

            if(count % 24 == 0):
                w = image.shape[1];
                h = image.shape[0];

                ratio = max(w / size, h / size);

                resized = cv2.resize(image, (int(w / ratio), int(h / ratio)));

                string = "Watermelon/image_" + str(count // 24) + ".jpg";

                cv2.imwrite(string, resized);

                print("Success: " + str(count));
            count += 1;
        except:
            print("Failure");
