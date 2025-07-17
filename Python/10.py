import cv2
print(cv2.__version__)
#setting the variables
width = 640
height = 360
snipW = 120 
snipH = 60

boxCR = int(width/2)  #box center row 
boxCC = int(height/2) #box center column

deltaRow = 1     # how many rows move at a time 
deltaColumn = 1  # how many columns move at a time


cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#set window width , height 
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
#set The Frame rate 30 frames per second
cam.set(cv2.CAP_PROP_FPS,30)
#set up the codec 
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

while True:
    ignore,frame = cam.read() 
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    
    #create snip frame 
    frameROI = flipped_frame[int(boxCR-snipH/2):int(boxCR+snipH/2),int(boxCC-snipW/2):int(boxCC+snipW/2)]
    flipped_frame = cv2.cvtColor(flipped_frame,cv2.COLOR_BGR2GRAY)
    flipped_frame = cv2.cvtColor(flipped_frame,cv2.COLOR_GRAY2BGR)
    print(flipped_frame) 
    flipped_frame[int(boxCR-snipH/2):int(boxCR+snipH/2),int(boxCC-snipW/2):int(boxCC+snipW/2)] = frameROI
    
    #make the snip frame move 
    boxCR = boxCR+deltaRow
    boxCC = boxCC+deltaColumn
    #change the direction when hits
    if boxCR-snipH/2 <=0 or boxCR+snipH/2 >= height:
        deltaRow = deltaRow*(-1)
    if boxCC-snipW/2 <=0 or boxCC+snipW/2 >= width:
        deltaColumn = deltaColumn*(-1)

    boxCR = boxCR + deltaRow  
    # show the snip frame 
    # cv2.imshow('my ROI',frameROI)
    # cv2.moveWindow('my ROI',width,0)

    # show the original frame 
    cv2.imshow('myWEBcam', flipped_frame)
    cv2.moveWindow('myWEBcam',0,0) 
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()