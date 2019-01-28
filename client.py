import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code
cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('10.1.9.71',8089))
while True:
    ret,frame=cap.read()
    frame = cv2.resize(frame, (256,144));
    cv2.imshow("client", frame);
    cv2.waitKey(1);
    data = pickle.dumps(frame) ### new code
    clientsocket.sendall(struct.pack("L", len(data))+data) ### new code
