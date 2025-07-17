import cv2
import numpy as np
print(cv2.__version__)
"""Setting Up The Camera"""
#setting the variables
width = 640
height = 360
cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#set window width , height 
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
#set The Frame rate 30 frames per second
cam.set(cv2.CAP_PROP_FPS,30)
#set up the codec 
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
"""Setting Up The TrackBars"""
# create trackbars call back functions 
# when you miss the trackbars 
# it goes and calls it's function
def onTrack1(val):
    global hueLow
    hueLow = val
    print('Hue Low',hueLow)

def onTrack2(val):
    global hueHigh
    hueHigh = val
    print('Hue High',hueHigh)   

def onTrack7(val):
    global hueLow2
    hueLow2 = val
    print('Hue Low 2',hueLow2)

def onTrack8(val):
    global hueHigh2
    hueHigh2 = val
    print('Hue High 2',hueHigh2)   


def onTrack3(val):
    global satLow
    satLow = val
    print('Sat Low',satLow)

def onTrack4(val):
    global satHigh
    satHigh = val
    print('Sat High',satHigh)   

def onTrack5(val):
    global valLow
    valLow = val
    print('Val Low',valLow)

def onTrack6(val):
    global valHigh
    valHigh = val
    print('Val High',valHigh)   
# those dont matter it's just the first 
# time through you have got numbers there or 
# the program will crash 

hueLow  = 10
hueHigh = 20
satLow  = 10 
satHigh = 250
valLow  = 10
valHigh = 250     
cv2.namedWindow('MyTracker dataset')
cv2.resizeWindow('MyTracker dataset', width, height)
cv2.moveWindow('MyTracker dataset',width,0) # what i want to move ==> MyTracker

#create six trackbars
cv2.createTrackbar('Hue Low','MyTracker dataset',2,179,onTrack1)
cv2.createTrackbar('Hue High','MyTracker dataset',31,179,onTrack2)
cv2.createTrackbar('Hue Low 2','MyTracker dataset',170,179,onTrack7)
cv2.createTrackbar('Hue High 2','MyTracker dataset',179,179,onTrack8)
cv2.createTrackbar('Sat Low','MyTracker dataset',112,255,onTrack3)
cv2.createTrackbar('Sat High','MyTracker dataset',255,255,onTrack4)
cv2.createTrackbar('Val Low','MyTracker dataset',0,255,onTrack5)
cv2.createTrackbar('Val High','MyTracker dataset',255,255,onTrack6)

while True:
    """Grap The Frame"""
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    # new frame in Hue Saturation Value Color Space
    frameHSV = cv2.cvtColor(flipped_frame,cv2.COLOR_BGR2HSV)
    # create the Little Box of low values and High values
    # at that looking my whole frame for all the pixels 
    # that fit within that box 
    lowerBound = np.array([hueLow,satLow,valLow])
    upperBound = np.array([hueHigh,satHigh,valHigh])

    lowerBound2 = np.array([hueLow2,satLow,valLow])
    upperBound2 = np.array([hueHigh2,satHigh,valHigh])

    """There where the MAGIC Happens"""
    myMask = cv2.inRange(frameHSV,lowerBound,upperBound)
    myMask2 = cv2.inRange(frameHSV,lowerBound2,upperBound2)
    myMaskComp = myMask | myMask2
    # myMaskComp = cv2.add(myMask,myMask2)
    contours,junk = cv2.findContours(myMaskComp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #draw them back in our original frame 
    # cv2.drawContours(flipped_frame,contours,-1,(255,0,0),3)
    # step throw the contours 
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= 200:
            # myContour = [contour]
            # cv2.drawContours(flipped_frame,[contour],0,(255,0,0),3)
            #tracking the object of intrest
            x,y,w,h=cv2.boundingRect(contour)
            cv2.rectangle(flipped_frame,(x,y),(x+w,y+h),(0,0,255),3)



    # mask the original frame 
    myObject = cv2.bitwise_and(flipped_frame,flipped_frame,mask=myMaskComp)
    myObjectSmall = cv2.resize(myObject,(int(width/2),int(height/2)))
    cv2.imshow('MyObject',myObjectSmall)
    cv2.moveWindow('MyObject',int(width/2),int(height))
    myMaskSmall = cv2.resize(myMask,(int(width/2),int(height/2)))
    cv2.imshow('MyMask',myMaskSmall)
    cv2.moveWindow('MyMask',0,height)

    myMaskSmall2 = cv2.resize(myMask2,(int(width/2),int(height/2)))
    cv2.imshow('MyMask 2',myMaskSmall2)
    cv2.moveWindow('MyMask 2',0,height+int(height/2)+30)



    """Show The Trame""" 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()