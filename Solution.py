import cv2
import time
import argparse
import numpy as np

video = cv2.VideoCapture(0)
print("Move out of screen, Capturing background in 3 Secs")
time.sleep(3)

#Capturing background
for i in range(60):
	check,background = video.read()


foo = True
while True:
	check,frame = video.read()
	# Converting the color space from BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# Generating mask to detect red color
	lower_red = np.array([0,120,70])
	upper_red = np.array([10,255,255])
	mask1 = cv2.inRange(hsv,lower_red,upper_red)

	lower_red = np.array([170,120,70])
	upper_red = np.array([180,255,255])
	mask2 = cv2.inRange(hsv,lower_red,upper_red)

	mask1 = mask1+mask2

	# Refining the mask corresponding to the detected red color
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=2)
	mask1 = cv2.dilate(mask1,np.ones((3,3),np.uint8),iterations = 1)
	mask2 = cv2.bitwise_not(mask1)

	# Generating the final output
	res1 = cv2.bitwise_and(background,background,mask=mask1)
	res2 = cv2.bitwise_and(frame,frame,mask=mask2)
	output = cv2.addWeighted(res1,1,res2,1,0)

	if foo:
		print("Press 'q' to exit")
		foo = False

	cv2.imshow('Output',output)
	k = cv2.waitKey(1)
	if k == ord('q'):
		break 

video.release()
cv2.destroyAllWindows()