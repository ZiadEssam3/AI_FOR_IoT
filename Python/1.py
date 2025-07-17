import cv2
#check the version of opencv
print(cv2.__version__)

#creating camera object 
cam = cv2.VideoCapture(0)

while True:
    #grab a fram From my camera
    ignore,frame = cam.read()  # original frame 
    grayframe = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # gray frame 
    #show the frame 
    # cv2.imshow('myWEBcam',frame)
    cv2.imshow('myWEBcam',grayframe)
    # put the window in a choosen position
    cv2.moveWindow('myWEBcam',0,0) # X,Y
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()