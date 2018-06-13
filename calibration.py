import time
import cv2
import math
import numpy as np
import sys
import shutil
import os

def empty_table_directory():
    try:
        shutil.rmtree("./Tables");
    except:
        print("No folder 'Tables' to remove.");
    os.makedirs("./Tables");

def read_calibration_count():
    count = input("Number of calibration filters: ");

    try:
        count = int(count);
    except:
        print("Invalid number. 1 calibration filter will be used.");
        count = 1;

    return(count);

def reprint(string):
    string = str(string);
    sys.stdout.write(string);
    sys.stdout.flush();
    sys.stdout.write("\b" * len(string));

def d1_distance(a,b):
    return(math.fabs(a - b));

def d2_distance(x1,y1,x2,y2):
    return(math.sqrt(math.pow(x1 - x2,2) + math.pow(y1 - y2,2)));

def center_text(string, img):
    font = cv2.FONT_HERSHEY_COMPLEX;
    textsize, _ = cv2.getTextSize(string, font, 2, 5);

    text_x = (img.shape[1] - textsize[0]) // 2;
    text_y = (img.shape[0] - textsize[1]) // 2;

    cv2.putText(img, string, (text_x, textsize[1] + 5), font, 2, (0,0,255), 5);

    return(img);

def avg_colorspace(c0,c1,c2,data_x,data_y):
    all_distances = [];
    for i in range(len(data_x)):
        x = data_x[i];
        y = data_y[i];

        real_y = c0 + c1 * x + c2 * x * x;
        all_distances.append(d1_distance(y,real_y));
    return(np.mean(all_distances));

def write_text_data(num,blue_data,green_data,red_data):
    with open("Tables/" + str(num) + "_blue.txt", 'w+') as f:
        for i in range(len(blue_data)):
            f.write("{!r}\n".format(blue_data[i]));
    with open("Tables/" + str(num) + "_green.txt", 'w+') as f:
        for i in range(len(green_data)):
            f.write("{!r}\n".format(green_data[i]));
    with open("Tables/" + str(num) + "_red.txt", 'w+') as f:
        for i in range(len(red_data)):
            f.write("{!r}\n".format(red_data[i]));

###############################################################################

def pixel_filter(blue,green,red):
    global calibration_filters;

    for i in range(len(calibration_filters)):
        a = calibration_filters.item(i,0,green,red);
        b = calibration_filters.item(i,1,blue,green);
        c = calibration_filters.item(i,2,red,blue);
        if(a != 0 and b != 0 and c != 0):
            return(1);

    return(0);

def custom_filter(img):
    height, width, _ = img.shape;

    x_points = [];
    y_points = [];

    bin_img = np.zeros((height,width));

    for x in range(width):
        for y in range(height):
            b = img.item(y,x,0);
            g = img.item(y,x,1);
            r = img.item(y,x,2);
            for i in range(len(calibration_filters)):
                temp = pixel_filter(b,g,r);
                if(temp != 0):
                    bin_img.itemset(y,x,255);
                    x_points.append(x);
                    y_points.append(y);

    x_points = np.asarray(x_points);
    y_points = np.asarray(y_points);
    return(x_points,y_points,bin_img);

def create_lookup_table(c0,c1,c2,distance):
    temp_table = np.zeros((256,256));

    for x in range(256):
        for y in range(256):
            d = math.fabs(y - (c0 + c1 * x + c2 * x * x));
            if(d < distance):
                d = 255 - (255 * d / distance);
                temp_table.itemset(y,x,d);

    return(temp_table);

###############################################################################
# Opens webcam to capture calibration image

