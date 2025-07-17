import cv2 
"""
 - create a camera object 
 - Grab a Frame Using Camer 
 - Show a  4 Frame [original , gray , gray , original]
"""
cam = cv2.VideoCapture(0)

while True: 
    ignore,frame = cam.read()
    grayfram = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #window 1 
    cv2.imshow('myWEBcam',frame)
    cv2.moveWindow('myWEBcam',0,0) # 0 0 
    #window 2 
    cv2.imshow('myGrayFrame',grayfram)
    cv2.moveWindow('myGrayFrame',640,0) # 640 0 
    #window 3 
    cv2.imshow('myWEBcam2',frame)
    cv2.moveWindow('myWEBcam2',640,480) # 640 480 
    #window 4 
    cv2.imshow('myGrayFrame2',grayfram)
    cv2.moveWindow('myGrayFrame2',0,480) # 0 480 

    
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()



