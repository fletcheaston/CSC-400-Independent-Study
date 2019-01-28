import time
import cv2
import math
import numpy as np
import sys
import shutil

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

###############################################################################

def pixel_filter(pixel):
    blue = pixel[0];
    green = pixel[1];
    red = pixel[2];

    for i in range(len(calibration_filters)):
        if(calibration_filters[i][0][green][red] == 1 and calibration_filters[i][1][blue][green] == 1 and calibration_filters[i][2][red][blue] == 1):
            return(pixel);

    pixel[0] = 0;
    pixel[1] = 0;
    pixel[2] = 0;
    return(pixel);

def calibrated_filter(img):
    height, width, _ = img.shape;

    for x in range(width):
        for y in range(height):
            pixel = img.item(y,x);
            new_pixel = pixel_filter(pixel);
            if(new_pixel != pixel):
                img.itemset(y,x,new_pixel);

    return(img);

def create_lookup_table(c0,c1,c2,distance):
    temp_table = np.zeros((256,256));

    for x in range(256):
        for y in range(256):
            if(math.fabs(y - (c0 + c1 * x + c2 * x * x)) < distance):
                temp_table.itemset(y,x,255);

    return(temp_table);

###############################################################################
# Opens webcam to capture calibration image

def prepare_calibration(camera, center, size):
    _, webcam = camera.read();
    countdown_time = 3;
    start = time.time();

    while(True):
        _, webcam = camera.read();
        #webcam = cv2.flip(webcam, 1);

        webcam = center_text("Calibration in: {:0.2f}".format(countdown_time - (time.time() - start)), webcam);
        cv2.ellipse(webcam,center,size,0,0,360,(0,0,255),5)
        cv2.imshow("Cailbrate", webcam);
        cv2.waitKey(1);

        if(time.time() - start >= countdown_time):
            break;

    return(webcam);


###############################################################################

# Calibrate coefficients for equations and creates lookup tables
def calibrate_tables(img, center, size, count):
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

    rg_coef = np.polynomial.polynomial.polyfit(red_data,green_data,2);
    gb_coef = np.polynomial.polynomial.polyfit(green_data,blue_data,2);
    br_coef = np.polynomial.polynomial.polyfit(blue_data,red_data,2);

    rg_avg = polynomial_clearance * avg_colorspace(rg_coef[0],rg_coef[1],rg_coef[2],red_data,green_data);
    gb_avg = polynomial_clearance * avg_colorspace(gb_coef[0],gb_coef[1],gb_coef[2],green_data,blue_data);
    br_avg = polynomial_clearance * avg_colorspace(br_coef[0],br_coef[1],br_coef[2],blue_data,red_data);

    rg_table = create_lookup_table(rg_coef[0],rg_coef[1],rg_coef[2],rg_avg);
    gb_table = create_lookup_table(gb_coef[0],gb_coef[1],gb_coef[2],gb_avg);
    br_table = create_lookup_table(br_coef[0],br_coef[1],br_coef[2],br_avg);

    global calibration_filters;

    calibration_slice = [rg_table, gb_table, br_table];
    calibration_filters.append(calibration_slice);

    cv2.imwrite("Tables/rg_table_" + str(count) + ".jpg", rg_table);
    cv2.imwrite("Tables/gb_table_" + str(count) + ".jpg", gb_table);
    cv2.imwrite("Tables/br_table_" + str(count) + ".jpg", br_table);

###############################################################################

def run(camera):
    cv2.destroyAllWindows();

    kernel = np.ones((2,2),np.uint8);
    divisor = 6;
    _, webcam = camera.read();
    height, width, _ = webcam.shape;

    while(True):
        _, webcam = camera.read();

        height, width, _ = webcam.shape;

        webcam = cv2.resize(webcam, (width // divisor, height // divisor));

        webcam = calibrated_filter(webcam);

        webcam = cv2.morphologyEx(webcam, cv2.MORPH_OPEN, kernel);

        webcam = cv2.resize(webcam, (width // 2, height // 2));

        cv2.imshow("webcam", webcam);
        cv2.waitKey(1);

def empty_table_directory():
    shutil.rmtree("./Tables");
    os.makedirs("./Tables");

def read_calibration_count():
    count = input("Number of calibration filters: ");

    return(count);

###############################################################################

def main():

    #empty_table_directory();
    count = read_calibration_count();

    camera = cv2.VideoCapture(0);
    _, webcam = camera.read();

    height, width, _ = webcam.shape;
    center = (width // 2, height // 2);
    size = (width // 8, height // 6);

    time.sleep(1);

    for i in range(count):
        calibration_frame = prepare_calibration(camera, center, size);
        calibrate_tables(calibration_frame, center, size, count);

    run(camera);


polynomial_clearance = 2;
calibration_filters = [];
# calibration_filters[which calibration][0 = rg, 1 = gb, 2 = br][color 1][color 2]

main();
