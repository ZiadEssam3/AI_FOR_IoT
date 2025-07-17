import cv2
print(cv2.__version__)
# params ==> grap the value
# calls  ==> pass the value
def myCallBack1(val): 
    global xPos 
    xPos = val 

def myCallBack2(val): 
    global yPos 
    yPos = val 
#change the camera resolution 
def myCallBack3(val): 
    width = val
    # calculate height 16:9 ratio
    height = int(width*9/16)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)

xPos = 0 
yPos = 0

#setting the variables
width = 680
height = 420
cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#set window width , height 
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
#set The Frame rate 30 frames per second
cam.set(cv2.CAP_PROP_FPS,30)
#set up the codec 
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

# create trackbar 
cv2.namedWindow('myTrackBars')
cv2.moveWindow('myTrackBars',width,0)
cv2.resizeWindow('myTrackBars',400,150)
cv2.createTrackbar('xPos','myTrackBars',0,2000,myCallBack1)
cv2.createTrackbar('yPos','myTrackBars',0,1000,myCallBack2)
cv2.createTrackbar('width','myTrackBars',width,1920,myCallBack3)
while True:
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
         

    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',xPos,yPos)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()