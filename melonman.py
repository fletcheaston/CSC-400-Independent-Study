import numpy as np
import cv2
import math

class shapedetector:

	def detect(self, c):
		shape = ""
		perimeter = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.01*perimeter, True)
		area = cv2.contourArea(c)
		(x, y, w, h) = cv2.boundingRect(c)
		rad = w/2

		if abs(area > 500) and len(approx) > 7:
			if abs(1-(h/w)) <= 0.4 and abs(1-(area / ( (math.pi) * (rad**2) ))) <= 0.4:
				shape = "watermelon"

		return shape

cap = cv2.VideoCapture(0)

se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25))
se2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(95,95))

while(1):
	ret, frame = cap.read()

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	max_y = frame.shape[0]
	max_x = frame.shape[1]

	lower = np.array([30,80,40])
	upper = np.array([55,255,255])

	mask = cv2.inRange(hsv, lower, upper)
	out = cv2.bitwise_and(frame, frame, mask = mask)

	clean_im = cv2.erode(mask, se)
	clean_im = cv2.dilate(clean_im, se2)

	contours = cv2.findContours(clean_im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = contours[1]

	sd = shapedetector()

	for c in contours:
		m = cv2.moments(c)
		cx = int(m["m10"] / (m["m00"] + 1e-7) )
		cy = int(m["m01"] / (m["m00"] + 1e-7) )
		shape  = sd.detect(c)

		delta_x = int(max_x/2) - cx
		delta_y = int(max_y/2) - cy
		rad = np.arctan(delta_x/delta_y)
		theta = (180/math.pi) * rad
		print(theta)

		if (len(c) > 10):
			ellipse = cv2.fitEllipse(c)
			cv2.ellipse(frame, ellipse, (0,255,0),2)
			cv2.putText(frame, shape, (cx, cy),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		else:
			continue

		cv2.imshow("Image", frame)
		k = cv2.waitKey(1)
		if k == 27:
			break
