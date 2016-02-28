# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
 
# initialize the camera and grab a reference to the raw camera capture
#camera = PiCamera()
#camera.resolution = (640, 480)
#camera.framerate = 32
#camera.rotation = -90
videopath = 'car-demo.mp4'
#videopath = '../basic-motion-detection/videos/example_01.mp4'
camera = cv2.VideoCapture(videopath)
rawCapture = PiRGBArray(camera)#, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.25)

firstFrame = None

# capture frames from the camera
#for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True): # use this if picam

count = 0

while True:
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	(grabbed, frame) = camera.read()
	
		
	#frame = frame.array # use this is picam
 	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	# show the frame
	#cv2.imshow("Frame", gray)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	if firstFrame is None or count == 5:
		print 'setting firstFrame'
		firstFrame = gray
		count += 1
		continue
		
	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
 	
	# loop over the contours

	for c in cnts:
		# if the contour is too small, ignore it
		
		if cv2.contourArea(c) < 640:
			continue
 		
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		if y + (h/2) < 225 and y + (h/2) > 60:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
	cv2.line(frame, (0,60), (640, 60), (255,0,0))
	cv2.line(frame, (0,225), (640, 225), (255,0,0)) 
	# draw the text and timestamp on the frame
	#cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
	#	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	#cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
	#	(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	
	key = cv2.waitKey(1) & 0xFF
	count += 1
 
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
# camera.close() # use for picamera
camera.release()
cv2.destroyAllWindows()
	
