import serial
import time
from math import *
from vision import *
import cv2


def serial_push(ser, bytes, need_encode):
    return(None);
    if(need_encode == True):
        ser.write(bytes.encode());
    else:
        ser.write(bytes);

def serial_pull(ser):
    return("");
    message = "";

    while(ser.inWaiting() > 0):
        message += ser.readline().decode().strip();
    return(message);


#wheelchair = serial.Serial(port="/dev/cu.usbmodem1451", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.1, write_timeout=0.01);
wheelchair = None;

time.sleep(1);

thresh = 20;

cam_control = False;

direction = 0;
# 1 is forward, -1 is reverse, 0 is brake

angle = 0;
# 1 is turning left, 0 is forward, -1 is turning right

buttons = [];

with tf.Session() as session:

    print("Opening webcam for analysis...");

    camera_port = 0;

    camera = cv2.VideoCapture(camera_port);

    saver.restore(session, path);

    try:
        while(True):

            if(cam_control == False):

                command = input('Choose a command: ').upper();

                if(command == 'F'):
                    serial_push(wheelchair, 'F', True);

                if(command == 'B'):
                    serial_push(wheelchair, 'B', True);

                if(command == 'R'):
                    serial_push(wheelchair, 'R', True);

                if(command == 'E'):
                    serial_push(wheelchair, 'E', True);

                if('W' in command):
                    try:
                        angle = int(input('Choose an angle: '));

                        serial_push(wheelchair, bytes([ord('W'),angle + 127]), False);

                    except:
                        print("Invalid angle. Must be between 0-255.");

                if(command == 'C'):
                    cam_control = not cam_control;

                    if(cam_control == True):
                        print("Running on camera.");
                    else:
                        print("Running on command.");

                serial_push(wheelchair, 'P', True);

            else:

                _, img = camera.read();

                webcam1 = img[0:512, 0:256];
                webcam2 = img[0:512, 232:488];
                webcam3 = img[0:512, 464:720];

                cv2.imwrite("webcam1.jpg", webcam1);
                cv2.imwrite("webcam2.jpg", webcam2);
                cv2.imwrite("webcam3.jpg", webcam3);

                '''cv2.imshow("webbcam1", webcam1);
                cv2.waitKey(1);
                cv2.imshow("webbcam2", webcam2);
                cv2.waitKey(1);
                cv2.imshow("webbcam3", webcam3);
                cv2.waitKey(1);'''

                guess = prediction.eval(feed_dict={x:[decode_image("webcam1.jpg").eval(), decode_image("webcam2.jpg").eval(), decode_image("webcam3.jpg").eval()], mode:False});

                left = 100 * np.mean(guess[0]);
                center = 100 * np.mean(guess[1]);
                right = 100 * np.mean(guess[2]);

                if(left > thresh and center > thresh and right > thresh):
                    angle = -1 * left + 1 * right;
                else:
                    angle = 0;
                    print("No watermelon.");

                if(left > thresh or center > thresh or right > thresh):
                    print("Left: {:0.3f} | Center: {:0.3f} | Right: {:0.3f}".format(left, center, right));

                serial_push(wheelchair, bytes([ord('W'),angle + 127]), False);

            time.sleep(0.1);

            message = serial_pull(wheelchair);
            if(message != ""):
                print(message);
    except:
        serial_push(wheelchair, 'B', True);
        print("Exiting.");
        sys.exit();
