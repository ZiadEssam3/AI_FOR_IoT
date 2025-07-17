import cv2
print(cv2.__version__)
# call back functions 
def myCallBack1(val):
    global xPos
    print('xPos: ',val)
    xPos = val

def myCallBack2(val):
    global yPos
    print('yPos: ',val)
    yPos = val

def myCallBack3(val):
    global myRad
    print('radius: ',val)
    myRad = val

def myCallBack4(val):
    global myThick
    
    print('thick: ',val)
    myThick = val

#setting the variables
width = 640
height = 360
myRad = 25
myThick = 1
xPos = int(width/2)
yPos = int(height/2)

cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# qset window width , height 
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
# set The Frame rate 30 frames per second
cam.set(cv2.CAP_PROP_FPS,30)
# set up the codec 
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
# create the window 
cv2.namedWindow('myTrackbars')
# resize window 
cv2.resizeWindow('myTrackbars',400,150)
# make the trackbar in front of main window 
cv2.moveWindow('myTrackbars',width,0)
#create the trackbar 
cv2.createTrackbar('xPos','myTrackbars',xPos,1920,myCallBack1) 
cv2.createTrackbar('yPos','myTrackbars',yPos,1080,myCallBack2) 
cv2.createTrackbar('radius','myTrackbars',myRad,int(height/2),myCallBack3) 
cv2.createTrackbar('thick','myTrackbars',myThick,7,myCallBack4) 

while True:
    ignore,frame = cam.read()  
    if myThick == 0:
        myThick = (-1)
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    cv2.circle(flipped_frame,(xPos,yPos),myRad,(255,0,0),myThick)


    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()