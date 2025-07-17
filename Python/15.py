import cv2
import numpy as np
print(cv2.__version__)
evt  = 0
xVal = 0
yVal = 0

def mouseClick(event,xPos,yPos,flags,params):
    global evt 
    #where the cursor was when the event happen
    global xVal
    global yVal
    if event == cv2.EVENT_LBUTTONDOWN:
        print(event)
        xVal = xPos
        yVal = yPos
        evt = event
    if event == cv2.EVENT_RBUTTONUP:
        evt = event
        print(event)


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

#setup mouse click 
cv2.namedWindow('myWEBcam')
cv2.setMouseCallback('myWEBcam',mouseClick)
while True:
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)

    if evt == 1:
        # create a blank picture 
        x = np.zeros([250,250,3],dtype=np.uint8)
        # Hue , Saturation , Value convert to HSV Color Space
        y = cv2.cvtColor(flipped_frame,cv2.COLOR_BGR2HSV)
        #grab the color 
        clr = y[yVal][xVal]
        # clr = flipped_frame[yVal][xVal]
        print(clr)
        x[:,:] = clr
        cv2.putText(x,str(clr),(0,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
        cv2.imshow('Color Picker',x)
        cv2.moveWindow('Color Picker',width,0)
        evt = 0


    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()