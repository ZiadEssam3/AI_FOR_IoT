import cv2
print(cv2.__version__) 
# seed the variable evt 
evt = 0
def mouseClick(event, xPos, yPos, flags, params):
    # accessable throw the program
    global pnt1 
    global pnt2  
    global evt 

    #look for 2 things 
    #if the left button pressed down the main 
    #thing we need to snag the position of it 

    if event == cv2.EVENT_LBUTTONDOWN:
        print(event) # snag position 
        pnt1 = (xPos, yPos) # upper left corner of ROI
        evt = event
    if event == cv2.EVENT_LBUTTONUP: 
        print(event)
        pnt2 = (xPos, yPos)
        evt = event
    if event == cv2.EVENT_RBUTTONUP:
        evt = event
        print(event)

#setting the variables
width = 640
height = 360
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#set window width , height 
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
#set The Frame rate 30 frames per second
cam.set(cv2.CAP_PROP_FPS, 30)
#set up the codec 
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
#create mouse callback 
# for sitting and listening mouse call back 
cv2.namedWindow('myWEBcam')
cv2.setMouseCallback('myWEBcam', mouseClick)

while True:
    ignore, frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    if evt == 4: 
        cv2.rectangle(flipped_frame, pnt1, pnt2, (0, 0, 255), 2)
        #create region of intersest 
        ROI = flipped_frame[pnt1[1]:pnt2[1], pnt1[0]:pnt2[0]]
        # Ensure ROI is not empty
        if ROI.size > 0:
            cv2.imshow('ROI', ROI)
            cv2.moveWindow('ROI', int(width * 1.1), 0)
    if evt == 5:
        cv2.destroyWindow('ROI')
        evt = 0

    #show the frame 
    cv2.imshow('myWEBcam', flipped_frame)
    cv2.moveWindow('myWEBcam', 0, 0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
