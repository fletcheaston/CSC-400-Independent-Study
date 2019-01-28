import serial
import pygame
import time
from math import *
import sys

def safe_exit():
    try:
        harvester.write(bytes([ord('W'),400]));
        harvester.write(bytes([ord('S'),0]));
    except:
        print("Error on safe exit. Exiting.");
        sys.exit();

# A=0,B=1,X=3,Y=4,LB=6,RB=7,START=11,LSTICK=13,RSTICK=14
def get_buttons():
    buttons = [];
    pygame.event.get();
    for i in range(xbox_pad.get_numbuttons()):
        if(xbox_pad.get_button(i) == 1):
            buttons.append(i);
    return(buttons);

def controller_connected():
    return(pygame.joystick.get_count() == 1);

def translate_buttons(buttons,harvester):
    if(0 in buttons):
        speed += 1; # Speed up - A
    if(1 in buttons):
        speed = 0 # Brake - B
    if(3 in buttons):
        harvester.write('H'.encode()); # Harvest - X
    if(4 in buttons):
        harvester.write('P'.encode()); # Pickup - Y
    if(6 in buttons):
        angle -= 1; # Turn left - LB
    if(7 in buttons):
        angle += 1; # Turn right - RB
    if(12 in buttons):
        pass; # No Xbox One button available
    if(13 in buttons):
        angle = 400; # Turn straight - LSTICK
    if(14 in buttons):
        pass;

    angle = max(0,angle);
    angle = min(965,angle);
    harvester.write(bytes([ord('W'),angle]));
    harvester.write(bytes([ord('S'),speed]));

def serial_pull(ser):
    message = "";

    while(ser.inWaiting() > 0):
        message += ser.readline().decode().strip();
    return(message);

def setup():
    global xbox_pad;
    global harvester;

    try:
        pygame.init();
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())];
        xbox_pad = joysticks[0];
        xbox_pad.init();
    except:
        print("No controllers available. Exiting safely.");
        sys.exit();

    try:
        harvester = serial.Serial(port="/dev/cu.usbmodem1411", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.1, write_timeout=0.01);
    except:
        try:
            harvester = serial.Serial(port="/dev/cu.usbmodem1421", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.1, write_timeout=0.01);
        except:
            print("No serial ports available. Exiting safely.");
            #sys.exit();

    # Allows for the serial ports to fully finish setting up.
    time.sleep(1);

def run():
    while(True):
        time.sleep(0.05);

        if(controller_connected() == False):
            print("No controllers connected. Exiting safely.");
            sys.exit();

        print(angle, speed);

        c, addr = harvest_socket.accept();
        time.sleep(0.25);
        print("Got a connection from: {!r}".format(addr));
        while(True):
            buttons = get_buttons();
            if(buttons == []):
                continue;
            c.send(b'');
            break;

        buttons = buttons[0];
        try:
            translate_buttons(buttons);
        except:
            print("Error tranlating buttons and/or writing to serial. Exiting safely.");
            #sys.exit();

def main():
    setup();
    run();

harvester = None;
xbox_pad = None;
angle = 400; # 400 is centered, straight ahead
speed = 0;
pickup_delay = time.time();
steering_blocked = True;
steering_block_delay = time.time();

harvest_socket = socket.socket();
print("Socket created.");

port = 5000;
harvest_socket.bind(('',port));
print("Socket binded to port: {!r}".format(port));

harvest_socket.listen(1);
print("Socket is listening.");

main();