def prepare_calibration(camera, center, size):
    _, webcam = camera.read();
    countdown_time = 10;
    start = time.time();
    height, width, _ = webcam.shape;

    while(True):
        _, webcam = camera.read();
        webcam = cv2.flip(webcam, 1);

        webcam = center_text("Calibration in: {:0.2f}".format(countdown_time - (time.time() - start)), webcam);
        cv2.ellipse(webcam,center,size,0,0,360,(0,255,0),5)

        webcam = cv2.resize(webcam, (width // 2, height // 2));

        cv2.imshow("Cailbrate", webcam);
        cv2.waitKey(1);

        if(time.time() - start >= countdown_time):
            break;

    _, webcam = camera.read();
    return(webcam);


###############################################################################

def process_calibration_data(red_data,green_data,blue_data,num):

    rg_coef = np.polynomial.polynomial.polyfit(red_data,green_data,2);
    gb_coef = np.polynomial.polynomial.polyfit(green_data,blue_data,2);
    br_coef = np.polynomial.polynomial.polyfit(blue_data,red_data,2);

    global polynomial_clearance;

    rg_avg = polynomial_clearance * avg_colorspace(rg_coef[0],rg_coef[1],rg_coef[2],red_data,green_data);
    gb_avg = polynomial_clearance * avg_colorspace(gb_coef[0],gb_coef[1],gb_coef[2],green_data,blue_data);
    br_avg = polynomial_clearance * avg_colorspace(br_coef[0],br_coef[1],br_coef[2],blue_data,red_data);

    rg_table = create_lookup_table(rg_coef[0],rg_coef[1],rg_coef[2],rg_avg);
    gb_table = create_lookup_table(gb_coef[0],gb_coef[1],gb_coef[2],gb_avg);
    br_table = create_lookup_table(br_coef[0],br_coef[1],br_coef[2],br_avg);

    global calibration_filters;

    calibration_slice = (rg_table, gb_table, br_table);
    calibration_filters.append(calibration_slice);

    rg_table = cv2.flip(rg_table, 0);
    gb_table = cv2.flip(gb_table, 0);
    br_table = cv2.flip(br_table, 0);

    cv2.imwrite("Tables/" + str(num) + "_rg_table.jpg", rg_table);
    cv2.imwrite("Tables/" + str(num) + "_gb_table.jpg", gb_table);
    cv2.imwrite("Tables/" + str(num) + "_br_table.jpg", br_table);

# Calibrate coefficients for equations and creates lookup tables
def process_calibration_image(img, center, size, num):
    height, width, _ = img.shape;

    blue_data = [];
    green_data = [];
    red_data = [];

    for x in range(width):
        for y in range(height):

            if(math.pow(center[0] - x,2) / math.pow(size[0],2) + (math.pow(center[1] - y,2) / math.pow(size[1],2)) <= 1):
                blue = img.item(y,x,0);
                green = img.item(y,x,1);
                red = img.item(y,x,2);

                blue_data.append(blue);
                green_data.append(green);
                red_data.append(red);
            else:
                img.itemset(y,x,0,0);
                img.itemset(y,x,1,0);
                img.itemset(y,x,2,0);

    cv2.imwrite("Tables/image_" + str(num) + ".jpg",img);

    process_calibration_data(red_data,green_data,blue_data,num);

    write_text_data(num,blue_data,green_data,red_data);

###############################################################################

def run(camera):
    cv2.destroyAllWindows();

    kernel = np.ones((3,3),np.uint8);
    divisor = 7;
    _, webcam = camera.read();
    height, width, _ = webcam.shape;

    start = time.time();

    avg = 0;
    avg_count = 0;

    while(True):
        _, webcam = camera.read();

        webcam = cv2.flip(webcam, 1);

        height, width, _ = webcam.shape;

        webcam = cv2.resize(webcam, (width // divisor, height // divisor));

        x_points, y_points, bin_img = custom_filter(webcam);

        if(len(x_points) > 10):
            x = int(np.mean(x_points));
            y = int(np.mean(y_points));

            cv2.circle(webcam,(x,y), 3, (0,0,255), -1)

        webcam = cv2.resize(webcam, (width // 2, height // 2));

        cv2.imshow("webcam", webcam);
        cv2.imshow("bin", bin_img);
        cv2.waitKey(1);

        frame_time = time.time() - start;
        start = time.time();
        avg += (1 / frame_time);
        avg_count += 1;
        reprint("FPS: {:0.2f} {!r}".format(avg / avg_count, len(x_points)));

###############################################################################

def main():

    empty_table_directory();
    count = read_calibration_count();

    camera = cv2.VideoCapture(0);
    _, webcam = camera.read();

    height, width, _ = webcam.shape;
    center = (width // 2, height // 2);
    size = (width // 4, height // 3);

    time.sleep(1);

    for i in range(count):
        calibration_frame = prepare_calibration(camera, center, size);
        process_calibration_image(calibration_frame, center, size, i);

    global calibration_filters;
    calibration_filters = np.asarray(calibration_filters);
    run(camera);

polynomial_clearance = 2;
calibration_filters = [];
# calibration_filters[which calibration][0 = rg, 1 = gb, 2 = br][color 1][color 2]

main();
