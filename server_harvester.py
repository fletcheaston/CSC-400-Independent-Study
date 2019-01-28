import socket
import sys
import cv2
import pickle
import pygame
import time

def get_buttons():
    buttons = [];
    pygame.event.get();
    for i in range(xbox_pad.get_numbuttons()):
        if(xbox_pad.get_button(i) == 1):
            buttons.append(i);
    return(buttons);

pygame.init();
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())];
xbox_pad = joysticks[0];
xbox_pad.init();

harvest_socket = socket.socket();
print("Socket created.");

port = 5000;
harvest_socket.bind(('',port));
print("Socket binded to port: {!r}".format(port));

harvest_socket.listen(1);
print("Socket is listening.");

while(True):
    c, addr = harvest_socket.accept();
    time.sleep(0.25);
    print("Got a connection from: {!r}".format(addr));
    while(True):
        buttons = get_buttons();
        if(buttons == []):
            continue;
        c.send(b'');
        break;
    c.close();
