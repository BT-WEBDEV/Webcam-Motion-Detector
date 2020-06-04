###### WEBCAM MOTION DETECTOR ######
###### CASE USE: Webcam will detect motion and record motion start & stop times and displays that information. 
###### PRESS Q TO QUIT PROGRAM 

import cv2, time, pandas
from datetime import datetime

#Variable setup - webcam & data framing along with and empty status list. 0 = no movement | 1 = movement
first_frame=None
status_list=[None,None]
times=[]
df=pandas.DataFrame(columns=["Start","End"])

#Video Object with Video Capture Method, 0 index argument sense we only have 1 webcam.
video=cv2.VideoCapture(0,cv2.CAP_DSHOW)

#While loop to iterate through webcam images at a fast rate, thus creating video. 
while True:
    #NumPy Array that displays BGR pixel output of each frame of the video. 
    check, frame=video.read()

    #Status is zero per frame when no movement is happening. 
    status=0 

    #convert first frame of video (an image) to grayscale and blur the image to reduce noise. 
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    #Get the first frame from the video that is converted into grayscale. On the 2nd iteration of loop, continue with the rest of the while loop
    if first_frame is None: 
        first_frame=gray
        continue
    
    #Delta Frame caluculates the absolute difference between the first frame & gray images
    delta_frame=cv2.absdiff(first_frame,gray)
    #Threshold Frame calculates the threshold of the delta frame and outputs black/white pixels that were closest to those colors
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    #Then we dilate the threshold frame so we can increase the white object region in the image. 
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)

    #Cnts finds the contours of the threshold frame. 
    cnts=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    #For every contour in cnts if the contour area is less than a 1000 pixels, go to the next cotnour. Status will change to 1 per frame when there is motion. 
    for contour in cnts: 
        if cv2.contourArea(contour) < 1000: 
            continue
        status=1
    
        #if greater than 1000 pixels, we will implement a rectangle on the current frame
        (x, y, w, h) = cv2.boundingRect(contour) 
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

    #Status data then gets appended into a status list. 
    status_list.append(status)

    #If the status list contains a [0,1] next to each other - motion has started and recorded datetime
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())
    
    #If the status list contains a [1,0] next to each oth er - motion has stopped and recorded datetime 
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())

    #Displays the webcam images. 
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    #press any key and the process stops
    key=cv2.waitKey(1)
    
    #stop the program by stop pressing Q on the keyboard
    if key==ord('q'):
        if status==1: 
            times.append(datetime.now())
        break
    
#For every item in the range of the Start/Stop times list, append the Start & End times to the data frame. 
for i in range(0,len(times),2):
    df=df.append({"Start":times[i], "End": times[i+1]}, ignore_index=True)

#After the start & end times have been added to the data frame, turn it into a CSV file. 
df.to_csv("Times.csv")

#Stops video and ends the program. 
video.release()
cv2.destroyAllWindows()