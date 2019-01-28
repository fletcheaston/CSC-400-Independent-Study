from cv_filters import *
from random import randint
import time

camera = cv2.VideoCapture(1);

max_count = 2793;
kernel = np.ones((3,3),np.uint8);

while(True): #Apply smoothing before? Filter out noise from image before/after processing
    _, frame = camera.read();

    original_frame = cv2.resize(frame, (256, 144));
    #original_frame = cv2.imread("Watermelon/small_image_" + str(randint(0,max_count)) + ".jpg");

    frame = original_frame;

    start = time.time();

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV);

    lower = np.array([30,80,40]);
    upper = np.array([55,255,255]);

    mask = cv2.inRange(hsv, lower, upper);
    frame = cv2.bitwise_and(frame, frame, mask = mask);

    frame = custom_filter(frame);

    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel);

    indices = np.where(frame != [0,0,0]);

    y = np.mean(indices[0]);
    x = np.mean(indices[1]);

    if(math.isnan(y) or math.isnan(x)):
        y = 128;
        x = 128;
    else:
        y = int(y);
        x = int(x);

    cv2.circle(frame,(x,y), 10, (0,0,255), -1);
    cv2.circle(original_frame,(x,y), 10, (0,0,255), -1);
    #frame = cv2.erode(frame,kernel,iterations = 1)

    #cv2.imwrite("Watermelon/filtered_image_" + str(i % max_count) + ".jpg", frame);

    cv2.imshow("Frame", frame);
    cv2.imshow("Original Frame", original_frame);
    cv2.waitKey(1);

    print("Time: {:0.3f}".format(time.time() - start));

    #time.sleep(1);
